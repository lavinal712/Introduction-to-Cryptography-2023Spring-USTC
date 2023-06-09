# -*- coding: utf-8 -*-
import pprint


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


def main():
    all_patterns = {}

    fo = open('dictionary.txt')
    word_list = fo.read().split('\n')
    fo.close()

    for word in word_list:
        pattern = get_word_pattern(word)

        if pattern not in all_patterns:
            all_patterns[pattern] = [word]
        else:
            all_patterns[pattern].append(word)

    fo = open('word_patterns.py', 'w')
    fo.write('all_patterns = ')
    fo.write(pprint.pformat(all_patterns))
    fo.close()


if __name__ == '__main__':
    main()
