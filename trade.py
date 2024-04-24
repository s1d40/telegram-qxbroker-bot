import os
import asyncio
import logging
import configparser
from pathlib import Path
from pyquotex.quotexapi.stable_api import Quotex
from connect import connect
from check_asset import check_asset
from termcolor import colored
# Set up root logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('application.log')])
logger = logging.getLogger(__name__)

# Load configuration
config_path = Path("./settings/config.ini")
if not config_path.exists():
    config_path.parent.mkdir(exist_ok=True, parents=True)
    text_settings = (f"[settings]\n"
                     f"email={input('Enter your account email: ')}\n"
                     f"password={input('Enter your account password: ')}\n"
                     f"email_pass={input('Enter your email account password: ')}\n"
                     f"user_data_dir={input('Enter a path for the browser profile: ')}\n")
    config_path.write_text(text_settings)

config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
email = config.get("settings", "email")
password = config.get("settings", "password")
email_pass = config.get("settings", "email_pass")
user_data_dir = config.get("settings", "user_data_dir")

# Initialize Quotex client
client = Quotex(email=email, password=password, email_pass=email_pass, user_data_dir=Path(user_data_dir))



client.set_account_mode("PRACTICE") # REAL or PRACTICE


async def trade(action: str, amount, asset: str, duration):
    connection = await connect(client)
    logger.debug('Connection established: %s', connection)
    if connection:   
        asset, asset_open = await check_asset(client,asset)
        if asset_open:
            print(f"OK: Asset {asset} está aberto.")
            status, buy_info = await client.buy(amount, asset, action, duration)  # Execute the buy operation
            logger.debug("Buy status: %s, Buy info: %s", status, buy_info)
            if status:
                print(colored(f"Buy successful: {buy_info}", "green"))
                win = await client.check_win(buy_info["id"])
                if win:
                    print(colored(f"Win:", "green"), client.get_profit())
                    return True
                else:
                    print(colored(f"Loss:", "red"), client.get_profit())
                    return False
                        
            else:
                print(colored(f"Buy failed: {buy_info}", "red"))



#asyncio.run(trade("call", 50, "EURUSD", 60)) #TEST RUN
