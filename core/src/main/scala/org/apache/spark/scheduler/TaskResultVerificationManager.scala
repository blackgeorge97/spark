package org.apache.spark.scheduler
import java.io._
import sys.process._
import org.apache.spark.internal.Logging
import scala.collection.mutable.{HashMap, HashSet}

object TaskResultVerificationManager
extends Logging {
  val sparkHome = sys.env.get("SPARK_HOME").orElse(sys.props.get("spark.test.home"))

  class DriverHashAdder(
    tid: Long,
    stageId: Long,
    taskhash: Long
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python" + sparkHome.toString + "/core/src/main/scala/org/apache/contract/hashAdderDriver.py ${tid} ${stageId} ${resultHash}" ! ProcessLogger(stdout append _, stderr append _)
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
    taskhash: Long,
    resultHash: Long
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python" + sparkHome.toString + "/core/src/main/scala/org/apache/contract/hashAdderExec.py ${tid} ${stageId} ${taskhash} ${resultHash}" ! ProcessLogger(stdout append _, stderr append _)
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
      val result = s"python" + sparkHome.toString + "/core/src/main/scala/org/apache/contract/resultVerifier.py ${stageId}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"\nVerification of stage with Id: ${stageId} completed.")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  } 
}