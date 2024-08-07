from aiogram import types, F
from aiogram.fsm.context import FSMContext
from utils.auth_utils import get_user, register_user, check_password, get_all_users
from keyboards import get_start_keyboard
import csv, os

from config import dp, Registration, Login, router


@dp.message(F.text == "/start")
async def start(msg: types.Message, state: FSMContext):
    user = get_user(msg.from_user.username)
    if user:
        await msg.answer(f"Hello {user.username}, you are logged in.")
    else:
        await msg.answer(
            "Welcome! Please choose an action:", reply_markup=get_start_keyboard()
        )


@dp.callback_query(F.data == "register")
async def register_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Please enter your desired username.")
    await state.set_state(Registration.waiting_for_username)


@dp.message(Registration.waiting_for_username)
async def process_username(msg: types.Message, state: FSMContext):
    username = msg.text
    if get_user(username):
        await msg.answer("Username already exists. Please choose a different username.")
    else:
        await state.update_data(username=username)
        await msg.answer("Please enter your email address.")
        await state.set_state(Registration.waiting_for_email)


@dp.message(Registration.waiting_for_email)
async def process_email(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data(email=email)
    await msg.answer("Please enter your password.")
    await state.set_state(Registration.waiting_for_password)


@dp.message(Registration.waiting_for_password)
async def process_password(msg: types.Message, state: FSMContext):
    password = msg.text
    user_data = await state.get_data()
    username = user_data["username"]
    email = user_data["email"]

    register_user(username, email, password)
    await msg.answer(f"User {username} registered successfully.")
    await state.clear()


@dp.callback_query(F.data == "login")
async def login_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Please enter your username.")
    await state.set_state(Login.waiting_for_username)


@dp.message(Login.waiting_for_username)
async def process_login_username(msg: types.Message, state: FSMContext):
    username = msg.text
    user = get_user(username)
    if user:
        await state.update_data(username=username)
        await msg.answer("Please enter your password.")
        await state.set_state(Login.waiting_for_password)
    else:
        await msg.answer(
            "Username not found. Please try again or register by sending /register."
        )


@dp.message(Login.waiting_for_password)
async def process_login_password(msg: types.Message, state: FSMContext):
    password = msg.text
    user_data = await state.get_data()
    username = user_data["username"]
    user = get_user(username)
    if user and check_password(user, password):
        await msg.answer(f"Welcome back, {username}!")
        await state.clear()
    else:
        await msg.answer("Invalid password. Please try again or reset your password.")


@dp.message(F.text == "/report")
async def report(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Please choose how you'd like to receive your report or specify the format."
    )


@dp.message(F.text == "/about")
async def about(msg: types.Message, state: FSMContext):
    await msg.answer(
        "This is a finance management bot. You can track your expenses, generate reports, and more."
    )


def generate_csv_report():
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Username", "Email", "Balance"])
        for user in get_all_users():
            writer.writerow([user.id, user.username, user.email, "Balance Placeholder"])
    return "report.csv"


@dp.message(F.text == "/get_report")
async def get_report(msg: types.Message, state: FSMContext):
    file_path = generate_csv_report()
    await msg.answer_document(open(file_path, "rb"))
    os.remove(file_path)
