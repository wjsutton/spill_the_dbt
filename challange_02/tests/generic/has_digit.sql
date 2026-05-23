{% test has_digit(model, column_name) %}

with validation as (
    select {{ column_name }} as validation_col from {{ model }} 
),
validation_errors as (
    select * from validation where validation_col like '%[0-9]%'
)
select * from validation_errors

{% endtest %}