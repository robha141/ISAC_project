import csv
import re
import nltk
import random
import os
import collections

# Constants

NUMBER_OF_DATA_TO_PROCESS = 50


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


class ProgressPrinter:

    def __init__(self, total_number_of_data):
        self.progress = 0
        self.last_progress = 0
        self.total_number_of_data = total_number_of_data

    def iteration_performed(self, iteration, message):
        self.progress = round((iteration / self.total_number_of_data) * 100)
        if self.progress != self.last_progress:
            self.last_progress = self.progress
            print(message, self.last_progress, '%')


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


# Crate arff file from data

def create_arff_result(processors, all_words):
    result_file_name = 'result.arff'
    progress_printer = ProgressPrinter(len(processors))
    print('Processors length', len(processors))

    all_words.sort()

    if os.path.exists(result_file_name):
        os.remove(result_file_name)
        print('Removed old arff file')

    with open(result_file_name, 'w+', encoding='utf8') as file:
        result = ''
        result += '@RELATION data\n\n'
        for word in all_words:
            result += f'@ATTRIBUTE {word} NUMERIC\n'

        result += '@ATTRIBUTE __CLASS__ { }'
        result += '\n@DATA\n\n'

        for i in range(len(processors)):
            processor = processors[i]
            for word in all_words:
                result += '1,' if word in processor.processed_data else '0,'
            result += '\n'
            progress_printer.iteration_performed(i, 'Processed data written')

        file.write(result)


# Processing

processors = create_processors_from_file('IMDB Dataset.csv')
chosen_processors = []
random.shuffle(processors)
all_words = set()
progress_printer = ProgressPrinter(NUMBER_OF_DATA_TO_PROCESS)

for i in range(NUMBER_OF_DATA_TO_PROCESS):
    processor = processors[i]
    chosen_processors.append(processor)
    processor.process_data()
    all_words.update(processor.processed_data)
    progress_printer.iteration_performed(i, 'Data processing')

create_arff_result(chosen_processors, list(all_words))
