from abc import ABC, abstractmethod

# Classe base abstrata (Interface)
class BaseRepository(ABC):
    
    @abstractmethod
    def add(self, item):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    # (Aqui entrarão os outros métodos do CRUD: get_by_id, update, delete)