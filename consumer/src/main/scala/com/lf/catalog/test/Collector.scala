package com.lf.catalog.test

class Collector {
  case class Metric(start: Long, end: Long) // using System.nanoTime
  case class WorkerShutdown(workerId: String)

}
