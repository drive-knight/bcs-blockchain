import hashlib
import time
import json
import requests
import datetime

from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.encoding.hexbytes import h2b
from pycoin.coins.tx_utils import create_tx
from pycoin.solve.utils import build_hash160_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator

IP = "45.32.232.25"
PORT = "3669"
RPCUSER = "bcs_tester"
RPCPASSWORD = "iLoveBCS"
ADDRESS = "BGyeo1SimmrFL2TLn4h4RHSF8j7RJQewJo"
PRIVATE_KEY = "KzvAhiGUrfHpYJfGruQbE6vvynyiXFNV7GFCqNsnYxbNUTx35Xod"
ONE_COIN = 100000000
FEE = 10000000


def get_address():
    data = {
        "method": "getnewaddress"
    }
    new_address = requests.post(url=f"http://{RPCUSER}:{RPCPASSWORD}@{IP}:{PORT}", json=data)
    return new_address.json()['result']


def method_of_sending(txhash=None):
    data = json.dumps({
        "method": "sendrawtransaction",
        "params": txhash
    })
    response = requests.post(url=f"http://{RPCUSER}:{RPCPASSWORD}@{IP}:{PORT}", data=data)
    return response


network = create_bitcoinish_network(symbol='BCS', network_name='BCSChain', subnet_name='',
                                    wif_prefix_hex="80", address_prefix_hex="19",
                                    pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
                                    bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
                                    bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
                                    bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666)


def get_spendables(my_address):
    resp = requests.get(f'https://bcschain.info/api/address/{my_address}/utxo')
    utxo = json.loads(resp.content)[0]
    spendables = Spendable(coin_value=int(utxo['value']), script=h2b(utxo['scriptPubKey']),
                           tx_hash=h2b(utxo['transactionId'])[::-1],
                           tx_out_index=int(utxo['outputIndex']))
    return spendables


def send_transaction():
    new_address = get_address()
    spendables = get_spendables(ADDRESS)
    calculate_commission = int(spendables.coin_value - (FEE + ONE_COIN))
    tx = create_tx(network=network, spendables=[spendables],
                   payables=[(new_address, ONE_COIN), (ADDRESS, calculate_commission)])

    wif = network.parse.wif(PRIVATE_KEY)
    secret_exponent = wif.secret_exponent()
    solver_hash = build_hash160_lookup([secret_exponent], [secp256k1_generator])

    sign_tx = tx.sign(solver_hash)
    sign_tx_hash = sign_tx.as_hex()
    transaction = method_of_sending([sign_tx_hash])
    return transaction.json()

