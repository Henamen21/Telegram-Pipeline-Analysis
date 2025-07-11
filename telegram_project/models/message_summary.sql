-- models/message_summary.sql
SELECT
    channel_name,
    COUNT(*) AS message_count,
    MIN(message_date) AS first_message,
    MAX(message_date) AS latest_message
FROM raw.telegram_messages
GROUP BY channel_name
ORDER BY message_count DESC
