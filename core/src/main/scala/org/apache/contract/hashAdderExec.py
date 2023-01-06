import web3
import sys

w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" } ], \"name\": \"addResultfromDriver\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"resultHash\", \"type\": \"int256\" } ], \"name\": \"addResultfromExec\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"name\": \"stageToDriverTaskHash\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"totalTasks\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"name\": \"stageToExecTaskHash\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"totalTasks\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"name\": \"stageToResultHash\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"totalTasks\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"verifyStageResults\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0xE0C357659a47257c6eF75F87D98aFC09b3cC52Ab', abi=abi)

tid = int(sys.argv[1])
stageId = int(sys.argv[2])
taskHash = int(sys.argv[3])
resultHash = int(sys.argv[4])

def main():
    try:
        tx_hash = c.functions.addResultfromExec(tid, stageId, taskHash, resultHash).transact({'from' : '0x4d92C5e5900455B82966162eb3AFdB021261f31b'})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return 0
    except Exception as err:
        sys.stderr.write(f'Exception: {err}')
        return 1

if __name__ == "__main__":
    main()