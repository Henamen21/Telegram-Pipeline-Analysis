{{ config(materialized='table') }}

SELECT
    cast(message_id as bigint) as message_id,
    detected_object_class,
    confidence_score
FROM {{ source('raw', 'yolo_detections') }}
