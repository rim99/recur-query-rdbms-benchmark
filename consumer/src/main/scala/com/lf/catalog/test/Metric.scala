package com.lf.catalog.test

import akka.event.slf4j.Logger

import scala.collection.immutable.ArraySeq

case class Metric(start: Long, end: Long) // using System.nanoTime

object Metrics {
  private val log = Logger("Metrics")

  def analyze(metrics: List[Metric]): Result = {
    log.debug(s"Analyzing total count: ${metrics.size}")

    // TODO ???
    val l = List(3, 1,9)
    l.sortWith(???).toIndexedSeq


    Result(
      p50LatencyInMs = 0,
      p90LatencyInMs = 0,
      p99LatencyInMs = 0,
      p999LatencyInMs = 0,
      maxLatencyInMs = 0,
      avgThroughPutInSec = 0,
      maxThroughPutInSec = 0
    )

  }
}
