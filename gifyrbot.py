from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultGif, InputTextMessageContent
import requests
import giphypop
import json
from random import randint

TELEGRAM_TOKEN = '685233513:AAECS0VxK1fEmNp66r7Y7id7EuzSeb-9zdQ'
GIPHY_APIKEY = 'guhuZC1dhHW81nD0waZILkFbloTBc7Fx'

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Just some text to test")

def get_gif_random(search_text):

  params = {
    'api_key': GIPHY_APIKEY,
    'tag': search_text
  }
  response = requests.get('http://api.giphy.com/v1/gifs/random', params=params) #, headers=headers)
  result = list()
  result.append(response.json()['data'])
  return result


def gifs_choice(bot, update):
    query = update.inline_query.query
    if not query:
        return
    result1 = get_gif_random(query)
    results = list()
    for i, result in enumerate(result1):
      url = result['images']['original']['url']
      results.append(
          InlineQueryResultGif(
              type="gif",
              id=i,
              gif_url=url,
              thumb_url=url,
              title=query,
              caption=query,
          )
      )
    bot.answer_inline_query(update.inline_query.id, results, cache_time=0)

updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

inline_handler = InlineQueryHandler(gifs_choice)
dispatcher.add_handler(inline_handler)

updater.start_polling()