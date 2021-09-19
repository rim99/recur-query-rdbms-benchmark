WITH RECURSIVE entity(
  operator_name,
  psr_type,
  entity_id,
  start_time,
  end_time,
  name,
  description
) AS (
    SELECT
      operator_name,
      psr_type,
      entity_id,
      start_time,
      end_time,
      name,
      description
    FROM specification
    WHERE
      operator_name = 'America Movil' AND
      entity_id = UUID_TO_BIN("190d11ec-12c1-5f25-9920-d541dede013f") AND
      psr_type = 4
  UNION
    SELECT 
      s.operator_name,
      s.psr_type,
      s.entity_id,
      s.start_time,
      s.end_time,
      s.name,
      s.description
    FROM specification s, spec_relationship sp, entity e
    WHERE 
       s.entity_id = sp.child_entity_id and sp.parent_entity_id = e.entity_id and
       s.operator_name = sp.operator_name and sp.operator_name = e.operator_name
)
SELECT * FROM entity;