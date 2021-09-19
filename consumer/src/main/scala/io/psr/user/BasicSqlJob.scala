package io.psr.user

import akka.event.slf4j.Logger

import java.sql.Connection

class BasicSqlJob(val id: String, override val con: Connection) extends SqlJob {
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
}
