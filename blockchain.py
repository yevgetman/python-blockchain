import hashlib, json, time

class Block():
    
    def __init__(self, index, transactions, timestamp, last_block_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.last_block_hash = last_block_hash
        self.nonce = nonce
        self.hash = None

    def generate_hash(self):
        strToHash = json.dumps(self.__dict__, sort_keys=True) # all the properties of Block as a JSON string
        return hashlib.sha256(strToHash.encode()).hexdigest()

class Blockchain():

    def __init__(self, difficulty=3):
        self.chain = []
        self.unconfirmed_transactions = []
        self.difficulty = difficulty # number of leading zero in hash generated from block with a given nonce value
        self.create_genesis_block()

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block, proof):
        # validate and add block to blockchain
        if(self.validate_block(block, proof) == False): return False
        block.hash = proof
        self.chain.append(block)
        return True

    def validate_block(self, block, proof):
        # block must have hash of last block
        if self.getLastBlock().hash != block.last_block_hash:
            return False
        # proof must have the correct difficulty
        # proof must match hash generated from current block, which will include nonce value if proof is valid
        return proof.startswith('0' * self.difficulty) and proof == block.generate_hash()

    def add_transactions(self,transactions):
        self.unconfirmed_transactions += transactions
    
    def clear_transactions(self):
        self.unconfirmed_transactions = []

    def create_genesis_block(self):
        # create the first block
        block = Block(0, [], time.time(), "Chancellor on the brink..")
        block.hash = block.generate_hash()
        self.chain.append(block)

    def proof_of_work(self, block, verbose=False):
        # compute the nonce value by incrementing nonce and hashing block with until valid hash with indicated difficuly is found
        computed_hash = block.generate_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.generate_hash()
        if(verbose):
            print("\nnonce with difficulty " + str(self.difficulty) + " found after " + str(block.nonce) + " iterations!")
        return computed_hash

    def mine(self, verbose=False):
        # create a new block from all unconfirmed transactions

        if(len(self.unconfirmed_transactions) == 0): 
            if(verbose == True):
                print("\nNo unconfirmed transactions.")
            return False

        # create a new block
        new_block = Block(
            index=self.getLastBlock().index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
            last_block_hash=self.getLastBlock().hash)

        # generate a proof of work
        proof = self.proof_of_work(new_block, verbose)

        # attempt to add the new block (proof may not be valid)
        if(self.addBlock(new_block, proof) == True):
            self.clear_transactions()
            if(verbose == True): 
                print("\nblock #" + str(new_block.index) + " added successfully!")
            return True
        else: return False


# initialize the blockchain with a genesis block
blockchain = Blockchain()

# add come transactions to be added to a block
transactions = ['fds','sdasdasd','sdasdasda','asdasdasda','juhytgdrs','htrge4scsx','egr4feads','y6rtegfed']
blockchain.add_transactions(transactions)

blockchain.mine(verbose=True)

print("\nblockchain:")
for block in blockchain.chain:
    print(block.index, block.timestamp, block.hash)
