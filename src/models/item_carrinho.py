from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base

#https://www.geeksforgeeks.org/column-and-data-types-in-sqlalchemy/

class ItemModel(Base):

    __tablename__ = 'itens'

    id = Column("pk_itens",Integer, primary_key=True)
    session_id = Column(String(150))
    pedido_id = Column(Integer, default=0)
    codigo_produto = Column(String(50))
    descricao = Column(String(150))
    titulo = Column(String(150))
    url_imagem = Column(String(150))
    quantidade = Column(Integer)
    preco = Column(Float) #(Float(precision=2))
    valor_total_item = Column(Float(precision=2))
    status_item = Column(Integer) #0 Para não faturado , #1 Para faturado, #2 Item expedido
    data_conclusao = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(
            self, codigo_produto,session_id,pedido_id,titulo,descricao,url_imagem,quantidade,preco, valor_total_item,status_item, 
            data_conclusao:Union[DateTime, None] = None,data_insercao:Union[DateTime, None] = None):
        """
        Adiciona um item

        Arguments:
            codigo_produto: código da api externa
            session_id: sessão do usuário
            pedido_id:  número do pedido quando é convertido em venda 
            titulo: nome do produto
            descricao: descrição do produto
            url_imagem: url da imagem na api
            quantidade: quantidade a comprar
            preco: preco da compra
            status_item: status do item: #0 Para não faturado , #1 Para faturado, #2 Item expedido
            data_conclusao: data de conclusao da compra
            data_insercao: data de quando o pedido foi inserido à base
        """
        self.codigo_produto = codigo_produto
        self.session_id = session_id
        self.pedido_id = pedido_id
        self.titulo = titulo
        self.descricao = descricao
        self.url_imagem = url_imagem
        self.quantidade = quantidade
        self.preco = preco
        self.valor_total_item = valor_total_item
        self.status_item = status_item
        self.data_conclusao = data_conclusao
        self.preco = preco

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao


    @classmethod
    def json(self):
        """
        Retorna a representação no formato Json do Objeto Pedido.
        """
        return {
            'id' : self.id,
            'codigo_produto' : self.codigo_produto,
            'session_id' : self.session_id,
            'pedido_id' : self.pedido_id,
            'descricao' : self.descricao,
            'titulo' : self.titulo,
            'url_imagem': self.url_imagem,
            'quantidade': self.quantidade,
            'preco' : self.preco,
            'valor_total_item' : self.valor_total_item,
            'status_item': self.status_item,
            'data_conclusao' : self.data_conclusao
        }

    def lista_itens(self):
        """ Retorna uma representação do itens seguindo o schema definido em
            ItemViewSchema.
        """
        result = []
        for item in self:
            result.append({
                "codigo_produto": item.codigo_produto,
                "session_id": item.session_id,
                "item_id": item.pedido_id,
                "titulo": item.titulo,
                "url_imagem": item.url_imagem,
                "quantidade": item.quantidade,
                "preco": item.preco,
                "valor_total_item": item.valor_total_item,
                "status_item": item.status_item,
                "data_conclusao": item.data_conclusao
            })

        return {"itens": result}


    def retorna_item(self):
        """ Retorna uma representação do item seguindo o schema definido em
            ItemViewSchema.
        """
        return {
            "id": self.id,
            "codigo_produto": self.codigo_produto,
            "session_id": self.session_id,
            "pedido_id": self.pedido_id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "url_imagem": self.url_imagem,
            "quantidade": self.quantidade,
            "preco": self.preco,
            "valor_total_item": self.valor_total_item,
            "status_item": self.status_item,
            "data_conclusao": self.data_conclusao
        }

    
    def update_quantidade_item(self,codigo_produto,session_id,pedido_id,titulo,descricao,url_imagem,quantidade,preco,valor_total_item,status_item):
        self.codigo_produto = codigo_produto
        self.session_id = session_id
        self.pedido_id = pedido_id
        self.titulo = titulo
        self.descricao = descricao
        self.url_imagem = url_imagem
        self.quantidade = quantidade
        self.valor_total_item = valor_total_item
        self.preco = preco
        self.status_item = status_item

