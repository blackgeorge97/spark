package org.apache.spark.scheduler
import java.io._
import sys.process._
import org.apache.spark.internal.Logging
import scala.collection.mutable.{HashMap, HashSet}

object TaskResultVerificationManager
extends Logging {
  val someRes = sys.env.get("SPARK_HOME").orElse(sys.props.get("spark.test.home"))
  val strbuild = new StringBuilder()
  someRes.addString(strbuild)
  val sparkHome = strbuild.toString
  
  class DriverHashAdder(
    tid: Long,
    stageId: Long,
    taskHash: Long
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/hashAdderDriver.py ${tid} ${stageId} ${taskHash}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Task hashcode of task index ${tid} of stage ${stageId} send to verifier Smart Contract")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

  class ExecHashAdder(
    tid: Long,
    stageId: Long,
    taskHash: Long,
    resultHash: Long
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/hashAdderExec.py ${tid} ${stageId} ${taskHash} ${resultHash}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Task hashcode and result hashcode of task index ${tid} of stage ${stageId} send to verifier Smart Contract")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  } 
  

  class StageResultsVerifier(
    stageId: Long,
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/resultVerifier.py ${stageId}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"\nVerification of stage with Id: ${stageId} completed.")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  } 
}