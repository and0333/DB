from flask import Blueprint, render_template, request, current_app
from work_with_db import select_dict, call_proc
from sql_provider import SQLProvider
from access import group_required, login_required
import os

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/work')
@login_required
@group_required
def work_with_reports():
    config = current_app.config['report_config']
    return render_template('report_menu.html', conf=config, key_list=config.keys())


@blueprint_report.route('/for_date/<proc>/<sql>', methods=['GET', 'POST'])
@login_required
@group_required
def create_report(proc, sql):
    if request.method == 'GET':
        return render_template('report_input.html')
    else:
        year_ = request.form.get('year')
        month_ = request.form.get('month')
        print(month_, year_)
        if (not year_) and (not month_):
            return render_template('report_input.html', error='Недостаточно входных данных')
        else:
            year_ = request.form.get('year')
            month_ = request.form.get('month') #Спросить у никиты
            print(month_, year_)
            _sql = provider.get(sql, month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)
            if not res:
                temp = call_proc(current_app.config['db_config'], proc, year_, month_)
                _sql = provider.get(sql, month_=month_, year_=year_)
                res = select_dict(current_app.config['db_config'], _sql)
                if res:
                    return render_template('report.html', sql=sql, msg='Отчёт успешно создан', y=year_, m=month_)
                else:
                    return render_template('report_input.html',
                                           error='Невозможно создать отчёт по указанному периоду. Недостаточно данных')
            else:
                print(1)
                return render_template('report.html', sql=sql, msg='Отчёт уже присутствует', y=year_, m=month_)


@blueprint_report.route('/report_show/<sql>', methods=['GET', 'POST'])
@login_required
@group_required
def report_show(sql):
    if 'year' in request.args.keys() and 'month' in request.args.keys():
        _sql = provider.get(sql, month_=request.args['month'], year_=request.args['year'])
        res = select_dict(current_app.config['db_config'], _sql)
        if res:
            return render_template('dynamic.html', result=res, key_list=res[0].keys())
    if request.method == 'GET':
        return render_template('report_input.html')
    else:
        year_ = request.form.get('year')
        month_ = request.form.get('month')
        if (not year_) and (not month_):
            return render_template('report_input.html', error='Недостаточно входных данных')
        else:
            year_ = request.form.get('year')
            month_ = request.form.get('month')
            print(month_, year_)
            _sql = provider.get(sql, month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)
            if res:
                return render_template('dynamic.html', result=res, key_list=res[0].keys())
            else:
                return render_template('report_input.html', error='Отчёт по данному периоду не существует')
