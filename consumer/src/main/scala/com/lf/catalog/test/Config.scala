package com.lf.catalog.test

//import com.zaxxer.hikari.{HikariConfig, HikariDataSource}

case class Config(concurrency: Int, hitsPerWorker: Int)

object Config {

//  def pooledConnection(concurrency: Int): DataSource = {
//    val testBehaviour = System.getenv("TEST_BEHAVIOUR") match {
//      case Search.name => Search
//      case Query.name => Query
//      case other => throw new IllegalArgumentException(s"Do not support test behaviour: ${other}")
//    }
//    val (dataSourceClassName, jdbcUrl) = System.getenv("TEST_DB") match {
//      case Postgres.name =>
//        val dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
//        val host = System.getenv("PG_HOST")
//        val dbName = System.getenv("PG_DB")
//        val username = System.getenv("PG_USER")
//        val password = System.getenv("PG_PASSWORD")
//        val jdbcUrl = s"jdbc:postgresql://${host}/${dbName}?user=${username}&password=${password}"
//        (dataSourceClassName, jdbcUrl)
//      case Mysql.name =>
//        val dataSourceClassName = "com.mysql.cj.jdbc.Driver"
//        val host = System.getenv("MYSQL_HOST")
//        val dbName = System.getenv("MYSQL_DB")
//        val username = System.getenv("MYSQL_USER")
//        val password = System.getenv("MYSQL_PASSWORD")
//        val jdbcUrl = s"jdbc:mysql://${host}/${dbName}?user=${username}&password=${password}"
//        (dataSourceClassName, jdbcUrl)
//      case other => throw new IllegalArgumentException(s"Do not support db type: ${other}")
//    }
//
//    val config = new HikariConfig()
//    config.setMaximumPoolSize(concurrency)
//    config.setDataSourceClassName(dataSourceClassName)
//    config.setJdbcUrl(jdbcUrl)
//
//    new HikariDataSource(config)
//  }

  def collect(): Config = {
    val concurrency = System.getenv("CONCURRENCY").toInt
    val hitsPerWorker = System.getenv("HITS_PER_WORKER").toInt
    Config(concurrency, hitsPerWorker)
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


