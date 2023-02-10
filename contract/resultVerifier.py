import web3
import sys
import time
#In case the return value is -1, keep trying to get the result till MAX_RETRIES

w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.1:7545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" } ], \"name\": \"addResultfromDriver\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" }, { \"internalType\": \"int256\", \"name\": \"taskHash\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"resultHash\", \"type\": \"int256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"addResultfromExec\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"checkData\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" }, { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" }, { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" } ], \"name\": \"returnAppStatus\", \"outputs\": [ { \"internalType\": \"int256\", \"name\": \"\", \"type\": \"int256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [], \"name\": \"returnTotalWorkers\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"id\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"hostname\", \"type\": \"string\" } ], \"name\": \"returnWorkerUsage\", \"outputs\": [ { \"internalType\": \"string\", \"name\": \"\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"tid1\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"tid2\", \"type\": \"uint256\" }, { \"internalType\": \"string\", \"name\": \"appId\", \"type\": \"string\" }, { \"internalType\": \"uint256\", \"name\": \"stageId\", \"type\": \"uint256\" } ], \"name\": \"updatePostedTaskPair\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" } ]"
c = w3.eth.contract(address='0xcfDd3fFb7224c7E45E442FdA1C9E8C0A53175d79', abi=abi)


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
                    (driverHash1, execHash1, resultHash1, driver1, exec1) = c.caller().checkData(taskIndex1, appId, stage)
                    (driverHash2, execHash2, resultHash2, driver2, exec2) = c.caller().checkData(taskIndex2, appId, stage)
                    if (driver1 == False  or driver2 == False ):
                        res = -2
                        break
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
                print("The verification of app with app Id: " + str(appId) + " was unsuccessful, but there is not enought information to find error!")
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