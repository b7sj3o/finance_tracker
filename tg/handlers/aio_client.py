"""
This module handles the routes for the Telegram bot.
"""

import aiohttp
from config import API_BASE_URL


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
    """
    async with aiohttp.ClientSession() as session:
        url = f"{API_BASE_URL}/{endpoint}"
        async with session.request(method, url, json=json, headers=headers) as response:
            return await response.json()
