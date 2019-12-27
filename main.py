import unicodedata as ud
import re
from googletrans import Translator
import wordninja
from transliterate import translit

def title_translator(word):
    #---------------------------------------------------
    latin_letters= {}

    def is_latin(uchr):
        try: return latin_letters[uchr]
        except KeyError:
            return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

    def only_roman_chars(unistr):
        return all(is_latin(uchr)
            for uchr in unistr
            if uchr.isalpha())  
    #---------------------------------------------------
    def slice_word(word):
        wm = wordninja.LanguageModel('words.txt.gz')
        name_list = wm.split(word)
        print(name_list)
        return name_list

    def contain_latin_stuff(trans_name):
        is_bad = False
        wordList = re.sub("[^\w]", " ",  trans_name.text).split()
        for word in wordList: 
            try: int(word)
            except ValueError:
                if only_roman_chars(word): is_bad = True
        
        return is_bad

    def trans_partly(name):
        wordList = re.sub("[^\w]", " ",  name).split()
        hlist = []

        hlist.append(wordList[-1])
        del wordList[-1]

        return wordList, hlist

    def trans_all(name):
        sl = False
        while True:
            translator = Translator() 
            trans_name = translator.translate(name, dest='bg') 
            print(trans_name)

            if contain_latin_stuff(trans_name):      
                sl = True      
                l1, l2 = trans_partly(name)
                name = ' '.join(l1)
            else:
                break

        wname = trans_name.text
            
        if sl:
            name = ' '.join(l2)
            translator = Translator() 
            trans_name = translator.translate(name, dest='bg') 
            print(trans_name)

            wname += ' ' + trans_name.text
        
        return wname

    word = word.lower()

    name_text = ' '.join(slice_word(word))
    result = trans_all(name_text).replace(',', '')
    trans_result = translit(result, "bg", reversed=True)
    print(trans_result)
    return trans_result

title_translator("League of Legends")
