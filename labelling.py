from transformers import pipeline
import transformers
import json
import sys
from time import sleep
from inputimeout import inputimeout, TimeoutOccurred
from transformers_training.paths import path_label
transformers.logging.set_verbosity_error()

# [{'dialog': ['But what about second breakfast?', "Don't think he knows about second breakfast."]}, {'dialog': ["I didn't think it would end this way!", "End? No, the journey doesn't end here."]}, {'dialog': ['Is it a dangerous business to go out my door?', 'It is, there is no knowing where you might be swept off to!']}, {'dialog': ['I never thought I would die fighting side by side with an Elf.', 'What about side by side with a friend?']}]

# [{'tag': 'dialog', 'questions': ['But what about second breakfast?'], 'responses': ["Don't think he knows about second breakfast."]}, {'tag': 'dialog', 'questions': ["I didn't think it would end this way!"], 'responses': ["End? No, the journey doesn't end here."]}, {'tag': 'dialog', 'questions': ['Is it a dangerous business to go out my door?'], 'responses': ['It is, there is no knowing where you might be swept off to!']}, {'tag': 'dialog', 'questions': ['I never thought I would die fighting side by side with an Elf.'], 'responses': ['What about side by side with a friend?']}]
# import tensorflow as tf
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# print("Num GPUs Available: ", len(tf.config.list_logical_devices('GPU')))
# tf.debugging.set_log_device_placement(True) 

def lessons_count():
    with open("classification_training/database/user/lessons.json", 'r') as file:
        lessons_file=json.load(file)
    lessons=lessons_file['lessons']
    return lessons

def data_to_dict(data):
    """
    data=[{'dialog': ['abc', 'xyz']}]
    """
    data_dicted=[]
    for i,elem in enumerate(data):
        entry={'tag': 'dialog', 'questions': [],'responses': []}
        for jter,flem in enumerate(elem['dialog']):
            if jter==0:
                entry['questions'].append(flem)
            if jter==1:
                entry['responses'].append(flem)
        data_dicted.append(entry)
    return data_dicted

"""
THIS IS MAIN \/
"""
def dialog_to_json(list_of_dialogs, lesson_number, is_load):
    """
    list_of_dialogs=[{'tag':'x','questions':[abc],'responses':[xyz]},{'tag': ...}]
    lesson_number= int(list_of_dialogs[id])
    for i,elem in enumerate(list_of_dialogs):
        dialog_to_json(list_of_dialogs, i, is_load)
    """
    dialog,classified_file=dialog_out(list_of_dialogs[lesson_number])
    # for elem in dialog:
        # print(elem)
    if is_load:
        classified_file['dialogs']=dialog
        with open("classification_training/classified.json", 'w') as file:
            json.dump(classified_file,file)
    else:
        print("Done")


def label_entry(given_tag, question, response, previous_tag, list_of_tags, dialogs):
    if given_tag not in list_of_tags:
        print("CREATING NEW TAG")
        list_of_tags.append(given_tag)
        dialogs.append({"tag": given_tag, "questions": [question], "responses": [response]})
    else:
        for entry in dialogs:
            if entry['tag']==str(given_tag) and (question not in entry['questions']):
                entry['questions'].append(question)
                if previous_tag!=given_tag and (previous_tag not in ['greeting', 'goodbye', 'thanks', 'about', 'name', 'help']):
                    entry['responses'].append(response)
    return dialogs

def dialog_out(elem):
    with open("classified.json", 'r') as f:
        classified_file=json.load(f)
    existing_dialogs=classified_file.copy()
    dialogs=existing_dialogs['dialogs']
    tags=[]
    for sentence in dialogs:
        tags.append(sentence['tag'])
    if not tags:
        print("Error")
        sys.exit()
    
    """
    model used here: bart-large-mnli
    clone with git clone https://huggingface.co/facebook/bart-large-mnli
    if you have a problem with cloning the repo, use "git config http.sslVerify false" and "git config http.sslVerify true" after downloading
    path to a dir with pretrained model; ex: '.../VSC/transformers/bart-large-mnli'
    """
    path=path_label()
    classifier=pipeline('zero-shot-classification',model=path, device=0)
    labels=['greeting', 'goodbye', 'thanks', 'about', 'name', 
        'help', 'film', 'garden', 'animal', 'color', 'breakfast',
        'journey', 'end','friend', 'weather', 'movie']
    response=elem['responses'][0]
    previous_tag=elem['tag']

    for q in elem['questions']:
        classified=classifier(q, labels)
        score=classified['scores']
        label=classified['labels']
        print("Question: ",q)
        for i in range(3):
            print("ID: ",i,"LABEL: ",label[i])
        sleep(1)
        try:
            # id=int(input("Which label is correct?: "))
            id=int(inputimeout(prompt="Which label is correct?: ", timeout=3))
        except (IndexError, TimeoutOccurred):
            id=score.index(max(score))
        correct_label=label[id]
        if correct_label!=previous_tag:
            print("chosen label: ",correct_label, "\nintended label: ",label[score.index(max(score))])
        dialogs=label_entry(correct_label, q, response, previous_tag, tags, dialogs)
    sleep(1)
    # for x in dialogs:
    #     print(x)
    return dialogs, classified_file


# data=[{'dialog': ['But what about second breakfast?', "Don't think he knows about second breakfast."]}, {'dialog': ["I didn't think it would end this way!", "End? No, the journey doesn't end here."]}, {'dialog': ['Is it a dangerous business to go out my door?', 'It is, there is no knowing where you might be swept off to!']}, {'dialog': ['I never thought I would die fighting side by side with an Elf.', 'What about side by side with a friend?']}]
data=[{'dialog':['What is the weather today', 'It is raining']}, {'dialog':['Did you watch Barbie movie?', 'Not yet but i heard it is great movie!']}]
data_dicted=data_to_dict(data)

for i,elem in enumerate(data_dicted):
    dialog_to_json(data_dicted, i, is_load=0)

