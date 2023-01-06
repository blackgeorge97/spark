import web3
import sys

w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"resultHash\", \"type\": \"string\" } ], \"name\": \"addNewResult\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"name\": \"stageToHash\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"totalTasks\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"verifyStageResults\", \"outputs\": [ { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" } ], \"stateMutability\": \"view\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0x9cB4c8E7744D8fA7A9E1FB456F942c51471A1943', abi=abi)

tid = int(sys.argv[1])
stageId = int(sys.argv[2])
taskhash = int(sys.argv[3])
resultcode = int(sys.argv[4])

def main():
    try:
        #tx_hash = c.functions.addNewResult(tid, stageId, hashcode).transact({'from' : '0x0e18280FFcC85827fCbbCc9382308211e0fCf931'})
        #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("hashAdderExec successfull\n")
        return 0
    except Exception as err:
        sys.stderr.write(f'Exception: {err}')
        return 1

if __name__ == "__main__":
    main()