# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import apps.authentication.models
from apps import db
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, select
from apps.authentication.models import Mociones
@blueprint.route('/index')
@login_required
def index():

    return render_template('home/mociones.html', segment='mociones')


@blueprint.route('/mociones.html', methods=['GET', 'POST'])
@login_required
def mociones_template():

    try:
        # Detect the current page
        segment = get_segment(request)
        ## ADD
        if 'Nombre' in request.form:
            Nombre = request.form['Nombre']
            PIN =  int(request.form['PIN'])
            Descripccion = request.form['Descripccion']
            stmt =Mociones(PIN=PIN,Mocion=Nombre,Description=Descripccion,Status='Open',Results='In Progress')
            db.session.add(stmt)
            db.session.commit()


        ## View

        stmt = Mociones.query.all()

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + segment, segment=segment,stmt=stmt)


    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



@blueprint.route('/lista.html')
@login_required
def lista_template():
    try:

        return render_template('home/lista.html')

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'mociones.html'

        return segment

    except:
        return None
