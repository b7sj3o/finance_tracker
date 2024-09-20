import os
import aiohttp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from utils.auth_utils import generate_csv_report
from keyboards import (
    get_start_keyboard,
    get_report_keyboard,
    get_back_to_start_keyboard,
    get_expense_period_keyboard,
    get_income_period_keyboard,
)
from config import dp, Registration, Login, Expense, Income, router
from db import db_session, User, Finance

API_BASE_URL = "http://your_django_api_url"


async def api_request(
    method: str, endpoint: str, json: dict = None, headers: dict = None
):
    async with aiohttp.ClientSession() as session:
        url = f"{API_BASE_URL}/{endpoint}"
        async with session.request(method, url, json=json, headers=headers) as response:
            return await response.json()


@dp.message(F.text == "/start")
async def start(msg: Message, state: FSMContext):
    user = db_session.query(User).filter_by(username=msg.from_user.username).first()
    await msg.delete()
    if user:
        await msg.answer(f"Hello {user.username}, you are logged in.")
    else:
        await msg.answer(
            "Welcome! Please choose an action:", reply_markup=get_start_keyboard()
        )


@dp.callback_query(F.data == "start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Welcome! Please choose an action:", reply_markup=get_start_keyboard()
    )


@dp.callback_query(F.data == "register")
async def register_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter your desired username.", reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(Registration.waiting_for_username)


@dp.message(Registration.waiting_for_username)
async def process_username(msg: Message, state: FSMContext):
    username = msg.text.strip()
    if db_session.query(User).filter_by(username=username).first():
        await msg.answer(
            "Username already exists. Please choose a different username.",
            reply_markup=get_back_to_start_keyboard(),
        )
    else:
        await state.update_data(username=username)
        await msg.answer(
            "Please enter your email address.",
            reply_markup=get_back_to_start_keyboard(),
        )
        await state.set_state(Registration.waiting_for_email)


