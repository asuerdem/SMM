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
            for token in doc: # select words if conditions hold
                if (token.pos_ in poss or token.tag_ in tags) and token.lemma_ not in STOP_WORDS + ['-PRON-']:
                    outword = token.lemma_ if lemmatize else token.text
                    filtered_words.append(outword)
            if counter % 1 == 0: print('Processed %s documents' % counter)
            news['Text'] = ' '.join(filtered_words)
            writer.writerow(news)
            counter += 1
    writefile.close()