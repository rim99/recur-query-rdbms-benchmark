package io.psr.user

import io.psr.test.{Operation, OperatorFactory}

import java.sql.Connection
import java.util.concurrent.ThreadLocalRandom
import javax.sql.DataSource

class JobBuilder(val database: Database, val datasource: DataSource, val testBehaviour: TestBehaviour) extends OperatorFactory {
  override def create(jobId: String): Operation = {
    val conn = datasource.getConnection()
    testBehaviour match {
      case Test => new BasicSqlJob(jobId, conn)
      case Search => new SearchSqlJob(database, conn)
      case Query => new QuerySqlJob(database, conn)
    }
  }
}

trait SqlJob extends Operation {

  val supportedCountries = Array(
    "Algeria",
    "Andorra",
    "Angola",
    "Japan",
    "UK",
    "Burundi",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Pakistan",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Maldives",
    "Mali",
    "Malta",
    "Sweden",
    "Switzerland",
    "Togo",
    "Tonga",
    "Tunisia",
    "Zambia",
  )

  val supportedOperators = Array(
    "AT&T",
    "Verizon",
    "Nippon",
    "Deutsche Telekom",
    "T-Mobile",
    "Vodafone",
    "Telefonica",
    "America Movil",
    "KDDI",
    "Orange",
    "Digi",
    "China Mobile",
    "LG",
    "Japan Telecom",
    "Samsung",
    "Jio",
    "Bharti Airtel",
  )

  val con: Connection

  def randomFrom[E](choices: Array[E]): E =
    choices(math.abs(ThreadLocalRandom.current().nextInt() % choices.length))

  def randomOperator(): String = randomFrom(supportedOperators)

  def randomCountry(): String = randomFrom(supportedCountries)

  override protected def onClose(): Unit = {
    if (!con.isClosed) con.close()
  }
}

