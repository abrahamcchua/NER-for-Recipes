# Built in modules
import json
import os
import string
# Python modules
import numpy as np
#finds where the .env is
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv()) 
except:
    ...
# Machine Learning Frameworks
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from nltk.tokenize import word_tokenize



'''
The prediction script for the project
:Date: January 22, 2023
:Author/s: 
    - Chua, Abraham <abrahamcchua@gmail.com>
'''


class ner_model():
    def __init__(self, text):
        self.text = text
        dir = os.getenv('DIR')
        mapping_path = dir + os.getenv('MAPPING')
        mapping_dict = self.get_mapping_dict(mapping_path)
        model_path = dir + os.getenv('MODEL')
        self.model = self.load_model(model_path)
        self.word2idx = mapping_dict['word2idx']
        self.tag2idx = mapping_dict['tag2idx']
        self.tags = mapping_dict['tags']
        
    
    def load_model(self, model_name):
        # Loads and returns the NER model
        return tf.keras.models.load_model(model_name)
    
    
    def get_mapping_dict(self, fname):
        # Read and return the json file
        with open(fname, 'r') as fcc_file:
           return json.load(fcc_file)
       
       
    def get_preprocess_text(self, text):
        """
        Main highlight of function "get_preprocess_text"
        Summary:
        This function returns a preprocessed lowercased string that has all of its punctuations, removed except for "-" 
        output of the function:
        -String
        """
        punctuations_to_be_removed = string.punctuation.replace('-', '')
        return text.translate(str.maketrans('', '', punctuations_to_be_removed)).lower()
    
    
    def get_preprocessed_list(self, test):
        """
        Main highlight of function "get_preprocessed_list"
        Summary:
        This function returns a list of integers of integers that corresponds to words based on the word2idx dictionary
        :param test: list; a list of tokenized words
        output of the function:
        -A list 
        """
        # max_len should have the same value as the one used in training
        max_len = 900
        # Use pad_sequence preprocessing to convert values to the same ones used in training the model
        preprocessed_list = pad_sequences(sequences=[[self.word2idx.get(w, 0) for w in test]], 
                                          padding="post", value=0, maxlen=max_len)
        return preprocessed_list
    
    
    def get_predicted_entities(self, unique=True):
        """
        Main highlight of function "get_predicted_entities"
        Summary:
        This function returns a dictionary containing the predictions of the NER model on the given text.
        :param unique: boolean; When set to true the function returns only unique predictions
        output of the function:
        -A dictionary 
        """
        # word_tokenize returns a list of tokenized strings
        test = word_tokenize(self.get_preprocess_text(self.text))
        preprocessed_list = self.get_preprocessed_list(test)
        # p stands for the probabilities predicted by the model on the input text
        p = self.model.predict(np.array([preprocessed_list[0]]))
        # Returns an array of the classes with the max probabilities of the prediction
        p = np.argmax(p, axis=-1)
        
        output_dict =  self._determine(test, p)
        if unique == True:
            return {k:set(v) for k, v in output_dict.items()}
        return output_dict
    
    
    def _determine(self, test, p):
        """
        Main highlight of function "_determine"
        Summary:
        This function contains the logic in creating the dictionary that will contain the predictions
        :param test: list; a list of tokenized words
        :param p: array; a list of probabilities
        output of the function:
        -A dictionary 
        """
        output_dict = {}
        for word, pred in zip(test, p[0]):
            
            # Convert the corresponding number to a string based on the tags list
            tag = self.tags[pred]
            
            if tag != "O":
                # To make the output look better
                word = word.title()
                prefix = tag[:1]; label = tag[2:]
                
                # Create a new key in the dictionary if the label is not a key yet
                if label not in output_dict.keys():
                    # Create a new list containing the predicted word
                    output_dict[label] = [word]
                else:
                    # Add a new entry in the list
                    if prefix == "B":
                        output_dict[label].append(word) 
                    else:
                        # Since the indexing starts at zero, subtracting one from the len is important
                        l = len(output_dict[label]) - 1
                        # Add the predicted word to the entry in the list
                        output_dict[label][l] += " " + word
        return output_dict
        
    
    


    
