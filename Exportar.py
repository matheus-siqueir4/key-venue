from openpyxl import Workbook

class Exportar:

    @staticmethod
    def para_excel(dados: list):
        wb = Workbook()
        ws = wb.active

        ws.append(["nome", "endereço", "contato"])

        for linha in dados:
             ws.append(linha if isinstance(linha, list) else list(linha.values()))

        wb.save("dados.xlsx")
        print(f"Arquivo salvo como dados.xlsx.")