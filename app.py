from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_wtf.csrf import CSRFProtect
from modelos import Usuario
#from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
import formularios

app=Flask(__name__)
app.config['SECRET_KEY']='123447a47f563e90fe2db0f56b1b17be62378e31b7cfd3adc776c59ca4c75e2fc512c15f69bb38307d11d5d17a41a7936789'
#app.config['DEBUG']=True
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://isnjonskuprehk:07d8bb3abcb665f2611cbf435a79c4dfeeac18604299189722d794802c1971fa@ec2-23-23-182-238.compute-1.amazonaws.com:5432/dbgnihpfcroaus'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#app.config.from_object(DevelopmentConfig)
#db=SQLAlchemy(app)
csrf=CSRFProtect(app)

#with app.app_context():
#    db.create_all()

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
@app.route('/create',methods=['GET','POST'])
def create_account():
    create_user_form=formularios.CreateAccount(request.form)
    #cuota=formularios.cuota_inicial(request.form)

    if request.method=='POST' and create_user_form.validate():
        usuario=Usuario(create_user_form.username.data,
                        create_user_form.email.data,
                        create_user_form.password.data)
        #print(cuota.cuota.data)

        #db.session.add(usuario)
        #db.session.commit()

        succes_message='Felicidades por registrarte {}'.format(create_user_form.username.data)
        flash(succes_message)
    else:
        print('Error en el la creacion')
    return render_template('create_account.html',form=create_user_form)
if __name__=='__main__':
    app.run(debug=True,port=8000)