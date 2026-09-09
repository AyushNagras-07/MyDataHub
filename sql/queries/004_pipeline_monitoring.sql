-- 1. Latest pipeline runs 
--What happened in the most recent pipeline executions?

SELECT
    id,
    started_at,
    completed_at,
    total_files,
    successful_files,
    failed_files,
    execution_time,
    status
FROM pipeline_runs
ORDER BY started_at DESC
LIMIT 10;

-- 2. Pipeline run status summary

SELECT
    COUNT(*) AS total_runs,
    COUNT(*) FILTER (WHERE status = 'SUCCESS') AS successful_runs,
    COUNT(*) FILTER (WHERE status = 'FAILED') AS failed_runs,
    COUNT(*) FILTER (WHERE status = 'PARTIAL_SUCCESS') AS partial_runs
FROM pipeline_runs;

--3. average pipeline execution time 

select avg(execution_time) as avg_execution_time from pipeline_runs;

--4 number of pipeline runs for each status

select status , count(status) as no_of_runs from pipeline_runs group by status ;

--Q5 — Conditional aggregation Find the total number of files processed, the total successful files, and the total failed files across all pipeline runs.

select sum(successful_files) , sum(failed_files) ,sum(total_files) from pipeline_runs ;

--Q6 — WHERE + ORDER BY Find all pipeline runs that had at least one failed file Show the run ID, total files, failed files, and status. Display the runs with the highest number of failed files first.

select id , total_files , failed_files , status from pipeline_runs where failed_files>=1 order by failed_files desc;

--Q7 — GROUP BY + AVG Find the average execution time for each pipeline status. Ignore runs where execution time is NULL.

select status , avg(execution_time) as avg_execution_time from pipeline_runs group by status having avg(execution_time) is not null;

--Q8 case based

select case when total_files>0 then(successful_files*100/total_files) else 0 end as success_percent from pipeline_runs;