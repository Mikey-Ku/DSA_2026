"""
Use a Markov process to generate random sentences based on a source text.
"""

import random


def build_word_list(source_text):
    """
    This function will take in a string of text and return a list of strings
    that represents the original string separated by every whitespace.

    Args:
        source_text: String of text user wants to separate

    Return: Returns a list of strings that represents the string of text
    separated into individual words
    """
    word = source_text.split()
    return word

def build_next_words(word_list):
    """
    This function takes in the separated string list and creates a dictionary
    that has each string as a key and has a list corresponding to each key
    that represents a string that could possibly follow it.

    Args:
        word_list: List of strings that represent a separated word

    Return: Returns a dictionary of each separated string as a key
    and the possible strings that could follow it as its items
    """
    words = [""] + word_list + [""]
    word_dict = {}
    punctuation = ".!?"
    i = 0
    while i < len(words) - 1:
        current = words[i]
        next_word = words[i + 1]
        if current != "" and current[-1] in punctuation:
            words.insert(i + 1, "")
            if current not in word_dict:
                word_dict[current] = [""]
        elif current in word_dict:
            word_dict[current].append(next_word)
        else:
            word_dict[current] = [next_word]
        i += 1
    if words[-1] == words[-2]:
        word_dict[words[-1]].remove("")

    last_word = words[-2]
    if punctuation not in last_word and last_word != "":
        del word_dict[last_word]
    return word_dict

def generate_sentence(next_words):
    """
    Function that takes in a dictionary of words and produces
    a randomly generated sentence using the previous words
    items to generate the next word

    args:
        next_words: Dictionary of words (key) and possible words that follow (items)

    Return: returns a randomly generated string sentence that was compiled from the
    dictionary of words and their possible items
    """
    previous_word = ""
    sentence = ""
    Run = True
    punctuation = ".!?"
    while Run is True:
        possible_words = next_words[previous_word]
        next_word = random.choice(possible_words)
        if next_word != "" and next_word[-1] in punctuation:
            sentence = sentence + next_word
            Run = False
        else:
            sentence = sentence + next_word + " "
        previous_word = next_word
    return sentence

def generate_text(next_words, num_sentences):
    """
    Function that takes in a dictionary of words and produces as many
    random generated sentences as num_sentences

    Args:
        next_words: A dictionary of strings as keys and their items as a
        list of possible strings that can follow
        num_sentences: An integer value that represents the number of
        sentences the user would like to output.

    Returns: A string that is num_sentences sentences long and is a
    combination of the random generated strings using the next_words dictionary
    """
    paragraph = ""
    for i in range(num_sentences):
        paragraph += generate_sentence(next_words)
        if i < num_sentences - 1:
            paragraph += " "
    return paragraph
