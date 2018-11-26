from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultGif, InputTextMessageContent
import requests
import giphypop
import json
from random import randint

TELEGRAM_TOKEN = '739333814:AAEl5ZOqeL9dj-Wk18y5Zos9672eElQrCIw'
GIPHY_APIKEY = 'guhuZC1dhHW81nD0waZILkFbloTBc7Fx'

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Just some text to test")

def search(bot, update, args):
  logging.info(args)
  result = get_gif_translate(' '.join(args))
  logging.info(result)
  logging.info(result==None)
  logging.info(len(result)==0)
  bot.send_video(chat_id=update.message.chat_id, video=result)


def get_gif_translate(search_text):
  # g = giphypop.Giphy(api_key=GIPHY_APIKEY, strict=True)
  # result = g.translate(phrase=search_text, strict=True)
  # return result

  params = {
    'api_key': GIPHY_APIKEY,
    's': search_text,
    'weirdness': randint(0, 10)
  }
  # headers = {
  #   'api_key': GIPHY_APIKEY,
  #   "User-Agent": "Something"
  # } 
  response = requests.get('http://api.giphy.com/v1/gifs/translate', params=params) #, headers=headers)
  result = list()
  result.append(response.json()['data'])
  return result

def get_gif_search(search_text):
    params = {
    'api_key': GIPHY_APIKEY,
    'q': search_text
    }
    # headers = {
    #   'api_key': GIPHY_APIKEY,
    #   "User-Agent": "Something"
    # } 
    response = requests.get('http://api.giphy.com/v1/gifs/search', params=params) #, headers=headers)
    # logging.info(response)
    return response.json()['data']



def get_gif_random(search_text):
  # g = giphypop.Giphy(api_key=GIPHY_APIKEY, strict=True)
  # result = g.translate(phrase=search_text, strict=True)
  # return result

  params = {
    'api_key': GIPHY_APIKEY,
    'tag': search_text
  }
  # headers = {
  #   'api_key': GIPHY_APIKEY,
  #   "User-Agent": "Something"
  # } 
  response = requests.get('http://api.giphy.com/v1/gifs/random', params=params) #, headers=headers)
  # logging.info(response)
  result = list()
  result.append(response.json()['data'])
  return result

updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def gifs_choice(bot, update):
    query = update.inline_query.query
    if not query:
        return
    result1 = get_gif_random(query)
    # logging.info(type(result1))
    # logging.info(result1)
    results = list()
    for i, result in enumerate(result1):
      url = result['images']['original']['url']
      results.append(
          InlineQueryResultGif(
              type="gif",
              id=i,
              gif_url=url,
              thumb_url=url,
              title=f"via @agify_bot {query}",
              caption=query,
              # input_message_content=InputTextMessageContent(query)
          )
      )
    bot.answer_inline_query(update.inline_query.id, results)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

search_handler = CommandHandler('gify', search, pass_args=True)
dispatcher.add_handler(search_handler)

inline_handler = InlineQueryHandler(gifs_choice)
dispatcher.add_handler(inline_handler)

updater.start_polling()