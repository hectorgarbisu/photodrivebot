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

def upload_named_file(bot, update, file_id, file_name):
    newFile = bot.get_file(file_id)
    newFile.download(file_name)
    driveUploader.uploadFile(file_name)
    update.message.reply_text(f'Uploaded {file_name}')
    os.remove(file_name)

def upload_unnamed_file(bot, update, file_id, chronological_filename):
    file_name = ""
    while not file_name or os.path.exists(file_name):
        sleep(1)
        file_name = chronological_filename()
    upload_named_file(bot, update, file_id, file_name)


def document(bot, update):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    update.message.reply_text(f'document file received {file_name}')
    upload_named_file(bot, update, file_id, file_name)


def audio(bot, update):
    file_id = update.message.audio.file_id
    file_name = update.message.audio.file_name
    update.message.reply_text(f'audio file received {file_name}')
    upload_named_file(bot, update, file_id, file_name)


def photo(bot, update):
    file_id = update.message.photo[-1]
    upload_unnamed_file(bot, update, file_id, photo_filename)

def video(bot, update):
    file_id = update.message.video.file_id
    update.message.reply_text(f'video file received {file_id}')
    upload_unnamed_file(bot, update, file_id, video_filename)

def video_note(bot, update):
    file_id = update.message.video_note.file_id
    update.message.reply_text(f'video_note received {file_id}')
    upload_unnamed_file(bot, update, file_id, video_filename)

def voice_note(bot, update):
    file_id = update.message.voice.file_id
    update.message.reply_text(f'voice_note received {file_id}')
    upload_unnamed_file(bot, update, file_id, audio_filename)



def photo_filename():
    return f'photo_{now_substring()}.jpg'

def video_filename():
    return f'video_{now_substring()}.mp4'

def audio_filename():
    return f'audio_{now_substring()}.ogg'



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
    dp.add_handler(MessageHandler(Filters.document, document))

    # audio video
    dp.add_handler(MessageHandler(Filters.video, video))

    # audio audio
    dp.add_handler(MessageHandler(Filters.audio, audio))

    # video_note
    dp.add_handler(MessageHandler(Filters.voice, voice_note))

    # video_note
    dp.add_handler(MessageHandler(Filters.video_note, video_note))


    # get photos
    dp.add_handler(MessageHandler(Filters.photo, photo))


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

