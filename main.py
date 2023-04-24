# Этот бот создан Прокопьевым Александром.
# Предназначен для выявления крупных одренров на криптобирже Бинанс.

from binance import Client
import telebot
from API import api_bot, api_key_binance, api_secret_binance

bot = telebot.TeleBot(api_bot)


api_key = api_key_binance
api_secret = api_secret_binance

client = Client(api_key, api_secret)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Добро пожаловать! Введите наименование криптовалютной пары и объем через пробел большими буквами, например: BTCUSDT 10')

@bot.message_handler(func=lambda message: True)
def get_order_book(message):
    try:
        # Получаем символ и объем от сообщения пользователя
        symbol, volume = message.text.strip().split()
        volume = float(volume)

        # получаем книгу ордеров с Бинанс (максимальное количество которое выдает Бинанс, это 5000 ордеров)
        depth = client.get_order_book(symbol=symbol, limit=5000)

        # фильтруем ордера на продажу по объему
        sell_orders = [order for order in depth['asks'] if float(order[1]) > volume]

        # фильтруем ордера на покупку по объему
        buy_orders = [order for order in depth['bids'] if float(order[1]) > volume]

        sell_orders_str = "Ордера на продажу:\n"
        for order in sell_orders:
            price = int(float(order[0]))
            volume = int(float(order[1]))
            sell_orders_str += f"Цена: {price}, Количество: {volume}\n"

        buy_orders_str = "Ордера на покупку:\n"
        for order in buy_orders:
            price = int(float(order[0]))
            volume = int(float(order[1]))
            buy_orders_str += f"Цена: {price}, Количество: {volume}\n"
        text_for_bot = sell_orders_str + "\n" + buy_orders_str
        bot.reply_to(message, text_for_bot)
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка. Убедитесь, что вы ввели символ и объем в правильном формате: например BTCUSDT 10')

bot.polling()
