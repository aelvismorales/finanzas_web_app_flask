from wtforms import Form
from wtforms import StringField,TextField,PasswordField,IntegerField,SelectField,FloatField,DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Length,ValidationError,NumberRange
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

class DatosBono(Form):
    valor_nominal=IntegerField("valor nominal : 1000",validators=[DataRequired(),NumberRange(0,message="El monto mas bajo es 0")])
    valor_comercial=IntegerField("valor comercial : 1000",validators=[DataRequired(),NumberRange(0,message="El monto mas bajo es 0")])
    n_anios=IntegerField("Num años : 1",validators=[DataRequired(),NumberRange(0,message="El valor mas bajo es 0")])
    frecuencia_cupon=SelectField(u'Frecuencia del cupon',choices=[('mensual','mensual'),('bimestral','bimestral'),\
        ('trimestral','trimestral'),('cuatrimestral','cuatrimestral'),('semestral','semestral'),('anual','anual')],validate_choice=True)
    diasanio=SelectField(u'Total de dias',choices=[(360,360),(365,365)])
    tipo_tasa=SelectField(label='Tipo de Tasa',choices=[('Efectiva','Efectiva'),('Nominal','Nominal')])
    capitalizacion=SelectField(label='Capitalizacion',choices=[('diario','diario'),('quincenal','quincenal'),\
        ('mensual','mensual'),('bimestral','bimestral'),('trimestral','trimestral'),('cuatrimestral','cuatrimestral'),\
            ('semestral','semestral'),('anual','anual')])
    tasa_interes=FloatField("Tasa Interes : 0.08",validators=[DataRequired(),NumberRange(0,message="El valor minimo es 0")])
    tasa_anual_dsct=FloatField("Tasa Anual Descuento : 0.10",validators=[DataRequired(),NumberRange(0,message="El valor minimo es 0")])
    imp_a_la_renta=FloatField("Impuesto a la Renta : 0.3",validators=[DataRequired(),NumberRange(0,message="El valor minimo es 0")])
    fecha_emision=DateField(label='Fecha de Emision',format='%Y-%m-%d',render_kw={'placeholder': '2020-06-25 para Junio 25, 2022'},validators=[DataRequired()])
    prima=FloatField('Prima: 0.01',validators=[DataRequired(),NumberRange(0,message='Valor minimo 0')])
    estructuracion=FloatField('Estructuracion: 0.01',validators=[DataRequired(),NumberRange(0,message='Valor minimo 0')])
    colocacion=FloatField('Colocacion: 0.0025',validators=[DataRequired(),NumberRange(0,message='Valor minimo 0')])
    flotacion=FloatField('Flotacion: 0.0045',validators=[DataRequired(),NumberRange(0,message='Valor minimo 0')])
    cavali=FloatField('Cavali: 0.005',validators=[DataRequired(),NumberRange(0,message='Valor minimo 0')])
