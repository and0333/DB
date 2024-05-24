from flask import Blueprint, render_template, current_app, session, request
from work_with_db import select_dict
from sql_provider import SQLProvider
from access import group_required, login_required
import os

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/menu_query', methods=['GET', 'POST'])
@group_required
@login_required
def query_menu():
    if request.method == 'GET':
        return render_template('menu_query.html')


@blueprint_query.route('/query_students_by_group', methods=['GET', 'POST'])
@group_required
@login_required
def query_students_by_group():
    if request.method == 'GET':
        return render_template('input.html', SGroup='-')
    else:
        SGroup = request.form.get('group')
        print(SGroup)
        _sql = provider.get('students_by_group.sql', SGroup=SGroup)
        res = select_dict(current_app.config['db_config'], _sql)
        print(res)
        if res:
            return render_template('dynamic.html', result=res, key_list=res[0].keys())
        else:
            return render_template('input.html', SGroup='-', error='Группа не найдена')


@blueprint_query.route('/project_by_name_of_student', methods=['GET', 'POST'])
@group_required
@login_required
def query_project_by_name_of_student():
    if request.method == 'GET':
        return render_template('input.html', SFull_name='-')
    else:
        SFull_name = request.form.get('full_name')
        print(SFull_name)
        _sql = provider.get('project_by_name_of_student.sql', SFull_name=SFull_name)
        res = select_dict(current_app.config['db_config'], _sql)
        print(res)
        if res:
            return render_template('dynamic1.html', result=res, key_list=res[0].keys())
        else:
            return render_template('input.html', SFull_name='-', error='Студент не найден')


@blueprint_query.route('/project_by_name_of_teacher', methods=['GET', 'POST'])
@group_required
@login_required
def query_project_by_name_of_teacher():
    if request.method == 'GET':
        return render_template('input.html', TFull_name='-')
    else:
        TFull_name = request.form.get('teacher_name')
        print(TFull_name)
        _sql = provider.get('project_by_teacher.sql', TFull_name=TFull_name)
        res = select_dict(current_app.config['db_config'], _sql)
        print(res)
        if res:
            return render_template('dynamic1.html', result=res, key_list=res[0].keys())
        else:
            return render_template('input.html', TFull_name='-', error='Преподаватель не найден')


@blueprint_query.route('/all_products')
@login_required
@group_required
def all_products():
    _sql = provider.get('all_products.sql')
    res = select_dict(current_app.config['db_config'], _sql)
    if res:
        return render_template('dynamic1.html', result=res, key_list=res[0].keys())


@blueprint_query.route('/all_providers')
@login_required
@group_required
def all_providers():
    _sql = provider.get('all_providers.sql')
    res = select_dict(current_app.config['db_config'], _sql)
    if res:
        return render_template('dynamic1.html', result=res, key_list=res[0].keys())
