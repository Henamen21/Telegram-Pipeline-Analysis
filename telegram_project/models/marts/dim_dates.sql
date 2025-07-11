{{ config(materialized='table') }}

WITH dates AS (
    SELECT DISTINCT message_date FROM {{ ref('stg_telegram_messages') }}
)

SELECT
    message_date AS date,
    extract(year FROM message_date) AS year,
    extract(month FROM message_date) AS month,
    extract(day FROM message_date) AS day,
    to_char(message_date, 'Day') AS day_name,
    CASE 
        WHEN extract(isodow FROM message_date) IN (6,7) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM dates
