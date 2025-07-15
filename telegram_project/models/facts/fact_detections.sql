-- models/facts/fact_detections.sql
with messages as (
    select * from {{ ref('stg_telegram_messages') }}
),

detections as (
    select * from {{ ref('stg_yolo_detections') }}
),

joined as (
    select
        d.message_id,
        m.channel_name,
        m.message_date,
        d.detected_object_class,
        d.confidence_score,
        m.message_text
    from detections d
    left join messages m on d.message_id = m.message_id
)

select * from joined
