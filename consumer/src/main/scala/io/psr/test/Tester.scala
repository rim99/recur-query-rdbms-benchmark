package io.psr.test

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
        val collector = ctx.spawn(new Collector(msg.concurrency, resultPrinter).start(), s"collector-${randomString}")
        val start = Start(
          totalHit = msg.hitsPerWorker,
          collector = collector
        )
        for (id <- Range(0, msg.concurrency)) {
          val worker = ctx.spawn(operatorFactory.create(id.toString).go(), s"worker-${id}")
          worker ! start
        }
        Behaviors.same
      }
    }
  }

  private def randomString = {
    System.currentTimeMillis().toHexString.reverse.substring(0, 4)
  }
}


