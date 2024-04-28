from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base

#https://www.geeksforgeeks.org/column-and-data-types-in-sqlalchemy/

class PedidoModel(Base):

    __tablename__ = 'pedidos'

    id = Column("pk_pedido",Integer, primary_key=True)
    session_id = Column(String(150))
    user_guid = Column(String(100))
    username = Column(String(150)) 
    nome_cliente = Column(String(150)) 
    cep = Column(String(10)) 
    logradouro = Column(String(150)) 
    bairro = Column(String(150)) 
    cidade = Column(String(50)) 
    complemento = Column(String(100)) 
    uf = Column(String(10)) 
    quantidade_itens = Column(Integer)
    valor_total = Column(Float(precision=2))
    forma_pagamento = Column(String(100)) 
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, user_guid,session_id,username,cep,nome_cliente,logradouro,bairro,cidade,complemento,uf,quantidade_itens,valor_total,forma_pagamento,data_insercao:Union[DateTime, None] = None):
        """
        Cria um pedido

        Arguments:
            session_id: sessao do carrinho
            username: username
            user_guid: guid usuário pedido
            nome_cliente: nome_cliente
            cep: cep entrega
            logradouro: logradoruo
            bairro: bairro entrega
            cidade: cidade entrega
            complemento: complemento entrega
            uf: uf entrega
            quantidade_itens: itens
            valor_total: valor_total
            forma_pagamento: forma_pagamento
            data_insercao: data de quando o pedido foi inserido à base
        """
        self.session_id = session_id
        self.user_guid = user_guid
        self.username = username
        self.nome_cliente = nome_cliente
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.complemento = complemento
        self.uf = uf
        self.quantidade_itens = quantidade_itens
        self.valor_total = valor_total
        self.forma_pagamento = forma_pagamento

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao


    def json(self):
        """
        Retorna a representação no formato Json do Objeto Pedido.
        """
        return {
            'session_id' : self.session_id,
            'id' : self.id,
            'user_guid' : self.user_guid,
            'username' : self.username,
            'nome_cliente': self.nome_cliente,
            'cep': self.cep,
            'logradouro': self.logradouro,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'complemento': self.complemento,
            'uf': self.uf,
            'quantidade_itens': self.quantidade_itens,
            'valor_total': self.valor_total,
            'forma_pagamento': self.forma_pagamento,
            'data_insercao': self.data_insercao
        }
    @classmethod
    def lista_pedidos(self):
        """ Retorna uma representação do pedidos seguindo o schema definido em
            TarefaViewSchema.
        """
        result = []
        for pedido in self:
            result.append({
            'session_id' : pedido.session_id, 
            'user_guid' : pedido.user_guid,   
            'id' : pedido.id,
            'username' : pedido.username,
            'nome_cliente': pedido.nome_cliente,
            'cep': pedido.cep,
            'logradouro': pedido.logradouro,
            'bairro': pedido.bairro,
            'cidade': pedido.cidade,
            'complemento': pedido.complemento,
            'uf': pedido.uf,
            'quantidade_itens': pedido.quantidade_itens,
            'valor_total': pedido.valor_total,
            'forma_pagamento': pedido.forma_pagamento,
            'data_insercao': pedido.data_insercao
            })

        return {"pedidos": result}


    def retorna_pedido(self):
        """ Retorna uma representação do pedido seguindo o schema definido em
            PedidoViewSchema.
        """
        return {
            'session_id' : self.session_id,    
            'user_guid' : self.user_guid,   
            'id' : self.id,
            'username': self.username,
            'nome_cliente': self.nome_cliente,
            'cep': self.cep,
            'logradouro': self.logradouro,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'complemento': self.complemento,
            'uf': self.uf,
            'quantidade_itens': self.quantidade_itens,
            'valor_total': self.valor_total,
            'forma_pagamento': self.forma_pagamento,
            'data_insercao': self.data_insercao
        }
    
    def update_pedido(self,user_guid,session_id,username,cep,nome_cliente,logradouro,bairro,cidade,complemento,uf,quantidade_itens,valor_total,forma_pagamento,data_insercao):
        self.session_id = session_id
        self.user_guid = user_guid
        self.username = username
        self.cep = cep
        self.nome_cliente = nome_cliente
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.complemento = complemento
        self.uf = uf
        self.quantidade_itens = quantidade_itens
        self.valor_total = valor_total
        self.forma_pagamento = forma_pagamento
        self.data_insercao = data_insercao
    #def save_pedido(self):
        # criando conexão com a base
        #session = Session()

        #cls.session.add(self)
        #PedidoModel.session.commit()