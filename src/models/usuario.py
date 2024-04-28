from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
import uuid

from  models import Base

#https://www.geeksforgeeks.org/column-and-data-types-in-sqlalchemy/


class TokenBlocklist(Base):

    __tablename__ = 'blacklist'


    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)


class UserModel(Base):

    __tablename__ = 'usuarios'

    id = Column("pk_usuario",Integer, primary_key=True)
    nome = Column(String(150))
    user_guid = Column(String(150))
    login = Column(String(150))
    senha = Column(String(50))
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, nome,user_guid,login,senha,data_insercao:Union[DateTime, None] = None):
        """
        Cria um usuário

        Arguments:
            nome: nome usuário
            login: login do usuário
            senha: senha do usuário
            data_insercao: data de quando o usuário foi inserido à base
        """
        self.nome = nome
        self.user_guid = user_guid
        self.login = login
        self.senha = senha

        if not user_guid:
            self.user_guid = str(uuid.uuid4())
        # se não for informada, será o data exata da inserção no banco        
        if data_insercao:
            self.data_insercao = data_insercao


    def json(self):
        """
        Retorna a representação no formato Json do Objeto Usuário.
        """
        return {
            'id' : self.id,
            'nome' : self.nome,
            'user_guid' : self.user_guid,
            'login' : self.login,
            'senha' : self.senha
        }
    @classmethod
    def lista_usuarios(self):
        """ Retorna uma representação do usuarios seguindo o schema definido em
            TarefaViewSchema.
        """
        result = []
        for usuario in self:
            result.append({
                "nome": usuario.nome,
                "user_guid": usuario.user_guid,
                "login": usuario.login,
                "senha": usuario.senha
            })

        return {"usuarios": result}


    def retorna_usuario(self):
        """ Retorna uma representação do usuário seguindo o schema definido em
            UsuarioViewSchema.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "user_guid": self.user_guid,
            "login": self.login,
            "senha": self.senha
        }
    
    def update_usuario(self,nome,user_guid,login,senha):
        self.nome = nome
        self.user_guid = user_guid
        self.login = login
        self.senha = senha

