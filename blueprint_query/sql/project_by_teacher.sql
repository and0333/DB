SELECT
    nameproject,
    SFull_name,
    SGroup,
    TFull_name,
    Date_of_protection,
    The_received_assessment
FROM
    student
        JOIN
    sproject ON Creditbook = SCreditbook
        JOIN
    teacher using (TAccount_number)
where TFull_name = '$TFull_name'