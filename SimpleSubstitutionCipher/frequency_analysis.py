# -*- coding: utf-8 -*-
from collections import Counter
import re


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
non_letters_or_space_pattern = re.compile('[^A-Z\s]')
FREQENCY = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
}
LETTERSFREQRANK = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
BIGRAMFREQRANK = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR', 'ST', 'TO', 'NT']
TRIGRAMFREQRANK = ['THE', 'AND', 'ING', 'ENT', 'ION', 'FOR', 'THA', 'TIO', 'OFT', 'STH']


def main():
    message = ""
    
    with open('ciphertext.txt', 'r') as file:
        message = file.read()
    
    print('Original ciphertext:')
    print(message)
    print()
    letter_frequency = frequency_analysis(message)
    print('Letter frequency:')
    print(letter_frequency)
    print()
    bigram_frequency = bigram_frequency_analysis(message)
    print('Bigram frequency:')
    print(bigram_frequency)
    print()
    trigram_frequency = trigram_frequency_analysis(message)
    print('Trigram frequency:')
    print(trigram_frequency)

        
def frequency_analysis(message):
    ciphertext = message.upper()
    ciphertext_frequency = dict(Counter(ciphertext))
    for c in list(ciphertext_frequency.keys()):
        if c not in LETTERS:
            ciphertext_frequency.pop(c)
    
    letter_num = sum(list(ciphertext_frequency.values()))
    for letter in LETTERS:
        if letter not in ciphertext_frequency:
            ciphertext_frequency[letter] = 0
        else:
            ciphertext_frequency[letter] /= (letter_num / 100)

    return sorted(ciphertext_frequency.items(), key=lambda x: x[1], reverse=True)


def bigram_frequency_analysis(message):
    bigram_frequency = {}
    cipherword_list = non_letters_or_space_pattern.sub('', message.upper()).split()
    
    for cipherword in cipherword_list:
        bigram_list = [cipherword[i: i + 2] for i in range(len(cipherword) - 1)]
        for bigram in bigram_list:
            if bigram in bigram_frequency:
                bigram_frequency[bigram] += 1
            else:
                bigram_frequency[bigram] = 1
    
    bigram_num = sum(list(bigram_frequency.values()))
    for bigram in bigram_frequency.keys():
        bigram_frequency[bigram] /= (bigram_num / 100)
    
    return sorted(bigram_frequency.items(), key=lambda x: x[1], reverse=True)[:(20 if len(bigram_frequency) > 20 else -1)]


def trigram_frequency_analysis(message):
    trigram_frequency = {}
    cipherword_list = non_letters_or_space_pattern.sub('', message.upper()).split()
    
    for cipherword in cipherword_list:
        trigram_list = [cipherword[i: i + 3] for i in range(len(cipherword) - 2)]
        for trigram in trigram_list:
            if trigram in trigram_frequency:
                trigram_frequency[trigram] += 1
            else:
                trigram_frequency[trigram] = 1
    
    trigram_num = sum(list(trigram_frequency.values()))
    for trigram in trigram_frequency.keys():
        trigram_frequency[trigram] /= (trigram_num / 100)
    
    return sorted(trigram_frequency.items(), key=lambda x: x[1], reverse=True)[:(20 if len(trigram_frequency) > 20 else -1)]
        

if __name__ == '__main__':
    main()