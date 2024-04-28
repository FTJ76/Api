from datetime import date
from pydantic import BaseModel,Field
from typing import Optional, List

class SessaoSchema(BaseModel):
    """ 
    Lista Itens da Sessão ID
    """
    session_id: Optional[str] = "session_id"
    pedido_id: Optional[str] = "pedido_id"

class User_Guid_Pedido_Schema(BaseModel):
    """ 
    Lista Pedido Pesquisado pelo id e user_guid
    """
    user_guid: Optional[str] = "user_guid"
    pedido_id: Optional[str] = "pedido_id"


class SessaoCarrinhoSchema(BaseModel):
    """ 
    Lista Itens da Sessão ID
    """
    session_id: str = "session_id"
    pedido_id: int = "pedido_id"

class RemoverItemSchema(BaseModel):
    """ 
    Remoção de Item Carrinho
    """
    codigo_produto: str = "codigo_produto"
    session_id : str = "session_id"

class ItemUpdateSchema(BaseModel):
    """ 
    Dados do item a alterar
    """
    codigo_produto: str = "codigo_produto"
    session_id : str = "session_id"

class ItemUpdatedSchema(BaseModel):
    """ 
    Retorno do Item Carrinho alterado
    """
    codigo_produto: str = "codigo_produto"
    session_id : str = "session_id"

class ItemSchema(BaseModel):
    """ 
    Mensagem de retorno referente a insercao
    """
    codigo_produto: str = "codigo_produto"
    session_id : str = "session_id"
    pedido_id : int = 0 
    descricao: Optional[str] = "Produto primeira linha"
    titulo: str = "Descrição Produto"
    url_imagem: str = "URL Imagem"
    quantidade: int = 1
    preco: float = 49.99
    status_item: int = 0

class ItemBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Item.
    """
    id: int = 1
    #nome: str = "Teste"

class ItemBuscaPorIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID do produto.
    """
    id: int = "1"

class ListagemItensSchema(BaseModel):
    """ Define como uma listagem de Items será retornada.
    """
    itens:List[ItemSchema]

class ItemViewSchema(BaseModel):
    """ Mensagem de retorno sobre inserção de item.
    """
    mensagem: str = "Mensagem sobre inserção"
    session_id: str = "ID da sessão do usuário (GUID)"
    codigo_produto: str = "Código do produto inserido"


class ItemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int

@classmethod
def lista_itens(itens: List[BaseModel]):
    """ Retorna uma representação do itens seguindo o schema definido em
        ItemViewSchema.
    """
    result = []
    for item in itens:
        result.append({
            "codigo_produto": item.codigo_produto,
            "titulo": item.titulo,
            "url_imagem": item.url_imagem,
            "quantidade": item.quantidade,
            "preco": item.preco
        })

    return {"itens": result}


def retorna_item(item: BaseModel):
    """ Retorna uma representação do item seguindo o schema definido em
        ItemViewSchema.
    """
    return {
        "id": item.id,
        "titulo": item.titulo,
            "url_imagem": item.url_imagem,
            "quantidade": item.quantidade,
            "preco": item.preco
    }








