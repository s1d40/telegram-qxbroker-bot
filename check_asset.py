import logging
from termcolor import colored
from asset_parse import asset_parse


async def check_asset(client, asset):
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