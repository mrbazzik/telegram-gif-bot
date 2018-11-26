from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultGif, InputTextMessageContent
import requests
# import giphypop
import json
from random import randint

TELEGRAM_TOKEN = '754397265:AAFQ5t9E-h_-lQL2J4jHJ7-pYORkWiaZpow'
GIPHY_APIKEY = 'guhuZC1dhHW81nD0waZILkFbloTBc7Fx'

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Just some text to test")


def search(search_text):
  prev_search = search_text
  offset = 0

  def get_gif_search(search_text):
    nonlocal prev_search
    nonlocal offset
    if prev_search == search_text:
      offset += 25
    else:
      offset = 0
      prev_search = search_text

    params = {
      'api_key': GIPHY_APIKEY,
      'q': search_text,
      'offset': offset
    }
    response = requests.get('http://api.giphy.com/v1/gifs/search', params=params)
    result = response.json()['data']
    return result
  return get_gif_search


def gifs_choice(bot, update):
    query = update.inline_query.query
    if not query:
        return
    # result1 = get_gif_random(query)
    result1 = search_func(query)
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

search_func = search("")
inline_handler = InlineQueryHandler(gifs_choice)
dispatcher.add_handler(inline_handler)

updater.start_polling()