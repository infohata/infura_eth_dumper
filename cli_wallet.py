from typing import Any
from web3 import Web3, exceptions as exceptions_web3
import json, requests
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
    help_dict = {}
    if len(args) == 0:
        print("List of commands and their usage. Arguments in [square brackets] are optional:")
        print("exit: close this program")
        print("list: print managed address list with their IDs")
        print("add: add an address")
        print("remove ID: remove specified address")
        print("save [wallet.json]: save addresses to a json file")
        print("load [wallet.json]: load addresses from a json file")
        print("balance ID: check balance of an address")
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
    float_balance = int(raw_balance) / 10 ** 18
    print(float_balance)
    return addresses

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
