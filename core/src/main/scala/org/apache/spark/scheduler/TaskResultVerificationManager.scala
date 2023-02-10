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
      val result = s"python3.8 ${sparkHome}/contract/hashAdderDriver.py ${tid} ${appId} ${stageId} ${taskHash}" ! ProcessLogger(stdout append _, stderr append _)
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
      val result = s"python3.8 ${sparkHome}/contract/hashAdderExec.py ${tid} ${appId} ${stageId} ${taskHash} ${resultHash} ${hostname}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Task hashcode and result hashcode of task index ${tid} of stage ${stageId} send to verifier Smart Contract")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

  class postUpdater(
    tid1: Long,
    tid2: Long,
    appId: String,
    stageId: Long
  )
  extends Runnable
  {
    override def run()
    {
      val result = s"python3.8 ${sparkHome}/contract/hashAdderExec.py ${tid1} ${tid1} ${appId} ${stageId}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Post action of taskpair ${tid1} ${tid1} send to Smart Contract")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }
}