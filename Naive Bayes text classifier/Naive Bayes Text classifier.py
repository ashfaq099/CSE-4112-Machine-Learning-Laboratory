# -*- coding: utf-8 -*-
"""1907099.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XIsm4ACtDltHrJUs8nnWHk41KLeESaLa

Imports
"""

import pandas as pd
import numpy as np

"""Datasets"""

# Load dataset
def load_dataset(file_path):
    return pd.read_excel(file_path)

"""Preprocess Text and Calculate Class Probabilities"""

def calculate_class_probabilities(data_frame):
    total_data_points = len(data_frame)
    class_probabilities = {}
    word_counts_per_class = {}
    all_words = set()

    for index, row in data_frame.iterrows():
        class_name = row['class']
        words = row['words'].split()

        if class_name not in word_counts_per_class:
            word_counts_per_class[class_name] = {}

        for word in words:
            all_words.add(word)
            word_counts_per_class[class_name][word] = word_counts_per_class[class_name].get(word, 0) + 1

        class_probabilities[class_name] = class_probabilities.get(class_name, 0) + 1

    for class_name in class_probabilities:
        class_probabilities[class_name] /= total_data_points

    total_unique_words = len(all_words)
    return class_probabilities, word_counts_per_class, total_unique_words

"""Calculate Conditional Probability of a word given a class"""

def get_conditional_probability(word, class_name, word_counts_per_class, total_unique_words):
    if word_counts_per_class.get(class_name) is None:
        return 1 / total_unique_words

    word_count_in_class = word_counts_per_class[class_name].get(word, 0)
    total_words_in_class = sum(word_counts_per_class[class_name].values())
    return (word_count_in_class + 1) / (total_words_in_class + total_unique_words)

""" Find the most probable class for a sentence"""

def find_most_probable_class(sentence, class_probabilities, word_counts_per_class, total_unique_words):
    sentence_words = sentence.split()
    class_probs = {}

    for class_name in class_probabilities:
        class_probability = class_probabilities[class_name]
        word_probabilities = [get_conditional_probability(word, class_name, word_counts_per_class, total_unique_words) for word in sentence_words]
        class_probs[class_name] = class_probability * np.prod(word_probabilities)

    return max(class_probs, key=class_probs.get)

"""Take input & determine most probable class"""

# Test sentence
input_string = input("Enter a sentence: ")
#example_input_string = "Chinese Chinese Chinese Tokyo Japan"
# Load dataset
dataset = load_dataset("/content/sample_data/dataset.xlsx")

# Preprocess data and calculate probabilities
class_probabilities, word_counts_per_class, total_unique_words = calculate_class_probabilities(dataset)

# Find most probable class
most_probable_class = find_most_probable_class(input_string, class_probabilities, word_counts_per_class, total_unique_words)
print("Most probable class for the input String:", most_probable_class)