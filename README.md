## Help Me Continue Working on this project

# Telegram-Qxbroker-Bot

This project consists of two main Python scripts, `producer.py` and `consumer.py`, designed to monitor Telegram chats for binary options signals, validate these signals, and execute trades on a broker platform based on the signals received.

## This project uses pyquotex, here is a thanks to the creators, you can find it here, :
--  https://github.com/cleitonleonel/pyquotex 
## a special thanks to the creators of this api

## Description

`producer.py` monitors Telegram channels for trade signals and extracts crucial information for trading binary options. `consumer.py` takes these signals, validates them, and if they are correct, executes the trade at the specified time.

## Features

### Consumer.py

- **Signal Reception and Validation**: Listens for incoming trade signals from `producer.py` and validates them to ensure all required fields are correct and formatted properly.
- **Trade Execution**: Engages with the trading platform to execute trades based on validated signals.
- **Martingale Strategy**: Implements a martingale strategy if the initial trade does not win.
- **Wait Mechanism**: Waits until the exact time specified in the trade signal before executing the trade.

## Technical Setup

### Dependencies

- `termcolor`: Used for colorizing printed messages in the terminal.
- `json`: For parsing JSON data.
- `asyncio` and `socket`: For asynchronous operations and socket communications respectively.
- Custom modules: `trade`, `wait_until_time` for executing trades and managing trade timing.

### Configuration

1. **Consumer Socket**: Set up a socket listener on localhost at port 9999 to receive signals from `producer.py`.
2. **Broker Configuration**: Configure the `trade` function with your broker API credentials and trading parameters.

### Usage

1. **Start `consumer.py`**:
   - Upon launching, it will prompt you for:
     - Your Quotex username and password.
     - Your email address and password.
     - A folder path to store web data separately for organizational purposes.

2. **Start `producer.py`**:
   - You will be asked for your Telegram phone number.
   - After providing it, a verification token will be sent to your Telegram.
   - Enter the provided token in the script to establish a connection.
   - Note: The `entity_id` used in the script is specific to the group where the signals are sourced. It may not work with other groups.

## Note

Both scripts work together to monitor, validate, and act on trading signals in real-time, leveraging asynchronous operations to manage multiple signals efficiently.
