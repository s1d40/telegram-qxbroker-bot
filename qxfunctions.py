import os
import asyncio
import datetime
from termcolor import colored
from quotexpy import Quotex
from quotexpy.utils import asset_parse
from quotexpy.utils.account_type import AccountType
from my_connection import MyConnection
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global client setup
EMAIL = YOUR_QUOTEX_EMAIL
PASSWORD = YOUR_QUOTEX_PASSWORD
client = Quotex(email=EMAIL, password=PASSWORD)
client.debug_ws_enable = False
# Function to delete session file
def delete_session_file():
    session_file_path = YOUR_SESSION_DOT_JSON_FILE_PATH
    try:
        if os.path.exists(session_file_path):
            os.remove(session_file_path)
            logging.info("Session file deleted successfully.")
            print(colored("Session file deleted successfully.", "green"))
        else:
            logging.info("Session file does not exist.")
            print(colored("Session file does not exist.", "yellow"))
    except Exception as e:
        logging.error(f"Error occurred while trying to delete the session file: {e}")
        print(colored(f"Error occurred while trying to delete the session file: {e}", "red"))

# Function to check asset availability
async def check_asset(asset):
    logging.info(f"Checking asset availability for {asset}")
    print(colored(f"Checking asset availability for {asset}", "blue"))
    asset_query = asset_parse(asset)
    asset_open = client.check_asset_open(asset_query)
    if not asset_open:
        logging.warning("Asset is closed. Trying OTC Asset.")
        print(colored("Asset is closed. Trying OTC Asset.", "yellow"))
        asset = f"{asset}_otc"
        asset_query = asset_parse(asset)
        asset_open = client.check_asset_open(asset_query)
    if not asset_open[2]:
        logging.warning("Asset is closed. Trying OTC Asset.")
        print(colored("Asset is closed. Trying OTC Asset again.", "yellow"))
        asset = f"{asset}_otc"
        asset_query = asset_parse(asset)
        asset_open = client.check_asset_open(asset_query)
    return asset, asset_open

# Function to fetch balance
async def get_balance():
    prepare_connection = MyConnection(client)
    if await prepare_connection.connect():
        client.change_account(AccountType.PRACTICE)  # Switch to REAL if necessary
        balance = await client.get_balance()
        if balance is not None:
            logging.info(f"Current Balance: {balance}")
            print(colored(f"Current Balance: {balance}", "green"))
        else:
            logging.warning("Failed to fetch balance.")
            print(colored("Failed to fetch balance.", "yellow"))
        prepare_connection.close()
        return balance
    else:
        logging.error("Failed to connect to the server.")
        print(colored("Failed to connect to the server.", "red"))
    prepare_connection.close()
    return None

async def wait_until_time_with_reconnect(entry_time):
    """
    Waits until the specified entry_time, checking and maintaining the connection.
    """
    while True:
        now = datetime.datetime.now()
        if now >= entry_time:
            logging.info("Reached the specified entry time.")
            print(colored("Reached the specified entry time.", "green"))
            break
        if not client.check_connect():
            logging.info("Connection lost. Attempting to reconnect...")
            print(colored("Connection lost. Attempting to reconnect...", "yellow"))
            if not await client.connect():
                logging.error("Reconnection failed. Aborting operation.")
                print(colored("Reconnection failed. Aborting operation.", "red"))
                return False
        else:
            logging.info("Connection is active. Waiting...")
            print(colored("Connection is active. Waiting...", "blue"))
        await asyncio.sleep(10)  # check every 10 seconds
    return True

async def trade_and_check_win(duration, action_type, time, pair):
    prepare_connection = MyConnection(client)
    if await prepare_connection.connect():
        client.change_account(AccountType.PRACTICE)  # or account_type.REAL
        entry_time = datetime.datetime.strptime(time, '%H:%M')
        entry_time = datetime.datetime.combine(datetime.datetime.today(), entry_time.time())
        if datetime.datetime.now() >= entry_time:
            logging.warning(f"Specified time {entry_time.strftime('%H:%M')} has already passed. Exiting function.")
            print(colored(f"Specified time {entry_time.strftime('%H:%M')} has already passed. Exiting function.", "red"))
            return
         # Ensure that we're connected and wait until the specified time
        if not await wait_until_time_with_reconnect(entry_time):
            prepare_connection.close()
            return
        logging.info("Checking asset status...")
        print(colored("Checking asset status...", "blue"))
        asset, asset_open = await check_asset(pair)
        if asset_open and asset_open[2]:
            #verify if we are connected right before trading.
            if client.check_connect():
                status, trade_info = await client.trade(action_type, 50, asset, duration)
                if status:
                    print(colored("Entry Sucessful, waiting for result...", "yellow"))
                    win = await client.check_win(asset, trade_info)
                    if win:
                        logging.info(f"Win -> Profit: {client.get_profit()}")
                        print(colored(f"Win -> Profit: {client.get_profit()}", "green"))
                    else:
                        logging.info(f"Loss -> Loss: {client.get_profit()}")
                        print(colored(f"Loss -> Loss: {client.get_profit()}", "red"))
                else:
                    logging.warning("Operation not realized.")
                    print(colored("Operation not realized.", "red"))
            else:
                logging.warning("Connection Lost, Operation not realized.")
                print(colored("Connection Lost, Operation not realized.", "red"))
        else:
            logging.warning("Asset is closed or not found.")
            print(colored("Asset is closed or not found.", "red"))
        prepare_connection.close()
    else:
        logging.error("Failed to connect for trading.")
        print(colored("Failed to connect for trading.", "red"))
    prepare_connection.close()
    #delete_session_file()

# Optionally, include cleanup or logging out logic if needed

# Removed the standalone execution block
