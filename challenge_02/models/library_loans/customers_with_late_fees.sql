SELECT 
    member_name,
    string_agg(book_name::text, ',') as late_books,
    discount_applied,
    ROUND(SUM(fee_applied),2) as fee_to_pay
FROM {{ ref('customer_withdrawls') }}
GROUP BY 1,3