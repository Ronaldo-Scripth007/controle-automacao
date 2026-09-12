# VERSÃO OFFICIAL. copia da versão que Miqueias colocou pra rodar. Melhorando a versão
# Envio de mensagem no watsap referente ao status de cada robo.
# Versão official que esta rodando!

import os
import psycopg2
import pyperclip
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options

# --- Imports do Selenium para o WhatsApp ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# 1. CREDENCIAIS DA TABELA
# ==========================================
DB_HOST = "aws-0-sa-east-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.ydavpkvmyglisemtgwvu"
DB_PASS = "Tkisli@2620"
DB_PORT = "5432"

# ==========================================
# 2. CONFIGURAÇÃO DOS ROBÔS E REGRAS
# ==========================================

# Robôs que rodam de tempos em tempos (em minutos)
robos_intervalo = {
    "Acompanhamento OPeracional SLI": 15,
    "Atualiza Fretebras": 50,
    "Espelhamento Shopee": 18,
    "Atualiza Validação de Emissão": 35,
    "Validar CTRBs Duplicados": 35,

}

# Robôs que rodam em horários  (Fixos)
robos_fixos = {
    "Envio Img Grupo Shopee": ["09:30"],
    "Extrator Horas Extras" : ["10:00"],
    "EXP - Emissões Bloqueadas": ["06:00"],
    "SLI - Analitico Operação": ["06:00"],
    "TKI - Consulta Adiant/Saldo": ["06:00"],
    "Robô Unilever PE": ["12:00", "18:00"],
    "Robô Unilever SP": ["12:00", "18:00"],
    "Robô Unilever ES": ["12:00", "18:00"],
    "Robô Unilever MG": ["12:00", "18:00"],
    #"Comercial - BI Faturamento": ["06:00", "12:00", "18:00"],    #este
    "Robô_Lanc_Infrutiferas": ["12:00", "19:00"],
    "FRT - Rentabilidade Frota": ["06:00"],
    "COM - CNPJ Agrupar": ["06:00"],
    "EXP - Produtividade": ["06:00"],
    "EXP - GNRE": ["06:00"],
    "TKI - Produtividade TK": ["06:00"],
    "TKI - Motoristas Parceiros": ["06:00"],
    "COM - Coletas Canceladas":["06:00"],
    "GR - Despesas GR": ["06:00"],
    "SLI - Rentabilidade": ["06:00"],
    "EXP - CTEs Cancelados": ["06:00"],
    "Validação Unidade Emissora": ["06:00"],
    "TKI - Histórico Frete Pago" : ["06:00"],
    "SLI - Metas Contratação" : ["06:00"],
    "ECOM - Rentabilidade" : ["06:00"],
    "EXP - CTRBs Sem Vinculo CTEs": ["06:00"],
    "SLI - Devoluções": ["06:00"],
    "FRT - Velocidade Excedida":["09:10"]

}

# Nome formatados para a Copy do Watsapp.
apelidos_whatsapp = {
    "Acompanhamento OPeracional SLI": ["SLI - BI Operacional"],
    "Atualiza Fretebras": ["TKI - FreteBras F5"],
    "Espelhamento Shopee": ["GR - Placas Fora PGR"],
    "Extrator Horas Extras" : ["DP - Horas Extras"],
    "Atualiza Validação de Emissão": ["EXP - Validação Emissões"],
    "Validar CTRBs Duplicados": ["EXP - CTRB Duplicados"],
    "Robô_Lanc_Infrutiferas": ["FIN - Desp Infrutiferas"],
    "Envio Img Grupo Shopee": ["ECOM - SHP KPI"],
    "Robô Unilever PE": ["FIN - Canhotos Unilever PE"],
    "Robô Unilever SP": ["FIN - Canhotos Unilever SP"],
    "Robô Unilever ES": ["FIN - Canhotos Unilever ES"],
    "Robô Unilever MG": ["FIN - Canhotos Unilever MG"],

    # Chave com Listas. Aqui estou definindo a lista dos arquivos com varios dashbords integrados.
    "FRT - Rentabilidade Frota": [
        "FRT - Despesas Frota(Dt Emissão)",
        "FRT - Faturamento",
        "FRT - Rentabilidade Frota",
        "FRT - Despesas Frota(Dt Pgto)"
    ],

    "Comercial - BI Faturamento": [ # este
        "EXP - Produtividade",
        "TKI - Produtividade TK",

    ],

    "Validação Unidade Emissora": [
        "COM - Faturamento",
        "COM - Metas Comerciais",

    ],

    "COM - CNPJ Agrupar": ["COM - CNPJ Sem Agrupar"],
    "COM - Coletas Canceladas": ["COM - Coletas Canceladas"]
}

