"""
This module handles the API requests for the Telegram bot.
"""

import aiohttp
from config import API_BASE_URL
from keyboards import (
    get_start_keyboard,
    get_back_to_start_keyboard,
)


async def api_request(
    method: str, endpoint: str, json: dict = None, headers: dict = None
):
    """
    Makes an HTTP request to the API.

    Args:
        method (str): HTTP method to use (e.g., "POST", "GET").
        endpoint (str): API endpoint to interact with.
        json (dict, optional): Data to send in the request body.
        headers (dict, optional): Additional headers for the request.

    Returns:
        dict: JSON response from the API.

    Raises:
        Exception: Raises an exception for HTTP errors or connection issues.
    """
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, json=json, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise Exception(f"Network error occurred: {str(e)}")
    except aiohttp.http_exceptions.HttpProcessingError as e:
        raise Exception(f"HTTP error occurred: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")


async def handle_api_request(
    method, endpoint, payload, success_message, error_message, msg
):
    try:
        response = await api_request(method, endpoint, json=payload)
        if response.get("status") == "success":
            await msg.answer(success_message, reply_markup=get_start_keyboard())
        else:
            raise Exception(error_message)
    except Exception as e:
        await msg.answer(
            f"Error: {str(e)}. Please try again later.",
            reply_markup=get_back_to_start_keyboard(),
        )
