import json
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en')
STOP_WORDS = list(STOP_WORDS)

def json_cleaner(jsondest,poss = ['NOUN','ADJ','ADV'],tags = [],lemmatize = True, cleansws = True, filterpunct=True):
    # initializing
    jsonname = jsondest.replace('.json','')
    if not filterpunct: poss.append('PUNCT')
    sws = STOP_WORDS + ['-PRON-'] if cleansws else ['-PRON-']
    counter = 1
    # opening json files, both input and output
    writefile = open(jsonname + '_processed.json','w') # output file
    writefile.write('[')
    with open(jsondest) as readfile:
        for news in readfile:
            if len(news) < 10: continue
            news = news.strip()
            if news.endswith(','): news = news[:-1]
            news = json.loads(news)
            doc = nlp(news['Text'])
            filtered_words  = []
            for token in doc: # select words if conditions hold
                if (token.pos_ in poss or token.tag_ in tags) and token.lemma_ not in STOP_WORDS + ['-PRON-']:
                    outword = token.lemma_ if lemmatize else token.text
                    filtered_words.append(outword)
            if counter % 1 == 0: print('Processed %s documents' % counter)
            news['Text'] = ' '.join(filtered_words)
            # Writing
            writefile.write('\n')
            json.dump(news, writefile)
            writefile.write(',')
            counter += 1
    # Son iterasyonda eklenen gereksiz virgul'u sil
    writefile.seek(writefile.tell()-1)
    writefile.truncate()
    # Bir satir asagiya
    writefile.write('\n]')
    writefile.close()