CREATE TABLE tag (
    tag_id          uuid not null,
    operator_name   varchar not null,
    name            varchar not null,
    PRIMARY KEY(tag_id, operator_name)
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
    PRIMARY KEY(entity_id, revision_id, operator_name)
) PARTITION BY HASH (operator_name);

CREATE TABLE spec_tag (
    operator_name   text not null,
    entity_id       uuid not null,
    revision_id     uuid not null,
    tag_id          uuid not null
) PARTITION BY HASH (operator_name);

CREATE INDEX spec_tag_s ON spec_tag using BTREE (operator_name, entity_id, revision_id);
CREATE INDEX spec_tag_t ON spec_tag using BTREE (operator_name, tag_id);
