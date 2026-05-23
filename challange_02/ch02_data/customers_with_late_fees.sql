WITH CTE AS (
    SELECT
        COALESCE(FAC.book_name, FIC.book_name) as book_name,
        M.member_name,
        M.discount_rate/100 as discount_applied,
        SUM(L.late_fee * (M.discount_rate/100)) as fee_applied
    FROM members AS M 
        INNER JOIN loans AS L ON M.member_id = L.member_id
        LEFT JOIN books_factual AS FAC ON FAC.book_id=L.book_id
        LEFT JOIN books_fictional AS FIC ON FIC.book_id=L.book_id
    GROUP BY 1,2,3
)
SELECT 
member_name,
string_agg(book_name::text, ',') as late_books,
discount_applied,
ROUND(SUM(fee_applied),2) as fee_to_pay
FROM CTE
GROUP BY 1,3;