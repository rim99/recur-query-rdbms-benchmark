package com.lf.catalog.test

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors

object Tester {
  def apply(): Behavior[Config] =
    Behaviors.receive { (context, message) =>

      /* spawn Workers and a Collector */


      /* trigger worker */

      Behaviors.stopped
    }
}


