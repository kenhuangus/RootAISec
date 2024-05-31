from web3 import Web3, HTTPProvider
import os
import json

def get_web3():
    WEB3_PROVIDER = os.getenv('WEB3_PROVIDER', 'http://localhost:8545')
    return Web3(HTTPProvider(WEB3_PROVIDER))

def get_abi():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ABI_PATH = os.path.join(CURRENT_DIR, 'RootAISecToken.json')
    with open(ABI_PATH) as f:
        return json.load(f)

def get_contract_address():
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0xE648666A5FC8f04242004454fA93a0eBa5452a70')
    return Web3.toChecksumAddress(CONTRACT_ADDRESS) 

def get_contract():
    web3 = get_web3()
    contract_address = get_contract_address()
    contract_abi = get_abi()
    return web3.eth.contract(address=contract_address, abi=contract_abi)

def get_payer_account():
    PAYER_PRIVATE_KEY = os.getenv('PAYER_PRIVATE_KEY', None)
    web3 = get_web3()
    return web3.eth.account.privateKeyToAccount(PAYER_PRIVATE_KEY)

def reward_tokens(recipient, amount):
    web3 = get_web3()
    web3.eth.defaultAccount = get_payer_account().address
    contract = get_contract()
    tx_hash = contract.functions.rewardTokens(recipient, amount).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)
    return tx_receipt