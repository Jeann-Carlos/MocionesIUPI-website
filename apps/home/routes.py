# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
import io
import random
import threading

import matplotlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from flask_restx import abort

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from apps import db
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from sqlalchemy import func, case
from apps.authentication.models import Mociones
from apps.authentication.models import Users
from apps.authentication.models import Mociones_Votos
from run import app


def closeMocion(PIN):
    with app.app_context():
        db.session.query(Mociones).filter_by(PIN=PIN).update({'Status': 'Closed'})
        vote = Votos()
        for Mocion_voto in db.session.query(Mociones_Votos).filter_by(Mocion_ID=PIN).all():
            vote.a_favor += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'A Favor', 1)], else_=None)))
                .scalar()
            )
            vote.en_contra += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'En Contra', 1)], else_=None)))
                .scalar()
            )
            vote.abstenido += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'Abstenido/a', 1)], else_=None)))
                .scalar()
            )

        max_vote = vote.abstenido
        result = 'Abstenido'
        if max_vote<vote.en_contra:
            max_vote = vote.en_contra
            result = 'En Contra'
        if max_vote<vote.a_favor:
            max_vote = vote.a_favor
            result = 'A Favor'

        db.session.query(Mociones).filter_by(PIN=PIN).update({'Results': f'{result}'})
        db.session.commit()

def time_Mocion(PIN,Time):


    t = threading.Timer(Time,closeMocion,[PIN])
    t.start()


class Votos:
    a_favor = 0
    en_contra = 0
    abstenido = 0

def format_mocion(stmt):
    lista_votos = []
    for mocion in stmt:
        if mocion is None:
            return stmt,lista_votos
        if len(mocion.Description) > 25:
            mocion.Description = mocion.Description[:25]
            mocion.Description += '...'
        if len(mocion.Mocion) > 15:
            mocion.Mocion = mocion.Mocion[:15]
            mocion.Mocion += '...'
        vote = Votos()
        for Mocion_voto in db.session.query(Mociones_Votos).filter_by(Mocion_ID=mocion.PIN).all():
            vote.a_favor += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'A Favor', 1)], else_=None)))
                .scalar()
            )
            vote.en_contra += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'En Contra', 1)], else_=None)))
                .scalar()
            )
            vote.abstenido += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'Abstenido/a', 1)], else_=None)))
                .scalar()
            )
        lista_votos.append(vote)
    return stmt, lista_votos

@blueprint.route('/mociones', methods=['GET', 'POST'])
@login_required
def mociones_template():
        # Detect the current page
        segment = get_segment(request)
        ## ADD
        if 'borrar' in request.args:
            Mociones.query.filter_by(PIN=int(request.args['borrar'])).delete()
            db.session.commit()
            stmt = Mociones.query.all()
            stmt, lista_votos = format_mocion(stmt)
            render_template("home/mociones.html", segment=segment, stmt=stmt, lista_votos=lista_votos, zip=zip)
        if 'Add' in request.form:
            try:
                if len(request.form['PIN'])!=6:
                    raise
                PIN = int(request.form['PIN'])
            except:
                PIN = random.randint(100000, 999999)

            if  Mociones.query.filter_by(PIN=PIN).first():
                Mociones.query.filter_by(PIN=PIN).delete()
            Nombre = request.form['Nombre']
            Descripccion = request.form['Descripccion']
            try:
                timer = request.form['Timer'].split(":")
                if len(timer) == 2:
                    time_Mocion(PIN=PIN, Time=int(timer[0]) * 60 + int(timer[1]))
                else:
                    time_Mocion(PIN=PIN, Time=int(timer[0]))
            except:
                timer = 0
                time_Mocion(PIN,timer)

            stmt = Mociones(PIN=PIN,Mocion=Nombre,Description=Descripccion,Status='Open',Results='In Progress')
            db.session.add(stmt)
            db.session.commit()
        ## View
        stmt = Mociones.query.all()
        stmt,lista_votos = format_mocion(stmt)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/mociones.html", segment=segment,stmt=stmt,lista_votos=lista_votos,zip=zip)






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



def create_plot(vote,Mocion_name):
    plt.figure(figsize=(15, 10))
    categories = ['A Favor', 'En Contra', 'Abstenido/a']
    plt.title(f'{Mocion_name} Votes')
    plt.xlabel('Vote Quantity')
    plt.ylabel('Vote Type')
    plt.barh(categories, [vote.a_favor, vote.en_contra, vote.abstenido])
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return plot_url

@blueprint.route('mociones/view/<PIN>')
@login_required
def view_mociones(PIN):
    segment = get_segment(request)
    for Mocion_data in db.session.query(Mociones).filter_by(PIN=PIN):
        vote = Votos()
        for Mocion_voto in db.session.query(Mociones_Votos).filter_by(Mocion_ID=Mocion_data.PIN).all():
            vote.a_favor += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'A Favor', 1)], else_=None)))
                .scalar()
            )
            vote.en_contra += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'En Contra', 1)], else_=None)))
                .scalar()
            )
            vote.abstenido += (
                db.session.query(func.count(case([(Mocion_voto.Voto == 'Abstenido/a', 1)], else_=None)))
                .scalar()
            )
        plot_url = create_plot(vote,Mocion_data.Mocion)
        return render_template("home/billing.html",segment=segment, Mocion_data=Mocion_data,Mocion_voto=vote,plot_url=plot_url)
    # else:
    #     for Mocion in db.session.query(Mociones).filter_by(PIN=PIN):
    #         Mocion_data = Mocion
    #         return render_template("home/billing.html", segment=segment, Mocion_data=Mocion_data)

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

def recieve_encrypted_message(key,encrypted_priv_key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_priv_key = unpad(cipher.decrypt(encrypted_priv_key), AES.block_size)
    return decrypted_priv_key

@blueprint.route('/vote',methods=['GET', 'POST'])
def get_vote():
    priv_key = b'MOCIONES_IUPI'
    if 'privKey_encrypt' not in request.args:
        return 'not acknowledge'
    if 'PIN' not in request.args:
        return 'not acknowledge'
    if 'votos' not in request.args:
        return 'not acknowledge'
    if 'Token' not in request.args:
        return 'not acknowledge'
    PIN = request.args['PIN']
    for Mocion in db.session.query(Mociones).filter_by(PIN=PIN):
        if Mocion.Status == 'Open':
            privKey_encrypt = request.args['privKey_encrypt']
            votes = request.args['votos']
            Token = request.args['Token']
            if priv_key!=recieve_encrypted_message(priv_key,privKey_encrypt):
                return 'not acknowledge'
            for alreadyin in db.session.query(Mociones_Votos).filter_by(Token_Participante=Token, Mocion_ID=PIN):
                db.session.query(Mociones_Votos).filter_by(Token_Participante=Token, Mocion_ID=PIN).update({'Voto': votes})
                db.session.commit()
                return 'acknowledge'
            stmt = Mociones_Votos(Mocion_ID=PIN, Token_Participante=Token, Voto=votes, Email_Votante='NULL',
                                  Nombre_Votante='NULL')
            db.session.add(stmt)
            db.session.commit()
            return 'acknowledge'
    return 'Motion is closed'










# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'mociones'

        return  segment.split(".")[0]

    except:
        return None
