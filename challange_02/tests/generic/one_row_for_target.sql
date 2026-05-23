{% test one_row_for_target(model, column_name) %}

with validation as (
    select {{ column_name }}, count(*) as occurance from {{ model }} group by {{ column_name }}
),
validation_errors as (
    select * from validation where occurance > 1 
)
select * from validation_errors

{% endtest %}