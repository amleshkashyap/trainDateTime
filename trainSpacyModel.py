import spacy
import random
import csv
import en_core_web_sm
import json
# spacy.require_gpu()

def createDataFromJSON():
    dataJSON = list()
    with open('sampleTest.txt', 'r') as csvinfile:
        spamreader = csv.reader(csvinfile)
        count = 0
        for line in spamreader:
            count = count + 1
            if(count%2 == 1):
                entities = dict()
                entityList = list()
                lineMod = line[0].replace("'", "\"")
                lineModNew = json.loads(lineMod)
                content = lineModNew['content']
                for ent in lineModNew['entities']:
                    entTup = tuple(ent)
                    entityList.append(entTup)
                entities['entities'] = entityList
                element = (content, entities)
                # print(element)
                dataJSON.append(element)
            if(count == 10000):
                break
    csvinfile.close()
    return dataJSON


data = createDataFromJSON()

def train_spacy(iterations):
    TRAIN_DATA = data
    nlp = spacy.load('en_core_web_sm')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            print("Shuffled Data")
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp


prdnlp = train_spacy(3)

# Save our trained Model
modelfile = input("Enter your Model Name: ")
prdnlp.to_disk(modelfile)

# Test your text
test_text = input("Enter your testing text: ")
doc = prdnlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
