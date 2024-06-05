import os
import json

def read_conll(file_path):
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        sentence = []
        for line in f:
            line = line.strip()
            if line == "":
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                word, tag = line.split("\t")
                sentence.append((word, tag))
        if sentence:
            sentences.append(sentence)
    return sentences

def convert_to_spacy_format(sentences):
    spacy_data = []
    for sentence in sentences:
        text = " ".join([word for word, tag in sentence])
        entities = []
        start = 0
        for word, tag in sentence:
            if tag != 'O':
                entity_label = tag.split("-")[-1]
                entities.append((start, start + len(word), entity_label))
            start += len(word) + 1
        spacy_data.append((text, {"entities": entities}))
    return spacy_data

def process_conll_files(input_dir, output_file):
    all_sentences = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.conll'):
            print(f"Processing {file_name}")
            file_path = os.path.join(input_dir, file_name)
            sentences = read_conll(file_path)
            all_sentences.extend(sentences)
    
    spacy_format_data = convert_to_spacy_format(all_sentences)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(spacy_format_data, f, ensure_ascii=False, indent=4)

# Örnek dosya yolları
input_directory = './conll_test_datas'  # .conll dosyalarının bulunduğu dizin
output_json_file = 'transfomer_for_test.json'  # Spacy için uygun formattaki çıktı dosyası

process_conll_files(input_directory, output_json_file)
