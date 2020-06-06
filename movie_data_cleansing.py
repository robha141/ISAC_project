import csv
import re
import nltk
import os


class DataProcessor:

    def __init__(self, review, sentiment):
        self.review = review
        self.sentiment = sentiment
        self.sentiment_number = 0
        self.processed_data = ''

    # update value, if positive == 1, otherwise 0

    def __value_to_number(self):
        self.sentiment_number = 1 if (self.sentiment == 'positive') else 0

    # Remove pattern

    def __remove_regex_pattern(self, text, pattern):
        pattern = re.compile(pattern)
        return re.sub(pattern, '', text)

    def __remove_stop_words(self, tokenized_text, stopwords):
        return [word for word in tokenized_text if not word in stopwords]

    def __list_to_string(self, s):
        str = " "
        return str.join(s)

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
        # Tokenize processed text
        tokenized = nltk.word_tokenize(fourth_processed)
        english_stopwords = nltk.corpus.stopwords.words('english')
        removed_stopwords = self.__remove_stop_words(tokenized, english_stopwords)
        self.processed_data = self.__list_to_string(removed_stopwords)


# Read CSV data

def read_data(file_name):
    result = {}
    with open(file_name, mode='r', encoding='utf8') as csv_file:
        data_reader = csv.reader(csv_file)
        # Skip headers
        next(data_reader)
        for row in data_reader:
            key = row[0]
            value = row[1]
            result[key] = value
    return result


dictionary = read_data('IMDB Dataset.csv')

# Cleansing


result_file_name = 'result.csv'

if os.path.exists(result_file_name):
  os.remove(result_file_name)


iterator = iter(dictionary.items())

with open(result_file_name, mode='+w') as result_file:
    result_writer = csv.writer(result_file, delimiter=',')

    for i in range(4):
        keyValue = next(iterator)
        processor = DataProcessor(keyValue[0], keyValue[1])
        processor.process_data()
        result_writer.writerow([processor.sentiment_number, processor.processed_data])


# for key in dictionary:
#     # value is positive or negative
#     value = dictionary[key]
#     value_number = value_to_number(value)
#     # key to lowercase
#
#     print(key)
