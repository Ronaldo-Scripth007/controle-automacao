import psycopg2
import pandas as pd
from datetime import datetime
import os

# ==========================================
# 1. CREDENCIAIS DO BANCO SUPABASE
# ==========================================
DB_HOST = "aws-0-sa-east-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.ydavpkvmyglisemtgwvu"
DB_PASS = "Tkisli@2620"
DB_PORT = "5432"


# ==========================================
# 2. FUNÇÃO PRINCIPAL DE EXTRAÇÃO
# ==========================================
def extrair_relatorio_excel():
    conexao = None
    try:
        print("☁️ Conectando ao banco de dados Supabase...")
        conexao = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cursor = conexao.cursor()

        # O comando SQL (GROUP BY) agrupa todos os nomes únicos e pega o MAX (maior/último) horário
        query = """
                SELECT nome_robo, MAX(data_hora) as ultima_execucao
                FROM execucoes_robos
                GROUP BY nome_robo
                ORDER BY ultima_execucao DESC; \
                """

        print("🔍 Buscando dados das automações...")
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()

        if not resultados:
            print("⚠ Nenhum dado encontrado na tabela 'execucoes_robos'.")
            return

        # ==========================================
        # 3. TRATAMENTO DOS DADOS (PANDAS)
        # ==========================================
        print("📊 Tratando os dados...")

        # Cria a tabela de dados em memória
        df = pd.DataFrame(resultados, columns=['Nome da Automação', 'Última Execução'])

        # Converte e formata a coluna de data para o padrão brasileiro: DD/MM/AAAA HH:MM:SS
        df['Última Execução'] = pd.to_datetime(df['Última Execução']).dt.strftime('%d/%m/%Y %H:%M:%S')

        # Define o nome do arquivo com a data e hora de agora para não sobrescrever arquivos antigos
        agora_str = datetime.now().strftime("%d-%m-%Y_%H-%M")
        nome_arquivo = f"Relatorio_Robos_{agora_str}.xlsx"
        caminho_salvar = os.path.join(os.getcwd(), nome_arquivo)

        # ==========================================
        # 4. SALVANDO EM EXCEL
        # ==========================================
        # engine='openpyxl' é o responsável por gerar o arquivo .xlsx
        df.to_excel(caminho_salvar, index=False, engine='openpyxl')

        print("\n" + "=" * 50)
        print("✅ RELATÓRIO GERADO COM SUCESSO!")
        print(f"📁 Arquivo salvo em: {caminho_salvar}")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Erro ao extrair os dados: {e}")
    finally:
        if conexao is not None:
            conexao.close()
            print("\nConexão com o banco encerrada.")


if __name__ == "__main__":
    extrair_relatorio_excel()