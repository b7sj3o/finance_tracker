from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard():
    """
    Creates the start keyboard with options for user actions.

    Returns:
        InlineKeyboardMarkup: A keyboard with buttons for registering, logging in, viewing and managing expenses, and other actions.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Register", callback_data="register")],
            [InlineKeyboardButton(text="Login", callback_data="login")],
            [InlineKeyboardButton(text="About", callback_data="about")],
            [InlineKeyboardButton(text="Report", callback_data="report")],
            [InlineKeyboardButton(text="View Expenses", callback_data="view_expenses")],
            [InlineKeyboardButton(text="Add Expense", callback_data="add_expense")],
            [InlineKeyboardButton(text="Edit Expense", callback_data="edit_expense")],
            [
                InlineKeyboardButton(
                    text="Delete Expense", callback_data="delete_expense"
                )
            ],
            [InlineKeyboardButton(text="View History", callback_data="view_history")],
        ]
    )


def get_report_keyboard():
    """
    Creates the report keyboard with options for generating a report or returning to the start menu.

    Returns:
        InlineKeyboardMarkup: A keyboard with buttons to generate a report or go back to the start menu.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Generate Report", callback_data="get_report")],
            [InlineKeyboardButton(text="Back to Start", callback_data="start")],
        ]
    )


def get_back_to_start_keyboard():
    """
    Creates a keyboard with a single button to return to the start menu.

    Returns:
        InlineKeyboardMarkup: A keyboard with a button to go back to the start menu.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to Start", callback_data="start")],
        ]
    )


def get_expense_period_keyboard():
    """
    Creates a keyboard for selecting the expense period (daily, monthly, yearly) or returning to the start menu.

    Returns:
        InlineKeyboardMarkup: A keyboard with buttons for viewing expenses by period or going back to the start menu.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Daily", callback_data="view_daily_expenses")],
            [
                InlineKeyboardButton(
                    text="Monthly", callback_data="view_monthly_expenses"
                )
            ],
            [InlineKeyboardButton(text="Yearly", callback_data="view_yearly_expenses")],
            [InlineKeyboardButton(text="Back to Start", callback_data="start")],
        ]
    )
