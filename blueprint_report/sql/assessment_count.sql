select
    report_year as 'Год',
    report_month as 'Месяц',
    assessment as 'Оценка',
    received_count as 'Количество'
from workproject.report_assessment
where report_year = "$year_" and report_month = "$month_"