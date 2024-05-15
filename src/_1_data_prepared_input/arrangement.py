import pandas as pd
import re

def set_lang(df):
    if '[EN]' in df['abstract'] and '[EN]' in df['title']:
        return 'en'
    elif '[DE]' in df['abstract'] and '[DE]' in df['title']:
        return 'de'
    else:
        return None


# Define the function to arrange text based on the language
def arrange_txt_en(row):
    title = extract_english_text(row['title'])
    abstract = extract_english_text(row['abstract'])

    return pd.Series([title, abstract])


def arrange_txt_de(row):
    title = extract_german_text(row['title'])
    abstract = extract_german_text(row['abstract'])

    return pd.Series([title, abstract])


def extract_english_text(text):
    # Match the text that follows [EN] until the next language tag or the end of the string
    match = re.search(r'\[EN\](.*?)(\[\w{2}\]|$)', text)
    if match:
        # Extract the English text and strip any leading/trailing whitespace
        english_text = match.group(1).strip()
        return english_text
    return None

def extract_german_text(text):
    # Match the text that follows [EN] until the next language tag or the end of the string
    match = re.search(r'\[DE\](.*?)(\[\w{2}\]|$)', text)
    if match:
        # Extract the English text and strip any leading/trailing whitespace
        english_text = match.group(1).strip()
        return english_text
    return None