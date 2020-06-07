import csv
import re
import nltk
import random
import os
from nltk.stem import PorterStemmer

# Constants

NUMBER_OF_DATA_TO_PROCESS = 1_000


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


# Balance data

def balance_data(processors):
    number_of_processors = NUMBER_OF_DATA_TO_PROCESS / 2
    positive_processors_count = 0
    negative_processors_count = 0
    balanced_processors = []

    for processor in processors:
        if processor.sentiment == 'positive' and positive_processors_count < number_of_processors:
            positive_processors_count += 1
            balanced_processors.append(processor)
        elif negative_processors_count < number_of_processors:
            negative_processors_count += 1
            balanced_processors.append(processor)
        else:
            break

    print(positive_processors_count, negative_processors_count)
    return balanced_processors


# Process data


def process_data(processors):
    chosen_processors = []
    all_words = set()
    progress_printer = ProgressPrinter(NUMBER_OF_DATA_TO_PROCESS)

    for i in range(len(processors)):
        processor = processors[i]
        chosen_processors.append(processor)
        processor.process_data()
        all_words.update(processor.processed_data)
        progress_printer.iteration_performed(i, 'Data processing')

    return chosen_processors, list(all_words)

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

        # Sentiment
        result += '@ATTRIBUTE _CLASS_ {0,1}\n'
        result += '@DATA\n'

        for i in range(len(processors)):
            processor = processors[i]
            for word in all_words:
                result += '1,' if word in processor.processed_data else '0,'
            result += f'{processor.sentiment_number}\n'
            progress_printer.iteration_performed(i, 'Processed data written')

        file.write(result)


# Main

def main():
    processors = create_processors_from_file('IMDB Dataset.csv')
    random.shuffle(processors)
    processors = balance_data(processors)
    processors, all_words = process_data(processors)
    create_arff_result(processors, all_words)


if __name__ == "__main__":
    main()
