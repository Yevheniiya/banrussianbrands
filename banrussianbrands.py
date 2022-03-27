import logging
import ast
import sqlite3
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "botID"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

db = sqlite3.connect('brandsDB.db')
sql = db.cursor()


def search(brandname):
    for val in sql.execute(f"SELECT Brands.Holding,Brands.Name, Category.Category,Country.Country,Status.Status FROM Brands  JOIN Category ON Brands.Category=Category.Category_ID  JOIN Country ON Brands.Country=Country.Country_id  JOIN Status ON Brands.Status = Status.Status_id  WHERE Rawname=:name", {"name": brandname}):
        return(f"{val}")


def torawtext(string):
    string = string.lower()
    string = ''.join(c for c in string if c.isalpha())
    return(string)


def answer(outputstr):
    words = ast.literal_eval(outputstr)
    words = [n.strip() for n in words]
    if words[4] == 'GREEN':
        words[4] = '✅'
    elif words[4] == 'RED':
        words[4] = '❌'
    else:
        words[4] = '❓'
    message = words[1] + ' ' + words[4] + '\n\nХолдінг: ' + \
        words[0] + '\nКатегорія: ' + words[2] + '\nКраїна: ' + words[3]
    return message


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт!\nЦе бот для перевірки брендів: які українські, іноземні чи москальські. Надішлі назву бренда, аби дізнатися про нього більше\nКидай друзям, аби вони теж бойкотували російські бренди.")


@dp.message_handler()
async def echo(message: types.Message):
    brandname = message.text
    await message.answer(f"Бренд для перевірки: {brandname}. Зачекайте хвилину.")
    if sql.fetchone() is None:
        if search(torawtext(brandname)) != None:
            await message.reply(answer(search(torawtext(brandname))))
        elif search(torawtext(brandname)) == None:
            await message.reply(f"Перевірте написання. \nЯкщо все вірно, нам невідомо про цей бренд. Відправте назву реплаєм на це повідомлення ")
            if message.reply_to_message:
                await message.reply(f"Дякуємо за звернення! Бренд: {brandname} буде додано в наступному оновленні")
                await bot.send_message(adminID, torawtext(brandname))

    else:
        print('pew')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
