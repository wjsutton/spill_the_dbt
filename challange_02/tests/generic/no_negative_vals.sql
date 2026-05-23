{% test no_negative_vals(model, column_name) %}
  
with validation as (
  select 
    {{ column_name }} as val_field
  from
    {{ model }} 
),
validation_errors as (
  select val_field from validation where val_field < 0
)

select * from validation_errors

{% endtest %}