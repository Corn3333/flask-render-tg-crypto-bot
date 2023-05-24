import os
from flask import Flask, request, Response
# from telegram import Update, Bot
# from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
variables = {'fromAddress' : '\nfrom: ', 'toAddress' : '\nto: ', 'value' : '\nsent: ', 'asset' : ' ', 'external' : '\ncategory: ', 'hash': '\nhash: '}
user_chat_id = os.environ['CHANNEL_ID']
user_id = os.environ['USER_ID']

@app.route('/')
def hello():
    return 'Service for sending notifications to a telegram channel '

@app.route('/notify', methods=['POST','GET'])
def notify():
    logs = request.json
    
    message = ""
    k = logs['event'].get('network')
    if k: message += f"<b>{k}</b>"
    for i in variables:
        res = logs['event']['activity'][0].get(i)
        if res: message += f"<b>{variables[i]}</b>" + f"<code>{str(res)}</code>"
    


    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={user_chat_id}&parse_mode=HTML&text={message}"
    requests.get(url, stream=True)
    
    debug = "https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={user_id}&text={logs}"       
    requests.get(debug, stream=True)
    
    return Response(status=200)
  
  

if __name__ == '__main__':
    app.run()
