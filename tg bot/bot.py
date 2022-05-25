from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import TOKEN, owner, shop_name, support_user
import sqlite3






#Settings
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

#Database
db_path = 'shop.db'



#States
class SendMsg(StatesGroup):
    waiting_msg = State()

class AddProduct(StatesGroup):
    name = State()
    category = State()
    size = State()
    price = State()



#KEYBOARD
product_button = KeyboardButton('👕Products👕')
cart_button = KeyboardButton('🛒Cart🛒')
sup_button = KeyboardButton('🧞‍♂️Support🧞‍♂️')
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.row(product_button, cart_button).add(sup_button)


#ADMIN KEYBOARD
add_product_button = KeyboardButton('➕Add product➕')
send_message_button = KeyboardButton('✉️Send message✉️')
back_button = KeyboardButton('◀️BACK')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.row(add_product_button, send_message_button).add(back_button)


#start & menu
@dp.message_handler(commands=['start', 'menu'])
async def start(message: types.Message):
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    sql.execute(f"SELECT tg_id FROM users WHERE tg_id = '{message.from_user.id}'")
    if sql.fetchone() is None:
	    sql.execute(f'INSERT INTO users(tg_id, admin) VALUES (?, ?)', (message.from_user.id, False))
	    db.commit()
	    sql.close()
	    await message.answer((f'''Hi 👋
								🤖 I'm a bot from {shop_name}.

								💫 Let's get you some cool clothes!
            					'''), reply_markup=start_kb)
    else:
        sql.close()
        await message.answer((f'Welcome back, {message.from_user.full_name}'), reply_markup=start_kb)


#🧞‍♂️Support🧞‍♂️
@dp.message_handler(Text(equals=['🧞‍♂️Support🧞‍♂️']))
async def support(message: types.message):
    await message.answer((f'💬 Do you have any questions? Write to the manager 👉 {support_user}'), reply_markup=start_kb)


#◀️BACK
@dp.message_handler(Text(equals=['◀️BACK']))
async def back(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(('Menu'), reply_markup=start_kb)
        return
    await state.finish()
    await message.answer(('Menu'), reply_markup=start_kb)


#ADMIN COMMANDS

#Admin panel
@dp.message_handler(commands=['adminpanel'])
async def adminpanel(message: types.Message):
    if message.from_user.id == owner:
        await message.answer((f"Welcome to the admin panel, {message.from_user.full_name}"), reply_markup=admin_kb)
    else:
        await message.answer(('This feature is not available to you!'), reply_markup=start_kb)

#✉️Send message✉️
@dp.message_handler(Text(equals=['✉️Send message✉️']))
async def send_message(message: types.message):
    try: 
        if message.from_user.id == owner:
                await message.answer('Enter the user id as well as the message with <,>nExample: 121231231, hello!')
                await SendMsg.waiting_msg.set()
    except:
        await message.answer('Error')
        await dp.storage.close()
        await dp.storage.wait_closed()


@dp.message_handler(state=SendMsg.waiting_msg)
async def send_msg(message: types.Message):
    try:
        if message.from_user.id == owner:
            msg = message.text
            msg = msg.split(', ')
            await bot.send_message(msg[0], f'You have a message from the administrator!\nMessage:\n\n{msg[1]}')
            await message.answer('Message sent!')
            await dp.storage.close()
            await dp.storage.wait_closed()
    except:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await message.answer('Error')


#➕Add product➕
@dp.message_handler(Text(equals=['➕Add product➕']))
async def add_product(message: types.message):
    try: 
        if message.from_user.id == owner:
            await message.answer('Enter name product: ')
            await AddProduct.name.set()
    except:
        await message.answer('Error')
        await dp.storage.close()
        await dp.storage.wait_closed()

@dp.message_handler(state=AddProduct.name)
async def send_name(message: types.Message, state: FSMContext):
    try:
        if message.from_user.id == owner:
            async with state.proxy() as data:
                data['name'] = message.text
            await AddProduct.next()
            await message.answer('Enter category: ')
    except:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await message.answer('Error')

@dp.message_handler(state=AddProduct.category)
async def send_cat(message: types.Message, state: FSMContext):
    try:
        if message.from_user.id == owner:
            async with state.proxy() as data:
                data['category'] = message.text
            await AddProduct.next()
            await message.answer('Enter size: ')
    except:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await message.answer('Error')

@dp.message_handler(state=AddProduct.size)
async def send_msg(message: types.Message, state: FSMContext):
    try:
        if message.from_user.id == owner:
            async with state.proxy() as data:
                data['size'] = message.text
            await AddProduct.next()
            await message.answer('Enter price: ')
    except:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await message.answer('Error')

@dp.message_handler(state=AddProduct.price)
async def send_msg(message: types.Message, state: FSMContext):
    try:
        if message.from_user.id == owner:
            async with state.proxy() as data:
                data['price'] = message.text
            db = sqlite3.connect(db_path)
            sql = db.cursor()
            sql.execute(f'INSERT INTO products(name, category, size, price) VALUES (?, ?, ?, ?)', (data['name'], data['category'], data['size'], data['price']))
            db.commit()
            sql.close()
            await message.answer('Done! Product added!')
            await state.finish()
    except:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await message.answer('Error')


#SHOP

#👕Products👕
# ...




if __name__ == '__main__':
    executor.start_polling(dp)







