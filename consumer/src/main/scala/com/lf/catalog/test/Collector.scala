package com.lf.catalog.test

import akka.actor.typed.{ActorRef, Behavior}
import akka.actor.typed.scaladsl.Behaviors
import akka.event.slf4j.Logger

case class WorkerShutdown(metrics: List[Metric])

class Collector(val workerNumber: Int,
                val ResultPrinter: ActorRef[Result]) {
  private val log = Logger("Collector")

  def start(): Behavior[WorkerShutdown] = {
    log.debug(s"work shutdown begin")
    collect(0, Nil)
  }

  private def collect(finishedWorkerNumber: Int,
                      metrics: List[Metric]): Behavior[WorkerShutdown] =
    Behaviors.receiveMessage { message =>
      log.debug(s"work shutdown ${finishedWorkerNumber + 1}")
      val finished = finishedWorkerNumber + 1
      if (finished == workerNumber) {
        log.debug(s"Received worker notification count: ${finished}. Start to analyze")
        ResultPrinter ! Metrics.analyze(message.metrics ::: metrics)
        Behaviors.stopped
      } else {
        log.debug(s"Received worker notification count: ${finished}")
        collect(finished, message.metrics ::: metrics)
      }
  }
}