@dp.message(Registration.waiting_for_email)
async def process_email(msg: Message, state: FSMContext):
    email = msg.text.strip()
    await state.update_data(email=email)
    await msg.answer(
        "Please enter your password.", reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(Registration.waiting_for_password)


@dp.message(Registration.waiting_for_password)
async def process_password(msg: Message, state: FSMContext):
    password = msg.text.strip()
    user_data = await state.get_data()
    username = user_data.get("username")
    email = user_data.get("email")

    if not username or not email:
        await msg.answer(
            "Error: Registration data is incomplete.",
            reply_markup=get_back_to_start_keyboard(),
        )
        await state.clear()
        return

    payload = {"username": username, "email": email, "password": password}
    response = await api_request("POST", "bot/register/", json=payload)
    if response.get("status") == "success":
        await msg.answer(
            f"User {username} registered successfully.",
            reply_markup=get_start_keyboard(),
        )
        await state.clear()
    else:
        await msg.answer(
            "Registration failed. Please try again later.",
            reply_markup=get_back_to_start_keyboard(),
        )
        await state.clear()


@dp.callback_query(F.data == "login")
async def login_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter your username.", reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(Login.waiting_for_username)


@dp.message(Login.waiting_for_username)
async def process_login_username(msg: Message, state: FSMContext):
    username = msg.text.strip()
    user = db_session.query(User).filter_by(username=username).first()
    if user:
        await state.update_data(username=username)
        await msg.answer(
            "Please enter your password.", reply_markup=get_back_to_start_keyboard()
        )
        await state.set_state(Login.waiting_for_password)
    else:
        await msg.answer(
            "Username not found. Please try again or register.",
            reply_markup=get_back_to_start_keyboard(),
        )


@dp.message(Login.waiting_for_password)
async def process_login_password(msg: Message, state: FSMContext):
    password = msg.text.strip()
    user_data = await state.get_data()
    username = user_data.get("username")

    if not username:
        await msg.answer(
            "Error: Login data is incomplete.",
            reply_markup=get_back_to_start_keyboard(),
        )
        await state.clear()
        return

    payload = {"username": username, "password": password}
    response = await api_request("POST", "bot/login/", json=payload)
    if response.get("status") == "success":
        await msg.answer(
            f"Welcome back, {username}!", reply_markup=get_start_keyboard()
        )
        # Store the token in the state or database if needed
        await state.update_data(token=response.get("token"))
        await state.clear()
    else:
        await msg.answer(
            "Invalid password. Please try again.",
            reply_markup=get_back_to_start_keyboard(),
        )


@dp.callback_query(F.data == "report")
async def report(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please choose how you'd like to receive your report or specify the format.",
        reply_markup=get_report_keyboard(),
    )


@dp.callback_query(F.data == "get_report")
async def get_report(callback: CallbackQuery, state: FSMContext):
    file_path = generate_csv_report()
    try:
        with open(file_path, "rb") as file:
            await callback.message.answer_document(file)
        os.remove(file_path)
        await callback.message.answer(
            "Here is your report.", reply_markup=get_start_keyboard()
        )
    except Exception as e:
        await callback.message.answer(
            "Failed to generate report. Please try again later.",
            reply_markup=get_start_keyboard(),
        )


@dp.callback_query(F.data == "view_expenses")
async def view_expenses(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Choose the period to view expenses:",
        reply_markup=get_expense_period_keyboard(),
    )


@dp.callback_query(F.data == "add_expense")
async def add_expense(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter the expense details in the following format:\n\nAmount Description",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Expense.waiting_for_expense_details)


@dp.message(Expense.waiting_for_expense_details)
async def process_expense_details(msg: Message, state: FSMContext):
    expense_details = msg.text.split(" ", 1)
    if len(expense_details) == 2:
        amount, description = expense_details
        try:
            amount = float(amount)
        except ValueError:
            await msg.answer(
                "Invalid amount format. Please enter a valid number.",
                reply_markup=get_back_to_start_keyboard(),
            )
            return

        user = db_session.query(User).filter_by(username=msg.from_user.username).first()
        if user:
            payload = {"amount": amount, "description": description}
            response = await api_request(
                "POST",
                "bot/expense/",
                json=payload,
                headers={"Authorization": f"Bearer {user.token}"},
            )
            if response.get("status") == "success":
                await msg.answer(
                    "Expense added successfully.", reply_markup=get_start_keyboard()
                )
            else:
                await msg.answer(
                    "Failed to add expense. Please try again later.",
                    reply_markup=get_back_to_start_keyboard(),
                )
        else:
            await msg.answer(
                "User not found. Please register or login.",
                reply_markup=get_start_keyboard(),
            )
    else:
        await msg.answer(
            "Invalid format. Please use 'Amount Description'.",
            reply_markup=get_back_to_start_keyboard(),
        )
    await state.clear()


@dp.callback_query(F.data == "update_expense")
async def update_expense(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter the ID of the expense you want to update, followed by the new details in the format:\n\nID Amount Description",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Expense.waiting_for_update_details)


@dp.message(Expense.waiting_for_update_details)
async def process_update_details(msg: Message, state: FSMContext):
    update_details = msg.text.split(" ", 2)
    if len(update_details) == 3:
        expense_id, amount, description = update_details
        try:
            amount = float(amount)
        except ValueError:
            await msg.answer(
                "Invalid amount format. Please enter a valid number.",
                reply_markup=get_back_to_start_keyboard(),
            )
            return

        user = db_session.query(User).filter_by(username=msg.from_user.username).first()
        if user:
            payload = {"amount": amount, "description": description}
            response = await api_request(
                "PUT",
                f"bot/expense/{expense_id}/",
                json=payload,
                headers={"Authorization": f"Bearer {user.token}"},
            )
            if response.get("status") == "success":
                await msg.answer(
                    "Expense updated successfully.", reply_markup=get_start_keyboard()
                )
            else:
                await msg.answer(
                    "Failed to update expense. Please try again later.",
                    reply_markup=get_back_to_start_keyboard(),
                )
        else:
            await msg.answer(
                "User not found. Please register or login.",
                reply_markup=get_start_keyboard(),
            )
    else:
        await msg.answer(
            "Invalid format. Please use 'ID Amount Description'.",
            reply_markup=get_back_to_start_keyboard(),
        )
    await state.clear()


@dp.callback_query(F.data == "delete_expense")
async def delete_expense(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter the ID of the expense you want to delete.",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Expense.waiting_for_delete_id)


@dp.message(Expense.waiting_for_delete_id)
async def process_delete_id(msg: Message, state: FSMContext):
    expense_id = msg.text.strip()
    user = db_session.query(User).filter_by(username=msg.from_user.username).first()
    if user:
        response = await api_request(
            "DELETE",
            f"bot/expense/{expense_id}/",
            headers={"Authorization": f"Bearer {user.token}"},
        )
        if response.get("status") == "success":
            await msg.answer(
                "Expense deleted successfully.", reply_markup=get_start_keyboard()
            )
        else:
            await msg.answer(
                "Failed to delete expense. Please try again later.",
                reply_markup=get_back_to_start_keyboard(),
            )
    else:
        await msg.answer(
            "User not found. Please register or login.",
            reply_markup=get_start_keyboard(),
        )
    await state.clear()


@dp.callback_query(F.data == "view_incomes")
async def view_incomes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Choose the period to view incomes:",
        reply_markup=get_income_period_keyboard(),
    )


@dp.callback_query(F.data == "add_income")
async def add_income(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter the income details in the following format:\n\nAmount Description",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Income.waiting_for_income_details)


@dp.message(Income.waiting_for_income_details)
async def process_income_details(msg: Message, state: FSMContext):
    income_details = msg.text.split(" ", 1)
    if len(income_details) == 2:
        amount, description = income_details
        try:
            amount = float(amount)
        except ValueError:
            await msg.answer(
                "Invalid amount format. Please enter a valid number.",
                reply_markup=get_back_to_start_keyboard(),
            )
            return

        user = db_session.query(User).filter_by(username=msg.from_user.username).first()
        if user:
            payload = {"amount": amount, "description": description}
            response = await api_request(
                "POST",
                "bot/income/",
                json=payload,
                headers={"Authorization": f"Bearer {user.token}"},
            )
            if response.get("status") == "success":
                await msg.answer(
                    "Income added successfully.", reply_markup=get_start_keyboard()
                )
            else:
                await msg.answer(
                    "Failed to add income. Please try again later.",
                    reply_markup=get_back_to_start_keyboard(),
                )
        else:
            await msg.answer(
                "User not found. Please register or login.",
                reply_markup=get_start_keyboard(),
            )
    else:
        await msg.answer(
            "Invalid format. Please use 'Amount Description'.",
            reply_markup=get_back_to_start_keyboard(),
        )
    await state.clear()


@dp.callback_query(F.data == "update_income")
async def update_income(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter the ID of the income you want to update, followed by the new details in the format:\n\nID Amount Description",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Income.waiting_for_update_details)


@dp.message(Income.waiting_for_update_details)
async def process_update_income(msg: Message, state: FSMContext):
    update_details = msg.text.split(" ", 2)
    if len(update_details) == 3:
        income_id, amount, description = update_details
        try:
            amount = float(amount)
        except ValueError:
            await msg.answer(
                "Invalid amount format. Please enter a valid number.",
                reply_markup=get_back_to_start_keyboard(),
            )
            return

        user = db_session.query(User).filter_by(username=msg.from_user.username).first()
        if user:
            payload = {"amount": amount, "description": description}
            response = await api_request(
                "PUT",
                f"bot/income/{income_id}/",
                json=payload,
                headers={"Authorization": f"Bearer {user.token}"},
            )
            if response.get("status") == "success":
                await msg.answer(
                    "Income updated successfully.", reply_markup=get_start_keyboard()
                )
            else:
                await msg.answer(
                    "Failed to update income. Please try again later.",
                    reply_markup=get_back_to_start_keyboard(),
                )
        else:
            await msg.answer(
                "User not found. Please register or login.",
                reply_markup=get_start_keyboard(),
            )
    else:
        await msg.answer(
            "Invalid format. Please use 'ID Amount Description'.",
            reply_markup=get_back_to_start_keyboard(),
        )
    await state.clear()


@dp.callback_query(F.data == "delete_income")
async def delete_income(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please enter the ID of the income you want to delete.",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Income.waiting_for_delete_id)


@dp.message(Income.waiting_for_delete_id)
async def process_delete_income(msg: Message, state: FSMContext):
    income_id = msg.text.strip()
    user = db_session.query(User).filter_by(username=msg.from_user.username).first()
    if user:
        response = await api_request(
            "DELETE",
            f"bot/income/{income_id}/",
            headers={"Authorization": f"Bearer {user.token}"},
        )
        if response.get("status") == "success":
            await msg.answer(
                "Income deleted successfully.", reply_markup=get_start_keyboard()
            )
        else:
            await msg.answer(
                "Failed to delete income. Please try again later.",
                reply_markup=get_back_to_start_keyboard(),
            )
    else:
        await msg.answer(
            "User not found. Please register or login.",
            reply_markup=get_start_keyboard(),
        )
    await state.clear()
