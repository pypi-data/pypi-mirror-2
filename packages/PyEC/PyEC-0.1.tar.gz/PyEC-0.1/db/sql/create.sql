BEGIN;
CREATE TABLE "db_segment" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(256) NOT NULL UNIQUE,
    "totalprob" double precision NOT NULL
)
;
CREATE TABLE "db_point" (
    "id" serial NOT NULL PRIMARY KEY,
    "point" double precision[],
    "bayes" text,
    "score" double precision NOT NULL,
    "probindex" double precision NOT NULL,
    "count" integer CHECK ("count" >= 0) NOT NULL,
    "segment_id" integer NOT NULL REFERENCES "db_segment" ("id") DEFERRABLE INITIALLY DEFERRED,
    "alive" boolean NOT NULL
)
;
CREATE TABLE "db_distance" (
    "id" serial NOT NULL PRIMARY KEY,
    "fro_id" integer NOT NULL REFERENCES "db_point" ("id") DEFERRABLE INITIALLY DEFERRED,
    "to_id" integer NOT NULL REFERENCES "db_point" ("id") DEFERRABLE INITIALLY DEFERRED,
    "distance" double precision NOT NULL,
    UNIQUE ("fro_id", "to_id")
)
;
CREATE TABLE "db_partition" (
    "id" serial NOT NULL PRIMARY KEY,
    "upper" double precision NOT NULL,
    "lower" double precision NOT NULL,
    "index" integer CHECK ("index" >= 0) NOT NULL,
    "segment_id" integer NOT NULL REFERENCES "db_segment" ("id") DEFERRABLE INITIALLY DEFERRED,
    "parent_id" integer,
    "point_id" integer UNIQUE REFERENCES "db_point" ("id") DEFERRABLE INITIALLY DEFERRED,
    "area" double precision NOT NULL
)
;
ALTER TABLE "db_partition" ADD CONSTRAINT "parent_id_refs_id_22f5a8e5" FOREIGN KEY ("parent_id") REFERENCES "db_partition" ("id") DEFERRABLE INITIALLY DEFERRED;

create index db_partition_parent on db_partition(parent_id);
create index db_partition_point on db_partition(point_id);

CREATE TABLE "db_scoretree" (
    "id" serial NOT NULL PRIMARY KEY,
    "segment_id" integer NOT NULL REFERENCES "db_segment" ("id") DEFERRABLE INITIALLY DEFERRED,
    "parent_id" integer,
    "point_id" integer UNIQUE REFERENCES "db_point" ("id") DEFERRABLE INITIALLY DEFERRED,
    "area" double precision NOT NULL,
    "min_score" double precision NOT NULL,
    "max_score" double precision NOT NULL,
    "child_count" integer CHECK ("child_count" >= 0) NOT NULL,
    "balance" integer NOT NULL,
    "taylor" double precision[],
    "height" integer CHECK ("depth" >= 0) NOT NULL
)
;
ALTER TABLE "db_scoretree" ADD CONSTRAINT "parent_id_refs_id_59af27d" FOREIGN KEY ("parent_id") REFERENCES "db_scoretree" ("id") DEFERRABLE INITIALLY DEFERRED;

create index db_scoretree_parent on db_scoretree(parent_id);
create index db_scoretree_height on db_scoretree(height);

create index db_distance_distance on db_distance(distance);
create index db_point_alive on db_point(alive);


COMMIT;
