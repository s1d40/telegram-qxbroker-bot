import socket
import json
import asyncio
from trade import trade
from termcolor import colored
from wait_until_time import wait_until_time

async def preprocess_and_validate_signal(signal):
    """
    Preprocesses the signal by removing '/' from the pair and validates the required fields.
    Directly passes hours and minutes from the signal without calculating wait seconds.
    """
    try:
        # Preprocess pair: Remove '/' and ensure it's not empty
        if '/' in signal['pair']:
            signal['pair'] = signal['pair'].replace('/', '')
        if not signal['pair']:
            print("Invalid pair:", signal['pair'])
            return False, None

        # Validate time: Ensure it's in HH:MM format
        hours, minutes = map(int, signal['time'].split(':'))
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            print("Invalid time:", signal['time'])
            return False, None

        # Validate expiration: Must be a proper minute format and one of the expected values
        if signal['expiration'] not in ['1 min', '5 min']:
            print("Invalid expiration:", signal['expiration'])
            return False, None

        # Validate entry_type: Must be 'CALL' or 'PUT'
        if signal['entry_type'] not in ['CALL', 'PUT']:
            print("Invalid entry type:", signal['entry_type'])
            return False, None

        return True, signal
    except Exception as e:
        print(f"Error during signal validation: {e}")
        return False, None

async def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as consumer_socket:
        consumer_socket.bind(('localhost', 9999))
        consumer_socket.listen(1)
        print(colored("Waiting for connection on port 9999...", "cyan"))
        connection, client_address = consumer_socket.accept()
        print(colored(f"Connected to {client_address}", "green"))

        try:
            buffer = ""
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8')

                # Print the buffer before attempting to parse it as JSON
                print(colored("Buffer before JSON parsing: " + buffer, "yellow"))

                try:
                    signal = json.loads(buffer)
                    print(colored("Received signal: " + json.dumps(signal, indent=2), "magenta"))
                    buffer = ""  # Reset buffer after successful parse

                    valid, processed_signal = await preprocess_and_validate_signal(signal)
                    if valid:
                        action_color = "green" if signal['entry_type'] == 'CALL' else "red"
                        print(colored("Valid signal received. Processing...", "blue"))
                        print(colored(f"Processed Signal: {processed_signal}", action_color))
                        # Call trade_and_check_win from qxfunctions
                        _duration = 300 if signal['expiration'] == '5 min' else 60
                        _action = signal["entry_type"].lower()
                        _amount = 50
                        _asset = signal["pair"]
                        
                        
                        
                        on_time = await wait_until_time(signal['time'])
                        
                        
                        if on_time:
                            win = await trade(
                                duration=_duration,
                                action=_action,
                                amount = _amount,
                                asset=_asset
                            )
                            if not win:
                                print(colored("Entering First Martingale"), "yellow")
                                win = await trade(
                                    duration=_duration,
                                    action=_action,
                                    amount = _amount*2,
                                    asset=_asset
                                )
                                if not win:
                                    print(colored("Entering Second Martingale"), "yellow")
                                    win = await trade(
                                        duration=_duration,
                                        action=_action,
                                        amount = _amount*4,
                                        asset=_asset
                                )
                        print(colored("Consumer [INFO]: Sleeping for 5 seconds...", "blue"))
                        await asyncio.sleep(5)
                    else:
                        print(colored("Invalid signal received. Ignoring...", "red"))
                        buffer = ''

                except json.JSONDecodeError:
                    print(colored("Failed to decode JSON, waiting for more data...", "red"))
                    buffer = ''
                    continue  # Continue receiving data if JSON is incomplete

        finally:
            connection.close()

if __name__ == "__main__":
    asyncio.run(main())