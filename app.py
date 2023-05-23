import os
from flask import Flask, request, Response
# from telegram import Update, Bot
# from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
variables = {'fromAddress' : '\nfrom: ', 'toAddress' : '\nto: ', 'value' : '\nsent: ', 'asset' : '', 'external' : '\ncategory: ', 'hash': '\nhash: '}
user_chat_id = os.environ['CHANNEL_ID']

@app.route('/')
def hello():
    return 'Service for sending notifications to a telegram channel '

@app.route('/notify', methods=['POST','GET'])
def notify():
    logs = request.json
    # network = logs['event']['network']
    # from_address = logs['event']['activity'][0]['fromAddress']
    # to_address = logs['event']['activity'][0]['toAddress']
    # value = logs['event']['activity'][0]['value']
    # assets = logs['event']['activity'][0]['asset']
    # category = logs['event']['activity'][0]['external']
    # tx_hash = logs['event']['activity'][0]['hash']
    
    message = f"<b>{logs['event']['network']}</b>"
    for i in variables:
        res = logs['event']['activity'][0].get(i)
        if res: message += variables[i] + str(res)
            
    

    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={user_chat_id}&parse_mode=HTML&text={message}"
    requests.get(url, stream=True)
    return Response(status=200)
  
  

if __name__ == '__main__':
    app.run()
