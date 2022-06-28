from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import pandas as pd
import numpy_financial as npf
import pyxirr
from datetime import datetime,date
db=SQLAlchemy()

class Usuario(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(40))
    password=db.Column(db.String(102))
    created_date=db.Column(db.DateTime,default=datetime.now)
    
    def __init__(self,username,email,password):
        self.username=username
        self.password=self.__create_password(password)
        self.email=email

    def __create_password(self,password):
        return generate_password_hash(password,"sha256")
        
    def verify_password(self,password):
        return check_password_hash(self.password,password)


def renta_bono(tep,c,n):
  return -c*(tep*pow((1+tep),n))/(pow(1+tep,n)-1)

class Bonos:
    def __init__(self,valor_nominal,valor_comercial,n_anios,tasa_interes,tasa_anual_dsct,imp_a_la_renta,fecha_emision,prima,\
            estructuracion,colocacion,flotacion,cavali,diasanio=360,tipo_tasa='efectiva',capitalizacion='diario',frecuencia_cupon='mensual',inflacion_proyectada=0.0,iep=0.0,plazo_gracia='s'):
        self.valor_nominal=valor_nominal
        self.valor_comercial=valor_comercial
        self.n_anios=n_anios
        self.frecuencia_cupon=frecuencia_cupon
        self.diasanio=diasanio
        self.tipo_tasa=tipo_tasa
        self.capitalizacion=capitalizacion
        self.tasa_interes=tasa_interes
        self.tasa_anual_dsct=tasa_anual_dsct
        self.imp_a_la_renta=imp_a_la_renta
        self.fecha_emision=fecha_emision
        self.prima=prima
        self.estructuracion=estructuracion
        self.colocacion=colocacion
        self.flotacion=flotacion
        self.cavali=cavali
        self.inflacion_proyectada=inflacion_proyectada
        self.iep=iep
        self.plazo_gracia=plazo_gracia
    
    def cartera_bonos(self):
        frecuencia_cupon_diccionario={'mensual':30,'bimestral':60,'trimestral':90,'cuatrimestral':120,'semestral':180,'anual':360}
        capitalizacion_diccionario={'diario':1,'quincenal':15,'mensual':30,'bimestral':60,'trimestral':90,'cuatrimestral':120,'semestral':180,'anual':360}
        
        self.frecuencia_cupon=frecuencia_cupon_diccionario[self.frecuencia_cupon]
        self.capitalizacion=capitalizacion_diccionario[self.capitalizacion]

        periodos_anio=int(self.diasanio/self.frecuencia_cupon)
        periodos_total=periodos_anio*self.n_anios

        if(self.tipo_tasa.lower()=="efectiva"):
            tasa_efec_anual=self.tasa_interes
        else:
            tasa_efec_anual=pow((1+self.tasa_interes/(self.diasanio/self.capitalizacion)),
                      (self.diasanio/self.capitalizacion))-1

        tasa_efec_periodo=pow((1+tasa_efec_anual),(self.frecuencia_cupon/self.diasanio))-1
        cok_periodo=pow((1+self.tasa_anual_dsct),(self.frecuencia_cupon/self.diasanio))-1
        costes_ini_emisor=(self.estructuracion+self.colocacion+self.flotacion+self.cavali)*self.valor_comercial
        costes_ini_bonista=(self.flotacion+self.cavali)*self.valor_comercial

        df_resultado_de_estructuracion=pd.DataFrame(index=['Frecuencia del cupon','Días capitalización','Nro. períodos por año',
                                                     'Nro. total de períodos','Tasa efectiva anual','Tasa efectiva del período',
                                                     'COK del período','Costes iniciales emisor','Costes iniciales bonista'],
                                            data=[round(self.frecuencia_cupon,0),round(self.capitalizacion,0),round(periodos_anio,0),round(periodos_total,0),
                                                  tasa_efec_anual,tasa_efec_periodo,cok_periodo,costes_ini_emisor,costes_ini_bonista],columns=['Resultado de la estructuración del bono'])
        df_resultado_de_estructuracion.style.format({
            'Tasa efectiva anual': '{:,.7%}'.format,
            'Tasa efectiva del período': '{:,.7%}'.format,
            'COK del período': '{:,.7%}'.format,
            'Costes iniciales emisor': '{:,.2f}'.format,
            'Costes iniciales bonista': '{:,.2f}'.format,

            })

        Cartera_De_bonos=[]
        saldo_final_bono=float('inf')
        n=0
        saldo_inicial_bono=self.valor_nominal
        tabla_bono=0.0
        while n<periodos_total:
            n=n+1
            if n<=periodos_total:
                if n==1:
                    tabla_bono=saldo_inicial_bono
                else:
                    tabla_bono=saldo_final_bono
                tabla_bono_indexado=tabla_bono*(1+self.iep)
                tabla_cupon=-tabla_bono_indexado*tasa_efec_periodo
                tabla_cuota=renta_bono(tasa_efec_periodo,tabla_bono_indexado,(periodos_total-n+1))
                tabla_amort=tabla_cuota-tabla_cupon
    
                if(n==periodos_total):
                    tabla_prima=-self.prima*tabla_bono_indexado
                else:
                    tabla_prima=0.0
                tabla_escudo=-tabla_cupon*self.imp_a_la_renta
                tabla_flujo_emisor=tabla_cuota+tabla_prima
                tabla_flujo_emisor_con_escudo=tabla_flujo_emisor+tabla_escudo
                tabla_flujo_bonista=-tabla_flujo_emisor
                tabla_flujo_act=tabla_flujo_bonista/pow((1+cok_periodo),n)
                tabla_fa_x_plazo=tabla_flujo_act*n*self.frecuencia_cupon/self.diasanio
                tabla_factor_x_convex=tabla_flujo_act*n*(1+n)
                saldo_final_bono=tabla_bono_indexado+tabla_amort

                Cartera_De_bonos.append([n,self.inflacion_proyectada,self.iep,self.plazo_gracia,round(tabla_bono,2),
                            round(tabla_bono_indexado,2),round(tabla_cupon,2),round(tabla_cuota,2),round(tabla_amort,2),
                            round(tabla_prima,2),round(tabla_escudo,2),round(tabla_flujo_emisor,2),round(tabla_flujo_emisor_con_escudo,2),
                            round(tabla_flujo_bonista,2),round(tabla_flujo_act,2),round(tabla_fa_x_plazo,2),round(tabla_factor_x_convex,2)
                            ])
        df = pd.DataFrame(Cartera_De_bonos,columns = ['Nro.','Inflación Anual','Inflación del periodo','Plazo de gracia','Bono',
                   'Bono Indexado','Cupón (Interes)','Cuota','Amort.','Prima','Escudo',
                   'Flujo Emisor','Flujo Emisor c/Escudo','Flujo Bonista','Flujo Act.',
                   'FA x Plazo','Factor p/Convexidad'])
        
        df.loc[len(df)] = [0,0,0,' ',0,0,0,0,0,0,0,0,0,0,0,0,0]
        df = df.shift()
        df.loc[0] = [0,0,0,' ',0,0,0,0,0,0,0,0,0,0,0,0,0]
        df['Nro.']=df['Nro.'].astype('int')
        df.loc[0, 'Flujo Emisor']=self.valor_comercial-costes_ini_emisor
        df.loc[0, 'Flujo Emisor c/Escudo']=df.loc[0, 'Flujo Emisor']
        df.loc[0, 'Flujo Bonista']=-self.valor_comercial-costes_ini_bonista
        
        NPV=0.0
        for n,x in enumerate(df['Flujo Bonista'][1:]):
            NPV=NPV+x/pow(1+cok_periodo,n+1)
        
        utilidad_perdida=df['Flujo Bonista'][0]+NPV

        df_resultado_del_precio_actual_utilidad=pd.DataFrame({'Precio actual'     :[NPV],
                                             'Utilidad pérdida'      :[utilidad_perdida]
                                             }
                                            ,index={'Resultado del precio actual y de utilidad'})

        df_resultado_del_precio_actual_utilidad.style.format({
        'Precio actual': '{:,.2f}'.format,
        'Utilidad pérdida': '{:,.2f}'.format
        })

        duracion=sum(df['FA x Plazo'][1:])/sum(df['Flujo Act.'][1:])
        convexividad=sum(df['Factor p/Convexidad'][1:])/(pow(1+cok_periodo,2)*sum(df['Flujo Act.'][1:])*pow(self.diasanio/self.frecuencia_cupon,2))

        total=duracion+convexividad
        duracion_modificada=duracion/(1+cok_periodo)
        df_resultado_del_ratio_desicion=pd.DataFrame({'Duración'            :[duracion],
                                              'Convexividad'        :[convexividad],
                                              'Total'               :[total],
                                              'Duracion modificada' :[duracion_modificada]
                                             }
                                            ,index={'Resultado del ratio de decisión'})
        df_resultado_del_ratio_desicion.style.format({
            'Duración': '{:,.2f}'.format,
            'Convexividad': '{:,.2f}'.format,
            'Total': '{:,.2f}'.format,
            'Duracion modificada': '{:,.2f}'.format
            })

        TCEA_emisor=pow(pyxirr.irr(list(df['Flujo Emisor']))+1,self.diasanio/self.frecuencia_cupon)-1
        TCEA_emisor_escudo=pow(pyxirr.irr(list(df['Flujo Emisor c/Escudo']))+1,self.diasanio/self.frecuencia_cupon)-1
        TCEA_bonista=pow(pyxirr.irr(list(df['Flujo Bonista']))+1,self.diasanio/self.frecuencia_cupon)-1

        fecha_deposito=pd.to_datetime(self.fecha_emision, format='%Y-%d-%m').date()
        fechas_deposito=pd.date_range(fecha_deposito, periods=periodos_total+1,freq='180D')
        fechas_xirr=[]
        for date in fechas_deposito:
            fechas_xirr.append(str(date.date()))

        TCEA_emisor_xirr=pyxirr.xirr(fechas_xirr,list(df['Flujo Emisor']))
        TCEA_emisor_escudo_xirr=pyxirr.xirr(fechas_xirr,list(df['Flujo Emisor c/Escudo']))
        TCEA_bonista_xirr=pyxirr.xirr(fechas_xirr,list(df['Flujo Bonista']))

        df_resultado__indicadores_rentabilidad=pd.DataFrame({'TCEA Emisor'            :[TCEA_emisor,TCEA_emisor_xirr],
                                              'TCEA Emisor c/Escudo'        :[TCEA_emisor_escudo,TCEA_emisor_escudo_xirr],
                                              'TREA Bonista'               :[TCEA_bonista,TCEA_bonista_xirr],
                                             }
                                            ,index={'IRR','XIRR'})

        df_resultado__indicadores_rentabilidad.style.format({
        'TCEA Emisor': '{:,.7%}'.format,
        'TCEA Emisor c/Escudo': '{:,.7%}'.format,
        'TREA Bonista': '{:,.7%}'.format
        })

        df['Fecha']= fechas_deposito
        
        return df,df_resultado_de_estructuracion,df_resultado_del_precio_actual_utilidad,df_resultado_del_ratio_desicion,df_resultado__indicadores_rentabilidad


