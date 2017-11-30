import requests
from time import sleep
from blockchain import BlockChain
from flask import Flask
from flask import request
import json
import threading

bc = BlockChain()
node = Flask(__name__)

this_nodes_transactions = []
peer_nodes = ['http://192.168.1.195:5000']


# TXN:
# { 'from': 'id',
#   'to' : 'id_to',
#   'amount': int
# }
# 
@node.route('/txn', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txn = request.get_json()
        print(request)
        print(request.get_json())

        if new_txn is not None:
            this_nodes_transactions.append(new_txn)
        print("### New Transaction ###")
        print("FROM: {}".format(new_txn['from']))
        print("TO: {}".format(new_txn['to']))
        print("\n")
    return "OK"


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"


def proof_of_work(last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
        # Once that number is found,
        # we can return it as a proof
        # of our work
    return incrementor


@node.route('/mine', methods=['GET'])
def mine():
    global this_nodes_transactions
    last_block = bc.previous_block
    last_proof = last_block['proof_of_work']
    proof = proof_of_work(last_proof)

    this_nodes_transactions.append(
        {"from": "networkd", "to": miner_address, "amount": 1}
    )

    new_block_data = {
        "proof_of_work": proof,
        "transactions": list(this_nodes_transactions)
    }

    this_nodes_transactions = []
    bc.add_block(new_block_data)
    return json.dumps(bc.previous_block)


@node.route('/blocks', methods=['GET'])
def get_blocks():
    return bc.toJson()


def find_new_chains(peer_nodes):
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + '/blocks').content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains


def consensus(peer_nodes):
    other_chains = find_new_chains(peer_nodes)
    longest_chain = bc
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    return longest_chain


def server_run():
    node.run(host='0.0.0.0')


def main():
    thread = threading.Thread(target=server_run, args=())
    thread.daemon = True
    thread.start()


def make_transaction():
    txn = {}
    txn['from'] = str(input("Your id: "))
    txn['to'] = str(input("To: "))
    txn['amount'] = int(input("Amount: "))
    requests.post('localhost:5000/txn', data=txn)


def test():
    main()
    sleep(2)
    print("Some transactions:")
    txn = {'from': 'ignaciobll', 'to': 'smone', 'amount': 3}
    for i in range(1, 3):
        requests.post(url='http://localhost:5000/txn', json=txn)
        requests.get(url='http://localhost:5000/mine')
