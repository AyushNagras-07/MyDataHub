# Database

PostgreSQL schema, indexes, views, and SQL queries for MyDataHub. This is the single database written to by the ETL pipeline ([../etl/README.md](../etl/README.md)) and read by the analytics/monitoring queries below — there is no separate OLAP warehouse or replication.

## Layout

```
sql/
├── schema/    # Table definitions, numbered 001-010 — see schema/README.md
├── indexes/   # 001_indexes.sql — indexes on log_date, is_completed, and every child table's daily_log_id FK
├── views/     # daily_summary, weekly_summary, monthly_summary — see views section below
├── queries/   # Analytics + pipeline monitoring queries — see queries/README.md
└── seeds/     # sample_data.sql — currently empty, no seed data yet
```

## Applying the Schema

Files are numbered and must be run in order, since later tables have foreign keys into earlier ones:

```bash
for f in sql/schema/*.sql; do psql -U postgres -d mydatahub -f "$f"; done
psql -U postgres -d mydatahub -f sql/indexes/001_indexes.sql
for f in sql/views/*.sql; do psql -U postgres -d mydatahub -f "$f"; done
```

Full setup instructions (including the test database) are in the [root README](../README.md#database-setup).

## Views

| View | Built on | What it does |
|---|---|---|
| `daily_summary` | `daily_logs` + all six topic tables | `LEFT JOIN`s every topic table onto `daily_logs` so each logged day is a single row, with `NULL`s where a topic table has no matching row |
| `weekly_summary` | `daily_summary` | Aggregates `daily_summary` by `DATE_TRUNC('week', log_date)` — sums/averages hours, expenses, habits, etc. |
| `monthly_summary` | `daily_summary` | Same aggregation, bucketed by `DATE_TRUNC('month', log_date)` |

`weekly_summary` and `monthly_summary` are both built **on top of `daily_summary`** rather than joining the base tables again — the join logic (which topic tables exist and how they relate) lives in exactly one place.

## Schema and Queries

- [sql/schema/README.md](./schema/README.md) — table-by-table breakdown and the ER relationships
- [sql/queries/README.md](./queries/README.md) — analytics and pipeline monitoring queries, including which ones are exploratory/incomplete
