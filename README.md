# SPRDE
Sistema para la revisión de exámenes con el uso de una RNA - CNN 

## Comenzando

Estas instrucciones te permitirán ejecutar el sistema
### Pre-requisitos

* Tener Python previamente instalado
* Conocimientos básicos de Python

### ¿Como ejecutar el sistema de revisión de exámenes sin generar problemas con otros posibles proyectos que tengo? 🔧

Para ello se instala pipenv, el que como su página menciona *"automáticamente crea y maneja un entorno virtual para tus proyectos, también como agregar/remover paquetes desde tu Pipfile como instalar/desinstalar paquetes. También genera el más importante Pipfile.lock, que es usado para producir determinado build."* El *pipfile.lock* será el usado para la instalación de las librerías/paquetes necesarias para la correcta ejecución del sistema.

### Pasos a seguir:

Estos son los comandos a seguir para instalar **PIPENV** y hacer uso de pipfile.lock del sistema para la instalación de los paquetes:
#### Instalación de "**PPENV**" teniendo Python previamente instalado:

```
pip install pipenv
```
#### Generar entorno virtual

```
pipenv shell
```
#### Instalación de paquetes usando el archivo **pipfile.lock**

```
pipenv install --dev --ignore-pipfile
```
El entorno para el sistema está listo para ser ejecutado, solo cuando estés dentro del entorno virtual, el cual debes de activar cada vez que necesites ejecutar el sistema usando *pipenv shell* y luego *py SI.py*
## Autor

* **Tristán Huerta** - *Sistema Web* - [trinat00](https://github.com/trinat00)
