
#BIBLIOTECAS
from datetime import datetime
#from sqlalchemy.exc import IntegrityError
from models import Session
from logger import logger
from schemas import *
from flask_cors import CORS
import pytz
from flask_jwt_extended import JWTManager,jwt_required,get_jwt
from flask_jwt_extended import create_access_token,jwt_required, get_jwt
from hmac import compare_digest
from flask_openapi3 import OpenAPI, Info, Tag, request
from datetime import timedelta
import uuid
from flask import redirect,request
import jwt

#https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking.html

#Modelos
from models import PedidoModel,UserModel,ItemModel,TokenBlocklist
from models.pedido import PedidoModel
from models.usuario import UserModel

ACCESS_EXPIRES = timedelta(hours=1)

info = Info(title="API Shopping", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'NaoConteParaNinguem'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]

    # criando conexão com a base
    session = Session()
    # fazendo a busca

    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pedido_tag = Tag(name="Pedidos", description="Adição, visualização e remoção de pedidos na base")
tarefa_tag = Tag(name="Tarefa", description="Adição, visualização e remoção de tarefas na base")
usuarios_tag = Tag(name="Usuários", description="Registro, Login e Logout de usuários na base")
item_carinho_tag = Tag(name="Itens", description="Adição, visualização e remoção de itens no pedido")
acesso_tag = Tag(name="Acesso", description="Login, Cadastro e Logout de Usuários")
login_tag = Tag(name="Login", description="Acesso (Login)")
logout_tag = Tag(name="Logout", description="Saida (Logout)")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#https://stackoverflow.com/questions/76297834/how-to-pass-a-js-variable-as-a-parameter-to-a-python-function-and-store-python-o


@app.get('/listar_itens_carrinho', tags=[item_carinho_tag], responses={"200": ItemViewSchema, "404": ErrorSchema})

