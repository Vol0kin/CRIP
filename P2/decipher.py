# -*- coding: utf-8 -*-

"""
This files contains functions to decipher texts that have been ciphered using
Caesar and Vigènere cipher. However, one must know which shift and key have been
used in each case.
"""

import numpy as np

ALPHABET = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
CHAR_TO_VAL_DICT = {ALPHABET[v]: v for v in range(len(ALPHABET))}
VAL_TO_CHAR_DICT = {v: c for c, v in CHAR_TO_VAL_DICT.items()}


def read_file(path):
    """
    Function that reads the content of a file and returns it.
    
    :param path: Path of the file to be read.
    
    :return Returns the content of the file as a string.
    """
    with open(path) as f:
        content = f.read()
    
    return content


def decipher_caesar(text, k):
    """
    Function that allows to decipher a text that has been ciphered using
    Cesar cipher.
    
    :param text: Text to be deciphered.
    :param k: Shift used to cipher the text.
    
    :return Returns a deciphered version of the input text.
    """
    # Transform text to numerical values
    text_vals = np.array([CHAR_TO_VAL_DICT[l] for l in text])
    
    # Get text length
    len_ALPHABET = len(ALPHABET)
    
    # Get original values by substracting the applied shift
    decipher_vals = (text_vals - k) % len_ALPHABET
    
    # Transform numerical values to chars
    deciphered_text = ''.join([VAL_TO_CHAR_DICT[v] for v in decipher_vals])
    
    return deciphered_text


def decipher_vigenere(text, key):
    """
    Function that allows to decipher a text that has been ciphered using
    Vigenere cipher.
    
    :param text: Text to be deciphered.
    :param key: Key used to cipher the original text.
    
    :return Returns a deciphered version of the input text.
    """
    # Create function to map chars to values
    map_char_to_val = lambda x: CHAR_TO_VAL_DICT[x]
    
    # Convert key characters to uppercase
    key = key.upper()
    
    # Convert key to numerical values values
    key_vals = list(map(map_char_to_val, key))
    
    # Repeat key so it has the same length as the text
    num_repetitions = len(text) // len(key) + 1
    key_long = np.array(key_vals * num_repetitions)
    key_long = key_long[:len(text)]
    
    # Convert text to numerical values
    text_vals = np.array(list(map(map_char_to_val, text)))
    
    # Get text length
    len_ALPHABET = len(ALPHABET)
    
    # Get original text values
    decipher_vals = (text_vals - key_long) % len_ALPHABET
    
    # Transform numerical values to chars
    deciphered_text = ''.join([VAL_TO_CHAR_DICT[v] for v in decipher_vals])
    
    return deciphered_text
    
    
    
    
