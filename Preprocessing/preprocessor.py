import json
import csv

'''
The preprocessor of the labelled data to make it easier to perform the machine learning task in a jupyter notebook.
:Date: January, 14, 2023
:Author/s: 
    - Chua, Abraham <abrahamcchua@gmail.com>
'''
class preprocessor():
    def __init__(self):
        
        # The labels for words that are included in the self.ignore_list are ignored 
        self.ignore_list = ['lid', 'fridge']
        self.header = ["Example #", "Word", "Label", "Start", "End"]
    
    def body(self):
        """Main highlight of function "body"
        Summary:
        This function acts as the frame of the code
        output of the function:
        -A csv file containing the preprocessed data set
        """
        # Read the data from the json file
        data = self.json_reader('Labelled-data.json')
        
        # Create a csv file where the data will be stored 
        with open('dataset.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # Header
            writer.writerow(self.header)
            for i in range(len(data)):
                d = dict()
                d = self.label_importer(data, i , d)
                self.converter(data, i, d, writer)


    def json_reader(self, fname):
        """Main highlight of function "json_reader"
        Summary:
        Loads the json file to a dictionary
        :param train_data: string; The dataset used for training
        output of the function includes:
        A dictionary containing the contents of the json file
        """
        
        with open(fname, 'r') as f:
            return json.load(f)
        
    
    def label_importer(self, data, i, d):
        """Main highlight of function "label_importer"
        Summary:
        The function reads the labelled-data and places relevant information to a new one
        :param data: list; The list containing the labelled data
        :param i: int; The example number where the labels will be imported from
        :param d: dictionary; The dictionary where the variables will be saved
        output of the function includes:
        A dictionary with
        key: 
        - Starting index of the string on the unlabelled text
        list of values containing:
        - The ending index of the word on the unlabelled text
        - The word
        - The label of the word
        """

        # The function loops through the ith data point in the list 
        # and returns the corresponding values of the key 'label'
        for label_idx in data[i]['label']:
            
            # Storing relevant parts of the dictionary to variables
            start = label_idx['start'] ; end = label_idx['end']
            word = label_idx['text'] ; label = label_idx['labels'][0]
            
            # If the word is in the self.ignore_list then skip it
            if word not in self.ignore_list:
                
                # Save the relevant variables to a dictionary
                d[start] = [end, word, label] 
        return d
            
        
    def converter(self, data, i, d, writer):
        """Main highlight of function "converter"
        Summary:
        The function reads the dic
        :param data: list; The list containing the labelled data
        :param i: int; The example number where the labels will be imported from
        :param d: dictionary; The dictionary where the variables will be saved
        output of the function includes:
        A dictionary with
        key: 
        - Starting index of the string on the unlabelled text
        list of values containing:
        - The ending index of the word on the unlabelled text
        - The word
        - The label of the word
        """
        
        # Starting position of the word; Compiled Word
        start = 0 ; t_words = ''
        
        # Summary:
        # c Stands for counter to be used to skip annotations that have more than one word in it
        # In Depth Explanation:
        # This is essential since the logic used to determine whether a word has a label 
        # is if the starting len of the word is in the dictionary d
        # Without the use of the variable the logic would create a duplicate row for it with label 'O' 
        c = 0
        
        # Split the unlabelled text into a list containing each word
        instruction = data[i]['Instructions'][0].lower().split()
        
        
        for word in instruction:
            l = len(word)
            
            
            # All words are included in t_words since there could be duplicate words when trying to index the word in the list
            # A space is added to get the accurate length of the text
            t_words += ' ' + word
            
            # Minus one was implemented since t_words has a leading blank space
            end = len(t_words) - 1
            
            # Check if the word was already used
            if c != 0:
                
                # Value of C determines how many more words to be skipped
                c -=1
            
            # Checks if the starting index of the word is in dictionary d
            # If it's not present there it means it has a label 'O'
            elif start not in d:
                    writer.writerow([i, word, 'O', start, end])
                    
            # Checks if the starting index of the word is in dictionary d  
            elif start in d:
                # t variable contains the word
                label = d[start][2][:2].upper() ; t = d[start][1]
                
                # Check if there is more than one word in the label
                if ' ' in d[start][1]:
                    # Since there is more than one word split the phrase into words
                    t = d[start][1].split()
                    
                    # Inititilizing the list that will contain length of each of the words
                    word_length_list = []
                    for j in range(len(t)):
                        
                        # logic to add the length of each of the words
                        word_length_list.append(len(t[j]))
                        
                        # B- stands for begining tag, I- stands for inside tag
                        if j == 0:
                            writer.writerow([i, t[j], "B-" + label, start, end])
                            
                            # Initializing the start position of labels that start with I-
                            i_start = end + 1
                        else:
                            # Row #508-511 
                            # Interesting to check, since it is one of the entities that has 4 words
                            # This makes some algorithms that can solve the issue for 2 words not applicable for 3 or more words.
                            
                            # Logic to get the appropriate length of tags that start with I-
                            i_end = i_start + word_length_list[j]
                            writer.writerow([i, t[j], "I-" + label, i_start, i_end])
                            i_start = i_end + 1
                            
                    # Minus one was implemented since t_words has a leading blank space
                    c += len(t)-1
                else:
                    writer.writerow([i, word, "B-" + label, start, end])
            start += l + 1

        

emp = preprocessor()
emp.body()