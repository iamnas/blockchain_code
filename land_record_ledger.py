

import datetime
import hashlib
import json
from flask import Flask,jsonify,request


class Blockchain:

    #  constructor 
    def __init__(self):
        self.chain = []
        #  index timestamp proof ownername reg_no previous_hash
        self.create_block(owner='creator',Reg_no = '001',proof=0,previous_hash = '0')
    
    def create_block(self,owner,Reg_no,proof,previous_hash):
        block = {
            'owner':owner,
            'Reg_no':Reg_no,
            'index': len(self.chain)+1,
            'timestamp':str(datetime.datetime.now()),
            'proof':proof,
            'previous_hash':previous_hash
        }

        self.chain.append(block)
        return block
    
    def proof_of_work(self,previous_proof):

        new_proof = 1 
        check_proof = False

        while check_proof is False :
            hash_val = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode() ).hexdigest()

            if hash_val[:4] == '0000':
                check_proof = True
            else:
                new_proof +=1
        return new_proof
    

    def hash(self,block):
        encoded_block = json.dumps(block).encode()

        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain) :
        previous_block = chain[0]
        block_idx = 1

        while block_idx < len(chain):
            block = chain[block_idx]
            if block['previous_block'] != self.hash(previous_block) :
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            
            hash_val = hashlib.sha256(str(proof**2 - previous_proof**2).encode() ).hexdigest()

            if hash_val[:4] != '0000':
                return False
            previous_block = block
            block_idx = block_idx + 1

        return True
    
    def get_last_block(self):
        return self.chain[-1]
    


# creating the web app


app = Flask(__name__)

blockchain = Blockchain()

@app.route('/') 
def welcome():

    return '<p>hello</p>'

@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response),200


@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)

    if is_valid:
        response = {"message": "The leager is a valid chain"}
    else :
        response = {"message": "The leager is not a valid chain"}
    return jsonify(response),200

@app.route('/mine_block',methods=['POST'])
def mine_block():
    values = request.get_json()

    required = ['owner','Reg_no']

    if not all(k in values for k in required):
        return 'Missing values',400
    
    owner = values['owner']
    Reg_no = values['Reg_no']
    previous_block = blockchain.get_last_block()
    previous_proof =  previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(owner,Reg_no,proof,previous_hash)

    response = {'message':'record will added to the ledger'}

    return jsonify(response),200

app.run(host='0.0.0.0',port=8080,debug=True)


