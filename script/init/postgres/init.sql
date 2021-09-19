CREATE TABLE tag (
    tag_id          uuid not null,
    operator_name   text not null,
    name            text not null,
    PRIMARY KEY(operator_name, tag_id)
) PARTITION BY HASH (operator_name);

CREATE TABLE tag_par_0 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE tag_par_1 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE tag_par_2 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE tag_par_3 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE tag_par_4 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE tag_par_5 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE tag_par_7 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE tag_par_8 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 7);



CREATE TABLE specification (
    start_time      timestamp(0) with time zone not null,
    end_time        timestamp(0) with time zone not null,
    entity_id       uuid not null,
    revision_id     uuid not null,
    operator_name   text not null,
    psr_type        smallint not null,
    name            text not null,
    description     text not null,
    -- spec_searchable_index_col tsvector GENERATED ALWAYS AS (to_tsvector('english', name || ' ' || description)) STORED,
    properties      jsonb not null,
    PRIMARY KEY(operator_name, entity_id, revision_id)
) PARTITION BY HASH (operator_name);

CREATE TABLE specification_par_0 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE specification_par_1 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE specification_par_2 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE specification_par_3 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE specification_par_4 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE specification_par_5 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE specification_par_6 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE specification_par_7 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 7);

-- CREATE INDEX spec_search_idx ON specification USING GIN (spec_searchable_index_col);


CREATE TABLE spec_tag (
    operator_name   text not null,
    entity_id       uuid not null,
    revision_id     uuid not null,
    tag_id          uuid not null
); -- PARTITION BY HASH (operator_name);

CREATE INDEX spec_tag_s ON spec_tag using BTREE (operator_name, entity_id, revision_id);
CREATE INDEX spec_tag_t ON spec_tag using BTREE (operator_name, tag_id);

-- CREATE TABLE spec_tag_par_0 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 0);
-- CREATE TABLE spec_tag_par_1 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 1);
-- CREATE TABLE spec_tag_par_2 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 2);
-- CREATE TABLE spec_tag_par_3 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 3);
-- CREATE TABLE spec_tag_par_4 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 4);
-- CREATE TABLE spec_tag_par_5 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 5);
-- CREATE TABLE spec_tag_par_6 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 6);
-- CREATE TABLE spec_tag_par_7 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 7);



CREATE TABLE spec_relationship (
    operator_name    text not null,
    parent_entity_id uuid not null,
    child_entity_id  uuid not null
) PARTITION BY HASH (operator_name);

CREATE INDEX spec_relationship_p ON spec_relationship using BTREE (operator_name, parent_entity_id);
CREATE INDEX spec_relationship_c ON spec_relationship using BTREE (operator_name, child_entity_id);

CREATE TABLE spec_relationship_par_0 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE spec_relationship_par_1 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE spec_relationship_par_2 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE spec_relationship_par_3 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE spec_relationship_par_4 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE spec_relationship_par_5 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE spec_relationship_par_6 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE spec_relationship_par_7 PARTITION OF spec_relationship FOR VALUES WITH (MODULUS 8, REMAINDER 7);
