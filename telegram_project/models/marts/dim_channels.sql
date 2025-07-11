{{ config(materialized='table') }}

SELECT DISTINCT
    Channel,
    md5(Channel) AS channel_id
FROM {{ ref('stg_telegram_messages') }}
