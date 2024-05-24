SELECT
    nameproject,
    SFull_name,
    SGroup,
    TFull_name,
    Date_of_protection,
    The_received_assessment
FROM
    workproject.student
        JOIN
    workproject.sproject ON Creditbook = SCreditbook
        JOIN
    workproject.teacher using (TAccount_number)
