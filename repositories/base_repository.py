from abc import ABC, abstractmethod

#classe base abstrata (Interface)
class BaseRepository(ABC):
    
    @abstractmethod
    def add(self, item):
        pass
    
    @abstractmethod
    def get_all(self, **filters): # MUDANÇA AQUI: Aceita filtros genéricos
        """
        Retorna todos os registos.
        Pode receber filtros opcionais (ex: user_id=1).
        """
        pass

    @abstractmethod
    def get_by_id(self, item_id):
        pass
    
    @abstractmethod
    def update(self, item):
        pass
    
    @abstractmethod
    def delete(self, item_id):
        pass
