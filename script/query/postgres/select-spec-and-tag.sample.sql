
select 
t.name, s.name 
from 
specification s left join spec_tag st on (
    s.operator_name = st.operator_name 
    and 
    s.entity_id = st.entity_id 
    and 
    s.revision_id = st.revision_id
)
left join tag t on (
    st.operator_name = t.operator_name
    and
    st.tag_id = t.tag_id
)
where
  s.operator_name = 'some' and 
  s.entity_id = '611aaf8d-0ce5-4da4-95a0-7c6370c0eb7e' and 
  s.revision_id = '611aaf8d-0ce5-4da4-95a0-7c6370c0eb7e';