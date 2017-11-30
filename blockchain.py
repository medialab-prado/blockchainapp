import datetime
import hashlib as hasher
import json


class Block:
    def __init__(self, index, timestamp, data, previous_hash, proof_of_work):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block(index, timestamp, data, previous_hash, proof_of_work)
        self.proof_of_work = proof_of_work

    def hash_block(self, index, timestamp, data, previous_hash, proof_of_work):
        sha = hasher.sha256()
        sha.update(str(index).encode('utf-8') +
                   str(timestamp).encode('utf-8') +
                   str(data).encode('utf-8') +
                   str(previous_hash).encode('utf-8')+
                   str(proof_of_work).encode('utf-8')
        )
        return sha.hexdigest()

    def __repr__(self):
        return "Block({},{},{},{},{})".format(repr(self.index),
                                           repr(self.timestamp),
                                           repr(self.data),
                                           repr(self.previous_hash),
                                           repr(self.proof_of_work))

    def __str__(self):
        strTimeStamp = str(self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        return json.dumps({"index": repr(self.index),
                           "timestamp": strTimeStamp,
                           "data": self.data,
                           "hash": str(self.previous_hash),
                           "proof_of_work": self.proof_of_work})

    def toJson(self):
        return str(self)


class BlockChain:
    import json
    import datetime

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.previous_block = self.chain[-1]

    def __str__(self):
        return json.dumps(self.chain)

    def __len__(self):
        return len(self.chain)

    def toJson(self):
        return json.dumps(self.chain)

    def create_genesis_block(self):
        return json.loads(Block(0, datetime.datetime.now(),
                                "Genesis Block", "0", 1).toJson())

    def next_block(self, data):
        index = int(self.previous_block['index']) + 1
        timestamp = datetime.datetime.now()
        return Block(index, timestamp, data,
                     self.previous_block['hash'], data['proof_of_work'])

    def add_block(self, data):
        if not isinstance(data, dict):
            return
        self.chain.append(json.loads(self.next_block(data).toJson()))
        self.previous_block = self.chain[-1]
