from abc import ABC, abstractmethod

# Classe base abstrata (Interface)
class BaseRepository(ABC):
    
    @abstractmethod
    def add(self, item):
        pass
    
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, item_id):
        pass
    
    @abstractmethod
    def update(self, item):
        pass
    
