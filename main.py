import unicodedata as ud
import json
import re
import os
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

        y = [s for s in name_list if not len(s) == 1]                
        print(word,'-->',y)

        return y

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

            wname += ' ' + trans_name.text
        
        return wname

    word = word.lower()

    name_text = ' '.join(slice_word(word))
    result = trans_all(name_text).replace(',', '')
    trans_result = translit(result, "bg", reversed=True)
    return trans_result

#listp = ["chrome", "apple", "steam", "Mario", "CS:GO", "Skype", "League of Legends", "Minecraft"]
#for word in listp:
#    title_translator(word)

print("-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("-=-=-BUKVALNO=-=-BURO=-=-=+")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

while True:
    num = str(input("type: \n1 - to translate \n2 - to undo the translate \n3 - to exit \n"))
    if num == '3': exit()
    if num == '1' or num == '2':
        break


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

with open('data.txt') as json_file:
    data = json.load(json_file)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

files_dir = os.path.join(os.path.join(os.path.expanduser('~')), "Desktop")
files = os.listdir(files_dir)

for _file in files:
    file_dir = os.path.join(files_dir, _file) 
    filename, file_extension = os.path.splitext(file_dir)

    base=os.path.basename(file_dir)
    name = os.path.splitext(base)[0]

    if file_extension == '.lnk':
        if num == '2':
            if name in data.keys():
                os.rename(file_dir, os.path.join(files_dir, data[name]+".lnk"))
                print(name,'-->',data[name])
                del data[name]
        elif name not in data.keys():
            translated = title_translator(name)
            os.rename(file_dir, os.path.join(files_dir, translated+".lnk"))
            data[translated] = name

            print(name,'-->',translated)


files_dir = os.path.join(os.environ["PUBLIC"], "Desktop")
files = os.listdir(files_dir)

for _file in files:
    file_dir = os.path.join(files_dir, _file)
    filename, file_extension = os.path.splitext(file_dir)

    base=os.path.basename(file_dir)
    name = os.path.splitext(base)[0]

    if file_extension == '.lnk':
        if num == '2':
            if name in data.keys():
                os.rename(file_dir, os.path.join(files_dir, data[name]+".lnk"))
                print(name,'-->',data[name])
                del data[name]
        elif name not in data.keys():
            translated = title_translator(name)
            os.rename(file_dir, os.path.join(files_dir, translated+".lnk"))
            data[translated] = name

            print(name,'-->',translated)


with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
