select
    report_year as 'Год',
    report_month as 'Месяц',
    TAccount_number as 'ID преподавателя',
    protection_count as 'Количество защит'
from workproject.report_protection
where report_year = "$year_" and report_month = "$month_"