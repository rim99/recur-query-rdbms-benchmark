package com.lf.catalog.test

object Worker {
  // sequentially execute query and send latency metrics result to collector
  case class Config(totalHit: Int)

}
