import unicodedata as ud
import re
from googletrans import Translator
import wordninja

#---------------------------------------------------
latin_letters= {}

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin
#---------------------------------------------------
def slice_word(word):
    wm = wordninja.LanguageModel('words.txt.gz')
    name_list = wm.split(word)
    print(name_list)
    return name_list

def trans_partly(name):
    # Minecraft laucher
    trans_name = []
    wordList = re.sub("[^\w]", " ",  name).split()
    for word in wordList:
        name_text = ' '.join(slice_word(word))
        translator = Translator()
        trans_word = translator.translate(name_text, dest='bg')
        trans_name.append(trans_word.text)
    return ' '.join(trans_name)
        

def trans_all(name):
    translator = Translator() 
    trans_name = translator.translate(name, dest='bg') 
    print(trans_name)
    
    is_bad = False
    wordList = re.sub("[^\w]", " ",  trans_name.text).split()
    for word in wordList: 
        if only_roman_chars(word): is_bad = True

    if is_bad: return False
    else: return trans_name

word = 'Minecraft launcher'.lower()

name_text = ' '.join(slice_word(word))
result = trans_all(name_text)
if not result: print(trans_partly(word))
else: print(result)

"""
trans_name = []
for word in name_list:
    translator = Translator()
    trans_word = translator.translate(word, dest='bg') 
    print(trans_word)
    trans_name.append(trans_word.text)

print(trans_name)
"""