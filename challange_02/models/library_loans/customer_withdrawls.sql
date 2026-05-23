SELECT
    BKS.book_name as book_name,
    M.member_name,
    M.discount_rate/100 as discount_applied,
    SUM(L.late_fee * (M.discount_rate/100)) as fee_applied
FROM {{ source('library','members') }} AS M 
    INNER JOIN {{ source('library','loans') }} AS L ON M.member_id = L.member_id
    LEFT JOIN {{ ref('stg_books') }} AS BKS ON BKS.book_id=L.book_id
GROUP BY 1,2,3