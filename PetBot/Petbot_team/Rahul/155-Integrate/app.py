from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

my_bot = ChatBot(name='PyBot',storage_adapter="chatterbot.storage.SQLStorageAdapter")
#english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
#trainer = ChatterBotCorpusTrainer(english_bot)
trainer = ListTrainer(my_bot)
#trainer.train("chatterbot.corpus.english")

main_list = []

def readFile(inputfile):
    fh = open(inputfile, 'r')
    ft = fh.read()
    fl = ft.split("\n")
    return list(fl)

intro_list = readFile("./Data/intro.txt")
cat_list   = readFile("./Data/cats.txt")
dog_list   = readFile("./Data/dogs.txt")
main_list  = intro_list + cat_list + dog_list

print("main list")
print(main_list)

trainer.train(main_list)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    if request.method == 'GET':
        if request.args.get('msg'):
            user_input = request.args.get('msg')
            print("bot =  " + user_input )
            bot_response = my_bot.get_response(user_input)
            
            if bot_response.confidence > 0.1:
                bot_response = str(bot_response)
                print("user = "+ bot_response)
                return str(my_bot.get_response(user_input))
                 
            else: 
                print("error")
                  
        else:
            return("invalid request.")
            




if __name__ == "__main__":
    app.run()