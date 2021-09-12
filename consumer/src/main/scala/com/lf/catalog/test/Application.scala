package com.lf.catalog.test

import akka.actor.typed.ActorSystem
import akka.event.slf4j.Logger

object Application extends App {
  val testing: ActorSystem[Config] = ActorSystem(Tester(User), "tester")
  val testConfig = Config.collect()
  testing ! testConfig
}

object User extends OperatorFactory {
  private val log = Logger("User")

  override def create(): Operation = new Operation {
    override protected def operate(): Unit = {
      log.debug("============= testing ============")
    }
  }
}
