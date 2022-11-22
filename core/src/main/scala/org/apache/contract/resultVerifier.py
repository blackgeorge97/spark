import web3
import sys

w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"resultHash\", \"type\": \"string\" } ], \"name\": \"addNewResult\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"name\": \"stageToHash\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"totalTasks\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"verifyStageResults\", \"outputs\": [ { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" } ], \"stateMutability\": \"view\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0x9cB4c8E7744D8fA7A9E1FB456F942c51471A1943', abi=abi)

stageId = int(sys.argv[1])


def main():
    try:
        res1 = c.caller().verifyStageResults(stageId)
        print("Stage with stage Id: " + str(stageId) + " has verified result of " + str(res1) + "\n")
        return 0
    except Exception as err:
        sys.stderr.write(f'Exception: {err}')
        return 1


if __name__ == "__main__":
    main()