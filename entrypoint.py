from flask import Flask, redirect,render_template,url_for
from flask import request,flash,session
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from modelos import db,Usuario
import formularios


app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect(app)
csrf.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

#@app.before_request
#def beforerequest():
    #if 'username' not in session and request.endpoint in ['comment']:
    #    return redirect(url_for('login'))
    #if 'username' in session and request.endpoint in ['login','create']:
    #    return redirect(url_for('index'))
    #if 'username' in session and request.endpoint in ['login','create']:
    #    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

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
            return redirect( url_for('create_account'))
        else:
            error_message='Usuario o contraseña no validos!'
            flash(error_message)
    else:
        print('Error en el formulario')
    return render_template('login.html',form=user_form)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/create',methods=['GET','POST'])
def create_account():
    create_user_form=formularios.CreateAccount(request.form)
    #cuota=formularios.cuota_inicial(request.form)

    if request.method=='POST' and create_user_form.validate():
        usuario=Usuario(create_user_form.username.data,
                        create_user_form.email.data,
                        create_user_form.password.data)
        #print(cuota.cuota.data)

        db.session.add(usuario)
        db.session.commit()

        succes_message='Felicidades por registrarte {}'.format(create_user_form.username.data)
        flash(succes_message)
    else:
        print('Error en el la creacion')
    return render_template('create_account.html',form=create_user_form)

#@app.route('/si',methods=['GET','POST'])
#def create_account():
#    cuota=formularios.cuota_inicial(request.form)

#    if request.method=='POST' and cuota.validate():

        #print(cuota.cuota.data)
        #db.session.add(usuario)
        #db.session.commit()
        #succes_message='Felicidades por registrarte {}'.format(create_user_form.username.data)
 #       flash("succes_message")
 #   else:
  #      print('Error en el la creacion')
 #   return render_template('si_no.html',form=cuota)

if __name__=='__main__':
    #csrf.init_app(app)
   # db.init_app(app)
  #  with app.app_context():
  #      db.create_all()
        #db.session.commit()
    app.run(debug=True)
    