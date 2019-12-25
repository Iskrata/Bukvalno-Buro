from googletrans import Translator
import wordninja

word = 'Minecraft launcher'

wm = wordninja.LanguageModel('words.txt.gz')
name_list = wm.split(word)
print(name_list)

#name_text = ' '.join(name_list)

trans_name = []
for word in name_list:
    translator = Translator()
    trans_word = translator.translate(word, dest='bg') 
    print(trans_word)
    trans_name.append(trans_word.text)

print(trans_name)