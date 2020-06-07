import csv
import re
import nltk
import random
import os
import collections

# Constants

NUMBER_OF_DATA_TO_PROCESS = 5_000


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
        self.processed_data = self.__remove_stop_words(tokenized, english_stopwords)


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