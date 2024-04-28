# API Shopping

Este projeto foi desenvolvido para atender o projeto MVP da Disciplina **Desenvolvimento Back End Avançado** 

O objetivo aqui é demonstrar o aprendizado da disciplina Desenvolvimento Back End Avançado.

Para atender ao conceito de "key constraints" (restrições/limitações-chave) o back end está separado do front-end.


# ACESSO AO SWAGGER (COM CONTAINER DE DOCKER RODANDO):

http://localhost:5000/openapi/swagger#

# OPÇÃO COM DOCKER DESKTOP

# 1) Acessar a pasta:
cd C:\Users\felis\Documents\PUC\MVP_2_Final\Api   (Minha máquina)

# 2) Construir a imagem:

```
$ docker build -t nome_da_sua_imagem .
```
Exemplo: docker build -t back .

# 3) Executar o container:

```
$ docker run -d -p 8080:80 nome_da_sua_imagem
```

Exemplo: docker run --name projeto_back -d -p 5000:5000 back


# OPÇÃO PELO PYTHON COM ENV (AMBIENTE VIRTUAL):
---
## Como executar o projeto:

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

# 1- criar ambiente virtual (na pasta src). Execute os seguintes comandos:
```
>> python -m venv env (cria o ambiente com nome env)
```

# 2- acessar ambiente. Execute os seguintes comandos (\Api\src):
```
>> env\Scripts\activate (para acessar ambiente env criado)

deactivate (para sair)

```

# 3- instalar bibliotecas. Execute os seguintes comandos:
```
 (env)$ pip install -r requirements.txt (para instalar as bibliotecas necessárias para o projeto MVP) 
Nota: Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

ARQUIVO REQUIREMENT OBTIDO PELO COMANDO NO AMBIENTE ENV: pip freeze > requirements.txt
```

# 4- Finalmente para executar a API  basta executar:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
