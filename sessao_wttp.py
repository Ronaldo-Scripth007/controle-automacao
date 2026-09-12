# SEÇÃO DO CHROME PERSISTENTE - SESSÃO SALVA DO WATSAP PARA COMPARTILHAR COM OUTRAS AUTOMAÇÃO.
# Quando os dois scripts roda em horario diferente. colocar este scrip nos dois scrit que roda em horarios diferentes.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def iniciar_navegador():
    opcoes = Options()
    # Lembre-se de colocar o caminho real da pasta aqui
    opcoes.add_argument(r"user-data-dir=C:\Caminho\Sessao_WhatsApp_Unica")
    driver = webdriver.Chrome(options=opcoes)

    return driver  # Entrega o navegador configurado
































  #= COLOCA EM CADA SCRIPT QUE VIA COMPARTILHAR O LOGUIM #=

# from sessao_wpp import iniciar_navegador      ## Importa a função lá do seu arquivo separado
# driver = iniciar_navegador()   # # Chama a função: ela abre o Chrome e guarda na variável 'driver'
# # A partir daqui, o código segue normalmente...
# driver.get("https://web.whatsapp.com")
# # ... resto da sua automação ...











