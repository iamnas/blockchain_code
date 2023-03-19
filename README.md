
//first install virtualenv
pip install virtualenv

virtualenv venv // to rename

/// to start venv 
source venv/bin/activate

pip install flask


to run 

python land_record_ledger.py

GET ALL RECORD
http://127.0.0.1:8080/get_chain

GET IS VALID

http://127.0.0.1:8080/is_valid


CREATE A BLOCK  POST
 payload 
    {
  "owner":"name",
  "Reg_no":"reg number"
}

http://127.0.0.1:8080/mine_block
