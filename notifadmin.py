import time
import telepot as telepot
from telepot.delegate import create_open, per_chat_id, pave_event_space
from telepot.loop import MessageLoop
import config

class MessageCounter(telepot.helper.ChatHandler):


    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)


    def on_chat_message(self, msg):
        if 'enquiry' in msg['text']:
            import Send_Notification
            user=bot.getChat(self.chat_id)
            fname=user['first_name']
            print(user['id'])
            Send_Notification.telegram_bot_sendapprove(self.chat_id, fname, '20/04/2019')
            self.sender.sendMessage("Request has been sent to admin")

        if 'leave' in msg['text']:
            import Send_Notification
            user=bot.getChat(self.chat_id)
            id=user['id']
            Send_Notification.telegram_bot_sendapprove(str(id))
            self.sender.sendMessage("you can take leave")











bot = telepot.DelegatorBot(config.BOT_TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=100),
])
MessageLoop(bot).run_as_thread()
while 1:
    time.sleep(100)


