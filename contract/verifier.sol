pragma solidity ^0.8.0;


library Library {
    struct taskData{
        int driverTaskHash;
        int execTaskHash;
        int resultHash;
        bool exec;
        bool posted;
    }
    struct taskSet{
        mapping(uint => taskData) task;
    }
    struct stages{
        mapping(uint => taskSet) stage;
        int status;
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
        if (app[appId].stage[stageId].task[tid1].posted == false || app[appId].stage[stageId].task[tid2].posted == false){
            return -2;
        }
        if (app[appId].stage[stageId].task[tid1].exec == false || app[appId].stage[stageId].task[tid2].exec == false){
            return -1;
        }
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
    }


    function updatePostedTaskPair(uint tid1, uint tid2, int taskHash1, int taskHash2, string memory appId, uint stageId) public {
        if (app[appId].stage[stageId].task[tid1].posted == false && app[appId].stage[stageId].task[tid2].posted == false) {
            app[appId].stage[stageId].task[tid1].driverTaskHash = taskHash1;
            app[appId].stage[stageId].task[tid2].driverTaskHash = taskHash2;
            app[appId].stage[stageId].task[tid1].posted = true;
            app[appId].stage[stageId].task[tid2].posted = true;
            int status = verifyPair(appId, stageId, tid1, tid2);
            if (status != 0) {
                app[appId].status = status;
            }
        }
    }

    function checkData(uint tid, string memory appId, uint stageId) public view returns (int, int, int, bool, bool) {
        return (app[appId].stage[stageId].task[tid].driverTaskHash, app[appId].stage[stageId].task[tid].execTaskHash, 
                app[appId].stage[stageId].task[tid].resultHash, app[appId].stage[stageId].task[tid].posted,
                app[appId].stage[stageId].task[tid].exec);
    }

    function returnAppStatus(string memory appId) public view returns (int) {
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