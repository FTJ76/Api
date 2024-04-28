from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from models.pedido import PedidoModel

class UserGuidSchema(BaseModel):
    """ Guid para pesquisa do pedidos do usuário
    """
    user_guid: Optional[str] = "user_guid"


class PedidoSchema(BaseModel):
    """ Define como um novo tarefa a ser inserido deve ser representado
    """
    session_id: str = "session_id"
    user_guid: str = "user_guid"
    username: str = "username"
    nome_cliente: str = "nome_cliente"
    cep: str = "cep"
    logradouro: str = "logradouro"
    bairro : str = "bairro" 
    cidade : str = "cidade" 
    complemento : str = "complemento" 
    uf : str = "uf"
    quantidade_itens : int = 0
    valor_total : float = 0
    forma_pagamento : str = "forma_pagamento" 


class PedidoIdSchema(BaseModel):
    """ Retorna o Id do pedido inserido.
    """
    id: int


class PedidoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do pedido.
    """
    id: int = 0

class PedidoBuscaPorIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID do produto.
    """
    id: int = 0

class ListagemPedidosSchema(BaseModel):
    """ Define como uma listagem de pedidos será retornada.
    """
    pedidos:List[PedidoSchema]

class PedidoViewSchema(BaseModel):
    """ Define como um pedido será retornado.
    """
    id: int = 1
    codigo_produto: str = "ID Produto"
    titulo: str = "Descrição Produto"
    url_imagem: str = "URL Imagem"
    quantidade: str = "Qt adquirida"
    preco: str = "Preço do produto"
   

class PedidoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    #id: int

def lista_pedidos(pedidos: List[PedidoModel]):
    """ Retorna uma representação do pedidos seguindo o schema definido em
        PedidoViewSchema.
    """
    result = []
    for pedido in pedidos:
        result.append({
            "codigo_produto": pedido.codigo_produto,
            "titulo": pedido.titulo,
            "url_imagem": pedido.url_imagem,
            "quantidade": pedido.quantidade,
            "preco": pedido.preco,
            "data_conclusao": pedido.data_conclusao
        })

    return {"pedidos": result}


def retorna_pedido(pedido: PedidoModel):
    """ Retorna uma representação do pedido seguindo o schema definido em
        PedidoViewSchema.
    """
    return {
        "id": pedido.id,
        "titulo": pedido.titulo,
            "url_imagem": pedido.url_imagem,
            "quantidade": pedido.quantidade,
            "preco": pedido.preco,
        "data_conclusao": pedido.data_conclusao
    }








