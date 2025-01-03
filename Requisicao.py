from urllib.parse import urlparse, parse_qs
from ParametrosBusca import ParametrosBusca
from dotenv import load_dotenv
import requests, os

class Requisicao:
    """
    Realiza requisições para a API Foursquare usando os parâmetros definidos
    em um objeto Data.
    
    Parâmetros:
        parametros (ParametrosBusca): Objeto contendo os parâmetros da busca
    """
    
    def __init__(self, parametros: ParametrosBusca):
        self.parametros = parametros    
        self.variaveis_env = self.__carregarVariaveisEnv()
        self._dados_estabelecimentos = []

    def buscarDadosDosEstabelecimentos(self) -> None:
        endpoint = f"{self.variaveis_env['URL_BASE']}{self.variaveis_env['URL_SEARCH_ENDPOINT']}"
        headers = {"accept": "application/json", "Authorization": self.variaveis_env["SECRET_KEY"]}

        while True:
            resposta = requests.get(url=endpoint, headers=headers, params=self.parametros.retornarTodosOsDados())
            self.__adicionarDadosNaListaDeEstabelecimentos(resposta)
            self.__proximaPagina(resposta.links)

            if not self.parametros.cursor:
                break
    @property
    def dados_estabelecimentos(self):
        return self._dados_estabelecimentos

    @dados_estabelecimentos.setter
    def dados_estabelecimentos(self, dados: dict):
        self._dados_estabelecimentos.append(dados)
    
    def __adicionarDadosNaListaDeEstabelecimentos(self, resposta_requisicao: requests.Response) -> None:
        resposta_json = resposta_requisicao.json()
        for conteudo_resposta in resposta_json.get('results', []): 
            dados = {
                'nome': conteudo_resposta.get('name', "Sem nome"),
                'endereco': conteudo_resposta.get('location', {}).get('formatted_address', 'Sem Endereço'),
                'contato': conteudo_resposta.get('tel', "Sem contato")
            }
            self.dados_estabelecimentos = dados
            
    def __carregarVariaveisEnv(self) -> dict:
        load_dotenv(dotenv_path="./config/.env")
        
        variaveis = {
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "URL_BASE": os.getenv("URL_BASE"),
            "URL_SEARCH_ENDPOINT": os.getenv("URL_SEARCH_ENDPOINT")
        }
        
        missing = [k for k, v in variaveis.items() if not v]
        if missing:
            raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing)}")
        
        return variaveis

    def __extrairCursor(self, link: str) -> str:
        """
        Extrai o parâmetro 'cursor' do link de paginação fornecido pela API Foursquare.
        """
        if not link:
            return None

        linkParsed = urlparse(link)
        parametros = parse_qs(linkParsed.query)
        return parametros.get('cursor', [None])[0]

    def __proximaPagina(self, link: dict):
        url = link.get('next', {}).get('url', None)
        self.parametros.cursor = self.__extrairCursor(url) 