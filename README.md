Demonstration of ORM bug.

1. `python manage.py migrate`
2. `python ./bug.py`

Observe that the SQL query is

```sql
SELECT
    "demo_classroom"."id"
FROM
    "demo_classroom"
WHERE
(
    NOT (
        EXISTS (
            SELECT
                1 AS "a"
            FROM
                "demo_classroom" U0 "demo_student" U1
            WHERE
                (
                    U1."id" = 4
                    AND U1."classroom_id" = ("demo_classroom"."id")
                    AND U0."school_id" IN (1)
                )
            LIMIT
                1
        )
    )
    AND "demo_classroom"."school_id" IN (1)
)
```

Which is invalid - note the missing comma in the subquery's FROM clause
