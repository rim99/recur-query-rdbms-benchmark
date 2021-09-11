package com.lf.catalog.test

import akka.actor.typed.ActorSystem

object Application extends App {
  val testing: ActorSystem[Config] = ActorSystem(Tester(), "catalog-tester")
  val config = Config.collect()
  testing ! config
}
