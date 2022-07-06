##Light Load

Es la versión inicial, hipoteticamente soporta menos 50 usuarios
concurrente

 - Esta diseñado con flask, requests y waitress
 - Se administra un pipenv
 - Se recomienda screen para dejar el proceso en segundo plano
 
##Heavy Load

(TO-Do) Esta versión es para cargas superiores a 50 usuarios
concurrentes

 - Esta diseñado con sanic y requests
 - Se administra con pipenv
 - Se recomienda screen para dejar el proceso en segundo plano

## Install on raspberry pi

Instalar en la raspberry tiene sus propios retos  se recomienda
instalar hostapp, screen, dnsmasq, pipenv

## How to run

Para correr propiamente se ejecuta como

screen -dmS Gateway pipenv run main.py 

dentro de la carpeta Light_Load o Heavy_Load (To-Do)
