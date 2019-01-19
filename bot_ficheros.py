# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from time import sleep
import os
import driveUploader
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('./data/apikey', 'r') as apikey_file:
    TOKEN = apikey_file.read()

with open('./data/folder_id', 'r') as folder_id_file:
    FOLDER_ID = folder_id_file.read()


command_list = "/start: no hace nada\n" + " /help: muestra esta lista\n" +\
"/echo: repite\n"



def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Lista de comandos:\n' + command_list)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
   

def documento(bot, update):
    pass
    """
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    newFile = bot.get_file(file_id)
    file_path = f'data/{file_name}'
    newFile.download(file_path)
    """
    
def foto(bot, update):
    file_id = update.message.photo[-1]
    file_name = photo_filename()
    newFile = bot.get_file(file_id)
    def download_photo(file_name):
        file_path = f'{file_name}'
        if os.path.exists(file_path):
            sleep(1)
            final_path = download_photo(photo_filename())
        else: 
            newFile.download(file_path)
            final_path = file_path
        return final_path
    file_path = download_photo(file_name)
    
    driveUploader.uploadFile(file_path)
    update.message.reply_text(f'Uploaded {file_name}')
    os.remove(file_path)


def photo_filename():
    return f'photo_{now_substring()}.png'

def now_substring():
    #example string image_2019-01-14_16-01-20.png"
    format_string = "%Y-%m-%d_%H-%M-%S"
    return datetime.now().strftime(format_string)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """ credenciales de google drive """
    
    driveUploader.setFolder(FOLDER_ID)
    
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # get files
    dp.add_handler(MessageHandler(Filters.document, documento))

    # get photos
    dp.add_handler(MessageHandler(Filters.photo, foto))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

