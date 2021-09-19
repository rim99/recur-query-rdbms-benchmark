package io.psr.user

sealed trait Database {
  val name: String
}

object Postgres extends Database {
  override val name: String = "postgres"
}

object Mysql extends Database {
  override val name: String = "mysql"
}

object Mariadb extends Database {
  override val name: String = "mariadb"
}

sealed trait TestBehaviour {
  val name: String
}

object Test extends TestBehaviour {
  /* for testing env */
  override val name: String = "test"
}

object Search extends TestBehaviour {
  /* for searching preferred product offering */
  override val name: String = "search"
}

object Query extends TestBehaviour {
  /* for query PSR model tree for specific product offering */
  override val name: String = "query"
}
