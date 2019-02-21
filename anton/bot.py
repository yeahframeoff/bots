import json

from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import CommandHandler

from collections import defaultdict, deque


class Bot:

    chat_messages = defaultdict(deque)

    def run(self):
        with open("../local-properties.json", "r") as f:
            token = json.loads(f.read())["anton"]
        updater = Updater(token=token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.message))
        dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=self.message))

        # dispatcher.add_error_handler(self.handle_error)

        updater.start_polling()

    def message(self, bot, update, *kwargs):
        try:
            chat_id = update.effective_chat.id
            messages = self.chat_messages[chat_id]

            if len(messages) > 5:
                messages.popleft()
            messages.append(update.message)
            
            if self.check_violation(messages):
                update.message.reply_text("Антон блять!")
        except Exception as e:
            update.message.reply_text("Ошибочка: " + str(e))

    def check_violation(self, messages):
        if len(messages) < 4:
            return False
        user = messages[0].from_user['username']
        for message in messages:
            if len(message.text) > 30:
                return False
            if message.from_user['username'] != user:
                return False
        return True


bot = Bot()
bot.run()

