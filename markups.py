from threading import main_thread
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


btnMain = KeyboardButton('Главное меню ')


#---Main Menu---
btnProfile = KeyboardButton("👨Профиль")
btnSub = KeyboardButton("💻Меню")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub)

#---Other Menu---
btnInfo = KeyboardButton('📑 Информация')
btnPurpose = KeyboardButton('🎯 Цели')
OtherMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(btnInfo, btnPurpose, btnMain)







