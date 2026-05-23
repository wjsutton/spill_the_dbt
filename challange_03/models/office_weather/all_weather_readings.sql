{{ config(
    materialized='incremental',
    unique_key= 'generationtime_ms'  
) }}

select * from office_weather
{% if is_incremental() %}
where generationtime_ms > {{ this }}
{% endif %}