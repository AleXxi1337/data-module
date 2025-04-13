from classes.words import STOP_WORDS, REDUCTIONS_WORDS
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def preprocess(text : str) -> str:
    words = text.lower().strip().replace('- ', '').replace('-', ' ').replace(',', '').replace('«', '').replace('»', '').replace('/', ' ').replace('(', '').replace(')', '').replace('|', '').replace('"', '').split()
    filtered_words = [word for word in words if word not in STOP_WORDS]

    normalized_words = [morph.parse(word)[0].normal_form for word in filtered_words]
    normalized_words = [REDUCTIONS_WORDS[word] if word in REDUCTIONS_WORDS.keys() else word for word in normalized_words]

    return ' '.join(normalized_words)