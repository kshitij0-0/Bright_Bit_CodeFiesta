from unicodedata import digit
from pdf2image import convert_from_path
from PIL import Image
from numpy import append
from pyparsing import Word
import pytesseract
import cv2
from distutils.command.config import config
from googletrans import Translator
import os
from PIL import Image
import re
import re
import numpy as np
import cv2
import pyautogui
import json

sent=""

filename=input()
poppler_path = r'/opt/homebrew/Cellar/poppler/22.06.0/bin'
pdf_path = filename
images = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)
file_names=[]
for count, img in enumerate(images):
    img_name = f"page_{count+1}.png"
    img.save(img_name, "PNG")
    file_names.append(img_name)
print(file_names)

lan=input("enter the language")

if lan=="kan":
    la='kn'
    state='karnataka'
elif lan=="guj":
    la='gu'
    state="gujrat"
else:
    la='hi'  
    state="delhi"      


for file in file_names:
    img=cv2.imread(file)
    text=pytesseract.image_to_string(Image.open(file), lang='eng+'+lan)
    translator = Translator()
    translated = translator.translate(text, src=la, dest='en')
    string = translated.text
    sent=sent+string

lin=re.search('(?<=Under Section )(.* )', sent).group(1)

string1=re.sub(r'\s*\([^)]+\)', '\n', sent)

with open('output.txt', 'w', encoding='utf-8') as f:
    print("Under Section "+lin,file=f)
    print(string1, file=f)
#####################################
   
str="klkl  "
cont=open('output.txt','r').read()
full_cont=cont
lists=['District ','Police ','Type of Information: ',' Date','Station r ','State ','Accused Name','Name'," Father's /",'Nationality','Date from','Time from','Time to','Year',' Date / Year of Birth ']
for val in lists:
    if val not in cont: 
        file_object = open('output.txt', 'a')
        file_object.write(val+' $')
        file_object.write('\n')
        file_object.close()  
content=open('output.txt','r').read()


if len(re.search("(?<=Father's / Hu)(.*)", content).group(1))==0:
    fname=re.search("Father's / Hu[\r\n]+([^\r\n]+)", content).group(1)
else:    
    fname=re.search("(?<=Father's / Hu)(.*)", content).group(1)

if len(re.search("(?<=Station r 0)(.*)", content).group(1)) ==0:
    nat=re.search("Station r 0[\r\n]+([^\r\n]+)", content).group(1)
    nat1=re.search(nat+"[\r\n]+([^\r\n]+)",content).group(1)
    no=nat+nat1
else:
    nat=re.search("(?<=Station r 0)(.*)", content).group(1)


if len(re.search(" Date / Year of Birth(.*)", content).group(1))==0:
    fn='$'
else:    
    fn=re.search(' Date / Year of Birth(.*)',content).group(1)    



if len(re.search('(?<= Name)(.*)', content).group(1))==0:
    ina='$'
else:    
    ina=re.search('(?<= Name)(.*)', content).group(1)    


t=re.search("Accused Name Age[\r\n]+([^\r\n]+)", content).group(1)
content=content.replace(t,'')
tre=re.search("Accused Name Age[\r\n]+([^\r\n]+)", content).group(1)

translator = Translator()
translated = translator.translate(tre, src='gu', dest='en')
string = translated.text
res = re.findall('([a-zA-Z ]*)\d*.*', string)

ere=re.search('Occupation[\r\n]+([^\r\n]+)', content).group(1),
sec=re.search('(?<=Under Section )(.*)', content).group(1)

ps=re.search('(?<=Police )(\w+ )', content).group(1)
di=re.search('(?<=District )(\w+ )', content).group(1)

sc=re.search(' Act (.\w+\w+)',content).group(1)
lal=[]
lanr=[ps,ere[0],di,'indian',fname,ina,res[0],sc]
translator = Translator()

for i in range(0,8):
    translated = translator.translate(lanr[i], src='en', dest='gu')
    lal.append(translated.text)



dict={

    'district': di, 
    'police station':ps, 
    'type_of_info':re.search('(?<=Type of Information: )(.*)', content).group(1),
    'date_of_fir':re.search('Date to (.*)',content).group(1),
    'accused_name':res[0],
    'accused_name_org':lal[6],
    'fir_no':no,
    'state':state,
    'act':sc,
    'act_org':lal[7],
    'date':re.search('(?<=Date to )(..........)',content).group(1),
    'complaint_informan_name':ina,
    'complaint_informan_name_org':lal[5],
    'complaint_informan_father_husband_name':fname,
    'complaint_informan_father_husband_name_org':lal[4],
    'complaint_informan_date_of_birth':fn,
    'nationality':'indian',
    'nationality_org':lal[3],
    'district_name_pdf':di,
    'district_name_pdf_org':lal[2],
    'fir_no_org':no,
    'occupation':ere[0],
    'occupation_org':lal[1],
    'occurence_of_offence_date_from':re.search('(?<=Date from )(..........)', content).group(1), 
    'occurence_of_offence_date_to':re.search('(?<=Date to )(..........)', content).group(1),  
    'occurence_of_offence_time_from':re.search('(?<=Time from )(.....)', content).group(1), 
    'occurence_of_offence_time_to':re.search('(?<=Time to )(.....)', content).group(1), 
    'police_station_org':lal[0], 
    'sections':sec, 
    'sections_org':sec,
    'year':re.search('(?<=Date to )(..........)', content).group(1)[6:], 

}

with open('data.json', 'w') as outfile:
    json.dump(dict, outfile,indent=2,ensure_ascii=False)
    
 

print("ocr process completed")
cv2.destroyWindow("Test")
cv2.destroyWindow("Main")