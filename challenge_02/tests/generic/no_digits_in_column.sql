{% test no_digits_in_column(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} LIKE '%0%'
    OR {{ column_name }} LIKE '%1%'
    OR {{ column_name }} LIKE '%2%'
    OR {{ column_name }} LIKE '%3%'
    OR {{ column_name }} LIKE '%4%'
    OR {{ column_name }} LIKE '%5%'
    OR {{ column_name }} LIKE '%6%'
    OR {{ column_name }} LIKE '%7%'
    OR {{ column_name }} LIKE '%8%'
    OR {{ column_name }} LIKE '%9%'
{% endtest %}