import os
import re

import emoji
import numpy as np
import regex
import spacy
from nltk.stem.snowball import SnowballStemmer

from src.moduls.config import PipeConfig

# Define the base directory relative to the current file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize the stemmer for German
german_stemmer = SnowballStemmer("german")

# Load the English language model
nlp = spacy.load("de_core_news_lg")

regular_punct = r".?!:\"',"
tag_include = {'PIDAT', 'PIAT', 'NN', 'NE', 'ADJA', 'ADJD', 'VVFIN', 'VVINF', 'VVPP', 'VMPP', 'VAPP', 'VVPP', 'VVIZU'}

relevant_words = set()
additional_stopwords = set()
stop_words = set(nlp.Defaults.stop_words)
custom_stop_words = (set(stop_words) - relevant_words) | additional_stopwords

pipe_cfg = PipeConfig()

def relevant_token(token, text, lemma):
    if len(lemma) < 3:
        return False
    if text in relevant_words or lemma in relevant_words:
        return True
    if text in custom_stop_words or lemma in custom_stop_words:
        return False
    return token.tag_ in tag_include

def txt_cleaning(txt):
    txt = regex.sub(r"\[DE\]", "", txt)
    txt = regex.sub(r"\(.*?\)", "", txt)
    txt = regex.sub(r"<.*?>", "", txt)
    txt = regex.sub(r"\[.*?\]", "", txt)
    txt = regex.sub(r"&gt;", "", txt)
    txt = regex.sub(r";", ",", txt)
    # remove numbers with specials between
    txt = regex.sub(r"\d+[[:punct:]]\d+", " ", txt)  
    # remove special chars except for regular punctuation
    txt = regex.sub(r"[^\p{L}" + regular_punct + r"\s]+", " ", txt)
    # remove space before punct
    txt = regex.sub(r"\s+([,.!?])", r"\1", txt) 
    # remove duplicate special chars
    txt = regex.sub(r'([^\p{L}])\1+', r"\1", txt, flags=re.IGNORECASE)
    # add space after punctuation except for :
    txt = regex.sub(r"([.?!\"',])([^\s])", r"\1 \2", txt, flags=re.IGNORECASE)
    txt = emoji.demojize(txt, language='de')
    # add space after :
    txt = regex.sub(r"([:])([^\s])", r"\1 \2", txt, flags=re.IGNORECASE)
    # add space between lower and upper case
    txt = regex.sub(r"([\p{Ll}])([\p{Lu}])", r"\1 \2", txt) 
    # remove char repetitions (more than 2)
    txt = re.sub(r'(.)\1{2,}', r"\1\1", txt, flags=re.IGNORECASE)
    # remove extra spaces
    txt = re.sub(r'\s+', " ", txt, flags=re.IGNORECASE)
    txt = remove_consecutive_word_groups(txt)
    return txt

def spacy_tokenize(txt):
    doc = nlp(txt)
    # Filter tokens: not a stop word, and its POS tag is in relevant_pos_tags
    filtered_lemmas = []
    for token in doc:
        text = regex.sub(r"[^\p{L}]+", "", token.text).lower()
        lemma = token.lemma_.lower()
        if relevant_token(token, text, lemma):
            filtered_lemmas.append(lemma)
    txt = ' '.join(filtered_lemmas)
    txt = remove_consecutive_word_groups(txt)
    return txt

def spacy_postags(txt):
    doc = nlp(txt)
    # return postags
    return [token.pos_ for token in doc]

def spacy_tags(txt):
    doc = nlp(txt)
    tokens = [token for token in doc if not token.is_punct]
    # return postags
    return [[token.lemma_.lower(), token.pos_, token.tag_] for token in tokens]

def remove_consecutive_word_groups(txt):
    txt = txt + ' '
    RE = regex.compile(r'\b((?:\p{L}+\s+)+)(?:\1)')
    # Function to apply regex replacement
    def replace_func(match):
        return match.group(1)

    # Apply the regex replacement iteratively until no changes are made
    while True:
        new_text, count = RE.subn(replace_func, txt)
        if count == 0:
            break
        txt = new_text

    return txt.strip()



def feature_selection(text):
    words = text.split()  # Split text into words
    filtered_words = [word for word in words if word in pipe_cfg.get_features()]  # Keep only words found in the vocabulary
    txt = ' '.join(filtered_words)  # Join words back into a string
    txt = remove_consecutive_word_groups(txt)
    return txt

def features2vec(txt):
    c_len = pipe_cfg.context_length
    stoi = {s: i + 1 for i, s in enumerate(pipe_cfg.get_features())}
    stoi['.'] = 0
    x = [stoi[v] for v in txt.split()]
    x = [0] * (c_len - len(x)) + list(x) if len(x) < c_len else x[:c_len]
    return ' '.join(str(v) for v in x)

def unify_tokens(txt):
    tokens = txt.split(' ')
    tokens = tokens[:39] if len(tokens) > 38 else tokens + ['<pad>'] * (39 - len(tokens))
    return ' '.join(tokens)

def preproc_pipe(txt):
    txt = txt_cleaning(txt)
    if len(txt.split()) <= 4:
        return None
    txt = spacy_tokenize(txt)
    if len(txt.split()) <= 4:
        return None
    txt = feature_selection(txt)
    if len(txt.split()) <= 4:
        return None
    x = features2vec(txt)
    return x