# -*- coding: utf-8 -*-
import gradio as gr
import pandas as pd
import simple_substitution_cipher as ssc
import frequency_analysis as freq
import preprocess as pps


def decrypt_with_key(key, ciphertext):
    if ciphertext == "":
        return ciphertext
    if key == "":
        key = ssc.hack_simple_sub(ciphertext)
    if isinstance(key, str):
        key = eval(key)
    
    translated_text = ""
    for symbol in ciphertext:
        if symbol.upper() in key:
            letter = key[symbol.upper()]
            if symbol.isupper():
                translated_text += letter
            else:
                translated_text += letter.lower()
        else:
            translated_text += symbol

    return translated_text


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
        bigram_frequency = freq.bigram_frequency_analysis(ciphertext)
        bigram_frequency = bigram_frequency[:(20 if len(bigram_frequency) > 20 else -1)]
        return gr.BarPlot.update(
            value=pd.DataFrame({
                'bigram': [bigram for bigram, _ in bigram_frequency],
                'freq': [freq for _, freq in bigram_frequency],
            }),
            x="bigram",
            y="freq",
            x_title="Cipher bigram",
            y_title="Frequency",
        )
    elif display == "trigram frequency":
        trigram_frequency = freq.trigram_frequency_analysis(ciphertext)
        trigram_frequency = trigram_frequency[:(20 if len(trigram_frequency) > 20 else -1)]
        return gr.BarPlot.update(
            value = pd.DataFrame({
                'trigram': [trigram for trigram, _ in trigram_frequency],
                'freq': [freq for _, freq in trigram_frequency],
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
    

with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Simple Subsititution Cipher
        """
    )
    inputs = gr.Textbox(label="Input Ciphertext")
    
    with gr.Tab("Decrypt"):
        with gr.Row():
            with gr.Column():
                outputs = gr.Textbox(label="Decrypted Text")
                key = gr.Textbox(label="Decrypted Key")

        with gr.Row():
            decrypt = gr.Button(value="Decrypt")
            change_key = gr.Button(value="Change Key")
            decrypt.click(
                fn=lambda key, ciphertext: ssc.hack_simple_sub(ciphertext) if key == "" else key, 
                inputs=[key, inputs],
                outputs=key,
            )
            decrypt.click(
                fn=decrypt_with_key, 
                inputs=[key, inputs],
                outputs=outputs,
            )
            change_key.click(
                fn=lambda key: eval(key) if key != "" else key,
                inputs=key,
                outputs=key,
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
        
    with gr.Tab("Preprocess"):
        with gr.Row():
            with gr.Column():
                inputs = gr.Textbox(label="Text")
                outputs = gr.Textbox(label="Transformed Text")
                table = gr.Textbox(label="Transform Table")
                inverse_table = gr.Textbox(label="Inversed Transform Table")
                transform = gr.Button(value="Transform")
        
        transform.click(
            fn=pps.transform, 
            inputs=inputs,
            outputs=[outputs, table, inverse_table],
        )
        
demo.launch()