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
    resultHash: Long,
    hostname: String
  ) 
  extends Runnable 
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/hashAdderExec.py ${tid} ${stageId} ${taskHash} ${resultHash} ${hostname}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"Task hashcode and result hashcode of task index ${tid} of stage ${stageId} send to verifier Smart Contract")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

  class deleteStageData(
  stageId: Long
  )
  extends Runnable
  {
    override def run()
    {
      val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/dataDeleter.py ${stageId}" ! ProcessLogger(stdout append _, stderr append _)
      if (result == 0){
        println(s"\nData stage with Id: ${stageId} is cleared.")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

  class ResultsVerifier() 
  extends Runnable 
  {

    private var stageQueue = Queue[Long]()

    def addStageId(
      stageId: Long
    )
    {
       stageQueue.enqueue(stageId)
    }

    override def run()
    {
      while (!stageQueue.isEmpty){
        val stageId = stageQueue.dequeue
        val result = s"python ${sparkHome}/core/src/main/scala/org/apache/contract/resultVerifier.py ${stageId}" ! ProcessLogger(stdout append _, stderr append _)
        if (result == 0){
          println(s"\nVerification of stage with Id: ${stageId} completed.")
        }
        else {
          println("Error while communicating with Smart Contract")
        }
        var deleter = new Thread(new deleteStageData(stageId))
        deleter.start()
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
        println(s"\nUsage of each worker has been returned successfully!")
      }
      else {
        println("Error while communicating with Smart Contract")
      }
    }
  }

}