from typing import Any
from web3 import Web3, exceptions as exceptions_web3
from eth_account.datastructures import SignedTransaction
import json
import infura

addresses = []
web3 = Web3(Web3.HTTPProvider(infura.url))

ERROR_ID_VALUE = "ERROR: ID must be a number."
ERROR_ID_INDEX = "ERROR: you must provide a correct address ID as an argument. If not sure, list addresses first."

def get_eth_address(address: str):
    try:
        verified_account = web3.to_checksum_address(address)
    except exceptions_web3.InvalidAddress:
        print(f"Invalid ETH address: {address}")
        return None
    else:
        return verified_account

def help(args: list[str]) -> None:
    help_dict = {
        'transfer': """
    Transfer default network tokens from one account to another. Arguments are separated by spaces. 
    Accounts must be loaded into the list. Receiving account private key is not required. Sender's is required.
    Arguments:
        from - sender's account ID from the list, from which tokens will be sent
        to - recipient's account ID from the list
        value - amount of tokens to be sent
        max fee - optional maximum amount of Gwei for transaction fee. Default is 200 Gwei.
        priority fee - optional maximum amount of Gwei for transaction priority. Default is 1 Gwei.
    The transaction ID will be printed if transaction is successful.
"""
    }
    if len(args) == 0:
        print("List of commands and their usage. Arguments in [square brackets] are optional:")
        print("exit: close this program")
        print("list: print managed address list with their IDs")
        print("add: add an address")
        print("remove ID: remove specified address")
        print("save [wallet.json]: save addresses to a json file")
        print("load [wallet.json]: load addresses from a json file")
        print("balance ID: check balance of an address")
        print("transfer FROM_ID TO_ID value [max_fee] [priority_fee]: transfer value from address to another")
        print("gas: check gas price of the network")
    elif args[0] in help_dict:
        print(help_dict[args[0]])
    else:
        print(f"The command {args[0]} is invalid or there is nothing more to say about it.")

def add(addresses: list[Any] = addresses) -> list[Any]:
    new_address = {
        "address": input("Address:"),
        "pk": input("Private Key:"),
    }
    if get_eth_address(new_address['address']):
        addresses.append(new_address)
        print(f"address {addresses[-1]['address']} added to the wallet with id:{len(addresses)-1}.")
    return addresses

def remove(id: int, addresses: list[Any] = addresses) -> list[Any]:
    removed = addresses.pop(id)
    print(f"address {removed['address']} was removed from the wallet.")
    return addresses

def list_addresses(addresses: list[Any] = addresses) -> None:
    print("Managed Addresses by this wallet:")
    print(f"{'ID':^5} | Address")
    for id, address in enumerate(addresses):
        print(f"{id:>5} | {address['address']}")

def save(filename: str, addresses: list[Any]) -> None:
    with open(filename, "w") as json_file:
        json.dump(addresses, json_file)
    print(f"{len(addresses)} addresses saved into {filename}.")

def load(filename: str) -> list[Any]:
    with open(filename, "r") as json_file:
        file_contents = json.load(json_file)
    print(f"{len(file_contents)} addresses loaded from {filename}.")
    return file_contents

def balance(id: int, addresses: list[Any] = addresses) -> list[Any]:
    account = get_eth_address(addresses[id]['address'])
    raw_balance = web3.eth.get_balance(account)
    float_balance = int(raw_balance) / (10 ** 18)
    addresses[id]['balance'] = float_balance
    print(f"The balance of {account} is {float_balance} coins.")
    return addresses

def transfer(
        from_id: int, 
        to_id: int, 
        value: float, 
        max_fee: float = 200.0, 
        priority_fee: float = 1.0, 
        addresses: list[Any] = addresses
    ) -> None:
    from_account = get_eth_address(addresses[from_id]['address'])
    to_account = get_eth_address(addresses[to_id]['address'])
    nonce = web3.eth.get_transaction_count(from_account)
    transaction = {
        'type': '0x2',
        'nonce': nonce,
        'from': from_account,
        'to': to_account,
        'value': web3.to_wei(value, 'ether'),
        'maxFeePerGas': web3.to_wei(max_fee, 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei(priority_fee, 'gwei'),
        'chainId': web3.eth.chain_id,
    }
    try:
        transaction['gas'] = web3.eth.estimate_gas(transaction)
        signed_transaction:SignedTransaction = web3.eth.account.sign_transaction(transaction, addresses[from_id]['pk'])
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    except Exception as error:
        print(f"Transaction Error: {error}")
    else:
        print(f"Sent {value} from {from_account} to {to_account}, gas limit: {transaction['gas']}, transaction hash: {transaction_hash.hex()}")

def get_gas() -> float:
    print(f'Gas price: {web3.eth.gas_price / (10 ** 18):0.12f}')
    return web3.eth.gas_price

if __name__ == "__main__":
    print("---[ Basic ETH Command Line Interface Wallet ]---")
    print("(C) 2024 Kestutis Januskevicius, github.com/infohata")
    print("type help[ENTER] for instructions.")
    while True:
        user_input = input(":").split(" ")
        command = user_input[0].casefold()
        if len(user_input) > 1:
            args = user_input[1:]
        else:
            args = []
        if command == "exit":
            print("bye!")
            break
        if command == "help":
            help(args)
        if command == "list":
            list_addresses(addresses)
        if command == "add":
            addresses = add(addresses)
        if command == "remove":
            try:
                id = int(args[0])
                addresses = remove(id, addresses)
            except ValueError:
                print(ERROR_ID_VALUE)
            except IndexError:
                print(ERROR_ID_INDEX)
        if command == "save":
            filename = args[0] if len(args) > 0 else "wallet.json"
            try:
                save(filename, addresses)
            except Exception as error:
                print(f"ERROR {error.__class__.__name__}: {error}")
        if command == "load":
            filename = args[0] if len(args) > 0 else "wallet.json"
            try:
                addresses = load(filename)
            except Exception as error:
                print(f"ERROR {error.__class__.__name__}: {error}")
        if command == "balance":
            try:
                id = int(args[0])
                addresses = balance(id, addresses)
            except ValueError:
                print(ERROR_ID_VALUE)
            except IndexError:
                print(ERROR_ID_INDEX)
        if command == "transfer":
            try:
                from_id = int(args[0])
                to_id = int(args[1])
                value = float(args[2])
                max_fee = float(args[3]) if len(args) > 3 else 200.0
                priority_fee = float(args[4]) if len(args) > 4 else 1.0
                addresses = transfer(from_id, to_id, value, max_fee, priority_fee, addresses)
            except Exception as error:
                print(error)
        if command == "gas":
            get_gas()