# ==========================================
# 3. FUNÇÃO DO WHATSAPP "À PROVA DE BALAS"
# ==========================================
def enviar_relatorio_grupo(mensagem):
    print("\nIniciando envio para o WhatsApp...")

    options = Options()

    # Perfil dedicado do WhatsApp
    perfil_whatsapp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whatsapp_chrome_profile")
    options.add_argument(f"--user-data-dir={perfil_whatsapp}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-notifications")

    # Prevenção contra crash do Chrome.
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Abrindo o WhatsApp Web...")
        driver.get("https://web.whatsapp.com")

        wait_load = WebDriverWait(driver, 60)
        wait_interact = WebDriverWait(driver, 15)

        print("Aguardando o WhatsApp carregar (Buscando barra de pesquisa)...")
        xpaths_pesquisa = [
            '//div[@contenteditable="true"][@data-tab="3"]',
            '//input[@placeholder="Pesquisar ou começar uma nova conversa"]',
            '//div[@title="Caixa de texto de pesquisa"]',
            '//*[@id="side"]//div[@contenteditable="true"]'
        ]

        caixa_pesquisa = None
        for xpath in xpaths_pesquisa:
            try:
                caixa_pesquisa = wait_load.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if caixa_pesquisa:
                    break
            except:
                continue

        if not caixa_pesquisa:
            raise Exception("Barra de pesquisa não encontrada. O WhatsApp deslogou ou mudou de layout.")

        # Pausa estratégica para garantir que a interface estabilizou após carregar
        time.sleep(3)

        print("Barra encontrada! Digitando o nome do grupo...")
        caixa_pesquisa.click()
        caixa_pesquisa.send_keys(Keys.CONTROL + "a")
        caixa_pesquisa.send_keys(Keys.BACKSPACE)
        caixa_pesquisa.send_keys("Automações ON")

        print("Aguardando o grupo aparecer na lista de resultados...")

        # Tratamento contra o Stale Element Reference
        from selenium.common.exceptions import StaleElementReferenceException

        xpath_grupo = '//span[@title="Automações ON"]'
        grupo_clicado = False

        for tentativa in range(3):  # Tenta clicar no grupo até 3 vezes
            try:
                time.sleep(2)  # Pequena pausa para a lista de resultados estabilizar
                grupo = wait_interact.until(EC.element_to_be_clickable((By.XPATH, xpath_grupo)))
                grupo.click()
                grupo_clicado = True
                break
            except StaleElementReferenceException:
                print(f"Tentativa {tentativa + 1}: Elemento atualizou. Tentando clicar no grupo novamente...")
                continue
            except Exception as e:
                print(f"Erro ao tentar clicar no grupo na tentativa {tentativa + 1}: {e}")
                continue

        if not grupo_clicado:
            raise Exception("Não foi possível clicar no grupo 'Automações ON' após várias tentativas.")

        print("Grupo aberto! Localizando caixa de texto...")

        # Pausa estratégica para garantir que o chat abriu
        time.sleep(2)

        xpaths_mensagem = [
            '//*[@id="main"]//div[@contenteditable="true"][@data-tab="10"]',
            '//*[@id="main"]//footer//div[@contenteditable="true"]'
        ]

        caixa_mensagem = None
        for xpath in xpaths_mensagem:
            try:
                caixa_mensagem = wait_interact.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if caixa_mensagem:
                    break
            except:
                continue

        if not caixa_mensagem:
            raise Exception("Caixa de mensagem não encontrada dentro do grupo.")

        print("Copiando relatório para a área de transferência e colando...")
        caixa_mensagem.click()
        pyperclip.copy(mensagem)
        caixa_mensagem.send_keys(Keys.CONTROL, 'v')

        print("Aguardando botão de envio aparecer...")
        xpath_botao_enviar = '//button[@aria-label="Enviar"] | //span[@data-icon="send"]/..'
        botao_enviar = wait_interact.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_enviar)))

        print("Enviando o relatório...")
        botao_enviar.click()

        print("\n[SUCESSO] Relatório enviado no grupo do WhatsApp!")

        time.sleep(4)

    except Exception as e:
        print(f"\n[ERRO] Falha na navegação do WhatsApp: {e}")
    finally:
        driver.quit()

