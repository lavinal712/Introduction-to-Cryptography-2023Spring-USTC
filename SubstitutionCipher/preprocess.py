# -*- coding: utf-8 -*-
from collections import Counter


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERSFREQRANK = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
BIGRAMFREQRANK = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR', 'ST', 'TO', 'NT']
TRIGRAMFREQRANK = ['THE', 'AND', 'ING', 'ENT', 'ION', 'FOR', 'THA', 'TIO', 'OFT', 'STH']


plaintext = 'agoodglassinthebishopshostelinthedevilsseattwentyonedegreesandthirteenminutesnortheastandbynorthmainbranchseventhlimbeastsideshootfromthelefteyeofthedeathsheadabeelinefromthetreethroughtheshotfiftyfeetout'
ciphertext = '53‡‡†305))6*;4826)4‡.)4‡);806*;48†8¶60))85;;]8*;:‡*8†83(88)5*†;46(;88*96*?;8)*‡(;485);5*†2:*‡(;4956*2(5*-4)8¶8*;4069285);)6†8)4‡‡;1(‡9;48081;8:8‡1;48†85;4)485†528806*81(‡9;48;(88;4(‡?34;48)4‡;161;:188;‡?;'


def transform(message):
    ciphertext = message.upper()
    ciphertext_frequency = dict(Counter(ciphertext))
    cipher_frequency_rank = ""
    for cipherletter, _ in sorted(ciphertext_frequency.items(), key=lambda x: x[1], reverse=True):
        cipher_frequency_rank += cipherletter
    
    tran_mapping = {LETTERSFREQRANK[i]: cipher_frequency_rank[i] for i, _ in enumerate(cipher_frequency_rank)}
    inverse_tran_mapping = {cipher_frequency_rank[i]: LETTERSFREQRANK[i] for i, _ in enumerate(cipher_frequency_rank)}
    translated_text = ""
    for symbol in ciphertext:
        if symbol.upper() in LETTERS:
            letter = inverse_tran_mapping[symbol.upper()]
            if symbol.isupper():
                translated_text += letter
            else:
                translated_text += letter.lower()
        else:
            translated_text += inverse_tran_mapping[symbol].lower()
            
    return translated_text, tran_mapping, inverse_tran_mapping


if __name__ == '__main__':
    print('Original ciphertext:')
    print(ciphertext)
    print()
    transformed_text, tran_table, inverse_tran_table = transform(ciphertext)
    print('Transformed text:')
    print(transformed_text)
    print()
    print('Transform table:')
    print(tran_table)
    print()
    print('Inversed transform table:')
    print(inverse_tran_table)