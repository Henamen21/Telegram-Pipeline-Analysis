-- models/staging/stg_yolo_detections.sql


{{ config(materialized='view') }}

SELECT
    message_id::BIGINT as Message_Id,
    detected_object_class,
    confidence_score
FROM {{ source('raw', 'yolo_detections') }}