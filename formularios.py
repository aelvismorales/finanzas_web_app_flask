from tokenize import Comment
from wsgiref.validate import validator
from click import command
from wtforms import Form,SelectMultipleField
from wtforms import StringField,TextField,PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Length,ValidationError
from wtforms import HiddenField
from modelos import Usuario

def length_honey_port(form,field):
    if len(field.data)>0:
        raise ValidationError('El campo debe estar vacio')

class CommentForm(Form):
    username=StringField('Username',validators=[Length(min=4,max=20,message='Ingrese un username valido!.'),DataRequired(message='El username es requerido!')])
    email=EmailField('Correo Electronico',validators=[DataRequired(message='El email es requerido!')])
    comment=TextField('comentario')
    honeypot=HiddenField('',[length_honey_port])

class LoginForm(Form):
    usern=StringField('username',validators=[DataRequired(message='El email es requerido!'),Length(min=4,max=20)])
    password=PasswordField('password',validators=[DataRequired()])
class CreateAccount(Form):
    username=TextField('Username',validators=[Length(min=4,max=30,message='Ingrese un username valido!.'),
    DataRequired(message='El username es requerido!')])
    email=EmailField('email',validators=[Length(min=4,max=50,message='Ingrese un email valido!.'),DataRequired(message='El email es requerido!')])
    password=PasswordField('password',validators=[DataRequired(message='Ingrese una contraseña'),
    Length(min=4,max=66,message="Escriba una contraseña valida")])

    def validate_username(form,field):
        username=field.data
        usuario=Usuario.query.filter_by(username=username).first()
        if usuario is not None:
            raise ValidationError("El username ya se encuentra registrado")
class cuota_inicial(Form):
    cuota=SelectMultipleField("Si-No",choices=[('yes','si'),('n','no')],validate_choice=True)
