from icecream import ic
import os

dataset_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/cran.all.1400"

# read the cran.all.1400 file that contain the all of the datasets
try:
    with open(dataset_path, "r") as f:
        raw_dataset = f.read()
except IOError:
    print("The file does not exist, or the entered path is invalid!")


raw_dataset = raw_dataset.split(".I") # split the docs by index
raw_dataset.remove(raw_dataset[0]) # remove the empty first index


doc_index = 0

# write each index in 'raw_dataset'
for doc in raw_dataset:
    doc_index += 1
    doc_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/docs" + "/doc" + str(doc_index) + ".txt"
    
    if os.path.exists(doc_path): # if file exist ignore
        pass
    else:
        with open(doc_path, "w") as document: # write each index into the separated doc
            document.write(doc)


###############################################################################################################
from nltk.stem import PorterStemmer 

# read the list of stop words
stopword_file_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/gist_stopwords.txt"
with open(stopword_file_path, "r") as file:
    stop_words = file.read()
    
# separate the doc section from the document
def transfer_to_list(doc):
    start = doc.find(".W")
    doc = doc[start + 2:]
    doc = doc.split()
    return doc

# stemming
stemmer = PorterStemmer()
dictionary = []
def create_dictionary(doc, dictionary):
    for element in doc:
        if element.isalpha:
            element = stemmer.stem(element)
            if (element not in stop_words) and (element not in dictionary):
                dictionary.append(element)
        
# read each doc and pass them through the methods
for num in range(1, doc_index + 1):
    doc_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/docs" + "/doc" + str(num) + ".txt"
    with open(doc_path, "r") as file:
        doc = file.read()
        doc = transfer_to_list(doc)
        create_dictionary(doc, dictionary)
#########################################################################################################################


