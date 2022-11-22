package org.apache.spark.scheduler
import java.io._
import sys.process._
import org.apache.spark.internal.Logging
import scala.collection.mutable.{HashMap, HashSet}

object TaskResultVerificationManager
extends Logging {

  def addNewResultForTid(tid: Long, stageId: Long, resultHash: String): Unit = {
    val result = s"python /home/kwstas/Workspace/spark/core/src/main/scala/org/apache/contract/resultAdder.py ${tid} ${stageId} ${resultHash}" ! ProcessLogger(stdout append _, stderr append _)
    if (result == 0){
      println(s"Hashcode of task ${tid} of stage ${stageId} send to verifier Smart Contract")
    }
    else {
      println("Error while communicating with Smart Contract")
    }
  }

  def verifyStageResults(stageId: Long): Unit = {
    val result = s"python /home/kwstas/Workspace/spark/core/src/main/scala/org/apache/contract/resultVerifier.py ${stageId}" ! ProcessLogger(stdout append _, stderr append _)
    if (result == 0){
      println(s"\nVerification of stage with Id: ${stageId} completed.")
    }
    else {
      println("Error while communicating with Smart Contract")
    }
  }
}