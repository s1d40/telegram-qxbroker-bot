# telegram-qxbroker-bot
 Python application to listen to telegram signal groups and automatically make operations in qxbroker
I'll update the README.md for your SignalBroker application to include the additional dependencies (`quotexpy`, `termcolor`, `shutup`) and emphasize the necessity for users to provide their Quotex broker access credentials directly in the `qxfunctions.py` script. Here is the enhanced README with these updates:

### Updated README.md for SignalBroker

---

# SignalBroker

SignalBroker is a Python application designed to automate trading by capturing trading signals from a specified Telegram group and executing trades based on these signals through the QX Broker API. The application consists of five main components:

1. **producer.py** - Listens to Telegram and captures signal messages from a specified group, then sends these signals to `consumer.py`.
2. **consumer.py** - Receives signals sent by `producer.py`, validates them, and if valid, calls `qxfunctions.py` to interact with the trading platform.
3. **qxfunctions.py** - Contains functions to interact with the QX Broker API, facilitating the execution of trades based on validated signals.
4. **singleton_decorator.py** - Implements a singleton pattern decorator to ensure that classes such as the API connection handler have only one instance throughout the application.
5. **my_connection.py** - Manages connections to the QX Broker API, ensuring robust and persistent communication for trading operations.

## Setup and Installation

### Environment

- **Development Environment**: Anaconda
- **Python Version**: 3.11.7
- **Tested on**: Windows 10

### Dependencies

Before you begin, ensure you have the required dependencies installed:

- Python 3.11.7+
- Telethon
- asyncio
- socket
- json
- quotexpy (for interaction with Quotex Broker API)
- termcolor (for colored console output)
- shutup (to suppress warnings)

Install the required Python libraries using pip:

```bash
pip install telethon quotexpy termcolor shutup
```

### Configuration

Create a `config.ini` file with your Telegram API credentials and phone number:

```ini
[credentials]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
phone = YOUR_PHONE_NUMBER
```

**Note:** Users need to provide their Quotex broker access credentials directly in the `qxfunctions.py` script.

#### Environment File Modifications

Modifications were needed in the Python environment files located at:

`C:\Users\User\AppData\Local\Programs\Python\Python39\Lib`

Specific changes include adjusting subprocess initiation settings by setting `shell=True` in the subprocess initialization to enable shell commands to be executed correctly within the Python environment.

Example change:
```python
# In subprocess.py, modify the Popen initialization as follows:
def __init__(self, args, bufsize=-1, ... , shell=False, ...):
    # Change shell=False to shell=True
```

## Components

### Producer.py

Responsible for monitoring Telegram channels for new trading signals and forwarding them via a socket connection.

**Usage:**

```bash
python producer.py
```

**TODOs:**
- Handle network exceptions and reconnection logic.
- Validate message formatting more robustly before attempting to parse.
- Improve robustness so it listens and parses messages from multiple groups, which might be formatted differently.

### Consumer.py

Receives and validates JSON serialized trading signals from `producer.py`. If the signals are valid, it triggers trading actions via `qxfunctions.py`.

**Usage:**

```bash
python consumer.py
```

**TODOs:**
- Implement detailed validation checks for each part of the signal.
- Manage incomplete data reception and ensure complete JSON parsing.
- Optimize connection to the API, addressing issues with frequent failed connections.
- Implement martingale strategies in case of loss.
- Set a stop-loss mechanism: if the bot incurs too many losses in a row, it will stop operations for the day and wait for the user's prompt to resume operations.

### QXFunctions.py

Handles direct interactions with the QX Broker API, sending trade commands based on validated signals.

**Usage:**

*Note: This script is typically not run independently but invoked by `consumer.py`.*

**TODOs:**
- Implement error handling for API interaction failures.
- Enhance security measures for sensitive information handling.
- Ensure secure handling of Quotex broker credentials.
- Add stop-loss
- Add Martingale Functionality

## Running the Application

To run SignalBroker, start `consumer.py` first to ensure it's ready to receive signals, then run `producer.py`:

```bash
# Terminal 1:
python consumer.py

# Terminal 2:
python producer.py
```

## Contributing

Contributions to SignalBroker are welcome. Please ensure you adhere to conventional Python coding standards and provide tests where applicable.

---

Help me continue to work on this application:
ETH: 0x594856Bc399E799edF4Ce57153a8305698156221
BTC: bc1qwv96wp0n4gxddq6pznurzy5t99s6hx0cw0q48m
Binance: 840308135
PIX: 75be39bb-e9c1-4335-80f7-375df4ca3ebf 