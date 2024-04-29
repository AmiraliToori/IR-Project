
def app(entry):
    import os
    raw_dataset = entry # the raw dataset that read from the one file
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

    from nltk.stem import PorterStemmer  # type: ignore

    # read the list of stop words
    stopword_file_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/gist_stopwords.txt"
    with open(stopword_file_path, "r") as file:
        stop_words = file.read()
        

    # separate the doc section from the document
    def transfer_to_list(doc):
        doc = doc.split()
        return doc


    # stemming
    stemmer = PorterStemmer()
    dictionary = []
    def create_dictionary(doc, dictionary):
        for element in doc:
            if element.isalpha():
                stem_word = stemmer.stem(element)
                if (stem_word not in stop_words) and (stem_word not in dictionary):
                    dictionary.append(stem_word)


    # read each doc and pass them through the methods
    for num in range(1, doc_index + 1):
        doc_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/docs" + "/doc" + str(num) + ".txt"
        with open(doc_path, "r") as file:
            doc = file.read()
            doc = transfer_to_list(doc)
            create_dictionary(doc, dictionary)
            

    #########################################################################################################################
    import numpy as np # type: ignore
    import pandas as pd # type: ignore

    # initializing the numpy arrays
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


    def calculate_inverse_document_frequency(doc, dictionary):
        for word in dictionary:
            if word in doc:
                row = dictionary.index(word)
                idf_array[row, 0] += 1


    doc_names_list = []
    for num in range(1, doc_index + 1):
        doc_path = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/docs" + "/doc" + str(num) + ".txt"
        doc_names_list.append("doc" + str(num) + ".txt")
        with open(doc_path, "r") as file:
            doc = file.read()
            calculate_term_frequency(doc, dictionary, num)
            calculate_inverse_document_frequency(doc, dictionary)


    # calculating tf array
    row, column = np.shape(tf_array)
    for r in range(row):
        for c in range(column):
            if tf_array[r, c] > 0:
                extracted_element = tf_array[r, c]
                tf_array[r, c] = 1 + np.log10(extracted_element)
            else:
                tf_array[r, c] = 1


    count_of_documents = column
    row, column = np.shape(idf_array)


    # calculating idf array
    for r in range(row):
        if idf_array[r, 0] > 0:
            extracted_element = idf_array[r, 0]
            idf_array[r, 0] = np.log10(count_of_documents / extracted_element)
        else:
            idf_array[r, 0] = 0


    # multiply peer to peer each row of tf-array in idf-array
    row, column = np.shape(tf_idf_array)
    r, c = 0, 0
    while r < row:
            tf_idf_array[r, c]= tf_array[r, c] * idf_array[r, 0]
            c += 1
            if c == column:
                r += 1
                c = 0

    # function to create the excel files
    def create_excel(input , name, columns, index):
        df = pd.DataFrame(input, columns = columns, index = index) # Create a pandas dataframe
        df.to_excel(name) # Create an excel file
        print(df)
        
    create_excel(tf_array, "tf_excel.xlsx", doc_names_list, dictionary)
    create_excel(idf_array, "idf_excel.xlsx", ["IDF"], dictionary)
    create_excel(tf_idf_array, "tf_idf_excel.xlsx", doc_names_list, dictionary)