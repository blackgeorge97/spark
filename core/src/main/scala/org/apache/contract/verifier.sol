pragma solidity ^0.8.0;


library Library {
    struct taskData{
        int driverTaskHash;
        int execTaskHash;
        int resultHash;
        bool driver;
        bool exec;
    }
    struct taskSet{
        mapping(uint => taskData) task;
    }
    struct stages{
        mapping(uint => taskSet) stage;
        int status;
        uint driverTasks;
        uint execTasks;
    }
}

contract sparkVerifier {

    mapping(string => Library.stages) private app;

    mapping(uint => string) private idToHostname;
    mapping(string => uint) private hostnameToId;
    mapping(uint => uint) private idToCount;
    uint totalWorkers = 0;
    uint totaltasks = 0;


    function verifyPair(string memory appId, uint stageId, uint tid1, uint tid2) private view returns (int){
        int status = 0;
        if (app[appId].stage[stageId].task[tid1].resultHash != app[appId].stage[stageId].task[tid2].resultHash){
            status = 1;
            if (app[appId].stage[stageId].task[tid1].execTaskHash != app[appId].stage[stageId].task[tid2].execTaskHash){
                if (app[appId].stage[stageId].task[tid1].execTaskHash == app[appId].stage[stageId].task[tid1].driverTaskHash &&
                app[appId].stage[stageId].task[tid2].execTaskHash == app[appId].stage[stageId].task[tid2].driverTaskHash){
                    status = 2;
                }
                else {
                    status = 3;
                }
            }
        }
        return status;
    }

    function addResultfromDriver(uint tid, string memory appId, uint stageId, int taskHash) public {
        app[appId].stage[stageId].task[tid].driverTaskHash = taskHash;
        app[appId].stage[stageId].task[tid].driver = true;
        app[appId].driverTasks++;
        if (app[appId].stage[stageId].task[tid].exec == true){
            uint tid2;
            if (tid % 2 == 0) {
                tid2 = tid + 1;
            }
            else {
                tid2 = tid - 1;
            }
            if (app[appId].stage[stageId].task[tid2].exec == true && app[appId].stage[stageId].task[tid2].driver == true){
                int status = verifyPair(appId, stageId, tid, tid2);
                if (status != 0){
                    app[appId].status = status;
                }
            }
        }
    }

    function addResultfromExec(uint tid, string memory appId, uint stageId, int taskHash, int resultHash, string memory hostname) public {
        if (hostnameToId[hostname] == 0) {
            totalWorkers += 1;
            hostnameToId[hostname] = totalWorkers;
            idToHostname[totalWorkers] = hostname;
            idToCount[totalWorkers] += 1;
        }
        else {
            idToCount[hostnameToId[hostname]] += 1;
        }
        totaltasks += 1;
        app[appId].stage[stageId].task[tid].execTaskHash = taskHash;
        app[appId].stage[stageId].task[tid].resultHash = resultHash;
        app[appId].stage[stageId].task[tid].exec = true;
        app[appId].execTasks++;

        if (app[appId].stage[stageId].task[tid].driver == true){
            uint tid2;
            if (tid % 2 == 0) {
                tid2 = tid + 1;
            }
            else {
                tid2 = tid - 1;
            }
            if (app[appId].stage[stageId].task[tid2].exec == true && app[appId].stage[stageId].task[tid2].driver == true){
                int status = verifyPair(appId, stageId, tid, tid2);
                if (status != 0){
                    app[appId].status = status;
                }
            }
        }
    }

    function returnAppStatus(string memory appId) public view returns (int) {
        if (app[appId].driverTasks !=app[appId].execTasks){
            return -1;
        }
        int result =  app[appId].status;
        return result;   
    }


    function returnTotalWorkers() public view returns (uint) {
        return totalWorkers;
    }

    function returnWorkerUsage(uint id, string memory hostname) public view returns (string memory, uint) {
        uint result;
        if (id == 0) {
            id = hostnameToId[hostname];
        }
        else {
            hostname = idToHostname[id];
        }
        result = idToCount[id]*100 / totaltasks;
        return (hostname, result);
    }

}