# Release v1.0.3
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
from calc import UserData
from config import TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN,
          parse_mode="MarkdownV2")

dp = Dispatcher(bot)


userdata = UserData()


@dp.message_handler(commands="start")
async def cmdStart(message: types.Message):
    await message.answer("*Добро пожаловать в бота для учета финансов FunPay\!*\n\nМеня разрабатывает начинающий программист *@solarmolly*\nИсходный код бота открыт для всех, Автор никого никак не ограничивает в использовании продукта\! \nЕсли вы разработчик, и вам понравилась моя идея \- буду рад, если вы поможете мне развивать продукт или на основе моих наработок начнете разрабатывать своего бота\! \n\nДля получения инструкции по использованию \- */help*")


@dp.message_handler(commands="help")
async def cmdHelp(message: types.Message):
    await message.answer("Итак, пока что разработчик\-масленок не добрался до FSM, поэтому использование бота тебе может показаться странным\. Но я попытаюсь объяснить максимально понятным языком \- как же всё\-таки использовать этого бота")
    await message.answer("Любая твоя команда будет начинаться с префикса \- он позволит боту понять, что ты хочешь сделать\n\n" +
                         "После префикса пойдут принимаемые ботом значения \- я их написал ниже вместе с префиксами\n\n"
                         "Следующие строки понимай так: _[команда]_ [префикс] [принимаемые значения]\n" +
                         "Итак, вот доступные тебе команды:\n" +
                         "_Покупка_ `-по количество цена` _\(за 1 единицу\)_\n" +
                         "_Продажа_ `-пр количество цена` _\(за 1 единицу\)_\n" +
                         "_Возврат_ `-во количество цена`\n" +
                         "_Вывод \(вывод средств с FunPay с учетом комиссии\)_ `-вы`\n" +
                         "_Профит \(рассчет общего дохода с учетом затрат\)_ `-п`")
    await message.answer("Пример использования команды Покупка:\n\n`-по 13 16\.2`\n\nТо есть я *закупил* *13* товаров по *16\.2* рублей\n\n" +
                         "`-п`\n\nА здесь я попросил бота *рассчитать мне прибыль*")


# Ищем сообщение, начинающееся с "-", чтобы опознать команду
@dp.message_handler(Text(startswith="-"))
async def doSmth(message: types.Message):
    input = message.text.split()
    prefix = input[0]
    # Теперь узнаем что за команду пользователь загадал
    if prefix == "-по":
        count = int(input[1])
        price = float(input[2])
        # Вызываем функцию из объекта userdata класса UserData, чтобы произвести рассчеты
        userdata.buy(count, price)
        await message.reply(f"Покупка `{count}` шт\. товара по `{price}` рублей на сумму `{round(float(count) * price, 2)}` рублей\n" +
                            f"Всего затрат на: `{round(userdata.spent, 2)}` рублей")
    elif prefix == "-пр":
        count = int(input[1])
        price = float(input[2])
        userdata.sell(count, price)
        await message.reply(f"Продажа `{count}` шт\. товара по `{price}` рублей на сумму `{round(float(count) * price, 2)}` рублей\n" +
                            f"Всего продаж: `{userdata.sold}`\nНовый баланс: `{round(userdata.balance, 2)}` рублей")
    elif prefix == "-во":
        count = float(input[1])
        refund_sum = float(input[2])
        userdata.refund(refund_sum)
        await message.reply(f"Возврат товаров на сумму `{round(refund_sum * float(count), 2)}` рублей\n" +
                            f"Всего возвратов: `{userdata.refunds}`\n" +
                            f"Всего продаж: `{userdata.sold}`\nНовый баланс: `{round(userdata.balance, 2)}` рублей")
    elif prefix == "-вы":
        old_balance = userdata.balance
        userdata.withdraw()
        await message.reply(f"Вывод средств на сумму `{round(old_balance, 2)}` рублей _\(за вычетом комиссии\)_\nВсего выведено: `{round(userdata.earned, 2)}` рублей\n" +
                            f"Баланс обнулен")
    elif prefix == "-п":
        await message.reply(f"Потрачено: `{round(userdata.spent, 2)}`, Выведено: `{round(userdata.earned, 2)}`\nОбщая прибыль составляет `{round(userdata.earned - userdata.spent, 2)}`")
    else:
        await message.reply("Проверьте правильность введенных данных")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
