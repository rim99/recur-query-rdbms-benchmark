WITH RECURSIVE entity(
  operator_name,
  psr_type,
  entity_id,
  start_time,
  end_time,
  name
) AS (
    SELECT
      searched.operator_name,
      searched.psr_type,
      searched.entity_id,
      searched.start_time,
      searched.end_time,
      searched.name
    FROM (
      SELECT
        operator_name,
        psr_type,
        entity_id,
        start_time,
        end_time,
        name
      FROM specification
      WHERE
        operator_name = 'AT&T' AND
        spec_searchable_index_col @@ to_tsquery('france')
      LIMIT 2  
    ) as searched

  UNION
    SELECT 
      s.operator_name,
      s.psr_type,
      s.entity_id,
      s.start_time,
      s.end_time,
      s.name
    FROM specification s, spec_relationship sp, entity e
    WHERE 
       s.entity_id = sp.parent_entity_id and sp.child_entity_id = e.entity_id and
       s.operator_name = sp.operator_name and sp.operator_name = e.operator_name
)
SELECT count(*) FROM entity WHERE psr_type = 4;