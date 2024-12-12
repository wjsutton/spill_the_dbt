SELECT 
	P.part_num
FROM parts as P
INNER JOIN inventory_parts as IP on P.part_num = IP.part_num
INNER JOIN inventories as I on I.id = IP.inventory_id
INNER JOIN sets as S on S.set_num = I.set_num
	GROUP BY P.part_num
	HAVING COUNT(*) = 1