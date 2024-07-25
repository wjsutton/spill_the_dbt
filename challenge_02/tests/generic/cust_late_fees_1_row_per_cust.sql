{% test cust_late_fees_1_row_per_cust(model,column_name) %}
    SELECT {{ column_name }}
    FROM {{ model }}
    GROUP BY {{ column_name }}
    HAVING COUNT(DISTINCT {{ column_name }})>1
{% endtest %}