# ==========================================
# 4. FUNÇÕES DE BD APRIMORADAS
# ==========================================
def obter_ultima_execucao(nome_robo, cursor):
    """Busca a ÚLTIMA data em que o robô inseriu algo na tabela."""
    try:
        cursor.execute('''
                       SELECT data_hora
                       FROM execucoes_robos
                       WHERE nome_robo = %s
                       ORDER BY data_hora DESC LIMIT 1
                       ''', (nome_robo,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Erro ao consultar o robô {nome_robo}: {e}")
        return None


# ==========================================
# 5. O SUPERVISOR (MONTANDO O RELATÓRIO)
# ==========================================
def main():
    agora = datetime.now()
    print(f"--- Iniciando Monitoramento às {agora.strftime('%H:%M:%S')} ---\n")

    # 1. DICIONÁRIO PARA GUARDAR OS ROBÔS SEPARADOS POR ÁREA
    grupos_relatorio = {}

    print("Conectando a tabela para analise das Automações...")
    try:
        conexao_monitor = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cursor_monitor = conexao_monitor.cursor()
    except Exception as e:
        print(f"Erro fatal: Não foi possível conectar ao banco de dados: {e}")
        return

    print("Verificando status dos robôs...\n")

    # Função interna para classificar o robô de acordo com a sigla dele
    def classificar_e_guardar(nome_tratado, status_simbolo):
        # Se o nome tiver " - ", ele pega o que tá antes. (Ex: "EXP - GNRE" vira "EXP")
        if " - " in nome_tratado:
            area = nome_tratado.split(" - ")[0].strip()
        else:
            area = "OUTROS"

        # Cria a "gaveta" da área se ela ainda não existir
        if area not in grupos_relatorio:
            grupos_relatorio[area] = []

        # Guarda o robô dentro da gaveta certa
        grupos_relatorio[area].append(f"{status_simbolo} {nome_tratado}")

    # --- VERIFICANDO ROBÔS DE INTERVALO ---
    for nome_banco, min_esperados in robos_intervalo.items():
        lista_nomes_tratados = apelidos_whatsapp.get(nome_banco, [nome_banco])
        data_banco = obter_ultima_execucao(nome_banco, cursor_monitor)

        if data_banco:
            min_passados = (agora - data_banco).total_seconds() / 60
            status_simbolo = "❌" if min_passados > (min_esperados + 15) else "✅"
        else:
            status_simbolo = "❓"

        # Guarda cada nome tratado na sua respectiva área
        for nome_tratado in lista_nomes_tratados:
            classificar_e_guardar(nome_tratado, status_simbolo)

    # --- VERIFICANDO ROBÔS FIXOS ---
    for nome_banco, horarios in robos_fixos.items():
        lista_nomes_tratados = apelidos_whatsapp.get(nome_banco, [nome_banco])
        data_banco = obter_ultima_execucao(nome_banco, cursor_monitor)

        if data_banco:
            teve_problema = False
            for horario_str in horarios:
                hora_alvo = datetime.strptime(horario_str, "%H:%M").replace(year=agora.year, month=agora.month,
                                                                            day=agora.day)

                if agora >= (hora_alvo + timedelta(minutes=15)):
                    if data_banco < hora_alvo:
                        teve_problema = True
                        break
            status_simbolo = "❌" if teve_problema else "✅"
        else:
            status_simbolo = "❓"

        # Guarda cada nome tratado na sua respectiva área
        for nome_tratado in lista_nomes_tratados:
            classificar_e_guardar(nome_tratado, status_simbolo)

    cursor_monitor.close()
    conexao_monitor.close()
    print("Conexão com o banco encerrada.\n")

    # =========================================================
    # 2. MONTANDO A MENSAGEM DO WHATSAPP AGRUPADA E BONITA
    # =========================================================
    relatorio = f"🤖 *STATUS AUTOMAÇÕES* 🤖\n"

    # Dicionário tradutor: Transforma a sigla no nome completo da área para o Zap!
    nomes_das_areas = {
        "EXP":     "📦 *EXPEDIÇÃO*",
        "FIN":     "💰 *FINANCEIRO*",
        "COM":     "🤝 *COMERCIAL*",
        "SLI":     "📊 *SLI*",
        "FRT":     "🚚 *FROTA*",
        "TKI":     "🏢 *TK*",
        "TK":      "🏢 *TK*",
        "GR":      "🛡️ *GERENCIAMENTO DE RISCO*",
        "DP":      "👥 *DEPARTAMENTO PESSOAL*",
        "SHP":     "🛒 *SHOPEE*",
        "ECOM":    "🌐 *E-COMMERCE*",
        "OUTROS":  "📌 *OUTRAS AUTOMAÇÕES*"
    }

    # Ordena as áreas em ordem alfabética
    for sigla in sorted(grupos_relatorio.keys()):
        # Pega o nome bonitinho do dicionário acima (ou usa a própria sigla se não achar)
        titulo_area = nomes_das_areas.get(sigla, f"📌 *{sigla}*")

        relatorio += f"\n{titulo_area}\n"

        # Lista os robôs pertencentes a essa área, também em ordem alfabética
        for linha in sorted(grupos_relatorio[sigla]):
            relatorio += f"  {linha}\n"

    print("RELATÓRIO GERADO:\n" + "=" * 40)
    print(relatorio)
    print("=" * 40)

    # Dispara o WhatsApp
    enviar_relatorio_grupo(relatorio)


if __name__ == "__main__":
    main()