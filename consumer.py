import socket
import json
from datetime import datetime
import qxfunctions
import asyncio

def preprocess_and_validate_signal(signal):
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

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as consumer_socket:
        consumer_socket.bind(('localhost', 9999))
        consumer_socket.listen(1)
        print("Waiting for connection on port 9999...")
        connection, client_address = consumer_socket.accept()
        print(f"Connected to {client_address}")

        try:
            buffer = ""
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8')

                # Print the buffer before attempting to parse it as JSON
                print("Buffer before JSON parsing:", buffer)

                try:
                    signal = json.loads(buffer)
                    print("Received signal:", signal)
                    buffer = ""  # Reset buffer after successful parse

                    valid, processed_signal = preprocess_and_validate_signal(signal)
                    if valid:
                        print("Valid signal received. Processing...")
                        print("Processed Signal:", processed_signal)
                        # Here you could add your logic to act on the validated signal
                        asyncio.get_event_loop().run_until_complete(qxfunctions.main(processed_signal))
                    else:
                        print("Invalid signal received. Ignoring...")

                except json.JSONDecodeError:
                    print("Failed to decode JSON, waiting for more data...")
                    continue  # Continue receiving data if JSON is incomplete

        finally:
            connection.close()

if __name__ == "__main__":
    main()
