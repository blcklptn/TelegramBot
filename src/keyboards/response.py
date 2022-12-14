from dispatcher import dp, bot
from aiogram import types
from utils.dataspace import *
from keyboards.start_menu import *
from aiogram.dispatcher import FSMContext 
from keyboards.states import *
from keyboards.admin_menu import *
from utils import validator
import core.config
from keyboards.load_files import *
import datetime
from utils.ozon import refactor_logic
import asyncio
from core import ozon_auth

rf_class = refactor_logic.GetReviews()

config.loop = asyncio.get_event_loop()
print(config.loop)
ManageAdmins().set_default_admin()


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    if ManageAdmins().check_admin(user_id = str(message.from_user.id)):
        await message.reply("admin", reply_markup=admin_keyboard)
    else:
        if core.config.Bot_on:
            if  ManageUsers().check_user(message.from_user.id):
                await message.reply("Привет!", reply_markup=main_kb)
            else: 
                await message.reply("Привет! Тебе нужно зарегестрироваться!", reply_markup=start_kb)

@dp.message_handler(commands=["test"])
async def process_start_command(message: types.Message):
    
    await message.reply("Введите номер телефона")
    await GetCookies.get_phone.set()

    
    

@dp.message_handler(state=GetCookies.get_phone, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
    global app
    await message.reply(f"Ваш номер: {message.text}")
    await message.answer("В течении 3х минут вам поступит код или звонок! Введите его")
    app = ozon_auth.Application()
    app.SignIn(message.text)
    await GetCookies.get_code.set()

@dp.message_handler(state=GetCookies.get_code, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(message.text)
    cookies_path = app.what_the_type(message.text)
    ManageUsers().load_cookies(message.from_user.id, dest=cookies_path)
    await message.answer("У нас есть ваши куки ;)")

"""
@dp.message_handler(commands=["add_admin"])
async def process_start_command(message: types.Message):
    admin = Admins(
    user_id = message.from_user.id
)
    ManageAdmins().add_admin(admin)
"""

@dp.message_handler(commands=["run"])
async def process_start_command(message: types.Message):
    await message.reply('run!')
    print('Here!')
    user = dataspace.ManageUsers().get_user(str(message.from_user.id))

    await rf_class.get_new_reviews_bot(str(user.user_id), str(user.company_id), str(user.cookies_file), user.list_of_products_file, user.recomendations_file)


@dp.message_handler(text="Расценки", state="*")
async def description(message: types.Message):
    if core.config.Bot_on:
        await message.reply("Текст расценок", reply_markup=return_kb)

@dp.message_handler(text="Описание", state='*')
async def description(message: types.Message):
    if core.config.Bot_on:
        await message.reply("Текст описания", reply_markup=return_kb)



@dp.message_handler(text="Оплата", state="*")
async def set_pay(message: types.Message, state: FSMContext):
    if core.config.Bot_on:
        await message.answer(f'Чтобы оплатить подписку, отправьте {settings.PRICE} на {settings.CARD_NUMBER} и отправьте скриншот!', reply_markup=return_kb)
        await Payment.qw.set()

@dp.message_handler(state=Payment.qw, content_types=['photo'])
async def fname_step(message: types.Message, state: FSMContext):
    if core.config.Bot_on:
        user_id = str(message.from_user.id)

        file = await bot.get_file(message.photo[-1].file_id)
        file_path = file.file_path
        print(file_path)
        destination = settings.DATA_STORAGE + 'to_admins' + "/" + user_id + '.png'
        await bot.download_file(file_path, destination)
        await message.reply('Оплата проверяется администраторами!', reply_markup=main_kb)
        photo = types.input_file.InputFile(destination)
        await bot.send_photo(dataspace.ManageAdmins().get_all_admins()[0].user_id, photo=photo, caption=f' {user_id}', reply_markup=inline_kb1)
        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Оплата подтверждена')
    capt = callback_query.message.caption
    await bot.send_message(capt, "Администратор подтвердил подписку!")
    dataspace.ManageUsers().new_pay(capt)
        


@dp.message_handler(text="Инструкция по настройке", state='*')
async def description(message: types.Message):
    if core.config.Bot_on:
        with open(settings.INSTRUCTIONS_FILE) as file:
            text = file.read()

        await message.reply(text, reply_markup=return_kb)

@dp.message_handler(text="Вопросы и пожелания", state='*')
async def description(message: types.Message):
    if core.config.Bot_on:
        await message.reply("Вы можете написать свой вопрос или пожелание по работе бота, мы постараемся ответит Вам в ближайшее время", reply_markup=return_kb)

@dp.message_handler(text="Вернуться", state='*')
async def description(message: types.Message):
    if core.config.Bot_on:
        if dataspace.ManageUsers().check_user(message.from_user.id):
            await message.answer("Привет!",reply_markup=main_kb)
        else:
            await message.answer("Привет! Тебе нужно зарегестрироваться",reply_markup=start_kb)