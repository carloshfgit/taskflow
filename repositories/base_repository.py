from abc import ABC, abstractmethod

# Classe base abstrata (Interface)
class BaseRepository(ABC):
    
    @abstractmethod
    def add(self, item):
        pass
    
    # (Aqui entrarão os outros métodos do CRUD: get, update, delete)