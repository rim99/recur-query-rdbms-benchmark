CREATE TABLE tag (
    tag_id          uuid not null,
    operator_name   text not null,
    name            text not null,
    PRIMARY KEY(operator_name, tag_id)
) PARTITION BY HASH (operator_name);

CREATE TABLE specification (
    start_time      timestamp(0) with time zone not null,
    end_time        timestamp(0) with time zone not null,
    entity_id       uuid not null,
    revision_id     uuid not null,
    operator_name   text not null,
    psr_type        smallint not null,
    name            text not null,
    description     text not null,
    properties      jsonb not null,
    PRIMARY KEY(operator_name, entity_id, revision_id)
) PARTITION BY HASH (operator_name);

CREATE TABLE spec_tag (
    operator_name   text not null,
    entity_id       uuid not null,
    revision_id     uuid not null,
    tag_id          uuid not null
) PARTITION BY HASH (operator_name);

CREATE INDEX spec_tag_s ON spec_tag using BTREE (operator_name, entity_id, revision_id);
CREATE INDEX spec_tag_t ON spec_tag using BTREE (operator_name, tag_id);

CREATE TABLE tag_par_0 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE tag_par_1 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE tag_par_2 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE tag_par_3 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE tag_par_4 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE tag_par_5 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE tag_par_7 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE tag_par_8 PARTITION OF tag FOR VALUES WITH (MODULUS 8, REMAINDER 7);

CREATE TABLE specification_par_0 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE specification_par_1 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE specification_par_2 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE specification_par_3 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE specification_par_4 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE specification_par_5 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE specification_par_6 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE specification_par_7 PARTITION OF specification FOR VALUES WITH (MODULUS 8, REMAINDER 7);

CREATE TABLE spec_tag_par_0 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE spec_tag_par_1 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE spec_tag_par_2 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE spec_tag_par_3 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE spec_tag_par_4 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE spec_tag_par_5 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE spec_tag_par_6 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE spec_tag_par_7 PARTITION OF spec_tag FOR VALUES WITH (MODULUS 8, REMAINDER 7);