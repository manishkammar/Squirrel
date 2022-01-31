import requests
import config
def telegram_bot_sendapprove(id,name,date):
    bot_token = config.BOT_TOKEN
    bot_chatID = config.bot_chatID

    send = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID +\
           '&parse_mode=Markdown&text=' + " " + name + " is requesting for leave on " + date + "  /approve"
    requests.get(send)
    return






