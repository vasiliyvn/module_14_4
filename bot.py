from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = InlineKeyboardMarkup(resize_keyboard=True)
kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Купить')
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
button5 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button6 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb.add(button)
kb.add(button1)
kb.add(button2)
kb1.add(button3)
kb1.add(button4)
kb2.add(button5)
kb2.add(button6)
kb2.add(button7)
kb2.add(button8)


initiate_db()
products = get_all_products()

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'photos/{i}.png', 'rb') as png:
            await message.answer_photo(png, f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f' (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A')
    await call.answer


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f'Привет {message.from_user.username}! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'ваша норма колорий: {res}')
    await state.finish()


@dp.message_handler(text=['Информация'])
async def bot_message(message):
    await message.answer('привет Urbanist')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
