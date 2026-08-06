-- ======================================================
-- PERSONAL ANALYTICS
-- ======================================================

--Which weekday has the highest mood?

select 
    to_char(d.created_at, 'day') as weekday_name,
    avg(p.mood) as average_mood
from 
    personal_logs as p
join 
    daily_logs as d on p.daily_log_id = d.id
group by 
    to_char(d.created_at, 'day')
order by 
    average_mood desc
limit 1;

-- ======================================================
-- OFFICE ANALYTICS
-- ======================================================

-- Total Office Hours This Month 

select 
    sum(hours_worked) as total_hours 
from 
    office_logs 
where 
    log_date >= date_trunc('month', current_date)
    and log_date < date_trunc('month', current_date) + interval '1 month';


--Number of Days with >8 Working Hours This Month

select 
    count(*) as long_days_count 
from 
    office_logs 
where 
    hours_worked > 8
    and log_date >= date_trunc('month', current_date)
    and log_date < date_trunc('month', current_date) + interval '1 month';

-- ======================================================
-- LEARNING ANALYTICS
-- ======================================================

--for seeing daily learning and number of hours i studied
select d.log_date,o.office_learnings , o.hours_worked , l.study_hours , l.topic_learned,l.project_progress from daily_logs d
join office_logs o
on d.id = o.daily_log_id
join learning_logs l
on d.id = l.daily_log_id
order by d.log_date;

-- ======================================================
-- FINANCE ANALYTICS
-- ======================================================

--montly finance

select date_trunc('month', d.log_date) , sum(f.daily_expense) as montly_spend, sum(f.income_received) as montly_recieved from finance_logs as f join daily_logs as d on f.daily_log_id = d.id group by date_trunc('month', d.log_date);

--Highest Spending Day

select 
    d.created_at as highest_spending_day,
    f.daily_expense as max_spend
from 
    finance_logs as f
join 
    daily_logs as d on f.daily_log_id = d.id
order by 
    f.daily_expense desc
limit 1;

-- ======================================================
-- FOOD ANALYTICS
-- ======================================================

--Tea Per Week

select 
    to_char(d.created_at, 'yyyy-iw') as financial_week,
    sum(f.tea_coffee_count) as total_tea
from 
    food_logs as f
join 
    daily_logs as d on f.daily_log_id = d.id
group by 
    to_char(d.created_at, 'yyyy-iw')
order by 
    financial_week desc;


--Breakfast Skipped Count

select 
    count(*) as breakfast_skipped_days
from 
    food_logs
where 
    breakfast is null 
    or lower(trim(breakfast)) in ('skipped', 'none', '');

--Dinner Skipped Count

select 
    count(*) as dinner_skipped_days
from 
    food_logs
where 
    dinner is null 
    or lower(trim(dinner)) in ('skipped', 'none', '');


--most common breakfast

select 
    breakfast,
    count(*) as frequency
from 
    food_logs
where 
    breakfast is not null 
    and lower(trim(breakfast)) not in ('skipped', 'none', '')
group by 
    breakfast
order by 
    frequency desc
limit 1;

--average tea count

select 
    avg(tea_coffee_count) as avg_daily_tea
from 
    food_logs;

-- ======================================================
-- HABIT ANALYTICS
-- ======================================================

-- weekly habits
select date_trunc('week', log_date) , count(h.hair_washed) , count(h.exercise_done) , count(h.hair_oil_applied),count(h.bath_taken) from habit_logs as h join daily_logs as d on h.daily_log_id = d.id

--Current Bath Streak

with ordered_logs as (
    select 
        d.created_at::date as log_date,
        bath_taken,
        row_number() over (order by d.created_at::date) - 
        row_number() over (partition by bath_taken order by d.created_at::date) as group_id
    from habit_logs h
    join daily_logs d on h.daily_log_id = d.id
),
streaks as (
    select 
        max(log_date) as last_date,
        count(*) as streak_length
    from ordered_logs
    where bath_taken = true
    group by group_id
)
select streak_length as current_bath_streak
from streaks
where last_date >= current_date - interval '1 day'
order by last_date desc
limit 1;

--Pushup Trend (Weekly Progress)

select 
    to_char(d.created_at, 'yyyy-iw') as financial_week,
    sum(h.pushups) as total_pushups,
    round(avg(h.pushups), 1) as avg_pushups_per_day
from 
    habit_logs h
join 
    daily_logs d on h.daily_log_id = d.id
group by 
    to_char(d.created_at, 'yyyy-iw')
order by 
    financial_week desc;


--Total Days Without Exercise

select 
    count(*) as days_without_exercise
from 
    habit_logs
where 
    exercise_done = false;

-- ======================================================
-- COMBINED ANALYTICS
-- ======================================================

--checking how mood is decided 

select p.mood , p.wake_up_time , o.hours_worked , l.project_progress , f.lunch,f.dinner from --complete this its big join

--more study improve mood ??

select p.mood as mood , l.study_hours as study_hours from personal_logs as p join learning_logs as l on p.daily_log_id = l.daily_log_id order by l.study_hours , p.mood desc;

--does exercise improve mood 

select 
    h.exercise_done,
    count(*) as total_days,
    round(avg(p.mood), 2) as average_mood
from 
    habit_logs h
join 
    personal_logs p on h.daily_log_id = p.daily_log_id
group by 
    h.exercise_done;

--Does office workload reduce study??

select 
    case 
        when o.working_hours > 8 then 'high workload (>8h)'
        else 'normal workload (<=8h)'
    end as workload_level,
    count(*) as total_days,
    round(avg(s.study_hours), 2) as average_study_hours
from 
    office_logs o
join 
    learning_logs s on o.daily_log_id = s.daily_log_id
group by 
    case 
        when o.working_hours > 8 then 'high workload (>8h)'
        else 'normal workload (<=8h)'
    end;

--Does tea consumption increase office hours?
select 
    case 
        when o.hours_worked > 8 then 'overtime day (>8h)'
        else 'normal day (<=8h)'
    end as workday_type,
    count(*) as recorded_days,
    round(avg(f.tea_coffee_count), 1) as avg_tea_consumed
from 
    office_logs o
join 
    food_logs f on o.daily_log_id = f.daily_log_id
group by 
    case 
        when o.working_hours > 8 then 'overtime day (>8h)'
        else 'normal day (<=8h)'
    end;
