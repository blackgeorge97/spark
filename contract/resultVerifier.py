import web3
import sys
import time
#In case the return value is -1, keep trying to get the result till MAX_RETRIES

w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" } ], \"name\": \"addResultfromDriver\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"resultHash\", \"type\": \"int256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"addResultfromExec\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"checkData\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" }, { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" } ], \"name\": \"returnAppStatus\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [], \"name\": \"returnTotalWorkers\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"id\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"returnWorkerUsage\", \"outputs\": [ { \"internalType\": \"string\", \"name\": \"\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid1\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"tid2\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"updatePostedTaskPair\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0x0F0D441C461d6ac36eDe6134dd64bB2C02d9e432', abi=abi)
#The next two lines should be replaced with a function two get the individual workers wallet address
#For now we get a ready address from Ganache
accountsArray = w3.eth.accounts
account = accountsArray[0]

def main():
    if (len(sys.argv) < 2):
        print("Please provide app file for Verification.")
        return 1
    elif (len(sys.argv) == 2):
        path = sys.argv[1]
        ver_method = 0
    else:
        path = sys.argv[1]
        ver_method = int(sys.argv[2])

    try:
        with open(path , 'r') as file:
            appId = file.readline().strip()
            if (ver_method == 0):
                res = c.caller().returnAppStatus(appId)
            else:
                res = 0
                for line in file:
                    if (res != 0):
                        break
                    stage = int(line.split()[0])
                    taskIndex1 = int(line.split()[1])
                    taskIndex2 = int(line.split()[2])
                    hash1 = int(line.split()[3])
                    hash2 = int(line.split()[4])
                    if (ver_method == 2):
                        try:
                            tx_hash = c.functions.updatePostedTaskPair(taskIndex1, taskIndex2, hash1, hash2, appId, stage).transact({'from' : account})
                        except Exception as err:
                            sys.stderr.write(f'Exception: {err}')
                    (driverHash1, execHash1, resultHash1, posted1, exec1) = c.caller().checkData(taskIndex1, appId, stage)
                    (driverHash2, execHash2, resultHash2, posted2, exec2) = c.caller().checkData(taskIndex2, appId, stage)
                    if (posted1 == False or posted2 == False):
                        print("To verify data of smart contract please post tasks.")
                    if (exec1 == False or exec2 == False):
                        res = -1
                        break
                    if (resultHash1 != resultHash2) :
                        res = 1
                        if (execHash1 != execHash2):
                            if (driverHash1 == execHash1 and driverHash2 == execHash2):
                                res = 2
                            else:
                                res = 3
                        break
            if res == 0:
                print("The verification of app with app Id: " + str(appId) + " was successful!\n")
            elif res == -2:
                print("The verification of app with app Id: " + str(appId) + " was unsuccessful because client didnt send tasks!\n")   
            elif res == -1:
                print("The verification of app with app Id: " + str(appId) + " was unsuccessful because worker didnt send tasks!\n")
            elif res == 1:
                print("The verification of app with app Id: " + str(appId) + " was unsuccessful because of worker's fault!")
            elif res == 2:
                print("The verification of app with app Id: " + str(appId) + " was unsuccessful because of client's fault!")
            elif res == 3:
                print("The verification of app with app Id: " + str(appId) + " failed because client sent wrong hash to executor!")
        workersNum = c.caller().returnTotalWorkers()
        for i in range(1, workersNum + 1):
            (host, res) =  c.caller().returnWorkerUsage(i, "")
            print("Worker with Hostname: " + host + " has usage percentage of " + str(res) + "%\n")
        return 0
    except Exception as err:
        sys.stderr.write(f'Exception: {err}')
        return 1


if __name__ == "__main__":
    main()