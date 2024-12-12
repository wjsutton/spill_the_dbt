SELECT 
	T.name as theme_name,
	S.name as set_name,
	S.year as set_year,
	CASE 
		WHEN UP.part_num IS NULL THEN 'Not Unique' 
		ELSE 'Unique' 
	END as unique_part,
	COUNT(P.part_num) as parts
FROM parts as P
LEFT JOIN {{ ref('unique_parts') }} as UP on P.part_num = UP.part_num
INNER JOIN inventory_parts as IP on P.part_num = IP.part_num
INNER JOIN inventories as I on I.id = IP.inventory_id
INNER JOIN sets as S on S.set_num = I.set_num
INNER JOIN themes as T on T.id = S.theme_id
GROUP BY 1,2,3,4