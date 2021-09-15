package io.psr.test

case class Config(concurrency: Int, hitsPerWorker: Int)

object Config {
  def collect(): Config = {
    val concurrency = System.getenv("CONCURRENCY").toInt
    val hitsPerWorker = System.getenv("HITS_PER_WORKER").toInt
    Config(concurrency, hitsPerWorker)
  }
}




