CREATE TABLE tag (
    tag_id            binary(16) not null,
    operator_name     varchar(64) not null,
    name              varchar(64) not null,
    PRIMARY KEY(operator_name, tag_id)
) PARTITION BY KEY (operator_name);

CREATE TABLE specification (
    start_time      timestamp(0) not null,
    end_time        timestamp(0) not null,
    entity_id       binary(16) not null,
    revision_id     binary(16) not null,
    operator_name   varchar(64) not null,
    psr_type        tinyint not null,
    name            varchar(64)  not null,
    description     varchar(2048)  not null,
    properties      json not null,
    PRIMARY KEY(operator_name, entity_id, revision_id)
); -- PARTITION BY KEY(operator_name);

-- CREATE FULLTEXT INDEX spec_search_idx ON specification(name, description);



CREATE TABLE spec_tag (
    operator_name   varchar(64) not null,
    entity_id       binary(16) not null,
    revision_id     binary(16) not null,
    tag_id          binary(16) not null,
    PRIMARY KEY(operator_name, entity_id, revision_id, tag_id)
) PARTITION BY KEY (operator_name);

CREATE INDEX spec_tag_s using BTREE ON spec_tag (operator_name, entity_id, revision_id);
CREATE INDEX spec_tag_t using BTREE ON spec_tag (operator_name, tag_id);

CREATE TABLE spec_relationship (
    operator_name    varchar(64) not null,
    parent_entity_id binary(16) not null,
    child_entity_id  binary(16) not null,
    PRIMARY KEY(operator_name, parent_entity_id, child_entity_id)
) PARTITION BY KEY (operator_name);

CREATE INDEX spec_relationship_p using BTREE ON spec_relationship (operator_name, parent_entity_id);
CREATE INDEX spec_relationship_c using BTREE ON spec_relationship (operator_name, child_entity_id);