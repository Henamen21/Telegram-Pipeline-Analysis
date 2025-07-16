{{ config(materialized='view') }}

SELECT
    message_id::BIGINT as Message_Id,
    channel_name AS Channel,
    message_date:: timestamp AS Date,
    message_text AS Message_Text,
    jsonb_array_length(json_data->'text') AS text_length,
    json_data->>'has_media' = 'true' AS has_media
FROM {{ source('raw', 'telegram_messages') }}
