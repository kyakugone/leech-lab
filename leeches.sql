WITH scored AS (
    SELECT
        subject_id,
        subject_type,
        GREATEST(meaning_incorrect, reading_incorrect) AS incorrect,
        NULLIF(LEAST(meaning_current_streak, reading_current_streak), 0) AS streak
    FROM review_statistics
)
SELECT characters, reading, meaning, incorrect, streak,
       ROUND(incorrect / POWER(streak, 1.5), 2) AS score
FROM scored
JOIN subjects ON subjects.id = scored.subject_id
WHERE incorrect >= 3
  AND incorrect / POWER(streak, 1.5) >= 1.0
ORDER BY score DESC
LIMIT 20;