import csv
import re



class DataProcessor:

    def __init__(self, review, sentiment):
        self.review = review
        self.sentiment = sentiment
        self.sentimentNumber = 0

    # update value, if positive == 1, otherwise 0

    def __value_to_number(self):
        self.sentimentNumber = 1 if (self.sentiment == 'positive') else 0

    # Remove pattern

    def __remove_regex_pattern(self, text, pattern):
        pattern = re.compile(pattern)
        return re.sub(pattern, '', text)

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
        print(fourth_processed)


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

iterator = iter(dictionary.items())
for i in range(4):
    keyValue = next(iterator)
    processor = DataProcessor(keyValue[0], keyValue[1])
    processor.process_data()

# for key in dictionary:
#     # value is positive or negative
#     value = dictionary[key]
#     value_number = value_to_number(value)
#     # key to lowercase
#
#     print(key)
