

# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    maestro.alert(
        task_id=execution.task_id,
        title="BotYoutube - Inicio",
        message="Estamos iniciando o processo",
        alert_type=AlertType.INFO
    )

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    bot.browser = Browser.CHROME
    bot.driver_path = r"C:\Users\Nelson Thiago\Desktop\Botcity\BotCotacao2\resources\chromedriver.exe"
    
    
    # Abre o canal da Python Brasil no YouTube
    #bot.browse("https://www.youtube.com/@pythonbrasiloficial")

    # Recuperando o parametro "canal" e assumindo valor padrão como
    # o canal da Python Brasil
    canal = execution.parameters.get("canal", "pythonbrasiloficial")

    # Abrindo o navegador com o canal informado
    bot.browse(f"https://www.youtube.com/@{canal}")
    
    # Faz a busca por ID
    elemento_inscritos = bot.find_element("subscriber-count", By.ID)

    # Se não encontrar, faz a busca por XPATH
    if not elemento_inscritos:
        print(f"nao achou o elemento pelo By.ID e vai usar o xpath")
        elemento_inscritos = bot.find_element('//span[contains(text(), "inscritos")]', By.XPATH)

    inscritos = elemento_inscritos.text
    print(f"Inscritos => {inscritos}")

    bot.wait(2000)
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Tarefa BotYoutube finalizada com sucesso",
        total_items=100, # Número total de itens processados
        processed_items=90, # Número de itens processados com sucesso
        failed_items=10 # Número de itens processados com falha
     )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
