import argparse
from Exportar import Exportar
from ParametrosBusca import ParametrosBusca
from Requisicao import Requisicao

def main():
    parser = argparse.ArgumentParser(description="Busca de lugares usando a API do Foursquare")

    parser.add_argument("consulta", type=str, help="O termo de busca (ex: 'restaurante')")
    parser.add_argument("local", type=str, help="A localização para buscar (ex: 'São Paulo, SP')")
    parser.add_argument("--limite", type=int, default=50, help="Limite de resultados (padrão: 50)")
    parser.add_argument("--fsq_id", type=str, default=None, help="O fsq_id do lugar para obter detalhes")

    args = parser.parse_args()

    parametros = ParametrosBusca(consulta=args.consulta, local=args.local, limite=args.limite, fields='name,location,tel')
    requisicao = Requisicao(parametros)

    requisicao.buscarDadosDosEstabelecimentos()
    Exportar.para_excel(requisicao.dados_estabelecimentos)

if __name__ == "__main__":
    main()
