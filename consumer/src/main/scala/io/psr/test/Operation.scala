package io.psr.test

import akka.actor.typed.ActorRef
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.event.slf4j.Logger

import scala.annotation.tailrec

case class Start(totalHit: Int,
                 collector: ActorRef[WorkerShutdown])

trait Operation {
  private val log = Logger("Operation")
  // sequentially execute query and send latency metrics result to collector
  final def go(): Behavior[Start] = Behaviors.receiveMessage { cfg =>
    val metrics = execute(0, cfg.totalHit, List.empty)
    log.trace("sending metric")
    cfg.collector ! WorkerShutdown(metrics)
    Behaviors.stopped
  }

  @tailrec
  private def execute(hit: Int, limit: Int, metrics: List[Metric]): List[Metric] = {
    val start = System.nanoTime()
    operate(hit)
    val end = System.nanoTime()
    val metric = Metric(start, end)

    if (limit == hit + 1) {
      log.trace("worker done")
      onClose()
      metric :: metrics
    } else {
      log.trace(s"worker continue with: ${hit+1}")
      execute(hit + 1, limit, metric :: metrics)
    }
  }

  protected def operate(cycle: Int): Unit
  protected def onClose(): Unit
}

trait OperatorFactory {
  def create(id: String): Operation
}
