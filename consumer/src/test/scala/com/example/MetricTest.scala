package com.example

import com.lf.catalog.test.{Metric, Metrics}
import org.scalatest.funspec.AnyFunSpec

class MetricTest extends AnyFunSpec {
  it("should return correct max throughput") {
    val baseline = System.nanoTime()
    val oneSecInNano = 1_000_000_000
    val metricA = Metric(baseline + oneSecInNano - 5_000, baseline + oneSecInNano + 5_000)
    val metricB = Metric(baseline + oneSecInNano + 10_000, baseline + oneSecInNano * 2 - 500_000)
    val metricC = Metric(baseline + oneSecInNano + 20_000, baseline + oneSecInNano * 2 - 400_000)
    val metricD = Metric(baseline + oneSecInNano + 15_000, baseline + oneSecInNano * 2 - 300_000)
    val metricE = Metric(baseline + oneSecInNano + 100_000, baseline + oneSecInNano * 2 + 300_000)
    val metricF = Metric(baseline + oneSecInNano * 3 + 100_000, baseline + oneSecInNano * 4 + 300_000)

    val result = Metrics.analyze(metricA :: metricB :: metricC :: metricD :: metricE :: metricF :: Nil)

    assert(result.maxThroughPutInSec == 3)
  }
}
