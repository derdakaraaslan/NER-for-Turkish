import random
import spacy
from spacy import displacy
from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
from old_data import OLD_DATAS
from new_data import NEW_DATA
from old_test_data import TRANSFORMER_FOR_TEST
from new_test_data import TEST_DATA
nlp = spacy.load("tr_core_news_trf")

all_data =  NEW_DATA + OLD_DATAS 
all_test_data =  TEST_DATA + TRANSFORMER_FOR_TEST 

doc_bin = DocBin()
training_data = []
i = 0
while len(all_data) > 0:
    random_number = random.randint(0, len(all_data) - 1)
    example = all_data[random_number]
    temp_dict = {}
    temp_dict['text'] = example[0]
    temp_dict['entities'] = []
    print(temp_dict['text'] )
    for annotation in example[1]['entities']:
      start = annotation[0]
      end = annotation[1]
      label = annotation[2]
      temp_dict['entities'].append((start, end, label))
    training_data.append(temp_dict)
    all_data.pop(random_number)

print(training_data[0])

for training_example  in tqdm(training_data): 
    text = training_example['text']
    labels = training_example['entities']
    doc = nlp.make_doc(text) 
    ents = []
    for start, end, label in labels:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    filtered_ents = filter_spans(ents)
    doc.ents = filtered_ents 
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy") 

doc_bin_test = DocBin()
test_data = []
for test_example in all_test_data:
    temp_dict = {}
    temp_dict['text'] = test_example[0]
    temp_dict['entities'] = []
    for annotation in test_example[1]['entities']:
      start = annotation[0]
      end = annotation[1]
      label = annotation[2]
      temp_dict['entities'].append((start, end, label))
    test_data.append(temp_dict)

for test_example  in tqdm(test_data):
    text = test_example['text']
    labels = test_example['entities']
    doc = nlp.make_doc(text) 
    ents = []
    for start, end, label in labels:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    filtered_ents = filter_spans(ents)
    doc.ents = filtered_ents 
    doc_bin_test.add(doc)

doc_bin_test.to_disk("test.spacy")

