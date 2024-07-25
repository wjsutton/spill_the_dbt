SELECT *
FROM {{ source("library", "members") }}
WHERE member_id IS NOT NULL
AND membership_tier IN ('Bronze', 'Silver', 'Gold')