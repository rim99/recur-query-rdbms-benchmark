name := "lf-psr-rdbms-test"

version := "1.0"

scalaVersion := "2.13.6"

lazy val akkaVersion = "2.6.16"

libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor-typed" % akkaVersion,
  "ch.qos.logback" % "logback-classic" % "1.2.3",
  "com.zaxxer" % "HikariCP" % "5.0.0",
  "mysql" % "mysql-connector-java" % "8.0.26",
  "org.postgresql" % "postgresql" % "42.2.23",

  "com.typesafe.akka" %% "akka-actor-testkit-typed" % akkaVersion % Test,
  "org.scalatest" %% "scalatest" % "3.1.0" % Test
)
