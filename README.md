# Proyecto de creacion de una IA en local

Voy a tratar de serguir los pasos de varios turoriales que encontré para añadir una IA a nuestros proyectos de forma local sin acceso a internet. Sera menos eficiente que las que encontramos pero vamos a ver hasta donde llegamos.

Una vez finalizado comentaré resultado.

Desarrollado con Python

Inicio::

-Instalar ollma (codespace(linux))

Visitar la web de Ollama -Download -Linux -->

curl -fsSL https://ollama.com/install.sh | sh 



Ver comandos: (en la terminal) ollama

    Comandos:
 
 Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  signin      Sign in to ollama.com
  signout     Sign out from ollama.com
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.

Seguimos instalando ollama serve

Visitamos de nuevo la web de Ollama -Models y buscamos llama3.2 (o última versión)

Instalamos en una nueva terminal --->

ollama pull llama3.2

Comprobar la instalacioncon : --> ollama list

nos deberia aparecer:
NAME               ID              SIZE      MODIFIED           
llama3.2:latest    a80c4f17acd5    2.0 GB    About a minute ago 

Para iniciar la IA de en la terminal:

ollama run llama3.2