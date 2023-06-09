# -*- coding: utf-8 -*-
import re, copy, word_patterns, make_word_patterns


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
non_letters_or_space_pattern = re.compile('[^A-Z\s]')


def main():
    message = ""
    
    with open('ciphertext.txt', 'r') as file:
        message = file.read()
    
    print('Original ciphertext:')
    print(message)
    print()
    print('Hacking...')
    letter_mapping = hack_simple_sub(message)
    print('Mapping:')
    print(letter_mapping)
    print()
    print('Decrypting...')
    hacked_message = decrypt_with_cipherletter_mapping(message, letter_mapping)
    print('Decrypted text:')
    print(hacked_message)
    
        
def get_blank_cipherletter_mapping():
    return {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}, 'G': {}, 'H': {}, 'I': {}, 'J': {}, 'K': {}, 'L': {}, 'M': {}, 'N': {}, 'O': {}, 'P': {}, 'Q': {}, 'R': {}, 'S': {}, 'T': {}, 'U': {}, 'V': {}, 'W': {}, 'X': {}, 'Y': {}, 'Z': {}}


def add_letters_to_mapping(letter_mapping, cipherword, candidate):
    for i in range(len(cipherword)):
        if candidate[i] not in letter_mapping[cipherword[i]]:
            letter_mapping[cipherword[i]][candidate[i]] = 1
        else:
            letter_mapping[cipherword[i]][candidate[i]] += 1
    

def intersect_mappings(map1, map2):
    intersected_mapping = get_blank_cipherletter_mapping()
    for letter in LETTERS:
        if map1[letter] == {}:
            intersected_mapping[letter] = copy.deepcopy(map2[letter])
        elif map2[letter] == {}:
            intersected_mapping[letter] = copy.deepcopy(map1[letter])
        else:
            for mapped_letter, weight in map1[letter].items():
                if mapped_letter in map2[letter]:
                    intersected_mapping[letter][mapped_letter] = weight + map2[letter][mapped_letter]
                    
    return intersected_mapping


def remove_solved_letters_from_mapping(letter_mapping):
    loop = True
    while loop:
        loop = False
        solved_letters = []
        for cipherletter in LETTERS:
            if len(letter_mapping[cipherletter]) == 1:
                solved_letters.append(list(letter_mapping[cipherletter].keys())[0])
        
        for cipherletter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipherletter]) != 1 and s in letter_mapping[cipherletter]:
                    letter_mapping[cipherletter].pop(s)
                    if len(letter_mapping[cipherletter]) == 1:
                        loop = True
                elif letter_mapping[cipherletter] == {}:
                    letter_mapping[cipherletter] = {cipherletter: 0}
    
    for cipherletter in LETTERS:
        if len(letter_mapping[cipherletter]) > 1:
            letter_mapping[cipherletter] = dict(sorted(letter_mapping[cipherletter].items(), key = lambda x: x[1], reverse = True))
    
    return letter_mapping

def hack_simple_sub(message):
    intersected_map = get_blank_cipherletter_mapping()
    cipherword_list = non_letters_or_space_pattern.sub('', message.upper()).split()
    
    for cipherword in cipherword_list:
        candidate_map = get_blank_cipherletter_mapping()
    
        word_pattern = make_word_patterns.get_word_pattern(cipherword)
        if word_pattern not in word_patterns.all_patterns:
            continue
        
        for candidate in word_patterns.all_patterns[word_pattern]:
            add_letters_to_mapping(candidate_map, cipherword, candidate)
        
        intersected_map = intersect_mappings(intersected_map, candidate_map)
        
    return remove_solved_letters_from_mapping(intersected_map)


def decrypt_with_cipherletter_mapping(ciphertext, letter_mapping):
    translated_text = ""
    for symbol in ciphertext:
        if symbol.upper() in letter_mapping:
            letter, weight = list(letter_mapping[symbol.upper()].items())[0]
            if symbol.isupper():
                translated_text += letter
            else:
                translated_text += letter.lower()
        else:
            translated_text += symbol

    return translated_text
    

if __name__ == '__main__':
    main()