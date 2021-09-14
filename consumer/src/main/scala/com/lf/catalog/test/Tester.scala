package com.lf.catalog.test

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.event.slf4j.Logger

object Tester {
  private val log = Logger("Tester")

  def apply(operatorFactory: OperatorFactory): Behavior[Config] = {
    Behaviors.setup { ctx =>
      val resultPrinter = ctx.spawn(ResultPrinter(), "result-printer")

      Behaviors.receiveMessage { msg =>
        log.info("Started")
        val collector = ctx.spawn(new Collector(msg.concurrency, resultPrinter).start(), "collector")
        val start = WorkerStart(
          totalHit = msg.hitsPerWorker,
          collector = collector
        )
        val operation = operatorFactory.create()
        for (id <- Range(0, msg.concurrency)) {
          val worker = ctx.spawn(operation.go(), s"worker-${id}")
          worker ! start
        }
        Behaviors.same
      }
    }
  }
}


