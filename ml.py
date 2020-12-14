from rich import print

import spacy

nlp = spacy.load("en_core_web_sm")
print(nlp)