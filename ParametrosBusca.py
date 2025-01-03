class ParametrosBusca:
    """
    Gerencia parâmetros para busca de lugares usando a API Foursquare Places.
    
    Parâmetros:
        consulta (str): Termo de busca (ex: "restaurante", "café")
        local (str): Localização para busca (ex: "São Paulo", "Rio de Janeiro")
        limite (int, opcional): Número máximo de resultados. Padrão é 50.
    
    Referência: https://docs.foursquare.com/developer/reference/place-search 
    """
    
    def __init__(self, consulta: str, local: str, fields: str, limite: int = 50, cursor: str = None):
        
        self.consulta = consulta
        self.local = local
        self.fields = fields
        self.limite = limite
        self.cursor = cursor
    
    @property
    def consulta(self):
        return self._consulta
    
    @consulta.setter
    def consulta(self, nova_consulta: str):
        self._consulta = nova_consulta.strip()

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, novo_local: str):
        self._local = novo_local.strip()
        
    @property
    def limite(self):
        return self._limite
    
    @limite.setter
    def limite(self, novo_limite: int):
        
        if novo_limite <= 0:
            raise ValueError("Limite deve ser positivo")
        
        self._limite = novo_limite
    
    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, novo_cursor):
        self._cursor = novo_cursor

    @property
    def fields(self):
        return self._fields
    
    @fields.setter
    def fields(self, novos_campos):
        self._fields = novos_campos
    
    
    def retornarTodosOsDados(self) -> dict:
        return {
            "near": self.local,
            "query": self.consulta,
            "limit": self.limite,
            "cursor": self.cursor,
            "fields": self.fields
        } 