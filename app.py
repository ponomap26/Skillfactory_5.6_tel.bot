import telebot
from config import keys, TOKEN
from utils import Recalculation, Monyeconvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def beginning(message: telebot.types.Message):
    text = "Что бы начать работу введите команду боту в следующем формате:\n<имя валюты>\
<В какую валюту перевести>\
<Количество переводимой валюты>\n Список доступных валют: /money"

    bot.reply_to(message, text)


@bot.message_handler(commands=['money'])
def date(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise Recalculation("В Ведите 3 параметра. /help")
        quote, base, amount = values
        quote, base, = quote.lower(), base.lower()
        total = Monyeconvertor.convert(quote, base, amount)
    except Recalculation as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удается обработать команду\n{e} /help")
    else:
        text = f"Цена {amount} {quote}  в  {base} - {total}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
