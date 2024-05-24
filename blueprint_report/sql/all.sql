select
    report_year as 'Год',
    report_month as 'Месяц',
    prod_id as 'ID продукта',
    quantity as 'Количество',
    cost as 'Стоимость'
from supermarket.report
where report_year = "$year_" and report_month = "$month_"