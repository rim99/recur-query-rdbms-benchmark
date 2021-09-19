package io.psr.user

import io.psr.test.OperatorFactory
import org.apache.tomcat.jdbc.pool.{PoolProperties, DataSource => ApacheDataSource}

import javax.sql.DataSource

object JobFactory {
  private def pooledConnection(): (Database, DataSource) = {
    val (dbVendor, driverClassName, jdbcUrl) = System.getenv("TEST_DB") match {
      case Postgres.name =>
        val driverClassName = "org.postgresql.Driver"
        val host = System.getenv("PG_HOST")
        val dbName = System.getenv("PG_DB")
        val username = System.getenv("PG_USER")
        val password = System.getenv("PG_PASSWORD")
        val jdbcUrl = s"jdbc:postgresql://${host}/${dbName}?user=${username}&password=${password}"
        (Postgres, driverClassName, jdbcUrl)
      case Mysql.name =>
        val driverClassName = "com.mysql.cj.jdbc.Driver"
        val host = System.getenv("MYSQL_HOST")
        val dbName = System.getenv("MYSQL_DB")
        val username = System.getenv("MYSQL_USER")
        val password = System.getenv("MYSQL_PASSWORD")
        val jdbcUrl = s"jdbc:mysql://${host}/${dbName}?user=${username}&password=${password}"
        (Mysql, driverClassName, jdbcUrl)
      case Mariadb.name =>
        val driverClassName = "org.mariadb.jdbc.Driver"
        val host = System.getenv("MARIADB_HOST")
        val port = System.getenv("MARIADB_PORT")
        val dbName = System.getenv("MARIADB_DATABASE")
        val username = System.getenv("MARIADB_USER")
        val password = System.getenv("MARIADB_PASSWORD")
        val jdbcUrl = s"jdbc:mariadb://${host}:${port}/${dbName}?user=${username}&password=${password}"
        (Mariadb, driverClassName, jdbcUrl)
      case other => throw new IllegalArgumentException(s"Do not support db type: ${other}")
    }
    val concurrency = System.getenv("CONCURRENCY").toInt

    (dbVendor, createDataSource(driverClassName, jdbcUrl, concurrency))
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

  def create(): OperatorFactory = {
    val testBehaviour = System.getenv("TEST_BEHAVIOUR") match {
      case Search.name => Search
      case Query.name => Query
      case Test.name => Test
      case other => throw new IllegalArgumentException(s"Do not support test behaviour: ${other}")
    }
    val (database, connection) = pooledConnection()
    new JobBuilder(database, connection, testBehaviour)
  }
}
