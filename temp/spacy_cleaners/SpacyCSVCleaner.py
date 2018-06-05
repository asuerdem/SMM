import csv
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en')
STOP_WORDS = list(STOP_WORDS)

def csv_cleaner(csvdest,poss = ['NOUN','ADJ','ADV'],tags = [],lemmatize = True, cleansws = True, filterpunct=True):
    # initializing
    csvname = csvdest.replace('.csv','')
    if not filterpunct: poss.append('PUNCT')
    sws = STOP_WORDS + ['-PRON-'] if cleansws else ['-PRON-']
    counter = 1
    # opening csv files, both input and output
    writefile = open(csvname + '_processed.csv','w') # output file
    with open(csvdest) as readfile:
        reader = csv.DictReader(readfile)
        writer = csv.DictWriter(writefile, fieldnames=reader.fieldnames)
        writer.writeheader()
        # reading, processing and writing files
        for news in reader:
            doc = nlp(news['Text'])
            filtered_words  = []
            filtered_lemmas = []
            for token in doc: # select words if conditions hold
                if (token.pos_ in poss or token.tag_ in tags) and token.lemma_ not in STOP_WORDS + ['-PRON-']:
                    filtered_words.append(token.text)
                    filtered_lemmas.append(token.lemma_)
            print('Document %s is processed' % counter)
            news['Text'] = ' '.join(filtered_lemmas) if lemmatize else ' '.join(filtered_words)
            writer.writerow(news)
            counter += 1
    writefile.close()