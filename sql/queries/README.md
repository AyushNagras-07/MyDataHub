# Queries

Hand-written SQL, run manually against the database — there is no query runner, API, or scheduled job that executes these.

| File | Status | Purpose |
|---|---|---|
| `001_validation_queries.sql` | Empty placeholder | No content yet |
| `002_constraint_tests.sql` | Empty placeholder | No content yet |
| `003_analytics_queries.sql` | Exploratory, partially broken | Personal analytics across all six topic tables |
| `004_pipeline_monitoring.sql` | Working | Pipeline run/error monitoring |

## `004_pipeline_monitoring.sql`

Eight queries against `pipeline_runs`, all consistent with the schema in [../schema/README.md](../schema/README.md):

- Latest 10 runs, most recent first
- Run counts by status (`SUCCESS` / `FAILED` / `PARTIAL_SUCCESS`) via `COUNT(*) FILTER (...)`
- Average `execution_time` overall and grouped by `status`
- Runs with at least one failed file, worst-first
- Total files/successful/failed summed across all runs
- A `CASE`-based success-percentage calculation per run

These are the queries referenced as "pipeline monitoring" in the [root README](../../README.md#pipeline-monitoring).

## `003_analytics_queries.sql`

Organized into sections — Personal, Office, Learning, Finance, Food, Habit, and Combined analytics — using plain aggregates, `GROUP BY`, and two window-function queries (a gaps-and-islands streak calculation for `bath_taken`, and a weekly pushup trend).

**This file has not been fully reconciled with the current schema.** When updating or reusing queries from it, be aware of:

- Several "Office Analytics" queries filter `office_logs` directly by `log_date` (`WHERE log_date >= date_trunc('month', ...)`), but `office_logs` has no `log_date` column — that column only exists on `daily_logs`. These queries need a join to `daily_logs` to run.
- Two "Combined Analytics" queries reference `o.working_hours`, but the actual column (per `sql/schema/004_office_logs.sql`) is `hours_worked`.
- The query under the comment `--checking how mood is decided` is incomplete (`select ... from --complete this its big join`) and is not valid SQL as written.

These are documented here as-is rather than silently fixed, since this file is source-controlled SQL, not application code the pipeline depends on — treat it as a set of analytics drafts to verify against the live schema before running.
