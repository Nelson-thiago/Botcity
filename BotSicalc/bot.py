"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""

# Import for the Desktop Bot
from botcity.core import DesktopBot

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = DesktopBot()
    #bot.browse("http://www.botcity.dev")

    # Implement here your logic...
    bot.execute(r"C:\Program Files (x86)\Programas RFB\Sicalc Auto Atendimento\SicalcAA.exe")
    
    if not bot.find( "popup_esclarecimento", matching=0.97, waiting_time=10000):
        not_found("popup_esclarecimento")
    bot.click_relative(304, 318)
    
    if not bot.find( "funcoes", matching=0.97, waiting_time=10000):
        not_found("funcoes")
    bot.click()
    
    if not bot.find( "preench_darf", matching=0.97, waiting_time=10000):
        not_found("preench_darf")
    bot.click()
    
    if not bot.find( "cod_receita", matching=0.97, waiting_time=10000):
        not_found("cod_receita")
    bot.click_relative(246, 18)
    
    bot.paste("5629")
    bot.tab()
    bot.wait(100)
    
    if not bot.find( "PA", matching=0.97, waiting_time=10000):
        not_found("PA")
    bot.click_relative(51, 36)
    # Inserindo PA
    bot.paste("310120")
    
    if not bot.find( "valor_reais", matching=0.97, waiting_time=10000):
        not_found("valor_reais")
    bot.click_relative(61, 40)
    # Inserindo valor
    bot.paste("10000")
    
    if not bot.find( "calcular", matching=0.97, waiting_time=10000):
        not_found("calcular")
    bot.click()
    #aqui temos a opção de utilizar visão computacional ou o atalho do teclado para executar a ação.
    #Esse trecho de código poderia ser substituído pelo comando bot.enter(),
    #pois a tecla enter aciona o botão de calcular no Sicalc.
    
    if not bot.find( "darf", matching=0.97, waiting_time=10000):
        not_found("darf")
    bot.click()
    
    if not bot.find( "nome", matching=0.97, waiting_time=10000):
        not_found("nome")
    bot.click_relative(99, 40)
    bot.paste("Petrobras")
    
    if not bot.find( "telefone", matching=0.97, waiting_time=10000):
        not_found("telefone")
    bot.click_relative(14, 37)
    bot.paste("1199991234")
    
    if not bot.find( "cpf_cnpj", matching=0.97, waiting_time=10000):
        not_found("cpf_cnpj")
    bot.click_relative(154, 11)
    bot.paste("33000167000101")
    
    if not bot.find( "referencia", matching=0.97, waiting_time=10000):
        not_found("referencia")
    bot.click_relative(203, 11)
    bot.paste("0")
    
    if not bot.find( "imprimir", matching=0.97, waiting_time=10000):
        not_found("imprimir")
    bot.click()
    
    if not bot.find( "janela_salvamento", matching=0.97, waiting_time=10000):
        not_found("janela_salvamento")
    bot.click()
    
    # Inserindo path do arquivo
    bot.paste(r"C:\Users\noturno\Documents\DARF.pdf")
    bot.enter()
    
    bot.wait(2000)

    # Fechando janela do formulário
    bot.alt_f4()

    # Fechando app do SiCalc
    bot.alt_f4()
    
    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()





