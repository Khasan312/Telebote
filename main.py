from email import message
import logging
# from msilib.schema import File
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import markups as nav
from markups import *
from db import Database



TOKEN = "5203636918:AAEDMv7gz3cfkN37s1CAZ8PfGE6kyZQ8rBc"
CHANNEL_ID = '@nurafromsaturan'
NOT_SUB_MESSAGE = 'ДЛЯ доступа к боту подпишитесь на канал'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database("database.db")


file = open ('hedef.txt', encoding='utf-8')
file.read()
    




class Form(StatesGroup):
    nickname = State()
    birth_date = State()
    position = State()


def check_sub_channel(chat_member):
    print(chat_member['status'])
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    if message.chat.type =='private':
    # check the exists of the user in the db
        if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
                await bot.send_message(message.from_user.id, 'Privet')
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
        else:
            await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.callback_query_handler(text='subchanneldone')
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, 'Privet')
    else:
        await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=nav.checkSubMenu)

    


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

        elif message.text == "💻Меню":
            await bot.send_message(message.from_user.id, 'Добро пожаловать {0.first_name}'.format(message.from_user),
                                   reply_markup=nav.OtherMenu)
            keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btnPurpose = types.KeyboardButton('🎯 Цели')
            btnInfo = types.KeyboardButton('📑 Информация')
            keyboard1.add(btnPurpose, btnInfo)

        elif message.text == '📑 Информация':
            await bot.send_message(message.from_user.id, 'Задача ментора — помочь человеку решить некую проблему и поделиться не столько знаниями, сколько опытом. Проблемы могут быть разного характера. Действительно, может случиться так, что человек хочет попасть на новую работу и не знает, с чего начать.')
        
        elif message.text == '🎯 Цели':
            await bot.send_message(message.from_user.id, 'Перееехать в Америку и стать Мувером')

        elif message.text == 'Главное меню':
            await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=nav.mainMenu)

        else:
            await message.reply('dont understanded')
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

                    # keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

@dp.callback_query_handler(lambda call: call.data == 'btnInfo')
async def choose(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    print(callback_query)
    # await db.add()
    await bot.send_message(callback_query.from_user.id, 'fahfgwjahgfjawgw')


    

                            
                    
        

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)