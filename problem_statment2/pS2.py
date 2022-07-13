from pdf2image import convert_from_path
from PIL import Image
from numpy import append
import pytesseract
import cv2
import re
from distutils.command.config import config
from googletrans import Translator
import os
from om_transliterator import Transliterator
import sys
from indicnlp.transliterate.unicode_transliterate import ItransTransliterator
from indicnlp import loader
from indicnlp import common

filename=input()
poppler_path = r'/opt/homebrew/Cellar/poppler/22.06.0/bin'
pdf_path = filename
lan=input()
images = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)
file_names=[]
for count, img in enumerate(images):
    img_name = f"page_{count+1}.png"
    img.save(img_name, "PNG")
    file_names.append(img_name)
print(file_names)
######################################
ss=""
for file in file_names:
    img=cv2.imread(file)
    text=pytesseract.image_to_string(Image.open(file), lang=lan)         
    ss+=text
with open('ocr.txt', 'w', encoding='utf-8') as f:
    print(ss, file=f)
print("ocr process completed")

cv2. destroyWindow("Test")
cv2.destroyWindow("Main")
######################################

transliterator = Transliterator()
original_text = open(r'ocr.txt','r',encoding='utf-8').read()

if lan=='hin':
    INDIC_NLP_RESOURCES = r'/Users/chirag/tesseract-ocr/indic_nlp_library-master/indicnlp'
    common.set_resources_path(INDIC_NLP_RESOURCES)
    loader.load()
    # Transliterate Hindi to Roman
    transliterated_text=ItransTransliterator.to_itrans(original_text, 'hi')

elif lan=="kan":
    transliterated_text = transliterator.knda_to_latn(original_text)   


text=transliterated_text.replace("ā", "a",10000)
text=text.replace("ḥ", "h",10000)
text=text.replace("ś", "s",10000)
text=text.replace("ē", "e",10000)
text=text.replace("ṁ", "m",10000)
text=text.replace("ṇ", "n",10000)
text=text.replace("ṭ", "t",10000)
text=text.replace("ū", "u",10000)
text=text.replace("ō", "o",10000)
text=text.replace("ḷ", "l",10000)
text=text.replace("ī", "i",10000)
text=text.replace("ḍ", "d",10000)
text=text.replace("ṅ", "n",10000)
text=text.replace("ṣ", "s",10000)
text=text.replace("ँ", "o",10000)
text=text.replace("़", "o",10000)
text=text.replace("R^", "r",10000)


with open('solution2.txt', 'w', encoding='utf-8') as f:
    print(text, file=f)