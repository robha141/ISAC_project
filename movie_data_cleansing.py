import csv
import re
import nltk
import random
import os
import collections
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Constants

NUMBER_OF_DATA_TO_PROCESS = 1000


class DataProcessor:

    def __init__(self, review, sentiment):
        self.review = review
        self.sentiment = sentiment
        self.sentiment_number = 0
        self.processed_data = []

    # update value, if positive == 1, otherwise 0

    def __value_to_number(self):
        self.sentiment_number = 1 if (self.sentiment == 'positive') else 0

    # Remove pattern

    def __remove_regex_pattern(self, text, pattern):
        pattern = re.compile(pattern)
        return re.sub(pattern, '', text)

    def __remove_stop_words(self, tokenized_text, stopwords):
        return [word for word in tokenized_text if not word in stopwords]

    # Stemming
    def __do_stemming(self, words):
        ps = PorterStemmer()
        stemmed = []
        for w in words:
            stemmed.append(ps.stem(w))
        return stemmed

    # Short words
    def __remove_shorts(self, words):
        no_shorts = []
        for w in words:
            if len(w) > 2:
                no_shorts.append(w)

        return no_shorts

    # Links and Web addresses
    def __remove_links(self, words):
        no_links = []
        for w in words:
            if not "www" in w:
                no_links.append(w)
        return no_links

    # Cleanse and process data

    def process_data(self):
        # value is positive or negative
        self.__value_to_number()
        # key to lowercase
        first_processed = self.review.lower()
        # Remove html tags
        second_processed = self.__remove_regex_pattern(first_processed, '<.*?>')
        # Remove punctuation
        third_processed = self.__remove_regex_pattern(second_processed, '[^\w\s]')
        # Remove numbers
        fourth_processed = self.__remove_regex_pattern(third_processed, '\w*\d\w*')
        # Remove _
        fift_processed = self.__remove_regex_pattern(fourth_processed, '[_]')
        # Tokenize processed text
        tokenized = nltk.word_tokenize(fift_processed)
        english_stopwords = nltk.corpus.stopwords.words('english')
        removed_stop_words = self.__remove_stop_words(tokenized, english_stopwords)
        # Stemming
        stemmed_words = self.__do_stemming(removed_stop_words)
        # Deleting short words
        no_short_words = self.__remove_shorts(stemmed_words)
        # Deleting links
        self.processed_data = self.__remove_links(no_short_words)


# Read CSV data and create processors

def create_processors_from_file(file_name):
    processors = []
    with open(file_name, mode='r', encoding='utf8') as csv_file:
        data_reader = csv.reader(csv_file)
        # Skip headers
        next(data_reader)
        for row in data_reader:
            processor = DataProcessor(review=row[0], sentiment=row[1])
            processors.append(processor)
    return processors


# Processing

processors = create_processors_from_file('IMDB Dataset.csv')
random.shuffle(processors)
all_words = set()

for i in range(NUMBER_OF_DATA_TO_PROCESS):
    processor = processors[i]
    processor.process_data()
    all_words.update(processor.processed_data)

words_array = list(all_words)

words_array.sort()
print(words_array)
