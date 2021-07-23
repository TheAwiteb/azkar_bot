import requests
import telebot
import time
import json
from random import choice

TOKEN = ""

bot = telebot.TeleBot(TOKEN)
emojis = "🌹 ♥️ 🤍 💙 🌺 🌸 🌹 🌷".split()
random_emojis = lambda n: ''.join([choice(emojis) for i in range(n)])

class Zkr:
    def __init__(self) -> None:
        self.host = "https://www.hisnmuslim.com/api/ar/"
        self.main_url = self.host+"husn_ar.json"
        self.zkr_url = self.host+"{}.json"
    def get(self, id:int, title:str) -> dict:
        data = requests.get(self.zkr_url.format(id))
        if data.ok:
            data = data = data.text.replace(title, "azkar").encode("utf-8").decode("utf-8-sig")
            zkr = choice(json.loads(data)["azkar"])
            return {
                "text":zkr["ARABIC_TEXT"],
                    "audio": zkr["AUDIO"]
            }
        else:
            raise Exception("ايدي الذكر غير موجود")
    def random(self,chat_id, msg_id) -> None:
        data = requests.get(self.main_url)
        data = data.text.replace("العربية", "ar").encode("utf-8").decode("utf-8-sig")
        zkr_type = choice(json.loads(data)['ar'])
        title = zkr_type["TITLE"]
        zkr = self.get(zkr_type['ID'], title)
        text = f"{title}\n\n{zkr['text']}{random_emojis(2)}"
        bot.send_audio(
            chat_id=chat_id, reply_to_message_id=msg_id,
                caption=text, audio=zkr["audio"]
        )

zkr = Zkr()

@bot.message_handler(func= lambda msg: msg.text and msg.text.startswith('/'))
def command_handler(message):
    command = message.text[1:].lower() # remove /
    if command.startswith('start'):
        bot.reply_to(message,"ارسل 'اذكار'")
    else:
        pass

@bot.message_handler(func= lambda msg: True)
def command_handler(message):
    chat_id = message.chat.id
    msg_id = message.id
    text = message.text
    if text == "اذكار":
        zkr.random(chat_id, msg_id)

while True:
    print(f"Start BOT")
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except Exception as e:
        print(e)
        time.sleep(10)