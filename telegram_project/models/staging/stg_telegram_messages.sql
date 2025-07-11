{{ config(materialized='view') }}

SELECT
    message_id,
    channel_name AS Channel,
    message_date AS Date,
    message_text AS Message_Text,
    json_data,
    jsonb_array_length(json_data->'text') AS text_length,
    json_data->>'has_media' = 'true' AS has_media
FROM {{ source('raw', 'telegram_messages') }}
