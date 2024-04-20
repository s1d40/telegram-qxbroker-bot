import sys
import time
import datetime
import shutup
import random
import asyncio
import collections
import schedule
from termcolor import colored
import numpy as np
import datetime
from quotexpy import Quotex
from quotexpy.utils import asset_parse
from quotexpy.utils.account_type import AccountType
from quotexpy.utils.operation_type import OperationType
from quotexpy.utils.duration_time import DurationTime
from quotexpy.ws.objects.timesync import TimeSync
from my_connection import MyConnection


#if error, access https://stackoverflow.com/questions/73193119/python-filenotfounderror-winerror-2-the-system-cannot-find-the-file-specifie

shutup.please()

asset_current = "AUDCAD"


def __x__(y):
    z = asyncio.get_event_loop().run_until_complete(y)
    return z


client = Quotex(
    email="bluebird22.s1d@gmail.com",
    password="rJsJr9]Q9f-RB?7X",
)

client.debug_ws_enable = False


def check_asset(asset):
    asset_query = asset_parse(asset)
    asset_open = client.check_asset_open(asset_query)
    if not asset_open[2]:
        print(colored("[WARN]: ", "yellow"), "Asset is closed.")
        asset = f"{asset}_otc"
        print(colored("[WARN]: ", "yellow"), "Try OTC Asset -> " + asset)
        asset_query = asset_parse(asset)
        asset_open = client.check_asset_open(asset_query)
    return asset, asset_open


async def get_balance():
    prepare_connection = MyConnection(client)
    check_connect, message = await prepare_connection.connect()
    if check_connect:
        client.change_account(AccountType.PRACTICE)  # "REAL"
        print(colored("[INFO]: ", "blue"), "Balance: ", await client.get_balance())
        print(colored("[INFO]: ", "blue"), "Exiting...")
    prepare_connection.close()


async def wait_until_time(target_time):
    """ Waits until the specified target_time """
    now = datetime.datetime.now()
    wait_seconds = (target_time - now).total_seconds()
    if wait_seconds > 0:
        print(f"Waiting for {wait_seconds} seconds to continue operation.")
        await asyncio.sleep(wait_seconds)

async def trade_and_check_win(duration, _action, time, pair):
    prepare_connection = MyConnection(client)
    check_connect, message = await prepare_connection.connect()
    if check_connect:
        client.change_account(AccountType.PRACTICE) #REAL
        entry_time = datetime.datetime.strptime(time, '%H:%M')
        entry_time = datetime.datetime.combine(datetime.datetime.today(), entry_time.time())  # ensure it's set for today
        now = datetime.datetime.now()

        # Check if the entry time has already passed
        if entry_time <= now:
            print(colored("[WARN]: ", "red"), f"Specified time {entry_time.strftime('%H:%M')} has already passed. Exiting function.")
            return  # Exit the function since the time has passed

        print(colored("[INFO]: ", "blue"), "Balance: ", await client.get_balance())
        amount = 50
        asset, asset_open = check_asset(pair)

        # Wait until the exact target time
        await wait_until_time(entry_time)

        if asset_open[2]:
            print(colored("[INFO]: ", "blue"), "Asset is open.")
            status, trade_info = await client.trade(_action, amount, asset, duration)
            print(status, trade_info)
            if status:
                print(colored("[INFO]: ", "blue"), "Waiting for result...")
                if await client.check_win(asset, trade_info):
                    print(colored("[INFO]: ", "green"), f"Win -> Profit: {client.get_profit()}")
                else:
                    print(colored("[INFO]: ", "light_red"), f"Loss -> Loss: {client.get_profit()}")
            else:
                print(colored("[WARN]: ", "light_red"), "Operation not realized.")
        else:
            print(colored("[WARN]: ", "light_red"), "Asset is closed.")
        print(colored("[INFO]: ", "blue"), "Balance: ", await client.get_balance())

    prepare_connection.close()
    print(colored("[INFO]: ", "blue"), "Exiting...")



async def main(signal):
    # await get_balance()
    # await get_signal_data()
    # await get_payment()
    # await get_payments_payout_more_than()
    # await get_candle_v2()
    # await assets_open()
    if signal['expiration'] == '1 min':
        expiration = DurationTime.ONE_MINUTE
    elif signal['expiration'] == '5 min':
        expiration = DurationTime.FIVE_MINUTES
    if signal['entry_type'] == 'CALL':
        entry_type = OperationType.CALL_GREEN
    elif signal['entry_type'] == 'PUT':
        entry_type = OperationType.PUT_RED
    
    await trade_and_check_win(duration=expiration, _action=entry_type, time=signal["time"], pair=signal["pair"])
    # await balance_refill()
    

def run_main():
    try:
        __x__(main())
    except KeyboardInterrupt:
        print("Aborted!")
        sys.exit(0)


