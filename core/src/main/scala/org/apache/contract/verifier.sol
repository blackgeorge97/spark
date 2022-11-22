pragma solidity ^0.8.0;


library Library {
  struct data {
    mapping(uint => string) hashes;
    uint totalTasks;
   }
}

contract sparkVerifier {

mapping(uint => Library.data) public stageToHash;

function addNewResult(uint tid, uint stageId, string memory resultHash) public {
    stageToHash[stageId].hashes[tid] = resultHash;
    stageToHash[stageId].totalTasks += 1;
}

function verifyStageResults(uint stageId) public view returns (bool) {
    bool result = true;
    for(uint i = 0; i < stageToHash[stageId].totalTasks; i += 2){
        if(keccak256(abi.encodePacked(stageToHash[stageId].hashes[i]))!= keccak256(abi.encodePacked(stageToHash[stageId].hashes[i+1]))){
            result = false;
            break;
        }
    } 
    return result;   
}

}