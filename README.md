# finanzas_web_app_flask
Desarrollo de una pagina web utilizando el framework de Flask, para el curso de Finanzas.

## Getting Started
Para poder desarrollar el proyecto, antes debemos de seguir algunos pasos para configurar un ambiente con todas
las dependencias necesarias, y que de esta manera, no tengamos problemas al momento de ejecutarlo localmente.

### Prerequisitos

Primero que nada, se debe de tener instalado Conda en el ordenador donde se desplegará este proyecto. Para ello, 
puede guiarse de la documentación oficial haciendo click [aquí](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Una vez ya se tenga Conda instalado, podemos continuar con la instalación.

### Instalación 

1. Iniciaremos con la clonación del repositorio:
```sh
   git clone https://github.com/aelvismorales/finanzas_web_app_flask.git
   cd finanzas_web_app_flask/
```
2. Crearemos un ambiente con Conda de la siguiente manera:
 ```sh
   conda create --name finanzas-api python=3.9
 ```
3. Ya que tengamos las varaibles de entorno configuradas, procederemos a reactivarlo con los siguientes comandos:
 ```sh
   conda deactivate
   conda activate finanzas-api
 ```
4. Luego, continuamos con la instalación de las dependencias necesarias, las cuales 
 ya se encuentran en el archivo **requirements.txt**, por lo que solo tendríamos que aplicar el siguiente comando:
 ```sh
   pip install -r requirements.txt
 ```
 
 ## Uso
 Cuando ya tengamos el ambiente creado y configurado con las dependencias, ya podremos realizar
 las modificaciones pertinentes. Asimismo, se podrá realizar la ejecución del proyecto con el comando:
  ```sh
   flask run
  ```
