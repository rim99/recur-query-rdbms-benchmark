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
                  maxThroughPutInSec: Double) {
  override def toString: String =
    s"""
      | Test Result:
      |   * Latency(ms):
      |     - p50:     ${p50LatencyInMs}
      |     - p90:     ${p90LatencyInMs}
      |     - p99:     ${p99LatencyInMs}
      |     - p999:    ${p999LatencyInMs}
      |     - max:     ${maxLatencyInMs}
      |  * ThroughPut(op/s):
      |     - average: ${avgThroughPutInSec}
      |     - max:     ${maxThroughPutInSec}
      |
      |
      |Please hit enter to trigger test. Type in `exit` to close application
      |""".stripMargin
}

object ResultPrinter {
  private val log = Logger("ResultPrinter")

  def apply(): Behavior[Result] = Behaviors.receive { (ctx, msg) =>
    log.info(msg.toString)
    Behaviors.same
  }
}
