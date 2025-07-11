{{ config(materialized='table') }}

WITH base AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
)

SELECT
    b.message_id,
    d.date AS message_date,
    c.channel_id,
    b.message_text,
    b.message_length,
    b.has_media
FROM base b
JOIN {{ ref('dim_dates') }} d ON b.message_date = d.date
JOIN {{ ref('dim_channels') }} c ON b.channel_name = c.channel_name