def listar_carrinho(query : SessaoSchema):
    """Lista os itens do carrinho da session_id
    """
    session_id = request.args.get("session_id", type=str)
    try:
        logger.info(f"Coletando Itens ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        itens = session.query(ItemModel).filter(ItemModel.session_id == session_id).filter(ItemModel.status_item == 0).all()

        if not itens:
            # se não há Pedidos cadastrados
            return {"Itens": []}, 200
        else:
            logger.info(f"%d itens econtrados" % len(itens))
            result = []
            for carrinho in itens:
                result.append({
                    "codigo_produto": carrinho.codigo_produto,
                    "session_id": carrinho.session_id,
                    "pedido_id": carrinho.pedido_id,
                    "titulo": carrinho.titulo,
                    "url_imagem": carrinho.url_imagem,
                    "quantidade": carrinho.quantidade,
                    "preco": carrinho.preco,
                    "valor_total_item": carrinho.valor_total_item
                })
            return {"itens": result},200
    except:
            return {"itens": []},401

@app.get('/listar_pedido_concluido', tags=[pedido_tag], responses={"200": ItemViewSchema, "404": ErrorSchema})

def listar_pedido_concluido(query : SessaoSchema):
    """Lista o pedido com os itens do carrinho da session_id
    """
    session_id = request.args.get("session_id", type=str)
    pedido_id = request.args.get("pedido_id", type=str)

    logger.info(f"Coletando Pedido")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        pedido = session.query(PedidoModel).filter(PedidoModel.session_id == session_id).filter(PedidoModel.id == pedido_id).first()
        itens = session.query(ItemModel).filter(ItemModel.session_id == session_id).filter(ItemModel.pedido_id == pedido_id).filter(ItemModel.status_item == 1).all()

        if  not pedido and not itens:
            # se não há Pedidos cadastrados
            return {"Pedido": 0,"Itens": []}, 200
        else:
            logger.info("pedido encontrado")
            logger.info(f"%d itens encontrados" % len(itens))
            result = []
            for carrinho in itens:
                result.append({
                    "codigo_produto": carrinho.codigo_produto,
                    "session_id": carrinho.session_id,
                    "pedido_id": carrinho.pedido_id,
                    "titulo": carrinho.titulo,
                    "url_imagem": carrinho.url_imagem,
                    "quantidade": carrinho.quantidade,
                    "preco": carrinho.preco,
                    "valor_total_item": carrinho.valor_total_item
                })
            return {
                "itens": result,
                "nome_cliente" : pedido.nome_cliente,
                "cep" : pedido.cep, 
                "logradouro" : pedido.logradouro, 
                "bairro" : pedido.bairro, 
                "cidade" : pedido.cidade, 
                "complemento" : pedido.complemento, 
                "estado" : pedido.uf, 
                "quantidade_itens" : pedido.quantidade_itens,
                "valor_total" : pedido.valor_total,
                "forma_pagamento" : pedido.forma_pagamento, 
                "data_insercao" : pedido.data_insercao.strftime("%d-%m-%Y %H:%M:%S")
            },200
    except:
            return {
                "itens": result,
                "nome_cliente" : "",
                "cep" : "", 
                "logradouro" : "", 
                "bairro" : "", 
                "cidade" : "", 
                "complemento" : "", 
                "estado" : "", 
                "quantidade_itens" : "",
                "valor_total" : 0,
                "forma_pagamento" : "", 
                "data_insercao" : datetime.fromtimestamp.strftime("%d-%m-%Y %H:%M:%S")
            },401
    
@app.get('/listar_detalhe_pedido', tags=[pedido_tag], responses={"200": ItemViewSchema, "404": ErrorSchema})

def listar_detalhe_pedido(query : User_Guid_Pedido_Schema):
    """Lista o pedido com os itens do carrinho da session_id
    """
    user_guid = request.args.get("user_guid", type=str)
    pedido_id = request.args.get("pedido_id", type=str)

    logger.info(f"Coletando Pedido")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        pedido = session.query(PedidoModel).filter(PedidoModel.user_guid == user_guid).filter(PedidoModel.id == pedido_id).first()
        itens = session.query(ItemModel).filter(ItemModel.session_id == pedido.session_id).filter(ItemModel.pedido_id == pedido_id).filter(ItemModel.status_item == 1).all()

        if  not pedido and not itens:
            # se não há Pedidos cadastrados
            return {"Pedido": 0,"Itens": []}, 200
        else:
            logger.info("pedido encontrado")
            logger.info(f"%d itens encontrados" % len(itens))
            result = []
            for carrinho in itens:
                result.append({
                    "codigo_produto": carrinho.codigo_produto,
                    "session_id": carrinho.session_id,
                    "pedido_id": carrinho.pedido_id,
                    "titulo": carrinho.titulo,
                    "url_imagem": carrinho.url_imagem,
                    "quantidade": carrinho.quantidade,
                    "preco": carrinho.preco,
                    "valor_total_item": carrinho.valor_total_item
                })
            return {
                "itens": result,
                "nome_cliente" : pedido.nome_cliente,
                "cep" : pedido.cep, 
                "logradouro" : pedido.logradouro, 
                "bairro" : pedido.bairro, 
                "cidade" : pedido.cidade, 
                "complemento" : pedido.complemento, 
                "estado" : pedido.uf, 
                "quantidade_itens" : pedido.quantidade_itens,
                "valor_total" : pedido.valor_total,
                "forma_pagamento" : pedido.forma_pagamento, 
                "data_insercao" : pedido.data_insercao.strftime("%d-%m-%Y %H:%M:%S")
            },200
    except:
            return {
                "itens": result,
                "nome_cliente" : "",
                "cep" : "", 
                "logradouro" : "", 
                "bairro" : "", 
                "cidade" : "", 
                "complemento" : "", 
                "estado" : "", 
                "quantidade_itens" : "",
                "valor_total" : 0,
                "forma_pagamento" : "", 
                "data_insercao" : datetime.fromtimestamp.strftime("%d-%m-%Y %H:%M:%S")
            },401
    


@app.get('/total_carrinho', tags=[item_carinho_tag], responses={"200": ItemViewSchema, "404": ErrorSchema})

#@jwt_required()  
def total_carrinho(query : SessaoSchema):
    """Apura total carrinho da session_id
    """
    session_id = request.args.get("session_id", type=str)

    logger.info(f"Coletando Itens ")
    # criando conexão com a base
    try:
        session = Session()
        itens = session.query(ItemModel).filter(ItemModel.session_id == session_id).filter(ItemModel.status_item == 0).all()

        if not itens:
            # se não há Pedidos cadastrados
            return {"total_itens": [],"quantidade_itens": 0 }, 200
        else:
            logger.info(f"%d itens econtrados" % len(itens))
            # retorna a representação do Carrinho
            result = []
            total_carrinho = 0
            for carrinho in itens:
                total_carrinho += carrinho.preco * carrinho.quantidade
            return {"total_itens": round(total_carrinho,2),"quantidade_itens": len(itens) }, 200
    except:
            return {"total_itens": 0,"quantidade_itens": 0 }, 401
    # fazendo a busca

@app.post('/cadastro', tags=[usuarios_tag],responses={"200": CadastroSchema, "404": ErrorSchema})

def cadastro_usuario(form : UsuarioSchema):
        """Cadastro de novo usuário no sistema."""        
        print(form)
        usuario_novo = UserModel(
            nome= form.nome,
            user_guid=str(uuid.uuid4()),
            login=form.login,
            senha=form.senha
        )
        logger.info(f"Adicionando usuário com login: '{usuario_novo.login}'")
        try:
            session = Session()
            # fazendo a busca
            usuario = session.query(UserModel).filter(UserModel.login ==  form.login).first()    

            if not usuario:
                # se não há usuário com esse username(login) cadastrado
                # criando conexão com a base
                session = Session()
                # adiciona o usuário
                session.add(usuario_novo)
                # efetivando a adição de novo usuário na tabela da DB 
                session.commit()
                logger.debug(f"Adicionado usuário com nome: '{usuario_novo.nome}'")
                return {"status" : 1,"message" : "Usuário com login '{}' criado com sucesso!".format(usuario_novo.login)}, 201
            else:
                logger.info("Usuário com login '{}' já existe.".format(usuario_novo.login))     
                return {"status" : 0,"message" : "Usuário com login '{}' já existe.".format(usuario_novo.login)}, 404
        except:
            return {"status" : 0,"message" : "Erro no processamento"}, 404


@app.post('/adicionar_item_carrinho', tags=[item_carinho_tag], responses={"200": ItemViewSchema, "404": ErrorSchema})
        
def adicionar_item_carrinho(form : ItemSchema):
        """
        Adiciona item no carrinho de compras.
        """
        print(form)
        item = ItemModel(
             codigo_produto=form.codigo_produto,
             session_id=form.session_id,
             pedido_id=form.pedido_id,
             descricao=form.descricao,
             titulo=form.titulo,
             url_imagem=form.url_imagem,
             quantidade=form.quantidade,
             preco=form.preco,
             valor_total_item = form.quantidade * form.preco,
             status_item=form.status_item
        )
        logger.info(f"Adicionando item : '{item.titulo}'")
        
        try:             
            session_1= Session()
            item_encontrado = session_1.query(ItemModel).filter(ItemModel.session_id == form.session_id).filter(ItemModel.codigo_produto == item.codigo_produto).filter(ItemModel.status_item == 0).first()
            # criando conexão com a base
            session_2 = Session()
            if not item_encontrado:
                # adicionando item se não existir no carrinho
                session_2.add(item)
            else:
                # aumenta a quantidade se já existir
                session_2.query(ItemModel).filter(ItemModel.session_id == form.session_id).filter(ItemModel.codigo_produto == item.codigo_produto).filter(ItemModel.status_item == 0).update({ItemModel.quantidade: ItemModel.quantidade + 1 })
            # efetivando o camando de adição de novo item na tabela
            session_2.commit()
            return {"mensagem" : "Item '{}' adicionado com sucesso no carrinho!".format(item.titulo),"session_id" : item.session_id, "codigo_produto" : item.codigo_produto}, 201
        except:
            return {"mensagem" : "Falha na adição do Item '{}' no carrinho!".format(item.titulo), "sessionId" : "","codigo_produto" : "" }, 401
             

@app.delete('/remover_item_carrinho', tags=[item_carinho_tag],responses={"200": ItemDelSchema, "404": ErrorSchema})

def delete(form : RemoverItemSchema):
    """
    Remove item no carrinho de compras.
    """

    print(form)
    item = RemoverItemSchema(
        codigo_produto = form.codigo_produto,
        session_id=form.session_id
    )

    # criando conexão com a base
    session = Session()
    item_encontrado = session.query(ItemModel).filter(ItemModel.session_id == item.session_id) \
    .filter(ItemModel.codigo_produto == item.codigo_produto).filter(ItemModel.status_item == 0).all()
    if item_encontrado:
        #https://stackoverflow.com/questions/65512022/sqlalchemy-delete-a-list-of-objects-opposite-of-bulk-save-objects
        #Apaga varios do banco em simultaneo (Lista) 
        obj_ids = [obj.id for obj in item_encontrado]
        query = session.query(ItemModel).filter(ItemModel.id.in_(obj_ids))
        query.delete(synchronize_session=False)
        session.commit()            
        logger.info(f"%d iten(s) removido(s)" % len(item_encontrado))
        return {'message' : 'Item removido.'},200
    return {'message' : 'Item não encontrado.'}, 404


@app.put('/add_quantidade_item_carrinho', tags=[item_carinho_tag],responses={"200": ItemUpdatedSchema, "404": ErrorSchema})

def add_quantidade_item_carrinho(form : ItemUpdateSchema):
    """
    Aumenta a quantidade do item no carrinho de compras.
    """

    print(form)
    item = ItemUpdateSchema(
        codigo_produto = form.codigo_produto,
        session_id=form.session_id
    )

    session = Session()
    item_encontrado = session.query(ItemModel).filter(ItemModel.codigo_produto == item.codigo_produto).filter(ItemModel.session_id == item.session_id).first() 
    if item_encontrado:
            item_encontrado.quantidade = item_encontrado.quantidade + 1
            item_encontrado.valor_total_item = item_encontrado.quantidade * item_encontrado.preco             
            # atualizando item
            session.add(item_encontrado)            
            # efetivando o comando de update de novo item na tabela
            session.commit()
            return {'message' : "Quantidade do item '{}' alterada".format(item_encontrado.titulo),'nova_quantidade' : item_encontrado.quantidade, 'novo_valor_total' : item_encontrado.valor_total_item}, 200
    return {'message' : 'Item não encontrado.'}, 404

@app.put('/subtract_quantidade_item_carrinho', tags=[item_carinho_tag],responses={"200": ItemUpdatedSchema, "404": ErrorSchema})

#@jwt_required()  
def subtract_quantidade_item_carrinho(form : ItemUpdateSchema):
    """
    Diminui a quantidade do item no carrinho de compras.
    """
    print(form)
    item = ItemUpdateSchema(
        codigo_produto = form.codigo_produto,
        session_id=form.session_id
    )

    session = Session()
    item_encontrado = session.query(ItemModel).filter(ItemModel.codigo_produto == item.codigo_produto).filter(ItemModel.session_id == item.session_id).first() 
    if item_encontrado:
        if item_encontrado.quantidade > 1:
            item_encontrado.quantidade = item_encontrado.quantidade -1
            item_encontrado.valor_total_item = item_encontrado.quantidade * item_encontrado.preco             

        else:
            item_encontrado.quantidade = item_encontrado.quantidade
            item_encontrado.valor_total_item = item_encontrado.valor_total_item

        # atualizando item
        session.add(item_encontrado)            
        # efetivando o comando de update de novo item na tabela
        session.commit()
        return {'message' : "Quantidade do item '{}' alterada".format(item_encontrado.titulo),'nova_quantidade' : item_encontrado.quantidade, 'novo_valor_total' : item_encontrado.valor_total_item}, 200
    return {'message' : 'Item não encontrado.'}, 404


@app.get('/pedidos', tags=[pedido_tag],responses={"200": ListagemPedidosSchema, "404": ErrorSchema})

@jwt_required()  
def get_pedidos(query: UserGuidSchema):     
    """Faz a busca por todos os Pedido cadastrados
    Retorna uma representação da listagem de Pedidos.
    """
    user_guid = request.args.get("user_guid", type=str)
    try:
        logger.info(f"Coletando Pedidos ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        pedidos = session.query(PedidoModel).filter(PedidoModel.user_guid == user_guid).order_by(PedidoModel.id.desc()).all()

        if not pedidos:
            # se não há Pedidos cadastrados
            return {"Pedidos": []}, 200
        else:
            logger.info(f"%d pedidos encontrados" % len(pedidos))
            # retorna a representação de Pedido
            result = []
            for pedido in pedidos:
                result.append({
                    "id" : pedido.id,
                    "user_guid" : pedido.user_guid,
                    "session_id" : pedido.session_id,
                    "username": pedido.username,
                    "nome_cliente": pedido.nome_cliente,
                    "cep": pedido.cep,
                    "logradouro": pedido.logradouro,
                    "bairro": pedido.bairro,
                    "cidade": pedido.cidade,
                    "complemento": pedido.complemento,
                    "uf": pedido.uf,
                    "quantidade_itens": pedido.quantidade_itens,
                    "valor_total": pedido.valor_total,
                    "forma_pagamento": pedido.forma_pagamento,
                    "data_insercao": pedido.data_insercao.strftime("%d-%m-%Y %H:%M:%S")
                })
            return {"pedidos": result}, 200
    except:    
            return {"pedidos": []}, 401

@app.post('/inserir_pedido', tags=[pedido_tag],responses={"200": PedidoIdSchema, "404": ErrorSchema})

@jwt_required()
def inserir_pedido(form : PedidoSchema):
    """
    Insere um novo Pedido de Compra e atualiza status dos itens do carrinho.
    """
    
    #https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python
    try:

        # criando conexão com a base
        session_1 = Session()
        #Calcula o valor total do carrinho e total de itens
        itens = session_1.query(ItemModel).filter(ItemModel.session_id == form.session_id).filter(ItemModel.status_item == 0).all()
        print(itens)
        valor_total = 0
        for val in itens:
            valor_total += val.quantidade * val.preco        

        print(form)

        # criando conexão com a base
        session_2 = Session()

        # adicionando pedido
        pedido = PedidoModel(
            session_id=form.session_id,
            user_guid=form.user_guid,
            username=form.username,
            nome_cliente=form.nome_cliente,
            cep=form.cep,
            logradouro=form.logradouro,
            bairro = form.bairro, 
            cidade = form.cidade, 
            complemento = form.complemento, 
            uf = form.uf,
            quantidade_itens = len(itens),
            valor_total = valor_total,
            forma_pagamento = form.forma_pagamento 
        )
        session_2.add(pedido)
        # efetivando o comando de adição de novo pedio na tabela
        session_2.commit()

        #Atualiza itens para faturado e numero de pedido
        session_3 = Session()
        session_3.query(ItemModel).filter(ItemModel.session_id == form.session_id).filter(ItemModel.status_item == 0).update({ItemModel.status_item: 1,ItemModel.pedido_id:pedido.id})
        session_3.commit()

        logger.info(f"Adicionado pedido id: '{pedido.id}'")
        return {"id_pedido" : pedido.id, "mensagem" : "Inserido com sucesso"}, 201
    except:
        return {"id_pedido" : 0, "mensagem" : "Erro desconhecido"}, 401


@app.get('/listar_usuarios', tags=[usuarios_tag], responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})

#def listar_usuarios(query : SessaoSchema):
def listar_usuarios():
    """Lista todos os usuários
    """
    logger.info(f"Coletando Itens ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(UserModel).all()

    if not usuarios:
        # se não há Pedidos cadastrados
        return {"usuarios": []}, 200
    else:
        logger.info(f"%d usuários econtrados" % len(usuarios))
        # retorna a representação de Pedido
        result = []
        for usuario in usuarios:
            result.append({
                "login": usuario.login,
                "user_guid": usuario.user_guid,
                "nome": usuario.nome
            })
        return {"usuarios": result}, 200


@app.put('/update_usuario', tags=[usuarios_tag],responses={"200": LoginViewSchema, "404": ErrorSchema})

def update_usuario(form: UsuarioSchema):
    session = Session()
    usuario_encontrado = session.query(UserModel).filter(UserModel.login == form.login).first() 
    if usuario_encontrado:
        usuario_encontrado.update_usuario(
            login=form.login,
            user_guid=usuario_encontrado.user_guid,
            nome=form.nome,
            senha=form.senha
            )
        # adicionando tarefa
        session.add(usuario_encontrado)            
        # efetivando o comando de update de novo item na tabela
        session.commit()
        return usuario_encontrado.json(), 200            
    return {'message' : 'Usuário não encontrado.'}, 404


@app.post('/login', tags=[acesso_tag],responses={"200": LoginViewSchema, "404": ErrorSchema})
    
def login(form: LoginSchema):
    """
    Login de usuário no sistema.
    """   
    print(form)
    dados = LoginSchema(
        login=form.login,
        senha=form.senha
    )
    # criando conexão com a base
    session = Session()
    try:
        # fazendo a busca
        usuario = session.query(UserModel).filter(UserModel.login == dados.login).first()
        if usuario and compare_digest(usuario.senha, dados.senha):
            logger.info(f"Usuário '{usuario.login}'")    
            token_acesso = create_access_token(identity=usuario.id)
            logger.info(f"novo token: '{token_acesso}'")
            return {"token_acesso": token_acesso, "usuario_logado": usuario.login, "user_guid" : usuario.user_guid,"message": "Sucesso"},200
        return {"token_acesso": '', "usuario_logado": "", "user_guid" : "","message": "Usuário ou senha inválidos."}, 401
    except:
        logger.info("Erro no acesso.")
        return {"token_acesso": '', "usuario_logado": "", "user_guid" : "","message": "Erro desconhecido"}, 401

@app.delete('/logout', tags=[acesso_tag],responses={"200": LogoutSchema, "404": ErrorSchema})

@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    newYorkTz = pytz.timezone("America/New_York")    
    now = datetime.now(newYorkTz)
    try:
        session = Session()

        session.add(TokenBlocklist(jti=jti, created_at=now))
        session.commit()
        return {"message": "Token acesso revogado"},200
    except:
        return {"message": "Falha no logout"},401


@app.put('/usuarios', tags=[usuarios_tag],responses={"200": ListagemPedidosSchema, "404": ErrorSchema})

@jwt_required()  
def atualizar_usuario(form : UsuarioSchema):
    """
    Atualização de dados de usuário no sistema.
    """        
    print(form)
    usuario_novo = UserModel(
        nome= form.nome,
        user_guid=str(uuid.uuid4()),
        login=form.login,
        senha=form.senha
    )
    logger.info(f"Adicionando produto de nome: '{usuario_novo.login}'")
    session = Session()
    # fazendo a busca
    usuario_encontrado = session.query(UserModel).filter(UserModel.login ==  form.login).first()    

    if usuario_encontrado:
        usuario_encontrado.update_usuario(**form)
        # adicionando tarefa
        session.add(usuario_encontrado)            
        # efetivando o comando de update de novo item na tabela
        session.commit()
        return usuario_encontrado.json(), 200            
    return {'message' : 'Usuário não encontrado.'}, 404

@app.delete('/usuarios', tags=[usuarios_tag],responses={"200": ListagemPedidosSchema, "404": ErrorSchema})

@jwt_required()  
def remover_usuario(self, id):
    """
    Remoção de usuário no sistema.
    """        
    session = Session()
    try:
        usuario_encontrado = session.query(UserModel).filter(UserModel.id == id).first()
        if usuario_encontrado:
            session.delete(usuario_encontrado)
            session.commit()
            return {'message' : 'Usuário excluído.'},200
        return {'message' : 'Usuário não encontrado.'}, 404
    except:
        return {'message' : 'Erro na pesquisa.'}, 404





