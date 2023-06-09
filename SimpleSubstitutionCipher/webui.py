# -*- coding: utf-8 -*-
import gradio as gr
import pandas as pd
import simple_substitution_cipher as ssc
import frequency_analysis as freq


def decrypt_with_dictionary(ciphertext):
    decrypted_map = ssc.hack_simple_sub(ciphertext)
    decrypted_text = ssc.decrypt_with_cipherletter_mapping(ciphertext, decrypted_map)
    return decrypted_text


def decrypt_key(ciphertext):
    LETTERS = ssc.LETTERS
    decrypted_map = ssc.hack_simple_sub(ciphertext)
    key = ""
    
    for letter in LETTERS:
        key += list(decrypted_map[letter].keys())[0]
    
    return key


def plot_frequency(display, ciphertext):
    if ciphertext == "":
        return None
    if display == "letter frequency":
        return gr.BarPlot.update(
            value = pd.DataFrame({
                'letter': [letter for letter, _ in freq.frequency_analysis(ciphertext)],
                'freq': [freq for _, freq in freq.frequency_analysis(ciphertext)],
            }),
            x="letter",
            y="freq",
            x_title="Cipher letter",
            y_title="Frequency",
        )
    elif display == "bigram frequency":
        return gr.BarPlot.update(
            value=pd.DataFrame({
                'bigram': [bigram for bigram, _ in freq.bigram_frequency_analysis(ciphertext)[:20]],
                'freq': [freq for _, freq in freq.bigram_frequency_analysis(ciphertext)[:20]],
            }),
            x="bigram",
            y="freq",
            x_title="Cipher bigram",
            y_title="Frequency",
        )
    elif display == "trigram frequency":
        return gr.BarPlot.update(
            value = pd.DataFrame({
                'trigram': [trigram for trigram, _ in freq.trigram_frequency_analysis(ciphertext)[:20]],
                'freq': [freq for _, freq in freq.trigram_frequency_analysis(ciphertext)[:20]],
            }),
            x="trigram",
            y="freq",
            x_title="Cipher trigram",
            y_title="Frequency",
        )
    
    
def decrypt_advice(display, ciphertext):
    if ciphertext == "":
        return ""
    if display == "letter frequency":
        return f'Cipher letter {freq.frequency_analysis(ciphertext)[0][0]} may be {freq.LETTERSFREQRANK[0]}'
    elif display == "bigram frequency":
        return f'Cipher bigram {freq.bigram_frequency_analysis(ciphertext)[0][0]} may be {freq.BIGRAMFREQRANK[0]}'
    elif display == "trigram frequency":
        return f'Cipher trigram {freq.trigram_frequency_analysis(ciphertext)[0][0]} may be {freq.TRIGRAMFREQRANK[0]}'


def decrypt_with_key(key, ciphertext):
    LETTERS = ssc.LETTERS
    def is_valid(key):
        key_list = list(key)
        letters_list = list(LETTERS)
        return sorted(key_list) == sorted(letters_list)
    
    if not is_valid(key):
        return f'{key} is not a valid key'
    elif ciphertext == "":
        return ""
    else:
        translated_text = ""
        for symbol in ciphertext:
            if symbol.upper() in key:
                letter = key[LETTERS.index(symbol.upper())]
                if symbol.isupper():
                    translated_text += letter
                else:
                    translated_text += letter.lower()
            else:
                translated_text += symbol

        return translated_text
    

with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Simple Subsititution Cipher
        """
    )
    inputs = gr.Textbox(label="Input Ciphertext")
    
    with gr.Tab("Decrypt with Word Pattern"):
        with gr.Row():
            with gr.Column():
                outputs = gr.Textbox(label="Decrypted Text")
                key = gr.Textbox(label="Decrypted Key")

        with gr.Row():
            gr.Button("Decrypt").click(
                fn=decrypt_with_dictionary, 
                inputs=inputs,
                outputs=outputs,
            )
            gr.Button("Decrypt").click(
                fn=decrypt_key, 
                inputs=inputs,
                outputs=key,
            )
    
    with gr.Tab("Decrypt with Key"):
        with gr.Row():
            with gr.Column():
                key = gr.Textbox(
                    label="Key: cipher letter correspond to alphabet",
                    placeholder="QWERTYUIOPASDFGHJKLZXCVBNM",
                )
                outputs = gr.Textbox(label="Decrypted Text")
                
        with gr.Row():
            gr.Button("Decrypt").click(
                fn=decrypt_with_key, 
                inputs=[key, inputs],
                outputs=outputs,
            )

    with gr.Tab("Frequency Analysis"):
        with gr.Row():
            with gr.Column():
                frequency_type = gr.Dropdown(
                    choices=["letter frequency", "bigram frequency", "trigram frequency"],
                    value=None,
                    label="Type of Frequency",
                )
                english_frequency = gr.Markdown(
                    """
                    ## English letter frequency rank:
                    E T A O I N S H R D L C U M W F G Y P B V K J X Q Z
                    ## English bigram frequency rank:
                    TH HE IN ER AN RE ON AT EN ND TI ES OR TE OF ED IS IT AL AR ST TO NT
                    ## English trigram frequency rank:
                    THE AND ING ENT ION FOR THA TIO OFT STH
                    """
                )
            with gr.Column():
                plot = gr.BarPlot()
                advice = gr.Textbox(label="Decrypt Advice")
        
        frequency_type.change(
            fn=plot_frequency, 
            inputs=[frequency_type, inputs], 
            outputs=plot
        )
        frequency_type.change(fn=decrypt_advice, 
                              inputs=[frequency_type, inputs], 
                              outputs=advice
        )
          
demo.launch()