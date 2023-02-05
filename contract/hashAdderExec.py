import web3
import sys

w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" } ], \"name\": \"addResultfromDriver\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"resultHash\", \"type\": \"int256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"addResultfromExec\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"checkData\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" }, { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" } ], \"name\": \"returnAppStatus\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [], \"name\": \"returnTotalWorkers\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"id\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"returnWorkerUsage\", \"outputs\": [ { \"internalType\": \"string\", \"name\": \"\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0xBc8e1084dBD6D882803394b7bb2758200F5Ef6bd', abi=abi)
#The next two lines should be replaced with a function two get the individual workers wallet address
#For now we get a ready address from Ganache
accountsArray = w3.eth.accounts
account = accountsArray[1]

tid = int(sys.argv[1])
appId = str(sys.argv[2])
stageId = int(sys.argv[3])
taskHash = int(sys.argv[4])
resultHash = int(sys.argv[5])
hostname = str(sys.argv[6])

def main():
    try:
        tx_hash = c.functions.addResultfromExec(tid, appId, stageId, taskHash, resultHash, hostname).transact({'from' : account})
        return 0
    except Exception as err:
        sys.stderr.write(f'Exception: {err}')
        return 1

if __name__ == "__main__":
    main()