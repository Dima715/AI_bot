import telebot # Бот работает на английском языке.
import requests

class LLM:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def query(self, payload):
        try:
            response = requests.post(self.url, headers={'Authorization': f"Bearer {self.token}"}, json={"inputs": payload})
            return response.json()[0]['generated_text']
        except:
            return "Технические неполадки!"

token = '7363727382:AAEIwpg3aGl3lBzaZZsZaeYsIbnpvw0vtGk'
bot = telebot.TeleBot(token)

start = False

AI = LLM("https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct", "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")

@bot.message_handler(commands=['start'])
def starting(message):
    global start
    if start == False:
        bot.send_message(message.chat.id, "Ассистент запущен!")
        start = True
    else:
        bot.send_message(message.chat.id, "Ассистент уже был запущен!")

@bot.message_handler(commands=['stop'])
def stoping(message):
    global start
    if start == True:
        bot.send_message(message.chat.id, "Работа Ассистента остановлена!")
        start = False
    else:
        bot.send_message(message.chat.id, "Ассистент не был запущен!")

@bot.message_handler()
def mess(message):
    global start
    if start == True:
        bot.send_message(message.from_user.id, AI.query(message.text))


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)