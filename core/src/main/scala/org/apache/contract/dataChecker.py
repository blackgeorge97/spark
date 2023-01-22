import web3
import sys

w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" } ], \"name\": \"addResultfromDriver\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"resultHash\", \"type\": \"int256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"addResultfromExec\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"checkData\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" } ], \"name\": \"returnAppStatus\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [], \"name\": \"returnTotalWorkers\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"id\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"returnWorkerUsage\", \"outputs\": [ { \"internalType\": \"string\", \"name\": \"\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0x3d7962e7f51CAcA2973318DBD264677EDfEb93A4', abi=abi)

tid = int(sys.argv[1])
appId = str(sys.argv[2])
stageId = int(sys.argv[3])

def main():
    try:
        (driverHash, execHash, resultHash) = c.caller().checkData(tid, appId, stageId)
        print("The codes are " + str(driverHash) + " " + str(execHash) + " " + resultHash)
        return 0
    except Exception as err:
        sys.stderr.write(f'Exception: {err}')
        return 1


if __name__ == "__main__":
    main()