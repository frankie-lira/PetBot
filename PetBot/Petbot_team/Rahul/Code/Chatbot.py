#####
### In the below package changed 
##/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/chatterbot/tagging.py
### Old line #13 : self.nlp = spacy.load(self.language.ISO_639_1.lower())
### New lines:
#### if self.language.ISO_639_1.lower() == 'en': 
#       self.nlp = spacy.load('en_core_web_sm') 
#    else: 
#       self.nlp = spacy.load(self.language.ISO_639_1.lower())

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
#from flask import app
from flask import Flask, request,jsonify
#from flask import Flask,


app = Flask(__name__)

my_bot = ChatBot(name='PyBot')
trainer = ListTrainer(my_bot)
main_list = []
intro_list = []


intro_file = open("./chat_data/intro.txt", 'r')
intro_text = intro_file.read()
intro_list = intro_text.split("\n")
#print(intro_list)


cat_file = open("./chat_data/cats.txt", 'r')
cat_text = cat_file.read()
cat_list = cat_text.split("\n")
#print(cat_list)

dog_file = open("./chat_data/dogs.txt", 'r')
dog_text = dog_file.read()
dog_list = dog_text.split("\n")

#dog_list = []
main_list = intro_list + cat_list + dog_list
#main_list.extend(intro_list)
#main_list.extend(cat_list)
#main_list.extend(dog_list)
print("main list")
print(main_list)
trainer.train(main_list)

# http://127.0.0.1:5000/bot?ask=hello
@app.route('/home', methods = ['GET'])
def hello_bot():
    if request.method == 'GET':
        if request.args.get('ask'):
            user_input = request.args.get('ask')
            print("user =  " + user_input )
            bot_response = my_bot.get_response(user_input)
            print(str(bot_response))
            print(bot_response.confidence)
            if bot_response.confidence > 0.1:
                bot_response = str(bot_response)
                print("bot = "+ bot_response)
                return jsonify({'status':'OK','answer':bot_response})
            else: 
                print("error")
                return jsonify({'status':'Error','answer':"I can't understand. Re enter response."})
            
        else:
            print("invalid request.")
            return jsonify({'status':'Error','answer':'Invalid request'})
        
        


app.run()
