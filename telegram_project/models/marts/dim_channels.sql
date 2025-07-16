{{ config(materialized='table') }}

SELECT 
    t."Channel", 
    AVG(y."confidence_score") AS avg_confidence
FROM 
    {{ ref('stg_telegram_messages') }}  t
JOIN 
    {{ ref('stg_yolo_detections') }} y 
ON 
    t."Message_Id" = y."Message_Id"
GROUP BY 
    t."Channel"