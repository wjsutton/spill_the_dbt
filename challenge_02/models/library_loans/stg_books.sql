
    SELECT 
        book_id,
        location,
        book_name, 
        'Fact' as genre
    FROM {{ source("library", "books_factual") }}
    WHERE book_id IS NOT NULL

UNION 

    SELECT 
        book_id,
        location,
        book_name, 
        'Fiction' as genre
    FROM {{ source("library", "books_fictional") }}
    WHERE book_id IS NOT NULL


