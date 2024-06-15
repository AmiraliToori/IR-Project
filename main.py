import nltk
from nltk.stem.snowball import SnowballStemmer  # type: ignore
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

import numpy as np # type: ignore
import pandas as pd # type: ignore

import tkinter as tk
from tkinter import filedialog

import re

#############################################################################################

# function to create the excel files
def create_excel_dataframe(input , name, columns, index):
    df = pd.DataFrame(input, columns = columns, index = index) # Create a pandas dataframe
    df.to_excel(name) # Create an excel file
    return df

nltk.download('wordnet')
nltk.download('stopwords')
stop_words = stopwords.words('english')

stemmer = SnowballStemmer(language='english')
dictionary = []

#############################################################################################

def is_meaningful(word) -> bool:
    
    if wn.synsets(word):
        return True
    else: 
        return False   

def convert_to_list(doc) -> list:
    doc = doc.split()
    return doc


def create_dictionary(doc, dictionary) -> list:
    for word_index, word in enumerate(doc):
        
        word = word.lower()
        
        if word.isalnum() and word not in stop_words and is_meaningful(word) and len(word) > 1:
            
            stem_word = stemmer.stem(word)
            doc[word_index] = stem_word
            
            if stem_word not in dictionary:
                dictionary.append(stem_word)
    
    return doc

def join_document(doc) -> str:
    doc = ' '.join(doc)
    return doc


def process_document(document) -> str:
    
    document = convert_to_list(document)
    
    document = create_dictionary(document, dictionary)
    
    document = join_document(document)
    
    return document

#####################################################################################################

def select_file():
    global raw_documents
    
    file_name = filedialog.askopenfilename(title = "Select Dataset",
                                           initialdir = "IR-Project",
                                           filetypes = (("All files","*.*"), ("Text files", "*.txt")))
    
    with open(file_name, "r") as f:
        raw_documents = f.read()
        window.destroy()


window = tk.Tk()
window.geometry("200x100")
window.title("Select Dataset")

button = tk.Button(
    window,
            text = "Select",
            command = select_file).pack()


window.mainloop()

#########################################################################################################

raw_dataset = raw_documents # the raw dataset that read from the one file

raw_dataset = raw_dataset.split(".I") # split the docs by index

raw_dataset.remove(raw_dataset[0]) # remove the empty first index

doc_index = 0
    

# write each index in 'raw_dataset'
for doc in raw_dataset:
    doc_index += 1
    doc_path = "./docs" + "/doc" + str(doc_index) + ".txt"
    doc = process_document(doc)
    
    
    with open(doc_path, "w") as document: # write each index into the separated doc
        document.write(doc)

doc_index = 0

for doc in raw_dataset:
    doc_index += 1
    doc_path = "./Original docs" + "/docs" + str(doc_index) + ".txt"
    
    
    with open(doc_path, "w") as document: # write each index into the separated doc
        document.write(doc)
        
df = pd.DataFrame(dictionary, columns=["Words"])
df.to_excel("dictionary.xlsx")

#############################################################################################################3

tf_array = np.zeros((len(dictionary), doc_index))
idf_array = np.zeros((len(dictionary), 1))
tf_idf_array = np.zeros((len(dictionary), doc_index))

def calculate_term_frequency(doc, dictionary, doc_no):
    for word in dictionary:
        if word in doc:
            frequency = doc.count(word)
            row = dictionary.index(word)
            column = doc_no - 1
            tf_array[row, column] += frequency


def calculate_document_frequency(doc, dictionary):
    for word in dictionary:
        if word in doc:
            row = dictionary.index(word)
            idf_array[row, 0] += 1
            
            
doc_names_list = []
for num in range(1, doc_index + 1):
    doc_path = "./docs" + "/doc" + str(num) + ".txt"
    doc_names_list.append("doc" + str(num) + ".txt")
    with open(doc_path, "r") as file:
        doc = file.read()
        calculate_term_frequency(doc, dictionary, num)
        calculate_document_frequency(doc, dictionary)
        




row, column = np.shape(tf_array)

for r in range(row):
    for c in range(column):
        if tf_array[r, c] > 0:
            extracted_element = tf_array[r, c]
            tf_array[r, c] = 1 + np.log10(extracted_element)
        else:
            tf_array[r, c] = 0
            
            
count_of_documents = column

row, column = np.shape(idf_array)

for r in range(row):
    if idf_array[r, 0] > 0:
        extracted_element = idf_array[r, 0]
        idf_array[r, 0] = np.log10(count_of_documents / extracted_element)
    else:
        idf_array[r, 0] = 0
        
        
row, column = np.shape(tf_idf_array)
r, c = 0, 0
while r < row:
        tf_idf_array[r, c]= tf_array[r, c] * idf_array[r, 0]
        c += 1
        if c == column:
            r += 1
            c = 0
            
            
tf_dataframe = create_excel_dataframe(tf_array, "tf_excel.xlsx", doc_names_list, dictionary)

idf_dataframe = create_excel_dataframe(idf_array, "idf_excel.xlsx", ["IDF"], dictionary)

tf_idf_dataframe = create_excel_dataframe(tf_idf_array, "tf_idf_excel.xlsx", doc_names_list, dictionary)

#####################################################################################################################################################

