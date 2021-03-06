package io.psr

import akka.actor.typed.ActorSystem
import akka.event.slf4j.Logger
import io.psr.test.{Config, Tester}
import io.psr.user.JobFactory

import java.util.Scanner
import scala.annotation.tailrec

object Application extends App {
  val log = Logger("App")
  val testConfig = Config.collect()
  val testing: ActorSystem[Config] = ActorSystem(Tester(JobFactory.create()), "tester")

  val sc = new Scanner(System.in)
  val guide = "Please hit enter to trigger test. Type in `exit` to close application"
  log.info(guide)

  @tailrec
  def run(): Unit = {
    val content = sc.nextLine()
    if (content.equalsIgnoreCase("exit")) {
      log.info("Closed")
      System.exit(0)
    } else {
      log.info("Testing, please don't touch keyboard")
      testing ! testConfig
    }
    run()
  }

  run()
}


