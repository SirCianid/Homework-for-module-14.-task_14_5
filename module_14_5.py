from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions import *

api = ""
health_bot = Bot(token=api)
dp = Dispatcher(health_bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
button_4 = KeyboardButton(text='Регистрация')
kb.add(button_1)
kb.add(button_2)
kb.add(button_3)
kb.add(button_4)

kb_in = InlineKeyboardMarkup()
butt_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
butt_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.add(butt_1)
kb_in.add(butt_2)

kb_in2 = InlineKeyboardMarkup()
butt1 = InlineKeyboardButton(text='Product_1', callback_data='product_buying')
butt2 = InlineKeyboardButton(text='Product_2', callback_data='product_buying')
butt3 = InlineKeyboardButton(text='Product_3', callback_data='product_buying')
butt4 = InlineKeyboardButton(text='Product_4', callback_data='product_buying')
kb_in2.row(butt1, butt2, butt3, butt4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (на латиннице):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.answer('Пользователь с таким именем существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=username)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = data['age']
    await add_users(username, email, age)
    await message.answer(f"Регистрация завершена! Ваш баланс: 1000", reply_markup=kb)
    await state.finish()


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора(М): '
                              '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ages=int(message.text))
    await message.answer('Введите свой рост в см:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growths=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weights=float(message.text))
    data = await state.get_data()
    calories = 10 * data['weights'] + 6.25 * data['growths'] - 5 * data['ages'] + 5
    await message.answer(f'Ваша ежедневная норма каллорий - {calories}')
    await state.finish()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию.', reply_markup=kb_in)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    count = 0
    for product in products:
        title, description, price = product[1], product[2], product[3]
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
        with open(f'files/{product[0]}.png', 'rb') as img:
            await message.answer_photo(img)
        count += 1
        if count == 4:
            break
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_in2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!', reply_markup=kb_in2)
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
