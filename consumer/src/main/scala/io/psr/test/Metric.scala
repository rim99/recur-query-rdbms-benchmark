package io.psr.test

import akka.event.slf4j.Logger

import scala.annotation.tailrec

case class Metric(startInNanoSec: Long, endInNanoSec: Long) // using System.nanoTime

object Metrics {
  private val log = Logger("Metrics")

  def analyze(metrics: List[Metric]): Result = {
    log.debug(s"Analyzing total count: ${metrics.size}")
    val (startL, endL, latencyL) = metrics.unzip3 { m => (
      m.startInNanoSec,
      m.endInNanoSec,
      m.endInNanoSec - m.startInNanoSec
    )}
    val (p50LatencyInMs, p90LatencyInMs, p99LatencyInMs, p999LatencyInMs, maxLatencyInMs) = calculateLatency(latencyL.toArray)
    val (avgThroughPutInSec, maxThroughPutInSec) = calculateThroughput(startL.toArray, endL.toArray)
    Result(
      p50LatencyInMs = p50LatencyInMs,
      p90LatencyInMs = p90LatencyInMs,
      p99LatencyInMs = p99LatencyInMs,
      p999LatencyInMs = p999LatencyInMs,
      maxLatencyInMs = maxLatencyInMs,
      avgThroughPutInSec = avgThroughPutInSec,
      maxThroughPutInSec = maxThroughPutInSec
    )
  }

  private def calculateLatency(unsortedLatencyList: Array[Long]): (Double, Double, Double, Double, Double) = {
    val sortedLatency = unsortedLatencyList.sortWith((a,b) => a <= b)
    val p50Index = (sortedLatency.length * 0.5).toInt
    val p90Index = (sortedLatency.length * 0.9).toInt
    val p99Index = (sortedLatency.length * 0.99).toInt
    val p999Index = (sortedLatency.length * 0.999).toInt

    (
      sortedLatency(p50Index) / 1_000_000.0d,
      sortedLatency(p90Index) / 1_000_000.0d,
      sortedLatency(p99Index) / 1_000_000.0d,
      sortedLatency(p999Index) / 1_000_000.0d,
      sortedLatency.last / 1_000_000.0d
    )
  }

  private def calculateThroughput(startL: Array[Long], endL: Array[Long]): (Double, Double) = {
    /**
     *    -----------*a--|------*b--------*c---------*d-|---*e---*f-------> start time of every metric
     *                   |                              |
     *                   |                              |
     *    ---------------|-*a------*b-------*c----------|-*d---*e------*f-> end time of every metric
     *                   |                              |
     *                   Ps                             Pe
     *
     *    To calculate throughput is to count events in given period. In the graph above, we use Ps and Pe to indicate
     *    the begin and end of that PERIOD. So want we want to count in are b and c, and we should rule out a and d.
     *    As we can imagine the Ps and Pe is moving forward in the direction of time flow, we can find that what we
     *    really want to count are the events that the start time is later than Ps and the end time is earlier than Pe,
     *    which is Ps <= Es < Ee <= Pe.
     *
     *    We will hold 2 counters each for Ps and Pe. Ps's counter only counts events by its start time. And Pe's
     *    counter only counts events by its end time. And the number of event happened in the period is the delta of
     *    these 2 counters. Actually, the counter is the index of happened events in the timeline.
     *
     *    Since we only care about the maximum of throughput, so we actively move the Period forward using the Pe only.
     */
    val avgThroughPut = startL.length / math.max(1, ((endL.last - startL.head) / 1_000_000_000.0d))

    @tailrec
    def walkThroughTimeline(startL: Array[Long], psPosition: Int,
                            endL: Array[Long], pePosition: Int,
                            maxCounted: Int, period: Long): Int = {
      if (pePosition == endL.length) {
        math.max(maxCounted, pePosition - psPosition)
      } else {
        val timeDelta = endL(pePosition) - startL(psPosition)
        if (timeDelta > period && pePosition > psPosition) {
          /* Ps should move forward */
          walkThroughTimeline(startL, psPosition + 1, endL, pePosition, maxCounted, period)
        } else {
          /* Pe should move forward */
          walkThroughTimeline(startL, psPosition, endL, pePosition + 1, math.max(maxCounted, pePosition - psPosition), period)
        }
      }
    }
    val period = 1_000_000_000
    val _start = System.nanoTime()
    val maxThroughPut = walkThroughTimeline(startL, 0, endL, 0, 0, period)
    val _end = System.nanoTime()
    log.debug(s"Calculate maxThroughPut in nano sec: ${_end - _start}")
    (avgThroughPut, maxThroughPut)
  }
}
