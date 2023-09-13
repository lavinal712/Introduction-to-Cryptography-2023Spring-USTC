# -*- coding: utf-8 -*-
import pprint


RANK1 = 'AOINSHR'
RANK2 = 'DLCUMWFGYPBVK'
RANK3 = 'JXQZ'


def get_word_pattern(word):
    word = word.upper()
    next_num = 0
    letter_nums = {}
    word_pattern = []

    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_pattern.append(letter_nums[letter])
    return '.'.join(word_pattern)


def get_word_pattern1(word):
    word = word.upper()
    word_pattern = []

    for letter in word:
        if letter in RANK1:
            word_pattern.append('1')
        elif letter in RANK2:
            word_pattern.append('2')
        elif letter in RANK3:
            word_pattern.append('3')
        else:
            word_pattern.append(letter)
    return '.'.join(word_pattern)


def main():
    all_patterns = {}
    all_patterns1 = {}

    fo = open('dictionary.txt')
    word_list = fo.read().split('\n')
    fo.close()

    for word in word_list:
        pattern = get_word_pattern(word)
        pattern1 = get_word_pattern1(word)

        if pattern not in all_patterns:
            all_patterns[pattern] = [word]
        else:
            all_patterns[pattern].append(word)
            
        if pattern1 not in all_patterns1:
            all_patterns1[pattern1] = [word]
        else:
            all_patterns1[pattern1].append(word)

    fo = open('word_patterns.py', 'w')
    fo.write('all_patterns = ')
    fo.write(pprint.pformat(all_patterns))
    fo.close()

    
    fo = open('word_patterns1.py', 'w')
    fo.write('all_patterns1 = ')
    fo.write(pprint.pformat(all_patterns1))
    fo.close()


if __name__ == '__main__':
    main()
