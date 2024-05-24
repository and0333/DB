from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from work_with_db import select_dict, insert_into_db
from sql_provider import SQLProvider
from datetime import datetime
from access import group_required, login_required
from DBconn import DBContextManager

import os

blueprint_basket = Blueprint('bp_basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_basket.route('/', methods=['GET', 'POST'])
@group_required
@login_required
def choose():
    if request.method == 'GET':
        return render_template('comission_number.html')
    else:
        number = request.form.get('number')
        if number:
            return redirect(url_for('bp_basket.comission_config', number=number))
        else:
            return render_template('comission_number.html', error="Введите номер комиссии")


@blueprint_basket.route('/comission/<number>', methods=['GET', 'POST'])
@group_required
@login_required
def comission_config(number):
    db_config = current_app.config['db_config']
    print(session.keys())
    if 'basket' not in session.keys():
        session['basket'] = {}
        print(session.keys())
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        print(items)
        print(session)
        return render_template('comission_show.html', number=number, items=items, basket=session['basket'],
                               bask_keys=session['basket'].keys())
    else:
        TAccount_number = request.form.get('TAccount_number')
        sql = provider.get('add_item.sql', TAccount_number=TAccount_number)
        item = select_dict(db_config, sql)[0]
        print(TAccount_number)
        print(session)
        session['basket'][str(item['TAccount_number'])] = {'TFull_name': item['TFull_name'],
                                                           'Tposition': item['Tposition']}
        if not session.modified:
            session.modified = True
    return redirect(url_for('bp_basket.comission_config', number=number))


@blueprint_basket.route('/datetime/<number>', methods=['GET', 'POST'])
@group_required
@login_required
def comission_datetime(number):
    if len(session['basket']) > 0:
        if request.method == 'POST':
            print(session['basket'])
            return redirect(url_for('bp_basket.save_comission', number=number, basket=session['basket'],
                                    bask_keys=session['basket'].keys()))
        return redirect(url_for('bp_basket.save_comission', number=number))
    else:
        return redirect(url_for('bp_basket.comission_config', number=number))


@blueprint_basket.route('/save_comission/<number>', methods=['GET', 'POST'])
@group_required
@login_required
def save_comission(number):
    if request.method == 'GET':
        return render_template('datetime.html', number=number, basket=session['basket'],
                               bask_keys=session['basket'].keys())
    else:
        db_config = current_app.config['db_config']
        with DBContextManager(db_config) as cursor:
            if cursor:
                for key in session['basket'].keys():
                    item = session['basket'][key]
                    print(key)
                    print(item)
                    print(number)
                    sql = provider.get('insert_comission.sql', number=number, TAccount_number=key)
                    cursor.execute(sql)
                    date = request.form.get('date')
                    print(date)
                    time = request.form.get('time')
                    print(time)
                    hall = request.form.get('hall')
                    print(hall)
                    if (not date) or (not time) or (not hall):
                        return render_template('datetime.html', number=number, basket=session['basket'],
                                               bask_keys=session['basket'].keys(), error="Введены не все параметры")
                    sql = provider.get('insert_datetime.sql', number=number, date=date, time=time, hall=hall)
                    cursor.execute(sql)
            else:
                raise ValueError('Курсор не создан')

        session['basket'] = {}
        return render_template('done.html')


@blueprint_basket.route('/sec')
@login_required
@group_required
def menu():
    session.pop('basket')
    return redirect(url_for('main_menu'))


@blueprint_basket.route('/clear/<number>')
@login_required
@group_required
def clear_basket(number):
    session.pop('basket')
    return redirect(url_for('bp_basket.comission_config', number=number))
