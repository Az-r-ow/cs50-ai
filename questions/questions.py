import nltk
import string
import math
import sys
import os


FILE_MATCHES = 1
SENTENCE_MATCHES = 5


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    currentDir = os.path.abspath(os.getcwd())
    txtFiles = dict()
    
    for fileName in os.listdir(os.path.join(currentDir, directory)):
        if not os.path.splitext(fileName)[1] == ".txt":
            continue
        with open(os.path.join(currentDir, directory, fileName), "r") as file:
           txtFiles[fileName] = file.read()
    
    return txtFiles


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized_sentence = nltk.tokenize.word_tokenize(document.lower())
    for word in tokenized_sentence:
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            tokenized_sentence.remove(word)

    return tokenized_sentence


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    
    # First calculate the occurrences of the words :
    for document in documents:
        tokenized = documents[document]
        # [*set(tokenized)] will remove the duplicates
        for word in [*set(tokenized)]:
            # to avoid counting same word twice
            if not word in idfs.keys():
                idfs[word] = 1
            else:
                idfs[word] += 1
    
    n = len(documents)
    
    # Calculate the IDF values of each word
    for word in idfs:
        idfs[word] = math.log(n / idfs[word])
            
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    filesScores = dict()
    wordIdfs = dict()
    
    for word in query:
        if not word in idfs:
            continue
        wordIdfs[word] = idfs[word]

    # Computing tf-idf 
    for file in files:
        wordFrequencies = dict()
        for word in files[file]:
            if word in wordIdfs:
                if word in wordFrequencies:
                    wordFrequencies[word] += 1
                else:
                    wordFrequencies[word] = 1
        fileScore = 0
        for word in wordFrequencies:
            if word in wordIdfs:
                fileScore += wordFrequencies[word] * wordIdfs[word]
        filesScores[file] = fileScore
    
    # Sorting and returning the first n files 
    return list(dict(sorted(filesScores.items(), key=lambda item : item[1], reverse=True)).keys())[0:n]                


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentencesScores = dict()
    wordIdfs = dict()
        
    for word in query:
        if not word in idfs.keys():
            continue
        wordIdfs[word] = idfs[word]
        
    for sentence in sentences:
        sentenceScore = 0
        for word in wordIdfs:
            if word in sentences[sentence]:
                sentenceScore += wordIdfs[word]
        sentencesScores[sentence] = sentenceScore
    
    sortedSentences = dict(sorted(sentencesScores.items(), key=lambda item: item[1], reverse=True))
    # Store on the first N number of sentences
    topSentences = list(sortedSentences.keys())[0:n]
    
    # Checking for similar values between sentences
    for i in range(len(topSentences)):
        if i == (len(topSentences) - 1):
            continue
        if sortedSentences[topSentences[i]] == sortedSentences[topSentences[i+1]]:
            # Calculate query term density
            biggerSentenceF = 0
            smallerSentenceF = 0
            for word in sentences[topSentences[i]]:
                if word in wordIdfs:
                    biggerSentenceF += 1
            
            for word in sentences[topSentences[i + 1]]:
                if word in wordIdfs:
                    smallerSentenceF += 1
            
            # Checking the term density
            if (biggerSentenceF / len(topSentences[i])) >= (smallerSentenceF / len(topSentences[i + 1])):
                 continue
            
            topSentences[i], topSentences[i + 1] = topSentences[i + 1], topSentences[i]
    
    return topSentences

if __name__ == "__main__":
    main()
