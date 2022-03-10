import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import markups as nav
from markups import *
from db import Database

TOKEN = "5203636918:AAEDMv7gz3cfkN37s1CAZ8PfGE6kyZQ8rBc"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database("database.db")


class Form(StatesGroup):
    nickname = State()
    birth_date = State()
    position = State()


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    # check the exists of the user in the db
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(
            message.from_user.id, "Hi!\nI'm Makers!\nPowered by aiogram."
        )
        await bot.send_message(message.from_user.id, "Укажите ваш ник")
        await Form.nickname.set()
        

    else:
        await bot.send_message(
            message.from_user.id,
            "Вы уже зарегистрированы",
            reply_markup=nav.mainMenu,
        )


    


@dp.message_handler(state=Form.nickname)
async def process_nickname(message: types.Message, state):
    await bot.send_message(message.from_user.id, "введи дату рождение ")
    # if len(message.text) > 12:


    # save client's nickname to db
    db.set_nickname(message.from_user.id, message.text)

    await Form.next()

@dp.message_handler(state=Form.birth_date)
async def process_birthday(message: types.Message, state):
    await bot.send_message(message.from_user.id, "введи свою позицию ")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('СТАЖЕР')
    btn2 = types.KeyboardButton('МЕНТОР')
    keyboard.add(btn1, btn2)

    await Form.next()
    await bot.send_message(message.from_user.id, reply_markup=keyboard, text= 'hello')

    

    # birth_date = message.text

    # save client's birthday to db
    db.set_date_of_birth(message.from_user.id, message.text)


@dp.callback_query_handler(lambda call: call.data =='btn1')
async def choose(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    print(callback_query)
    # await db.add()
    await bot.send_message(callback_query.from_user.id, 'fahfgwjahgfjawgw')






@dp.message_handler(state=Form.position)
async def process_position(message: types.Message, state):
    db.set_position(message.from_user.id, message.text)
    await Form.next()


    db.set_signup(message.from_user.id, "Готово")

    await bot.send_message(message.from_user.id, "Сделано")
    await bot.send_message(
                        message.from_user.id,
                        "Регистрация прошла успешно",
                        reply_markup=nav.mainMenu,
                    )

    # await Form.next()





@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == "private":
        if message.text == "👨Профиль":
            date_birth = "Дата рождения: " + db.get_date_of_birth(
                message.from_user.id
            )
            user_nickname = "Ваш ник: " + db.get_nickname(message.from_user.id)
            position = 'Ваша позиция: ' + db.get_position(message.from_user.id)
            await bot.send_message(message.from_user.id, user_nickname)
            await bot.send_message(message.from_user.id, date_birth)
            await bot.send_message(message.from_user.id, position)

        else:
                if db.get_signup(message.from_user.id) == "setnickname":
                    if len(message.text) > 15:
                        await bot.send_message(
                            message.from_user.id,
                            "никнэйм не должен превышать 15 символов и больше 2 символов",
                        )
                    elif "@" in message.text or "/" in message.text:
                        await bot.send_message(
                            message.from_user.id, "вы ввели запрещенный символ"
                        )
                    else:
                        # db.set_nickname(message.from_user.id, message.text)
                        # db.set_date_of_birth(message.from_user.id, message.text)
                        db.set_signup(message.from_user.id, "Готово")
                        await bot.send_message(
                            message.from_user.id,
                            "Регистрация прошла успешно",
                            reply_markup=nav.mainMenu,
                        )
                else:
                    await bot.send_message(message.from_user.id, "Что?")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)