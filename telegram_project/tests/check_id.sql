select * 
from {{ ref('dim_channels') }}
where channel_id is NULL