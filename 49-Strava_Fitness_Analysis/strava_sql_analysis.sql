-- SQL Analysis for Strava Fitness Data

-- 1. Create tables and import data (run this in DB Browser for SQLite)
CREATE TABLE daily_steps (
    Id INTEGER,
    ActivityDay DATE,
    StepTotal INTEGER
);

CREATE TABLE sleep_data (
    Id INTEGER,
    SleepDay DATE,
    TotalSleepRecords INTEGER,
    TotalMinutesAsleep INTEGER,
    TotalTimeInBed INTEGER
);

CREATE TABLE weight_data (
    Id INTEGER,
    Date DATE,
    WeightKg REAL,
    WeightPounds REAL,
    Fat REAL,
    BMI REAL,
    IsManualReport BOOLEAN,
    LogId INTEGER
);

-- 2. Basic Data Exploration
SELECT 'Daily Steps' as Table_Name, COUNT(*) as Total_Records, COUNT(DISTINCT Id) as Unique_Users
FROM daily_steps
UNION ALL
SELECT 'Sleep Data', COUNT(*), COUNT(DISTINCT Id) FROM sleep_data
UNION ALL
SELECT 'Weight Data', COUNT(*), COUNT(DISTINCT Id) FROM weight_data;

-- 3. Average Steps by Day of Week
SELECT 
    CASE strftime('%w', ActivityDay)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END as DayOfWeek,
    ROUND(AVG(StepTotal), 0) as AvgSteps,
    COUNT(*) as RecordCount
FROM daily_steps
GROUP BY strftime('%w', ActivityDay)
ORDER BY strftime('%w', ActivityDay);

-- 4. User Activity Classification
WITH UserActivity AS (
    SELECT 
        Id,
        AVG(StepTotal) as AvgDailySteps,
        COUNT(*) as DaysRecorded
    FROM daily_steps
    GROUP BY Id
)
SELECT
    CASE 
        WHEN AvgDailySteps < 5000 THEN 'Sedentary'
        WHEN AvgDailySteps BETWEEN 5000 AND 7499 THEN 'Lightly Active'
        WHEN AvgDailySteps BETWEEN 7500 AND 9999 THEN 'Active'
        ELSE 'Very Active'
    END as ActivityLevel,
    COUNT(*) as UserCount,
    ROUND(AVG(AvgDailySteps), 0) as AvgStepsInCategory,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM UserActivity)), 1) as Percentage
FROM UserActivity
GROUP BY ActivityLevel
ORDER BY AvgDailySteps;

-- 5. Sleep Patterns Analysis
SELECT 
    CASE strftime('%w', SleepDay)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END as DayOfWeek,
    ROUND(AVG(TotalMinutesAsleep)/60, 1) as AvgSleepHours,
    ROUND(AVG(TotalTimeInBed)/60, 1) as AvgTimeInBedHours,
    ROUND((AVG(TotalMinutesAsleep) * 100.0 / AVG(TotalTimeInBed)), 1) as SleepEfficiency
FROM sleep_data
GROUP BY strftime('%w', SleepDay)
ORDER BY strftime('%w', SleepDay);

-- 6. Top Performers Analysis
SELECT 
    ds.Id,
    ROUND(AVG(ds.StepTotal), 0) as AvgDailySteps,
    COUNT(ds.ActivityDay) as DaysRecorded,
    ROUND(AVG(sd.TotalMinutesAsleep)/60, 1) as AvgSleepHours
FROM daily_steps ds
LEFT JOIN sleep_data sd ON ds.Id = sd.Id
GROUP BY ds.Id
HAVING AVG(ds.StepTotal) >= 10000
ORDER BY AvgDailySteps DESC
LIMIT 10;

-- 7. Data Completeness Analysis
SELECT 
    Id,
    COUNT(DISTINCT ActivityDay) as DaysWithSteps,
    (SELECT COUNT(DISTINCT ActivityDay) FROM daily_steps) as TotalPossibleDays,
    ROUND((COUNT(DISTINCT ActivityDay) * 100.0 / (SELECT COUNT(DISTINCT ActivityDay) FROM daily_steps)), 1) as CoveragePercentage
FROM daily_steps
GROUP BY Id
ORDER BY CoveragePercentage DESC;

-- 8. Correlation Analysis (Users with both steps and sleep data)
SELECT 
    ds.Id,
    ROUND(AVG(ds.StepTotal), 0) as AvgSteps,
    ROUND(AVG(sd.TotalMinutesAsleep), 0) as AvgSleepMinutes,
    ROUND(AVG(sd.TotalMinutesAsleep)/60, 1) as AvgSleepHours
FROM daily_steps ds
JOIN sleep_data sd ON ds.Id = sd.Id
GROUP BY ds.Id
ORDER BY AvgSteps DESC;