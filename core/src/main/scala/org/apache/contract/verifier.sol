pragma solidity ^0.8.0;


library Library {
    struct data{
        mapping(uint => int) hashes;
        uint totalTasks;
    }
}

contract sparkVerifier {

    mapping(uint => Library.data) public stageToResultHash;

    mapping(uint => Library.data) public stageToDriverTaskHash;

    mapping(uint => Library.data) public stageToExecTaskHash;

    mapping(uint => string) public idToHostname;
    mapping(string => uint) public hostnameToId;
    mapping(uint => uint) public idToCount;
    uint totalWorkers = 0;
    uint totaltasks = 0;

    function addResultfromDriver(uint tid, uint stageId, int taskHash) public {
        stageToDriverTaskHash[stageId].hashes[tid] = taskHash;
        stageToDriverTaskHash[stageId].totalTasks += 1;
    }

    function addResultfromExec(uint tid, uint stageId, int taskHash, int resultHash, string memory hostname) public {
        stageToExecTaskHash[stageId].hashes[tid] = taskHash;
        stageToExecTaskHash[stageId].totalTasks += 1;
        stageToResultHash[stageId].hashes[tid] = resultHash;
        totaltasks += 1;
        if (hostnameToId[hostname] == 0) {
            totalWorkers += 1;
            hostnameToId[hostname] = totalWorkers;
            idToHostname[totalWorkers] = hostname;
            idToCount[totalWorkers] += 1;
        }
        else {
            idToCount[hostnameToId[hostname]] += 1;
        }

    }

    function verifyStageResults(uint stageId) public view returns (int) {
        int result = 0;
        if (stageToExecTaskHash[stageId].totalTasks != stageToDriverTaskHash[stageId].totalTasks){
            result = -1;
            return result;
        }
        for(uint i = 0; i < stageToExecTaskHash[stageId].totalTasks; i += 2){
            if(stageToResultHash[stageId].hashes[i] != stageToResultHash[stageId].hashes[i+1]){
                result = 1;
                break;
            }
        } 
        if (result == 0){
            return result;
        } 
        for(uint i = 0; i < stageToExecTaskHash[stageId].totalTasks; i += 2){
            if(stageToExecTaskHash[stageId].hashes[i] != stageToExecTaskHash[stageId].hashes[i + 1]){
                if (stageToExecTaskHash[stageId].hashes[i] == stageToDriverTaskHash[stageId].hashes[i] && 
                stageToExecTaskHash[stageId].hashes[i+1] == stageToDriverTaskHash[stageId].hashes[i+1]){
                    result = 2;
                    break;
                }
                else {
                    result = 3;
                    break;
                }
            }
        }
        return result;   
    }

    function emptyStageData(uint stageId) public {
        stageToExecTaskHash[stageId].totalTasks = 0;
        stageToDriverTaskHash[stageId].totalTasks = 0;
    }

    function returnTotalWorkers() public view returns (uint) {
        return totalWorkers;
    }

    function returnWorkerUsage(uint id, string memory hostname) public view returns (string memory, uint) {
        uint result;
        if (id < 0) {
            id = hostnameToId[hostname];
        }
        else {
            hostname = idToHostname[id];
        }
        result = idToCount[id]*100 / totaltasks;
        return (hostname, result);
    }

}