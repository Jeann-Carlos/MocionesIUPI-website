# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import requests
from flask_restx import abort
from google.oauth2 import id_token

import apps.authentication.models
from apps import db
from apps.authentication.routes import flow, GOOGLE_CLIENT_ID
from apps.home import blueprint
from flask import render_template, request, jsonify, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, select
from apps.authentication.models import Mociones
from apps.authentication.models import Users
from pip._vendor import cachecontrol
import google.auth.transport.requests
from apps.authentication.models import Mociones_Votos

# @blueprint.route('/index')
# @login_required
# def index():
#
#     return render_template('home/mociones.html', segment='mociones')


@blueprint.route('/mociones', methods=['GET', 'POST'])
@login_required
def mociones_template():


        # Detect the current page
        segment = get_segment(request)
        ## ADD

        if 'borrar' in request.args:
            Mociones.query.filter_by(PIN=int(request.args['borrar'])).delete()
            db.session.commit()
        if 'Add' in request.form:

            if  Mociones.query.filter_by(PIN=int(request.form['PIN'])).first():
                Mociones.query.filter_by(PIN=int(request.form['PIN'])).delete()
                db.session.commit()
            Nombre = request.form['Nombre']
            PIN =  int(request.form['PIN'])
            Descripccion = request.form['Descripccion']
            stmt = Mociones(PIN=PIN,Mocion=Nombre,Description=Descripccion,Status='Open',Results='In Progress')
            db.session.add(stmt)
            db.session.commit()

        ## View
        stmt = Mociones.query.all()
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/mociones.html", segment=segment,stmt=stmt)






@blueprint.route('/lista')
@login_required
def lista_template():
    try:
        Usuarios = Users.query.order_by(Users.id).all()
        return render_template('home/lista.html',segment=get_segment(request),Usuarios=Usuarios)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('mociones/view/<PIN>')
@login_required
def view_mociones(PIN):
    segment = get_segment(request)
    for Mocion in db.session.query(Mociones_Votos, Mociones).join(Mociones).filter_by(PIN=PIN):
        Mocion_voto,Mocion_data = Mocion
        return render_template("home/billing.html",segment=segment, Mocion_data=Mocion_data,Mocion_voto=Mocion_voto)
    else:
        for Mocion in db.session.query(Mociones).filter_by(PIN=PIN):
            Mocion_data = Mocion
            return render_template("home/billing.html", segment=segment, Mocion_data=Mocion_data)

    return  abort(500)



@blueprint.route('/send',methods=['GET', 'POST'])
def send_mociones():
    if 'PIN' in request.args:
        PIN = request.args['PIN']
        for Mocion in db.session.query(Mociones).filter_by(PIN=PIN):
                stmt = Mocion
                return stmt.as_dict()
        return{
            'Error': 'No hay mocion con ese PIN.'
        }
    else:
        return {
            'Error': 'No hay atributo PIN encontrado.'
        }

@blueprint.route('/vote/<PIN>',methods=['GET', 'POST'])
def get_vote(PIN):
    flow.fetch_token(authorization_response=request.url)
    if not session["state"]== request.args["state"]:
        abort(500)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    if 'Voto' in request.args:
        stmt = Mociones(Mocion_ID=PIN, Nombre_Votante=Nombre, Description=Descripccion, Status='Open', Results='In Progress')







# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'mociones'

        return  segment.split(".")[0]

    except:
        return None
