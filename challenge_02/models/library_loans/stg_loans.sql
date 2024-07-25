
SELECT *
FROM {{ source("library", "loans") }}
WHERE loan_id IS NOT NULL
AND book_id IS NOT NULL
AND member_id IS NOT NULL
AND book_id IN (SELECT book_id FROM {{ ref('stg_books') }})
AND member_id IN (SELECT member_id FROM {{ ref('stg_members') }})