SELECT
    nameproject,
    SFull_name,
    SGroup,
    TFull_name, Date_of_protection,
    The_received_assessment
FROM
    student
        JOIN
    sproject ON Creditbook = SCreditbook
        JOIN
    teacher using (TAccount_number)
WHERE
    YEAR(Date_of_protection) = 2020
        AND MONTH(Date_of_protection) = 5
