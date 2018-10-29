from flask import render_template, flash, redirect, request, jsonify, escape, Response
from app import app
from .forms import IndicatorForm
from config import TTL_VALUES, DATA_TYPES, DIRECTIONS, SOURCES, VALIDATE
from .models import Indicator, db
from .my_datatables import ColumnDT, DataTables
from sqlalchemy.exc import IntegrityError
import re


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/indicator/add', methods=['GET', 'POST'])
def mitigation_add():
    form = IndicatorForm()
    form.data_type.choices = [(val, val) for val in DATA_TYPES]
    form.ttl.choices = [(val, val) for val in TTL_VALUES]
    form.source.choices = [(val, val) for val in SOURCES]
    form.direction.choices = [(val, val) for val in DIRECTIONS]
    if form.validate_on_submit():

        ind = Indicator(value=form.value.data,
                        source=form.source.data,
                        ttl=form.ttl.data,
                        data_type=form.data_type.data,
                        direction=form.direction.data,
                        details=form.details.data)
        print ind
        #try:
        db.session.add(ind)
        db.session.commit()
        flash('"%s" indicator submitted, Source=%s' % (form.value.data, form.source.data))
        #except IntegrityError:
            #flash('Failed Insert, Duplicate Record')
            #db.session.rollback()
        return redirect('/indicator/add')
    return render_template('indicator_add.html', title='Add Indicator', form=form)


@app.route('/indicator/edit/<int:_id>', methods=['GET', 'POST'])
def indicator_edit(_id):
    i = Indicator.query.get(_id)
    form = IndicatorForm(obj=i)
    form.data_type.choices = [(val, val) for val in DATA_TYPES]
    form.ttl.choices = [(val, val) for val in TTL_VALUES]
    form.source.choices = [(val, val) for val in SOURCES]
    form.direction.choices = [(val, val) for val in DIRECTIONS]
    if form.validate_on_submit():
        form.populate_obj(i)
        try:
            db.session.commit()
            flash('"%s" indicator submitted, Source=%s' % (form.value.data, form.source.data))
        except IntegrityError, e:
            flash('Failed Update, Error=%s' % e)
            db.session.rollback()
        return redirect('/index')
    return render_template('indicator_edit.html', title='Edit Indicator', form=form, indicator=i)


@app.route('/indicator/data')
def indicator_data():
    """Return server side data."""
    # defining columns
    columns = []
    columns.append(ColumnDT('id'))
    columns.append(ColumnDT('value'))
    columns.append(ColumnDT('data_type'))
    columns.append(ColumnDT('source'))
    columns.append(ColumnDT('direction'))
    columns.append(ColumnDT('ttl'))
    columns.append(ColumnDT('created'))

    base_query = db.session.query(Indicator)

    rowTable = DataTables(request.args, Indicator, base_query, columns)

    # xss catch just to be safe
    res = rowTable.output_result()
    for item in res['data']:
        for k, v in item.iteritems():
            item[k] = escape(v)

    return jsonify(res)


@app.route('/indicator/getlist/<data_type>')
def indicator_getlist(data_type):
    if not (data_type in DATA_TYPES):
        raise Exception("Bad Values")

    query = db.session.query(Indicator).filter(Indicator.data_type == data_type)

    res = [item.as_dict() for item in query.all()]
    return jsonify(res)


@app.route('/indicator/getioc/<data_type>/<value>')
def indicator_getioc(data_type, value):
    if not (data_type in DATA_TYPES):
        raise Exception("Bad Values")

    rex = VALIDATE.get(data_type)
    if rex and not re.search(rex, value):
        raise Exception("Value doesn't match data_type")

    query = db.session.query(Indicator)\
        .filter(Indicator.value == value)\
        .filter(Indicator.data_type == data_type)

    res = [item.as_dict() for item in query.all()]
    return jsonify(res)