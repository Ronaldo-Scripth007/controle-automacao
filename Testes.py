# # Importa a biblioteca 'os' para interagir com o sistema operacional (ex: buscar variáveis de ambiente)
# import os
# # Importa a biblioteca 'time' para aplicar pausas/esperas físicas (segundos) no código
# import time
# # Importa o construtor 'datetime' para capturar o dia e horário atual do sistema
# from datetime import datetime
# # Importa o driver 'psycopg2', necessário para conectar e executar comandos no banco de dados PostgreSQL (Supabase)
# import psycopg2
# # Importa a classe Options do Selenium para configurar opções do navegador Chrome (como modo anônimo, tirar tela cheia, etc.)
# from selenium.webdriver.chrome.options import Options
# # Importa o próprio módulo principal do webdriver do Selenium para gerenciar e abrir o navegador
# from selenium import webdriver
# # Importa a classe 'By' para indicar ao Selenium como localizar elementos na página (por ID, XPATH, Nome, etc.)
# from selenium.webdriver.common.by import By
# # Importa a classe 'WebDriverWait' que cria esperas inteligentes e dinâmicas até que elementos carreguem na tela
# from selenium.webdriver.support.ui import WebDriverWait
# # Importa as condições esperadas ('EC') que definem os critérios das esperas inteligentes (ex: se o elemento já está clicável)
# from selenium.webdriver.support import expected_conditions as EC
#
# # ==============================
# # CREDENCIAIS DO BANCO SUPABASE
# # ==============================
# # Variável que guarda o endereço do servidor em nuvem fornecido pelo Supabase
# DB_HOST = "aws-0-sa-east-1.pooler.supabase.com"
# # Variável que define o nome do banco de dados principal dentro do PostgreSQL
# DB_NAME = "postgres"
# # Variável que define o nome de usuário administrador do banco de dados
# DB_USER = "postgres.ydavpkvmyglisemtgwvu"
# # Variável que guarda a senha de acesso ao banco de dados
# DB_PASS = "Tkisli@2620"
# # Variável que define a porta padrão de conexão do PostgreSQL
# DB_PORT = "5432"
#
# # ==============================
# # INFORMAÇÕES DESTE ROBÔ PARA O LOG
# # ==============================
# # Define o nome de identificação deste robô para salvar no relatório de automações
# NOME_ROBO = "Atualiza Validação de Emissão"
# # Define o nome ou apelido do computador/servidor onde este robô roda atualmente
# MAQUINA_ATUAL = "Pc das Autom."
# # Descreve o modelo de recorrência da automação (neste caso, executa uma vez ou via agendador de tarefas)
# CICLO_ATUAL = "Execução Única / Agendador"
# # Descreve o objetivo de negócio que esta automação cumpre
# FINALIDADE = "Validação Unidades Emissão CTe"
#
#
# # ==============================
# # FUNÇÃO DE LOG NO BANCO
# # ==============================
# # Define uma função que recebe dados de status e envia para a nuvem, servindo de histórico/monitoramento
# def registrar_execucao_nuvem(nome_robo, status, detalhes, maquina, ciclo, finalidade):
#     """Gravando o resultado da execução no Supabase para o Monitor rastrear"""
#     # Bloco try/except tenta executar a conexão, capturando erros se algo der errado na rede ou credenciais
#     try:
#         # Estabelece a conexão física com o banco usando as variáveis credenciais definidas lá em cima
#         conexao = psycopg2.connect(
#             host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
#         )
#         # Cria um cursor, objeto indispensável para fazer consultas e comandos SQL passarem pela conexão
#         cursor = conexao.cursor()
#         # Captura exatamente o ano, mês, dia, hora, minuto e segundo atual para o registro
#         agora = datetime.now()
#
#         # Executa o comando SQL 'INSERT INTO' para inserir uma nova linha com os dados do robô na tabela 'execucoes_robos'
#         cursor.execute('''
#                        INSERT INTO execucoes_robos (nome_robo, data_hora, status, detalhes, maquina, ciclo, finalidade)
#                        VALUES (%s, %s, %s, %s, %s, %s, %s)
#                        ''', (nome_robo, agora, status, detalhes, maquina, ciclo, finalidade))
#
#         # Confirma e salva definitivamente a alteração/inserção dos dados no banco de dados (sem isso, o comando é descartado)
#         conexao.commit()
#         # Fecha o cursor liberando os recursos internos do banco
#         cursor.close()
#         # Fecha a conexão ativa com o servidor do Supabase
#         conexao.close()
#         # Mostra uma mensagem de confirmação no terminal do seu computador
#         print(f"☁️ Log gravado no banco: {status}")
#     # Caso a conexão ou a inserção SQL falhe, o fluxo cai neste bloco capturando o motivo no 'e'
#     except Exception as e:
#         # Imprime no terminal o alerta de falha e o texto detalhado do erro
#         print(f"⚠️ Erro ao gravar log no banco: {e}")
#
#
# # ==============================
# # CREDENCIAIS POWER BI
# # ==============================
# # Tenta buscar a credencial em uma variável de ambiente do Windows/Linux; se não achar, usa o e-mail padrão fornecido
# USER_PBI = os.environ.get("USER_PBI", "danilo.lacerda@transking.com.br")
# # Tenta buscar a senha em uma variável de ambiente; se não achar, usa a string de senha padrão fornecida
# PASS_PBI = os.environ.get("PASS_PBI", "QwErTyAsDfgH!2#4%5")
#
#
# # ==============================
# # LOGIN POWER BI
# # ==============================
# # Define a função responsável por abrir a página, digitar os dados e vencer as etapas de autenticação
# def login_power_bi(navegador):
#     # Inicia o bloco de proteção contra erros durante as ações na página da web
#     try:
#         # Comanda o navegador web automatizado a navegar e abrir o site oficial do Power BI
#         navegador.get("https://app.powerbi.com/")
#         # Pausa o código de forma fixa por 5 segundos para que a página inicial e scripts carreguem totalmente
#         time.sleep(5)
#
#         # --- Etapa do Email ---
#         # Aguarda de forma inteligente por até 20 segundos até que o campo com ID "email" apareça fisicamente na tela
#         WebDriverWait(navegador, 20).until(
#             EC.presence_of_element_located((By.ID, "email"))
#         )
#         # Localiza o campo de ID "email" e digita o conteúdo armazenado na variável USER_PBI
#         navegador.find_element(By.ID, "email").send_keys(USER_PBI)
#         # Localiza o botão com ID "submitBtn" (Avançar) e clica nele
#         navegador.find_element(By.ID, "submitBtn").click()
#         # Aguarda 2 segundos fixos para dar tempo da tela mudar para a página de senha da Microsoft
#         time.sleep(2)
#
#         # --- Etapa da Senha ---
#         # Aguarda até 20 segundos para que a caixa de texto de ID "i0118" (campo de senha padrão Microsoft) apareça
#         WebDriverWait(navegador, 20).until(
#             EC.presence_of_element_located((By.ID, "i0118"))
#         )
#         # Pausa por mais 2 segundos garantindo a transição visual das animações de login
#         time.sleep(2)
#
#         # Localiza o campo de senha "i0118" e digita a senha contida na variável PASS_PBI
#         navegador.find_element(By.ID, "i0118").send_keys(PASS_PBI)
#         # Localiza o botão de ID "idSIButton9" (botão "Entrar" da Microsoft) e clica nele
#         navegador.find_element(By.ID, "idSIButton9").click()
#         # Pausa por 2 segundos esperando a próxima página carregar
#         time.sleep(2)
#
#         # --- Etapa "Manter conectado?" ---
#         # Aguarda de forma inteligente até o botão de ID "idSIButton9" (botão "Sim" para manter logado) estar clicável
#         WebDriverWait(navegador, 20).until(
#             EC.element_to_be_clickable((By.ID, "idSIButton9"))
#         ).click()  # Efetua o clique logo após a validação terminar
#
#         # Aguarda 5 segundos fixos para o painel principal terminar de carregar após os logins
#         time.sleep(5)
#         # Imprime uma mensagem de confirmação de sucesso no terminal
#         print("✅ Login no Power BI realizado com sucesso")
#
#     # Se qualquer botão sumir, ID mudar ou a internet cair, o erro é capturado aqui
#     except Exception as e:
#         # Interrompe o robô e envia uma mensagem personalizada contendo o erro técnico original
#         raise Exception(f"❌ Erro ao fazer login no Power BI: {e}")
#
#
# # ==============================
# # ATUALIZA DATASET
# # ==============================
# # Define a função que vai navegar até o modelo de dados específico e forçar a sincronização de dados
# def atualizar_dataset(navegador):
#     # Inicia o bloco de proteção para a atualização do conjunto de dados
#     try:
#         # Link direto para a página de visão geral do modelo de dados (dataset) específico no Power BI Service
#         dataset_url = (
#             "https://app.powerbi.com/onelake/details/dataset/e310f74c-e506-41ce-a05d-7e20f1c3fc76/overview?experience=power-bi"
#         )
#
#         # Direciona o navegador para abrir o link do dataset configurado acima
#         navegador.get(dataset_url)
#         # Aguarda 5 segundos fixos para garantir o carregamento dos componentes complexos do OneLake/PowerBI
#         time.sleep(5)
#
#         # --- Botão Atualizar (dropdown) ---
#         # Aguarda até 20 segundos para que o menu de ID "model-actionbar-refresh" esteja visível e liberado para clique
#         WebDriverWait(navegador, 20).until(
#             EC.element_to_be_clickable((By.ID, "model-actionbar-refresh"))
#         )
#         # Encontra o botão e faz o clique para abrir as opções de atualização
#         navegador.find_element(By.ID, "model-actionbar-refresh").click()
#         # Espera 3 segundos fixos para o menu flutuante aparecer em tela
#         time.sleep(3)
#
#         # --- Opção "Atualizar Agora" ---
#         # Espera até 10 segundos até encontrar o botão exato cujo texto de acessibilidade seja 'Atualizar agora' via XPath
#         elemento = WebDriverWait(navegador, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Atualizar agora']"))
#         )
#         # Clica na opção "Atualizar agora" para disparar a rotina de atualização dos dados
#         elemento.click()
#
#         # Aguarda 5 segundos fixos para o comando ser processado nos servidores da Microsoft
#         time.sleep(5)
#         # Imprime a confirmação do comando no terminal
#         print("🔄 Dataset updated com sucesso")
#



def calcular_imposto(valor):
    if valor < 1000:
        imposto =  valor * 0.1

    elif valor < 2000:
        imposto = valor * 0.13

        