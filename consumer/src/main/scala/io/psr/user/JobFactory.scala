package io.psr.user

import akka.event.slf4j.Logger
import io.psr.test.{Operation, OperatorFactory}

import java.sql.Connection
import org.apache.tomcat.jdbc.pool.{DataSource => ApacheDataSource}

import javax.sql.DataSource
import org.apache.tomcat.jdbc.pool.PoolProperties

object JobFactory {
  private def pooledConnection(): DataSource = {
    val testBehaviour = System.getenv("TEST_BEHAVIOUR") match {
      case Search.name => Search
      case Query.name => Query
      case other => throw new IllegalArgumentException(s"Do not support test behaviour: ${other}")
    }
    val (driverClassName, jdbcUrl) = System.getenv("TEST_DB") match {
      case Postgres.name =>
        val driverClassName = "org.postgresql.Driver"
        val host = System.getenv("PG_HOST")
        val dbName = System.getenv("PG_DB")
        val username = System.getenv("PG_USER")
        val password = System.getenv("PG_PASSWORD")
        val jdbcUrl = s"jdbc:postgresql://${host}/${dbName}?user=${username}&password=${password}"
        (driverClassName, jdbcUrl)
      case Mysql.name =>
        val driverClassName = "com.mysql.cj.jdbc.Driver"
        val host = System.getenv("MYSQL_HOST")
        val dbName = System.getenv("MYSQL_DB")
        val username = System.getenv("MYSQL_USER")
        val password = System.getenv("MYSQL_PASSWORD")
        val jdbcUrl = s"jdbc:mysql://${host}/${dbName}?user=${username}&password=${password}"
        (driverClassName, jdbcUrl)
      case other => throw new IllegalArgumentException(s"Do not support db type: ${other}")
    }
    val concurrency = System.getenv("CONCURRENCY").toInt

    createDataSource(driverClassName, jdbcUrl, concurrency)
  }

  private def createDataSource(dataSourceClassName: String,
                               jdbcUrl: String,
                               concurrency: Int): ApacheDataSource  = {
    val prop = new PoolProperties
    prop.setMaxActive(concurrency * 2)
    prop.setMaxIdle(concurrency * 2)
    prop.setInitialSize(concurrency)
    prop.setMinIdle(concurrency)
    prop.setUrl(jdbcUrl)
    prop.setDriverClassName(dataSourceClassName)
    prop.setTestOnBorrow(true)
    prop.setValidationQuery("SELECT 1")
    prop.setTestOnReturn(true)
    prop.setTimeBetweenEvictionRunsMillis(60_000)
    prop.setMaxWait(10_000)
    prop.setMinEvictableIdleTimeMillis(120_000)
    val ds = new ApacheDataSource()
    ds.setPoolProperties(prop)
    ds
  }

  def create(): OperatorFactory = new Job(pooledConnection())
}

class Job(val datasource: DataSource) extends OperatorFactory {
  private val log = Logger("Job")
  override def create(id: String): Operation = {
    val conn = datasource.getConnection()
    new BasicSqlOperation(id, conn)
  }
}

class BasicSqlOperation(val id: String, val con: Connection) extends Operation {
  val log = Logger(s"BasicSqlOperation-${id}")
  override protected def operate(cycle: Int): Unit = {
    log.trace("execute {}", cycle)
    val st = con.createStatement
    val rs = st.executeQuery("select 1")
    if (rs.getFetchSize > 1) {
      log.trace("fetched sth")
    } else {
      log.trace("fetched nothing")
    }
    rs.close()
    st.close()
  }

  override protected def onClose(): Unit = {
    if (!con.isClosed) con.close()
  }
}

sealed trait Database {
  val name: String
}

object Postgres extends Database {
  override val name: String = "postgres"
}

object Mysql extends Database {
  override val name: String = "mysql"
}

sealed trait TestBehaviour {
  val name: String
}

object Search extends TestBehaviour {
  /* for searching preferred product offering */
  override val name: String = "search"
}

object Query extends TestBehaviour {
  /* for query PSR model tree for specific product offering */
  override val name: String = "query"
}
