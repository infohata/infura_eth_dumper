from time import sleep
import cli_wallet, bot_config
from datetime import datetime

addresses = cli_wallet.load("wallet.json")

print("---[ ETH Auto Withdrawal Bot ]---")
print("(C) 2024 Kestutis Januskevicius, github.com/infohata")
print(f"This bot will be checking every {bot_config.CHECK_INTERVAL} seconds")
print(f"the {addresses[bot_config.CHECK_WALLET_ID]['address']} address.")
print(f"When there are more than {bot_config.ACCUMULATED_THRESHOLD} coins")
print(f"all but {bot_config.LEAVE_FOR_FEES} will be transferred")
print(f"to {addresses[bot_config.DESTINATION_WALLET_ID]['address']} address.")
print("This bot will work indefinitely until interrupted with CTRL+C.")
abort = input("""Press ENTER to start. If something above is not correct:
      press CTRL+C now and go fix the bot_config.py file.""")
while abort == '':
    print(f"Now is: {datetime.now()}. Checking for balance...")
    addresses = cli_wallet.balance(bot_config.CHECK_WALLET_ID, addresses)
    if addresses[bot_config.CHECK_WALLET_ID]['balance'] >= bot_config.ACCUMULATED_THRESHOLD:
        amount = addresses[bot_config.CHECK_WALLET_ID]['balance'] - bot_config.LEAVE_FOR_FEES
        max_fee = bot_config.MAX_FEE if bot_config.MAX_FEE and bot_config.MAX_FEE >= 0.1 else 10
        priority_fee = bot_config.PRIORITY_FEE if bot_config.PRIORITY_FEE and bot_config.PRIORITY_FEE >= 0.1 else 0.1
        print(f"Tranfering {amount} to {addresses[bot_config.DESTINATION_WALLET_ID]['address']}...")
        print(f"    max fee: {max_fee} Gwei, priority fee: {priority_fee} Gwei")
        cli_wallet.transfer(
            bot_config.CHECK_WALLET_ID,
            bot_config.DESTINATION_WALLET_ID,
            amount,
            max_fee,
            priority_fee,
            addresses,
        )
    sleep(bot_config.CHECK_INTERVAL)
