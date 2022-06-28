from turtle import title
from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_wtf.csrf import CSRFProtect
from modelos import Usuario,db,Bonos
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import formularios

app=Flask(__name__)


app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf=CSRFProtect(app)
csrf.init_app(app)

with app.app_context():
    db.create_all()

@app.before_request
def beforerequest():

    if 'username' in session and request.endpoint in ['login','create']:
        return redirect(url_for('index'))
    if 'username' not in session and request.endpoint in ['cuota']:
        return redirect(url_for('index'))



@app.route('/cuota',methods=['GET','POST'])
def cuota():
    frecuencia_cupon_form=formularios.DatosBono(request.form)
    if request.method=='POST' and frecuencia_cupon_form.validate():

        valor_nominal=frecuencia_cupon_form.valor_nominal.data
        valor_comercial=frecuencia_cupon_form.valor_comercial.data
        n_anios=frecuencia_cupon_form.n_anios.data
        frecuencia_cupon=frecuencia_cupon_form.frecuencia_cupon.data
        diasanio=int(frecuencia_cupon_form.diasanio.data)
        tipo_tasa=frecuencia_cupon_form.tipo_tasa.data
        capitalizacion=frecuencia_cupon_form.capitalizacion.data
        tasa_interes=frecuencia_cupon_form.tasa_interes.data
        tasa_anual_dsct=frecuencia_cupon_form.tasa_anual_dsct.data
        imp_a_la_renta=frecuencia_cupon_form.imp_a_la_renta.data
        fecha_emision=frecuencia_cupon_form.fecha_emision.data
        prima=frecuencia_cupon_form.prima.data
        estructuracion=frecuencia_cupon_form.estructuracion.data
        colocacion=frecuencia_cupon_form.colocacion.data
        flotacion=frecuencia_cupon_form.flotacion.data
        cavali=frecuencia_cupon_form.cavali.data

        cartera_bono=Bonos(valor_nominal,valor_comercial,n_anios,tasa_interes,tasa_anual_dsct,imp_a_la_renta,fecha_emision,prima,\
            estructuracion,colocacion,flotacion,cavali,diasanio,tipo_tasa,capitalizacion,frecuencia_cupon)
        
        cartera_data,estructuracion,precio_actual,ratio_decision,indicadores=cartera_bono.cartera_bonos()
        return render_template('cuota.html',form=frecuencia_cupon_form,tables=[cartera_data.to_html(classes='data',header="true")],table=[estructuracion.to_html(classes='data',header="true")],title=estructuracion.columns.values,\
            tabla_precio=[precio_actual.to_html(classes='data',header="true")],tabla_ratio=[ratio_decision.to_html(classes='data',header="true")],\
                tabla_indicadores=[indicadores.to_html(classes='data',header="true")])
    else: 
        print("F")
    
    return render_template('cuota.html',form=frecuencia_cupon_form)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    user_form=formularios.LoginForm(request.form)
    if request.method=='POST' and user_form.validate():
        username=user_form.usern.data
        password=user_form.password.data

        usuario=Usuario.query.filter_by(username=username).first()

        if usuario is not None and usuario.verify_password(password):
            succes_message='Bienvenido {}'.format(user_form.usern.data)
            flash(succes_message)
            session['username']=username
            return redirect( url_for('index'))
        else:
            error_message='Usuario o contraseña no validos!'
            flash(error_message)
    else:
        print('Error en el formulario')
    return render_template('login.html',form=user_form)

@app.route('/create',methods=['GET','POST'])
def create_account():
    create_user_form=formularios.CreateAccount(request.form)


    if request.method=='POST' and create_user_form.validate():
        usuario=Usuario(create_user_form.username.data,
                        create_user_form.email.data,
                        create_user_form.password.data)


        db.session.add(usuario)
        db.session.commit()

        succes_message='Felicidades por registrarte {}'.format(create_user_form.username.data)
        flash(succes_message)
    else:
        print('Error en el la creacion')
    return render_template('create_account.html',form=create_user_form)
if __name__=='__main__':
    app.run(debug=True)