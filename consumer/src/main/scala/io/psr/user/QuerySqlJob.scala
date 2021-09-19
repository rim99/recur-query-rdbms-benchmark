package io.psr.user

import java.sql.{Connection, ResultSet}
import scala.annotation.tailrec

class QuerySqlJob(val database: Database, override val con: Connection) extends SqlJob {

  val entityIdOfProductOfferPerOperator: Map[String, Array[String]] = {
    val query = database match {
      case Postgres => "select entity_id from specification where operator_name = ? and psr_type = 4 limit 2000"
      case Mysql | Mariadb => "select BIN_TO_UUID(entity_id) as entity_id from specification where operator_name = ? and psr_type = 4 limit 2000"
    }
    val stmt = con.prepareStatement(query)
    supportedOperators.map { op =>
      stmt.setString(1, op)
      val rs = stmt.executeQuery()
      @tailrec
      def fetch(rs: ResultSet, fetched: List[String]): List[String] = {
        if (rs.next()) {
          val newId = rs.getString("entity_id")
          fetch(rs, newId :: fetched)
        } else {
          fetched
        }
      }
      val idList = fetch(rs, List.empty[String]).toArray
      (op, idList)
    }.toMap

  }

  override protected def operate(cycle: Int): Unit = {
    val operator = randomOperator()
    stmt.setString(1, operator)
    stmt.setString(2, randomFrom(entityIdOfProductOfferPerOperator(operator)))
    val rs = stmt.executeQuery()
    rs.close()
  }

  private val stmtStr: String = database match {
    case Postgres =>
      """
        |WITH RECURSIVE entity(
        |  operator_name,
        |  psr_type,
        |  entity_id,
        |  start_time,
        |  end_time,
        |  name
        |) AS (
        |    SELECT
        |      operator_name,
        |      psr_type,
        |      entity_id,
        |      start_time,
        |      end_time,
        |      name
        |    FROM specification
        |    WHERE
        |      operator_name = ? AND
        |      entity_id = ?::uuid AND
        |      psr_type = 4
        |  UNION
        |    SELECT
        |      s.operator_name,
        |      s.psr_type,
        |      s.entity_id,
        |      s.start_time,
        |      s.end_time,
        |      s.name
        |    FROM specification s, spec_relationship sp, entity e
        |    WHERE
        |       s.entity_id = sp.child_entity_id and sp.parent_entity_id = e.entity_id and
        |       s.operator_name = sp.operator_name and sp.operator_name = e.operator_name
        |)
        |SELECT * FROM entity;
        |""".stripMargin
    case Mariadb | Mysql =>
      """
        |WITH RECURSIVE entity(
        |  operator_name,
        |  psr_type,
        |  entity_id,
        |  start_time,
        |  end_time,
        |  name,
        |  description
        |) AS (
        |    SELECT
        |      operator_name,
        |      psr_type,
        |      entity_id,
        |      start_time,
        |      end_time,
        |      name,
        |      description
        |    FROM specification
        |    WHERE
        |      operator_name = ? AND
        |      entity_id = UUID_TO_BIN(?) AND
        |      psr_type = 4
        |  UNION
        |    SELECT
        |      s.operator_name,
        |      s.psr_type,
        |      s.entity_id,
        |      s.start_time,
        |      s.end_time,
        |      s.name,
        |      s.description
        |    FROM specification s, spec_relationship sp, entity e
        |    WHERE
        |       s.entity_id = sp.child_entity_id and sp.parent_entity_id = e.entity_id and
        |       s.operator_name = sp.operator_name and sp.operator_name = e.operator_name
        |)
        |SELECT * FROM entity;
        |""".stripMargin
  }

  private val stmt = con.prepareStatement(stmtStr)
}
