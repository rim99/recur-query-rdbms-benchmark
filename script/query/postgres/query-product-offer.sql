WITH RECURSIVE entity(
  operator_name,
  psr_type,
  entity_id,
  start_time,
  end_time,
  name
) AS (
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
      entity_id = 'b70e39fa-17ba-11ec-b8be-fd3982f95263' AND
      psr_type = 4
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
       s.entity_id = sp.child_entity_id and sp.parent_entity_id = e.entity_id and
       s.operator_name = sp.operator_name and sp.operator_name = e.operator_name
)
SELECT * FROM entity;


-- select * from specification where operator_name = 'AT&T' and psr_type = 4 limit 5;