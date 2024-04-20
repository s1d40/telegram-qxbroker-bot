import asyncio
import socket
import json  # Import json for serialization
from telethon import TelegramClient, events

api_id = YOUR_API_KEY
api_hash = YOUR_API_HASH
phone = YOUR_PHONE_NUMBER

client = TelegramClient('session_name', api_id, api_hash)

# Setup socket for IPC
producer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
producer_socket.connect(('localhost', 9999))  # Connect to consumer script listening on port 9999

async def start_telegram_client():
    await client.start()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the verification code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

@client.on(events.NewMessage(chats=1775614507)) # magicos vip 1775614507 #test channel 7033220336
async def handle_new_message(event):
    message_text = event.message.message
    if 'CALL' in message_text or 'PUT' in message_text:
        signal = parse_signal(message_text)
        if signal:
            # Convert the dictionary to a JSON string
            signal_json = json.dumps(signal)
            # Send this JSON string over the socket
            producer_socket.sendall(signal_json.encode('utf-8'))

def parse_signal(message):
    try:
        entry_type = 'CALL' if 'CALL' in message else 'PUT'
        parts = message.split(';')
        if len(parts) > 1:
            time_part = parts[1].strip()
            section = parts[0].split("\n")
            expiration = section[0].strip()
            pair = section[1].strip().replace('/', '')  # Remove '/' from the currency pair
            if "1 minuto" in expiration:
                expiration = "1 min"
            elif "5 minutos" in expiration:
                expiration = '5 min'
            return {"expiration": expiration, "pair": pair, "time": time_part, "entry_type": entry_type}
    except Exception as e:
        print(f"Error parsing message: {e}")
    return None

async def main():
    await start_telegram_client()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())