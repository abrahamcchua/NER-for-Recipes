import json
import csv

class preprocessor():
    def __init__(self) -> None:
        self.ignore_list = ['lid', 'fridge']
    
    
    def body(self):
        data = self.json_reader('Labelled-data.json')
        with open('dataset.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Example #", "Word", "Label", "Start", "End"])
            for i in range(len(data)):
                d = dict()
                d = self.label_importer(data, i , d)
                self.converter(data, i, d, writer)


    def json_reader(self, fname):
        with open(fname, 'r') as f:
            return json.load(f)
        
    
    def label_importer(self, data, i, d):
        for label_idx in data[i]['label']:
            start = label_idx['start'] ; end = label_idx['end']
            text  = label_idx['text'] ; label = label_idx['labels'][0]
            if text not in self.ignore_list:
                d[start] = [end, text, label] 
        return d
            
        
    def converter(self, data, i, d, writer):
        # Total Words
        start = 0 ; t_words = ''
        # c Stands for counter to be used to skip annotations that have more than one word in it
        c = 0
        instruction = data[i]['Instructions'][0].lower().split()
        for word in instruction:
            l = len(word)
            # All words are included in t_words since there could be duplicate words when trying to index the word in the list
            # A space is added to get the accurate length of the text
            t_words += ' ' + word
            end = len(t_words) - 1
            if c != 0:
                c -=1
            elif start not in d:
                    writer.writerow([i, word, 'O', start, end])
            elif start in d:
                label = d[start][2][:2].upper() ; t = d[start][1]
                # To check if there is more than one word in the label
                if ' ' in d[start][1]:
                    t = d[start][1].split()
                    for j  in range(len(t)):
                        if j == 0:
                            writer.writerow([i, t[j], "B-" + label, start, end])
                        else:
                            writer.writerow([i, t[j], "I-" + label, start, end])
                    c += len(t)-1
                else:
                    writer.writerow([i, word, "B-" + label, start, end])
            start += l + 1

        

emp = preprocessor()
emp.body()