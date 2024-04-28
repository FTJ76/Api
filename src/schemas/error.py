from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Erro na execução. Verifique por favor
    """
    mesage: str
