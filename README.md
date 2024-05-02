# Infura ETH dumper
Simple bot using Infura API to keep configured ethereum wallet(s) emptied to target address

## Instructions
Create a .env file with the following configuraition

### Setup Python

Create a Python virtual environment

```bash
python3 -m venv venv
```

Activate virutal environment

in Linux/MacOS:

```bash
source venv/bin/activate
```

in Windows:

```cmd
venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

### Configure Infura API

```env
INFURA_API_KEY = 'Your Infura API key'
INFURA_NETWORK = 'mainnet' # Network identifier, you should first try with 'sepolia'
```

You can get Infura API key [here](https://app.infura.io/): 

### Configure bot wallet

* Run `python cli_wallet.py`
* Use commands `add` to add two addresses. The address for destination does not require private key, Checking address does.
* Use `save` command to save entered addresses to `wallet.json` file.
* You can check the wallet with `list` command. If you have added the destination address first, it should have ID 0. Checking account then would have ID 1.
* You can use `balance` command with arguments of either address ID to check the balance of these addresses. It should work if Infura API is configured correctly.
* Open with your favorite text editor `bot_config.py` and check if all is in order. Most important are IDs. Accumulated threshold is the amount which triggers the transfer out. If you increase fees for gas, make sure to leave enough for gas bidding.

```Python
WALLET_FILENAME = 'wallet.json'
DESTINATION_WALLET_ID = 0   # does not need private key
CHECK_WALLET_ID = 1         # needs private key
CHECK_INTERVAL = 30         # in seconds
LEAVE_FOR_FEES = 0.001          # in ETH
ACCUMULATED_THRESHOLD = 0.01    # in ETH
MAX_FEE = 10                    # in Gwei
PRIORITY_FEE = 0.1              # in Gwei
``` 

* run `python auto_withdraw.py`, check the configuration on screen, press ENTER and let it run...

## DISCLAIMER

This bot is not idiot proof. Making errors in configuration may result in epic failure. I do not take responsibility for the function of the bot, the wallet or the code in general.
