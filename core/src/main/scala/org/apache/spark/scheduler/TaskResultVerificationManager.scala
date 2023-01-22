package org.apache.spark.scheduler
import java.io._
import sys.process._
import org.apache.spark.internal.Logging
import scala.collection.mutable.{HashMap, HashSet}
import scala.collection.mutable._

object TaskResultVerificationManager
extends Logging {
  val someRes = sys.env.get("SPARK_HOME").orElse(sys.props.get("spark.test.home"))
  val strbuild = new StringBuilder()
  someRes.addString(strbuild)
  val sparkHome = strbuild.toString
  
  class DriverHashAdder(
    tid: Long,
    appId: String,
    stageId: Long,
    taskHash: Long
  )
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/hashAdderDriver.py ${tid} ${appId} ${stageId} ${taskHash}" ! ProcessLogger(stdout append _, stderr append _)
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
    appId: String,
    stageId: Long,
    taskHash: Long,
    resultHash: Long,
    hostname: String
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/hashAdderExec.py ${tid} ${appId} ${stageId} ${taskHash} ${resultHash} ${hostname}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Task hashcode and result hashcode of task index ${tid} of stage ${stageId} send to verifier Smart Contract")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

  class ResultsVerifier(
    appId: String
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/resultVerifier.py ${appId}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Verification of app with Id: ${appId} completed.")
      }
      else {
          println("Error while communicating with Smart Contract")
      }
    }
  }

  class workerUsageReturner() 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/usageReturner.py" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Usage of each worker has been returned successfully!")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

}