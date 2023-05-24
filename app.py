import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
variables = {'fromAddress' : '\nfrom:', 'toAddress' : '\nto:', 'value' : '\nsent: ', 'asset' : ' ', 'hash': '\nhash: '}
user_chat_id = os.environ['CHANNEL_ID']
NETWORK = {
    "ARB_MAINNET" : {"name" : "ARBITRUM", "url_address" : "https://arbiscan.io/address/", "url_hash" : "https://arbiscan.io/tx/"}, 
    "MATIC_MAINNET" : {"name" : "POLYGON", "url_address" : "https://polygonscan.com/address/", "url_hash" : "https://polygonscan.com/tx/"}, 
    "ETH_MAINNET": {"name" : "ETH", "url_address" : "https://etherscan.io/address/", "url_hash" : "https://etherscan.io/tx/"}, 
    "OPT_MAINNET": {"name" : "OPTIMISM", "url_address" : "https://optimistic.etherscan.io/address/", "url_hash" : "https://optimistic.etherscan.io/tx/"}}

@app.route('/')
def hello():
    return 'Service for sending notifications to a telegram channel '


@app.route('/notify', methods=['POST','GET'])
def notify():
    logs = request.json
    
    message = ""
    k = logs['event'].get('network')
    if k: message += f"<b>{NETWORK[k]['name']}</b>"
    for i in variables:
        res = logs['event']['activity'][0].get(i)
        if res and (i == "fromAddress" or i == "toAddress"): 
            message += f"<i>{variables[i]}</i> <a href='{NETWORK[k]['url_address'] + str(res)}'>{str(res)[:6]}</a>"
        elif res and i == "hash":
            message += f"\n<a href='{NETWORK[k]['url_hash'] + str(res)}'>Tx hash</a>"
        elif res:
            message += f"<i>{variables[i]}</i>" + f"<code>{str(res)}</code>"
    
    # message += f"\n\n{logs}"

    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?disable_web_page_preview=true&chat_id={user_chat_id}&parse_mode=HTML&text={message}"
    requests.get(url, stream=True)
    return Response(status=200)
  
  

if __name__ == '__main__':
    app.run()
