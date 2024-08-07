from aiogram import types, F
from aiogram.fsm.context import FSMContext
from utils.auth_utils import generate_csv_report
from keyboards import (
    get_start_keyboard,
    get_report_keyboard,
    get_back_to_start_keyboard,
    get_expense_period_keyboard,
)
import os
from config import dp, Registration, Login, Expense, router
from db import db_session, User, Finance


@dp.message(F.text == "/start")
async def start(msg: types.Message, state: FSMContext):
    """
    Handles the /start command. Greets the user if they are logged in,
    otherwise presents the start menu.
    """
    user = db_session.query(User).filter_by(username=msg.from_user.username).first()
    await msg.delete()
    if user:
        await msg.answer(f"Hello {user.username}, you are logged in.")
    else:
        await msg.answer(
            "Welcome! Please choose an action:", reply_markup=get_start_keyboard()
        )


@dp.callback_query(F.data == "start")
async def back_to_start(callback: types.CallbackQuery, state: FSMContext):
    """
    Handles the 'start' callback. Displays the start menu again.
    """
    await callback.message.edit_text(
        "Welcome! Please choose an action:", reply_markup=get_start_keyboard()
    )


@dp.callback_query(F.data == "register")
async def register_start(callback: types.CallbackQuery, state: FSMContext):
    """
    Initiates the registration process by asking for the username.
    """
    await callback.message.edit_text(
        "Please enter your desired username.", reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(Registration.waiting_for_username)


@dp.message(Registration.waiting_for_username)
async def process_username(msg: types.Message, state: FSMContext):
    """
    Processes the username entered by the user during registration.
    Checks if the username already exists.
    """
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
async def process_email(msg: types.Message, state: FSMContext):
    """
    Processes the email address entered by the user during registration.
    """
    email = msg.text.strip()
    await state.update_data(email=email)
    await msg.answer(
        "Please enter your password.", reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(Registration.waiting_for_password)


@dp.message(Registration.waiting_for_password)
async def process_password(msg: types.Message, state: FSMContext):
    """
    Processes the password entered by the user during registration.
    """
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

    user = User(username=username, email=email, password_hash=password)
    db_session.add(user)
    db_session.commit()
    await msg.answer(
        f"User {username} registered successfully.", reply_markup=get_start_keyboard()
    )
    await state.clear()


@dp.callback_query(F.data == "login")
async def login_start(callback: types.CallbackQuery, state: FSMContext):
    """
    Initiates the login process by asking for the username.
    """
    await callback.message.edit_text(
        "Please enter your username.", reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(Login.waiting_for_username)


@dp.message(Login.waiting_for_username)
async def process_login_username(msg: types.Message, state: FSMContext):
    """
    Processes the username entered by the user during login.
    """
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
async def process_login_password(msg: types.Message, state: FSMContext):
    """
    Processes the password entered by the user during login.
    """
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

    user = db_session.query(User).filter_by(username=username).first()
    if user and user.password_hash == password:
        await msg.answer(
            f"Welcome back, {username}!", reply_markup=get_start_keyboard()
        )
        await state.clear()
    else:
        await msg.answer(
            "Invalid password. Please try again.",
            reply_markup=get_back_to_start_keyboard(),
        )


@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery, state: FSMContext):
    """
    Provides information about the bot.
    """
    await callback.message.edit_text(
        "This is a finance management bot. You can track your expenses, generate reports, and more.",
        reply_markup=get_back_to_start_keyboard(),
    )


@dp.callback_query(F.data == "report")
async def report(callback: types.CallbackQuery, state: FSMContext):
    """
    Prompts the user to choose how they would like to receive the report.
    """
    await callback.message.edit_text(
        "Please choose how you'd like to receive your report or specify the format.",
        reply_markup=get_report_keyboard(),
    )


@dp.callback_query(F.data == "get_report")
async def get_report(callback: types.CallbackQuery, state: FSMContext):
    """
    Generates and sends the CSV report to the user.
    """
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
async def view_expenses(callback: types.CallbackQuery, state: FSMContext):
    """
    Prompts the user to choose a period to view their expenses.
    """
    await callback.message.edit_text(
        "Choose the period to view expenses:",
        reply_markup=get_expense_period_keyboard(),
    )


@dp.callback_query(F.data == "add_expense")
async def add_expense(callback: types.CallbackQuery, state: FSMContext):
    """
    Prompts the user to enter expense details.
    """
    await callback.message.edit_text(
        "Please enter the expense details in the following format:\n\nAmount Description",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Expense.waiting_for_expense_details)


@dp.callback_query(F.data == "edit_expense")
async def edit_expense(callback: types.CallbackQuery, state: FSMContext):
    """
    Prompts the user to enter the ID of the expense they want to edit.
    """
    await callback.message.edit_text(
        "Please enter the ID of the expense you want to edit:",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Expense.waiting_for_expense_id)


@dp.callback_query(F.data == "delete_expense")
async def delete_expense(callback: types.CallbackQuery, state: FSMContext):
    """
    Prompts the user to enter the ID of the expense they want to delete.
    """
    await callback.message.edit_text(
        "Please enter the ID of the expense you want to delete:",
        reply_markup=get_back_to_start_keyboard(),
    )
    await state.set_state(Expense.waiting_for_expense_id)


@dp.callback_query(F.data == "view_history")
async def view_history(callback: types.CallbackQuery, state: FSMContext):
    """
    Informs the user that viewing history is not yet implemented.
    """
    await callback.message.edit_text(
        "Viewing history is not yet implemented.",
        reply_markup=get_back_to_start_keyboard(),
    )


@dp.message(Expense.waiting_for_expense_details)
async def process_expense_details(msg: types.Message, state: FSMContext):
    """
    Processes the details of an expense entered by the user.
    """
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
            expense = Finance(user_id=user.id, amount=amount, description=description)
            db_session.add(expense)
            db_session.commit()
            await msg.answer(
                "Expense added successfully.", reply_markup=get_start_keyboard()
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


@dp.message(Expense.waiting_for_expense_id)
async def process_expense_id(msg: types.Message, state: FSMContext):
    """
    Processes the ID of an expense for editing or deletion.
    """
    expense_id = msg.text.strip()
    user = db_session.query(User).filter_by(username=msg.from_user.username).first()
    if user:
        expense = (
            db_session.query(Finance).filter_by(id=expense_id, user_id=user.id).first()
        )
        if expense:
            db_session.delete(expense)
            db_session.commit()
            await msg.answer(
                "Expense deleted successfully.", reply_markup=get_start_keyboard()
            )
        else:
            await msg.answer(
                "Expense not found. Please check the ID and try again.",
                reply_markup=get_back_to_start_keyboard(),
            )
    else:
        await msg.answer(
            "User not found. Please register or login.",
            reply_markup=get_back_to_start_keyboard(),
        )
    await state.clear()
