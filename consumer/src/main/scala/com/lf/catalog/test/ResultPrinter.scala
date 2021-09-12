package com.lf.catalog.test

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.event.slf4j.Logger

case class Result(p50LatencyInMs: Double,
                  p90LatencyInMs: Double,
                  p99LatencyInMs: Double,
                  p999LatencyInMs: Double,
                  maxLatencyInMs: Double,
                  avgThroughPutInSec: Double,
                  maxThroughPutInSec: Double)

object ResultPrinter {
  private val log = Logger("ResultPrinter")

  def apply(): Behavior[Result] = Behaviors.receive { (ctx, msg) =>
    log.info(msg.toString)
    Behaviors.stopped
  }
}
