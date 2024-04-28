from datetime import date
from pydantic import BaseModel
from typing import Optional, List
import uuid
#from models.pedido import PedidoModel
#from models.usuario import UserModel



class LoginSchema(BaseModel):
    """ Define os dados de usuário para Login
    """
    #nome: Optional[str] = "Nome do Usuário"
    login: str = "email@domiminio.com.br"
    senha: str = "Senha de Acesso"

class LoginViewSchema(BaseModel):
    """ Define os dados de usuário após login bem sucedido
    """
    token_acesso: str = "Token de acesso"
    usuario_logado: str = "email@domiminio.com.br"
    user_guid: str = "guid do usuário"
    message: str = "Mensagem de retorno"

def dados_login(acesso: BaseModel):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        #"token_acesso": acesso.token_acesso,
        "usuario_logado": acesso.usuario_logado,
        "user_guid": acesso.user_guid,
        "message": acesso.message
        #"total_cometarios": len(produto.comentarios),
        #"comentarios": [c.texto for c in produto.comentarios]
    }

class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """

    nome: str = "nome do usuário"
    login: str = "login do usuário"
    senha: str = "senha de acesso"
    #user_guid: str = str(uuid.uuid4())

class CadastroSchema(BaseModel):
    """ Define o retorno de um novo cadastro
    """

    status: int = 0
    message: str = "mensagem sobre retorno de cadastro"


class TokenSchema(BaseModel):
    """ Token da sessão para logout
    """

    Authorization: str = "Bearer Token"

class LogoutSchema(BaseModel):
    """ Mensagem de logout.
    """
    message: str


class UsuarioListaSchema(BaseModel):
    """ Modelo de consulta de usuários
    """

    id: int = "email@domiminio.com.br"
    nome: str = "email@domiminio.com.br"
    user_guid: str = "email@domiminio.com.br"
    login: str = "email@domiminio.com.br"
    #senha: str = "Senha de Acesso"


class ListagemUsuariosSchema(BaseModel):
    """ Retorna uma listagem de usuários.
    """
    pedidos:List[UsuarioListaSchema]


