import telebot
from config import keys, TOKEN
from extensions import APIException, MoneyConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def beginning(message: telebot.types.Message):
    text = "Что бы начать работу введите команду боту в следующем формате:\n<имя валюты>\
<В какую валюту перевести>\
<Количество переводимой валюты>\n Список доступных валют: /values"

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def date(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("В Ведите 3 параметра. /help")
        quote, base, amount = values
        quote, base, = quote.lower(), base.lower()
        total = MoneyConvertor.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удается обработать команду\n{e} /help")
    else:
        text = f"Цена {amount} {quote}  в  {base} - {total}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