def rank_cosine(export_string: str,
                cosine_docs: list,
                cosine_values: list) -> None:
    
    cosine_rank = sorted(dict(zip(cosine_docs, cosine_values)).items(), key = lambda x: x[1], reverse = True)
    
    text_box.delete("0.0", tk.END)
    
    for index, doc in enumerate(cosine_rank[:10], 1):
        text_box.insert(tk.END, str(index)+ "." + str(doc[0]) + " : " + str(doc[1]) + "\n")
    
    df = pd.DataFrame([doc[1] for doc in cosine_rank], index = [doc[0] for doc in cosine_rank], columns = ['cosine'])
    df.to_excel(export_string +".xlsx")
    

def calculate_cosine(query_tfidf: np.array) -> tuple:    
    cosine_values = []
    cosine_docs = []

    for number in range(1, column + 1):
        
        doc_name = "doc"+ str(number) +".txt"
        doc_column = tf_idf_dataframe[doc_name].tolist()
        
        nominator = np.dot(query_tfidf, doc_column)
        
        doc_column_norm = np.linalg.norm(doc_column)
        query_tfidf_norm = np.linalg.norm(query_tfidf)
        
        denominator = doc_column_norm * query_tfidf_norm
        
        cosine_theta = nominator / denominator
        
        cosine_values.append(cosine_theta)
        cosine_docs.append(doc_name)
        
    return cosine_values, cosine_docs



def take_query_from_user():
    global query_tfidf
    global query_words_list
    
    query = query_var.get()
    query_entry.delete("0", tk.END)
    
    query_lower = query.lower()
    query_words_list = query_lower.split()
    
    temp = []
    for word in query_words_list:
        if word not in stop_words and is_meaningful(word) and len(word) > 1:
            temp.append(word) 

    
    query_words_list = temp
    temp = [stemmer.stem(word) for word in query_words_list]
    query_words = temp
    query_words_list = list(set(temp))
    query_words_str = " ".join(query_words)

    
    query_idf_lst = [idf_array[dictionary.index(word)][0] for word in query_words_list]
    
    query_tf_lst = [np.log10(query_words_str.count(word)) + 1 for word in query_words_list]
    
    query_tfidf = [idf*query_tf_lst[count] for count, idf in enumerate(query_idf_lst)]
    
    row = np.shape(tf_idf_array)[0]
    query_tfidf = np.pad(query_tfidf, (0, row - len(query_tfidf)), 'constant', constant_values = (0))
    for count, value in enumerate(query_tfidf):
        if count < len(query_words_list):
            if value > 0:
                if count != dictionary.index(query_words_list[count]):
                    dest_index = dictionary.index(query_words_list[count])
                    query_tfidf[dest_index] = value
                    query_tfidf[count] = 0

    cosine_values, cosine_docs = calculate_cosine(query_tfidf)

    
    rank_cosine("cosine_similarity_rank",
                cosine_docs,
                cosine_values)

def rerank():

    def get_doc_names() -> list:
        temp = []
        pattern = r'docs(\d+)\.txt'

        for path in files_path:
            temp.append(re.findall(pattern, path))
            
        return [int(value[0]) for value in temp]

    def add_tfidf_selected_docs():
        for doc in target_doc_numbers:
            for count, word in enumerate(query_words_list):
            
                word_index_in_dictionary = dictionary.index(word)
                query_tfidf[word_index_in_dictionary] += tf_idf_array[word_index_in_dictionary ,doc] 

    target_doc_numbers = get_doc_names()
    add_tfidf_selected_docs()
    
    
    cosine_values, cosine_docs = calculate_cosine(query_tfidf) 
    rank_cosine("cosine_similarity_rerank",
                cosine_docs,
                cosine_values)


window = tk.Tk()
window.geometry("930x300")

def choose():
    global files_path
    files_path = filedialog.askopenfilenames(
                parent = window,
                initialdir = "./Original docs",
                title = "Choose the docs",
                filetypes = [("text name","*.txt")]
                )
    
    rerank()


frame = tk.Frame(window)
frame.columnconfigure(0, weight = 1)
frame.columnconfigure(1, weight = 1)
frame.columnconfigure(2, weight = 1)

STICKY = tk.E + tk.W
PAD_VALUE = 10

query_var = tk.StringVar()

query_label = tk.Label(
                        frame,
                        text = "Query: "
                        )
query_label.grid(
                row = 0,
                column = 0,
                sticky = STICKY,
                padx = PAD_VALUE,
                pady = PAD_VALUE
                )

query_entry = tk.Entry(
                        frame,
                        textvariable = query_var
                        )
query_entry.grid(
                row = 0,
                column = 1,
                sticky = STICKY,
                padx = PAD_VALUE,
                pady = PAD_VALUE
                )

query_btn = tk.Button(
                frame,
                   text = 'Enter Query',
                   command = take_query_from_user,
                   font = ('Arial', 10)
                   )
query_btn.grid(
                row = 0,
                column = 2,
                sticky = STICKY,
                padx = PAD_VALUE,
                pady = PAD_VALUE
                )

rerank_btn = tk.Button(
                frame,
                   text = 'Rerank',
                   command = choose,
                   font = ('Arial', 10)
                   )
rerank_btn.grid(
                row = 1,
                column = 2,
                sticky = STICKY,
                padx = PAD_VALUE,
                pady = PAD_VALUE
                )

text_box = tk.Text(
            frame,
                    height = 10
                    )
text_box.grid(
            row = 1,
            column = 1,
            sticky = STICKY,
            padx = PAD_VALUE,
            pady = PAD_VALUE
            )

frame.pack()

window.mainloop()