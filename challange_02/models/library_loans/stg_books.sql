with fact_ids as (select distinct book_id, book_name from books_factual where book_id is not null),
fict_ids as (select distinct book_id, book_name from books_fictional  where book_id is not null)
select * from fact_ids union select * from fict_ids