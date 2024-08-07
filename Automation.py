import os
import shutil
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from DownloadPhotos import PegarElementoModificado,TryDownloadSheetAlphaProject,move_specific_file_Alpha_Project,PegarElementoModificadoAlphaProject,CorrigirLinhasVazias
from ResolveLinhasVazias import TratamentoLinhasVazias

def ErrorEmailVerification(driver,attempts=5,delay=1):
    tries= 1
    while tries<=attempts:
        try:
            driver.find_element(By.XPATH,"/html/body/div/div/section/form/div[1]/div[2]/button[2]").click()
        except Exception as e:
            print("Nao recebeu error de verificação de email!")
        time.sleep(delay)
        tries+=1
    print("Passou pela fase de error na verificação de email!")

    


def TryGetElement(driver,type,pathelement):
    if type == 'css':
       try:
           WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, pathelement))
            )
           return True
       except Exception as e:
           return False
    elif type == 'xpath':
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, pathelement))
            )
        except Exception as e:
            return False



def GetCity(driver,pathelement):
    print('------------Clicando na primeira imagem---------------------')
    
    #Verificando se o elemento existe na tela
    while True:
        if TryGetElement(driver,'css',pathelement) == True:
            break
    #Clicando na imagem
    time.sleep(5)
    img_element = driver.find_elements(By.CSS_SELECTOR, pathelement)
    img_element[0].click()
    print('Clickou na Image')
    #Verificando se o elemento existe na tela
    while True:
        if TryGetElement(driver,'css','div.item > p.main-info') == True:
            break
    time.sleep(5)
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.item > p.main-info')
    str=elements[len(elements)-1].text
    array = str.split(', ')
    return array[1]
    



def VerifyPaths():
    paths = []
    try:
        #Verificar se os caminhos existem no arquivo txt
        with open('paths.txt', 'r') as file:
            for line in file:
                # Strip the newline character from the end of each line and add to the list
                paths.append(line.strip())
        #Após estarem no arquivo txt, esses serão atribuidos no aos forms:
        return paths
    except FileNotFoundError:
        print("Error: The file 'filename.txt' does not exist.")
        return []


 
def DownloadingPhotos1(driver):
    print("---------------------Download Photos-------------------------------------------")
    tamanho = driver.find_element(By.XPATH,"/html/body/s123-app/div/main/ng-component/div/ng-component/div/div[1]/header-menubar/div/feature-count/div").text.split("/")[0]
    total= int(tamanho)

    rows = []
    maxlen = 0
    for i in range(total):
        element = driver.get(f'https://survey123.arcgis.com/surveys/7c7eb1d6f2b74421a50e01a2d9eb2667/data?extent=-80.6008,-21.9941,-13.8039,-9.7200&objectIds={(i)}')
        # Wait for a specific element to be present on the page (adjust the locator as needed)
        try:
            # Example: wait for an element with id "element_id" to be present
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.\\30 .ir.ir-middle"))
            )
            img_elements = driver.find_elements(By.CSS_SELECTOR, "img.\\30 .ir.ir-middle")
            element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.answer"))
        )
            Idfazenda =  driver.find_elements(By.CSS_SELECTOR, "p.answer")[2].text
            print(Idfazenda)
            # Iterate over the found elements and print their 'src' attribute
            row = []
            row.append(Idfazenda)

            #Iterando sobre a lista de imagens e obtendo link-----------------------------------------

            urls = []
            for img in img_elements:
                urls.append(img.get_attribute('src'))
            if len(urls)>maxlen:
                maxlen = len(urls)
            #Obtendo a cidade-------------------------------------------------------------------------   
            city=GetCity(driver,'img.ir.ir-middle') 
            row.append(city)
            #Combinandos dois arrays----------------------------------------------------
            unique_array=  row+urls
            #Gerando arry final----------------------------------------------------------
            rows.append(unique_array)
            
            print(f'fazenda {i}, linha :{row}')
            
        except Exception as e:
            print(f"Error waiting for page to load: {e}")
    

    print('----------------Criando dataframe-------------------------------')

    #Determinando o número de colunas para foto-------------------------------------------------------------
    pictures=[]
    for i in range(1,maxlen+1):
        pictures.append(f'Foto {i}')
    header = ['ID fazenda','Cidade']
    header = header+pictures
    print(header)
    df = pd.DataFrame(rows,columns=header)
    df['ID fazenda'] = df['ID fazenda'].str.replace('.', '', regex=False)
    df['ID fazenda'] = df['ID fazenda'].astype(float)
    print("-----------------------Download Photos Encerrado--------------------")
    return df
        #df.to_excel('ProjetoTerraFotos.xlsx',index=False)
#DownloadPhotos-------------------------------------------------------------------------------------------------------------------
def Isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
def TryGetElementFazenda(driver,path):
    try:
        # Wait until the element containing <b>ID Fazenda</b> is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[b[text()='ID Fazenda']]"))
        )

        # Find the sibling <p> element and get its text
        answer = element.find_element(By.XPATH, "following-sibling::p[@class='answer']").text

        return answer
    except Exception as e:
            TryGetElementFazenda(driver,path)
def GetElementIdFazenda(driver,path):
    IdFazenda = TryGetElementFazenda(driver,path)
    return IdFazenda
def DownloadingPhotos(driver):
    print("---------------------Download Photos-------------------------------------------")
    tamanho = driver.find_element(By.XPATH,"/html/body/s123-app/div/main/ng-component/div/ng-component/div/div[1]/header-menubar/div/feature-count/div").text.split("/")[0]
    total= int(tamanho)
    #total = 5
    rows = []
    maxlen = 0
    for i in range(1,total+1):
        element = driver.get(f'https://survey123.arcgis.com/surveys/7c7eb1d6f2b74421a50e01a2d9eb2667/data?extent=-80.6008,-21.9941,-13.8039,-9.7200&objectIds={(i)}')
        # Wait for a specific element to be present on the page (adjust the locator as needed)
        try:
            # Example: wait for an element with id "element_id" to be present
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.\\30 .ir.ir-middle"))
            )
            img_elements = driver.find_elements(By.CSS_SELECTOR, "img.\\30 .ir.ir-middle")
            #Pegando IdFazenda----------------------------------------------------------------------
            Idfazenda = GetElementIdFazenda(driver, "p.answer")
         
            # Iterate over the found elements and print their 'src' attribute
            row = []
            row.append(Idfazenda)

            #Iterando sobre a lista de imagens e obtendo link-----------------------------------------

            urls = []
            for img in img_elements:
                urls.append(img.get_attribute('src'))
            if len(urls)>maxlen:
                maxlen = len(urls)
            #Obtendo a cidade-------------------------------------------------------------------------   
            city=GetCity(driver,'img.ir.ir-middle') 
            row.append(city)
            #Combinandos dois arrays----------------------------------------------------
            unique_array=  row+urls
            #Gerando arry final----------------------------------------------------------
            rows.append(unique_array)
            
            print(f'fazenda {i}, linha :{row}')
            
        except Exception as e:
            print(f"Error waiting for page to load: {e}")
    

    print('----------------Criando dataframe-------------------------------')

    #Determinando o número de colunas para foto-------------------------------------------------------------
    pictures=[]
    for i in range(1,maxlen+1):
        pictures.append(f'Foto {i}')
    header = ['ID fazenda','Cidade']
    header = header+pictures
    print(header)
    df = pd.DataFrame(rows,columns=header)
    df['ID fazenda'] = df['ID fazenda'].str.replace('.', '', regex=False)
    df['ID fazenda'] = df['ID fazenda'].astype(float)
    print("-----------------------Download Photos Encerrado--------------------")
    return df       
#DownloadPhotos-------------------------------------------------------------------------------------------------------------------

def RemovingColumns(path):
    print("--------------------Removendo colunas------------------------------------")
    """
    Dado o nome do arquivo excel e supondo que ele esteja na mesma pasta onde o programa está sendo executado, iremos tratar essa base de dados de modo que iremos 
    remover algumas colunas e deixar apenas três colunas que é ID Fazenda, x e y. Assim após efetuar as devidas operações a função retorna o dataframe
    
    Parameters:
    path(str): Nome do arquivo excel que será tratado.

    Returns:
    Dataframe
    """
    sheet_name = 'PROJETO_TRIANGULO_0'
    df = pd.read_excel(path, sheet_name=sheet_name)
    removeColumns = [column for column in df.columns if 'ID Fazenda' not in column and 'x' not in column and 'y' not in column]
    etl =  df.drop(removeColumns,axis=1)
    etl.columns = ["ID fazenda","longitude","latitude"]
    print("--------------------Dataframe criado com as colunas: ID Fazenda, longitude, latitude--------------------")
    return etl


def CreatingFiltredDataframe(df):
    print("------------------Criando Dataframe Filtrado com ID Fazenda, Latitude, Longitude-----------------------")
    """
    Após ter filtrado as colunas necessárias do dataframe, será criado um novo dataframe que é resultado de operar sobre todas as linhas do antigo dataframe
    e ao iterar sobre todas as linhas criar um novo dataframe onde a primeira coluna é ID Fazenda, e a segunda é o resultado de aplicar o método get_city_name
    nas colunas latitude e longitude para retornar a cidade.
    
    Parameters:
    df(dataframe): Dataframe

    Returns:
    Dataframe
    """
    newdf = []
    # Iterating over each row using iloc
    for i in range(len(df)):
        row = df.iloc[i]        
        rows = [row['ID fazenda'],get_city_name(row['latitude'],row['longitude'])]
        print(rows)
        newdf.append(rows)
        
    newdf = np.array(newdf)
    newdf = pd.DataFrame(newdf,columns=['ID fazenda','Cidade'])
    newdf["ID fazenda"] =newdf["ID fazenda"].astype(float)
    print("-------------------------Operacao De Dataframe filtrado realizada---------------------------------------------")
    return newdf


def CreatingExcel(df,name):
    """
    Recebe um dataframe e o nome do arquivo excel que será gerado e retorna um arquivo excel com nome que foi informado.
    Parameters:
    df(dataframe): Dataframe
    name(str): Nome do novo arquivo excel que será criado. Deve ser da forma :nome.xlsx
    Returns:
    ExcelFile
    """  
    file_path = name
    
    try:
        # Attempt to write the DataFrame to an Excel file
        df.to_excel(file_path, index=False)
        print(f"File '{file_path}' has been successfully created/overwritten.")
    except Exception as e:
        # Catch and print any exception that occurs during the process
        print(f"An error occurred while trying to create/overwrite the file '{file_path}': {e}")
        
    print(f'O dataframe foi criado para : {file_path}')


def get_city_name(latitude, longitude):
    geolocator = Nominatim(user_agent="my_unique_app_name")
    geocode = RateLimiter(geolocator.reverse, min_delay_seconds=2)
    location = geocode((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    
    city = address.get('city', '')
    if not city:
        city = address.get('town', '')
    if not city:
        city = address.get('village', '')
    
    return city


#def MoveFile(downloads,target):
    # Essa função pega o arquivo baixado e coloca ele na pasta
    # onde o programa esta rodando

    # Alterando path para a pasta de downloads
    #os.chdir(rf'{downloads}')

    # Iremos iterar pela pasta de downloads e procurar o arquvio desejado

    #for file in os.listdir('.'):
        #if '_EXCEL' in file:
            #shutil.move(rf'{downloads}\{file}',rf'{target}')
            #print(f'Arquivo: {file} movida com sucesso para {target}!')

#Versão antiga             
def MoveFile1(downloads, target):
    # This function takes the downloaded file and places it in the folder
    # where the program is running

    # Ensure the paths are properly escaped
    downloads = downloads.replace('\\', '\\\\')
    target = target.replace('\\', '\\\\')

    # Changing path to the downloads folder
    os.chdir(downloads)

    # We will iterate through the downloads folder and look for the desired file
    cont = 0
    for file in os.listdir('.'):
        if '_EXCEL' in file:
            shutil.move(f'{downloads}\\{file}', f'{target}')
            print(f'Arquivo: {file} movido com sucesso para {target}!')
            cont=cont+1
            print(cont)
            break
            
    if cont == 0:
        print('Arquivo não estava na pasta downloads!')
#Versão alterada
def MoveFile(submain2_instance,downloads, target):
    # This function takes the downloaded file and places it in the folder
    # where the program is running

    # Ensure the paths are properly escaped
    #downloads = downloads.replace('\\', '\\\\')
    #target = target.replace('\\', '\\\\')

    # Changing path to the downloads folder
    os.chdir(downloads)

    # We will iterate through the downloads folder and look for the desired file
    cont = 0
    for file in os.listdir('.'):
        if '_EXCEL' in file:
            try:
                destination = os.path.join(target, file)
                if os.path.exists(destination):
                    os.remove(destination)
                    submain2_instance.insert_text(f'Arquivo: {file} já existia em {target}. Reescrevendo o arquivo.')
                    #print(f'Arquivo: {file} já existia em {target}. Reescrevendo o arquivo.')

                shutil.move(f'{downloads}\\{file}', destination)
                #print(f'Arquivo: {file} movido com sucesso para {target}!')
                submain2_instance.insert_text(f'Arquivo: {file} movido com sucesso para {target}!')
            except shutil.Error as e:
                submain2_instance.insert_text(f'Ocorreu um erro ao mover o arquivo: {e}')
                print(f'Ocorreu um erro ao mover o arquivo: {e}')
            cont += 1
            print(cont)
            break
            
    if cont == 0:
        #print('Arquivo não estava na pasta downloads!')
        submain2_instance.insert_text('Arquivo não estava na pasta downloads!')
    

def PreProcessorDataframe(df):
    return
            
def TransformingSheet(submain2_instance,driver,target):

    """
    Supondo que o path do diretório atual esteja na pasta onde o arquivo 
    esteja sendo executado( essa suposição é valida pois a função movefile
    será responsável por tal atividade), a planilha do excel baixada, será
    transformada em uma nova contendo apenas o ID da fazenda e em seguida 
    transformará a coluna de latitude e longitude em nome da cidade.

    Essa função ao fazer as devidas alterações cria uma nova planilha 
    sem alterar a atual.

    Parameters:
    excel_name (str): Nome da planilha do excel

    Returns:
    None
    """
    os.chdir(target)
    for file in os.listdir('.'):
        if 'S123_7c7eb1d6f2b74421a50e01a2d9eb2667_EXCEL' in file:
            submain2_instance.insert_text('---------------------------Criando Excel com as fotos-----------------------------------')
            #print('---------------------------Criando Excel com as fotos-----------------------------------')
            #print('Encontrou o arquivo excel que será transformado')
            submain2_instance.insert_text('Encontrou o arquivo excel que será transformado')
            etl = RemovingColumns(file)
            submain2_instance.insert_text("Filtrando colunas do excel que foi baixado e retornando um dataframe")
            #print("Filtrando colunas do excel que foi baixado e retornando um dataframe")
            #etl = CreatingFiltredDataframe(etl)
            
            photo = DownloadingPhotos(driver)
            #Agora que temos o dataframe formatado iremos baixar as fotos
            #e em seguida combinar o dataframe
            #submain2_instance.insert_text("------- Terminou de baixar as fotos agora iremos juntar as bases de dados --------------------")
            #print("------- Terminou de baixar as fotos agora iremos juntar as bases de dados --------------------")
            #merged_df = pd.merge(etl, photo, on='ID fazenda', how='inner')
            submain2_instance.insert_text("------------Criando a planilha excel com a planilha resultante final--------------------")
            #print("------------Criando a planilha excel com a planilha resultante final--------------------")
            CreatingExcel(photo,"arquivofinal.xlsx")
            submain2_instance.insert_text('Finalizado!')
            #print('Finalizado!')
            submain2_instance.insert_text("-----------------------------------------------------------------------------")
            #print('---------------------------------------------------------------------------')
            break
    return etl

  
def DownloadingSheet(submain2_instance,driver):
    """
    Após a função que faz o login ter sido chamado devemos, passar em seguida 
    para a função que irá fazer o download da planilha e em seguida irá
    mover os dados par a pasta onde o programa esta sendo executado.

    Parameters:
    driver(obj): Objeto driver da lib do selenium necessário para poder fazer
    as devidas automações necessárias
    downloads (str): O caminho do download do usuário
    target( str): O caminho da pasta onde será enviada a planilha (pasta
    onde o programa está sendo executada)
    

    Returns:
    None
    """

    submain2_instance.insert_text("-----------------------------------------------------------------------------")
    submain2_instance.insert_text('Clicando no elemento para abrir o menu de exportar arquivo ')

    driver.find_element(By.XPATH,'/html/body/s123-app/div/main/ng-component/div/ng-component/div/div[1]/header-menubar/div/print-util-menus/div/div[2]/a').click()
    time.sleep(5)
    submain2_instance.insert_text('Exportando arquivo EXCEL ')
    driver.find_element(By.XPATH,'/html/body/s123-app/div/main/ng-component/div/ng-component/div/div[1]/header-menubar/div/print-util-menus/div/div[2]/ul/li[4]/a/div').click()
    submain2_instance.insert_text("-----------------------------------------------------------------------------")
    time.sleep(5)

    return
def logIn(submain2_instance,pathWebDriver,driver):
    """
    Dado o path onde se encontra o webdriver.exe e também o prórprio driver
    nós iremos fazer o login na página.

    Parameters:
    pathWebDriver (str): O caminho onde está o webdriver.exe
    driver(obj): Objeto driver da lib do selenium necessário para poder fazer
    as devidas automações necessárias

    Returns:
    None
    """
    #path = r'C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\chromedriver.exe'
    submain2_instance.insert_text("-----------------------------------------------------------------------------")

    submain2_instance.insert_text('Iniciando as configurações inicias do login')
    pathWebDriver = rf'{pathWebDriver}'
    service = Service(executable_path=pathWebDriver)


    driver = webdriver.Chrome(service=service)


    # Maximize the brownser window
    driver.maximize_window()
    link = "https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=survey123hub&display=default&redirect_uri=https%3A%2F%2Fsurvey123.arcgis.com%2Fsurveys&parent=https://survey123.arcgis.com&locale=pt-br&response_type=token&expiration=720"
        
  
    submain2_instance.insert_text('Iniciando o acesso a página para logar')
    driver.get(link)

   
    time.sleep(3)


    driver.find_element(By.XPATH,'//*[@id="user_username"]').send_keys("GISinnovatech")


    driver.find_element(By.XPATH,'//*[@id="user_password"]').send_keys("GIS@innova10#")

 
    driver.find_element(By.XPATH,'//*[@id="signIn"]').click()
    time.sleep(3)
    ErrorEmailVerification(driver)
    print('Login Feito!')
   
    link_dados = "https://survey123.arcgis.com/surveys/7c7eb1d6f2b74421a50e01a2d9eb2667/data"

    submain2_instance.insert_text('Indo para a página onde será feito o download do Excel')
    driver.get(link_dados)

    

    submain2_instance.insert_text('Finalizado o login!')
    print('Finalizado o login!')
    submain2_instance.insert_text("-----------------------------------------------------------------------------")
 
    return driver


#path =  str(input('Digite o caminho da pasta:'))
#target = str(input('Digite o pasta alvo:'))


#MoveFile(path,target)
# Functions ----------------------------------------------------------------------------------------
"""
Função Corrigir Linhas vazias:------------------------------------------------------------------------------

"""


def AutomationRpa(self,submain2_instance, download, target,chromedriver):

    
   
    # Add your automation code here, e.g., interacting with webdriver, downloading files, etc.

    # Simulating some actions
    if download == "" or target == "":
        submain2_instance.insert_text("Error! Por favor Preencha os campos adequadamente para antes de iniciar a automação.")

    else:
        options = Options()
        options.add_argument("--headless")

        #PARÂMETRO PARA MANTER WEBDRIVER ATUALIZADO
        servico = Service(ChromeDriverManager().install())

        #ENVIANDO PARÂMETROS PARA O DRIVER
        driver = webdriver.Chrome(options=options,service=servico)
       

        submain2_instance.insert_text("-----------------------------------------------------------------------------")
        submain2_instance.insert_text('---------------------Iniciando a automação-----------------------------------')
        #driver = webdriver.Chrome()
        #pathsWebdriver = str(input('Digite o caminho do webdriver:'))
        
        #pathsWebdriver = r'C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\RPAInnovatech\chromedriver.exe'
        pathsWebdriver = chromedriver
        #downloadspath = str(input('Digite o caminho do download: '))
        #targetpath = str(input('Digite o caminho onde o programa está sendo executado: '))
        #pathsWebdriver = arg3
        downloadspath = download
        targetpath = target
        
        if len(VerifyPaths()) > 0:
            pass
        else:
            lines = [f'{download}\n',f'{target}\n']
            with open('paths.txt','w') as file:
                file.writelines(lines)
            
        


        
        driver=logIn(submain2_instance,pathsWebdriver,driver)
        # DownloadingSheet(submain2_instance,driver)
        # submain2_instance.insert_text("Baixando o arquivo...")
        # time.sleep(20)
        # MoveFile(submain2_instance,downloadspath,targetpath)
        TryDownloadSheetAlphaProject(driver)
        time.sleep(2)
        move_specific_file_Alpha_Project(download,target)
        os.chdir(targetpath)
        PegarElementoModificado(driver)
        
        """
        Resolvendo problema com linhas brancas
        """
        TratamentoLinhasVazias(driver)








        os.chdir(targetpath)
        submain2_instance.insert_text("---------------------------Encerrando Automação-----------------------------")
def AutomationRpa1(self,submain2_instance, download, target,chromedriver):

    
   
    # Add your automation code here, e.g., interacting with webdriver, downloading files, etc.

    # Simulating some actions
    if download == "" or target == "":
        submain2_instance.insert_text("Error! Por favor Preencha os campos adequadamente para antes de iniciar a automação.")

    else:
        
            
        
        options = Options()
        options.add_argument("--headless")

        # Definindo o caminho diretamente para o ChromeDriver
        try:
            service = Service(chromedriver)
            driver = webdriver.Chrome(service=service, options=options)
        except OSError as e:
            print(f"Erro ao iniciar o ChromeDriver: {e}")
            return

        downloadspath = download
        targetpath = target

        if len(VerifyPaths()) > 0:
            pass
        else:
            lines = [f'{download}\n', f'{target}\n']
            with open('paths.txt', 'w') as file:
                file.writelines(lines)






        
        driver=logIn(submain2_instance,chromedriver,driver)
        # DownloadingSheet(submain2_instance,driver)
        # submain2_instance.insert_text("Baixando o arquivo...")
        # time.sleep(20)
        # MoveFile(submain2_instance,downloadspath,targetpath)
        TryDownloadSheetAlphaProject(driver)
        time.sleep(2)
        move_specific_file_Alpha_Project(download,target)
        os.chdir(targetpath)
        PegarElementoModificado(driver)
        
        """
        Resolvendo problema com linhas brancas
        """
        TratamentoLinhasVazias(driver)








        os.chdir(targetpath)
        submain2_instance.insert_text("---------------------------Encerrando Automação-----------------------------")
#LoginAlphaProject---------------------------------------------------------------------------------------------------------
def logInProjetoAlpha(pathWebDriver,driver):
    """
    Dado o path onde se encontra o webdriver.exe e também o prórprio driver
    nós iremos fazer o login na página.

    Parameters:
    pathWebDriver (str): O caminho onde está o webdriver.exe
    driver(obj): Objeto driver da lib do selenium necessário para poder fazer
    as devidas automações necessárias

    Returns:
    None
    """
    #path = r'C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\chromedriver.exe'
    #submain2_instance.insert_text("-----------------------------------------------------------------------------")

    #submain2_instance.insert_text('Iniciando as configurações inicias do login')
    pathWebDriver = rf'{pathWebDriver}'
    service = Service(executable_path=pathWebDriver)


    driver = webdriver.Chrome(service=service)


    # Maximize the brownser window
    driver.maximize_window()
    link = "https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=survey123hub&display=default&redirect_uri=https%3A%2F%2Fsurvey123.arcgis.com%2Fsurveys&parent=https://survey123.arcgis.com&locale=pt-br&response_type=token&expiration=720"
        
  
    #submain2_instance.insert_text('Iniciando o acesso a página para logar')
    driver.get(link)

   
    time.sleep(3)


    driver.find_element(By.XPATH,'//*[@id="user_username"]').send_keys("GISinnovatech")


    driver.find_element(By.XPATH,'//*[@id="user_password"]').send_keys("GIS@innova10#")

 
    driver.find_element(By.XPATH,'//*[@id="signIn"]').click()
    time.sleep(3)

    ErrorEmailVerification(driver)
    
    print('Login Feito!')
   
    link_dados = "https://survey123.arcgis.com/surveys/75bc7c0c6e674430b13433169665526f/data?extent=-77.4500,-54.3446,-167.4500,81.1536a"

    #submain2_instance.insert_text('Indo para a página onde será feito o download do Excel')
    driver.get(link_dados)

    
    #time.sleep(50)
    #submain2_instance.insert_text('Finalizado o login!')
    print('Finalizado o login!')
    #submain2_instance.insert_text("-----------------------------------------------------------------------------")
 
    return driver

#AutomationAlphaProject-----------------------------------------------------------------------------------------------------
def AutomationRpaAlphaProject(self,submain2_instance, download, target,chromedriver):

    
   
    # Add your automation code here, e.g., interacting with webdriver, downloading files, etc.

    # Simulating some actions
    if download == "" or target == "":
        submain2_instance.insert_text("Error! Por favor Preencha os campos adequadamente para antes de iniciar a automação.")

    else:
        options = Options()
        options.add_argument("--headless")

        #PARÂMETRO PARA MANTER WEBDRIVER ATUALIZADO
        servico = Service(ChromeDriverManager().install())

        #ENVIANDO PARÂMETROS PARA O DRIVER
        driver = webdriver.Chrome(options=options,service=servico)
       

        submain2_instance.insert_text("-----------------------------------------------------------------------------")
        submain2_instance.insert_text('---------------------Iniciando a automação-----------------------------------')
        #driver = webdriver.Chrome()
        #pathsWebdriver = str(input('Digite o caminho do webdriver:'))
        
        #pathsWebdriver = r'C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\RPAInnovatech\chromedriver.exe'
        pathsWebdriver = chromedriver
        #downloadspath = str(input('Digite o caminho do download: '))
        #targetpath = str(input('Digite o caminho onde o programa está sendo executado: '))
        #pathsWebdriver = arg3
        downloadspath = download
        targetpath = target
        
        if len(VerifyPaths()) > 0:
            pass
        else:
            lines = [f'{download}\n',f'{target}\n']
            with open('paths.txt','w') as file:
                file.writelines(lines)
            

        # TryDownloadSheetAlphaProject(driver)
        # time.sleep(2)
        # destination_path = 'C:\\Users\\jorge\\OneDrive\\Desktop\\rpa'
        # path_download = 'C:\\Users\\jorge\\Downloads'
        # move_specific_file_Alpha_Project(path_download,destination_path)
        
        #driver=logIn(submain2_instance,pathsWebdriver,driver)
        driver = logInProjetoAlpha(pathsWebdriver,driver)
        TryDownloadSheetAlphaProject(driver)
        time.sleep(2)
        move_specific_file_Alpha_Project(download,target)
        os.chdir(targetpath)
        PegarElementoModificadoAlphaProject(driver)
        #TransformingSheet(submain2_instance,driver,targetpath)
        """
        Resolvendo problema com linhas brancas
        """
        TratamentoLinhasVazias(driver)
        


        os.chdir(targetpath)
        submain2_instance.insert_text("---------------------------Encerrando Automação-----------------------------")
def AutomationRpaAlphaProject1(download, target, chromedriver_path):
    if download == "" or target == "":
        pass
    else:
        options = Options()
        options.add_argument("--headless")

        # Definindo o caminho diretamente para o ChromeDriver
        try:
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
        except OSError as e:
            print(f"Erro ao iniciar o ChromeDriver: {e}")
            return

        downloadspath = download
        targetpath = target

        if len(VerifyPaths()) > 0:
            pass
        else:
            lines = [f'{download}\n', f'{target}\n']
            with open('paths.txt', 'w') as file:
                file.writelines(lines)

        # Adicionando suas funções de automação aqui
        driver = logInProjetoAlpha(chromedriver_path, driver)
        TryDownloadSheetAlphaProject(driver)
        time.sleep(2)
        move_specific_file_Alpha_Project(download, target)
        os.chdir(targetpath)
        PegarElementoModificadoAlphaProject(driver)
        TratamentoLinhasVazias(driver)
        os.chdir(targetpath)
    
#---------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #AutomationRpa(r'C:\Users\JORGEMETRIMIRANDA\Downloads',r'C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\RPAInnovatech')
    #TransformingSheet('Projeto Terra 5.xlsx',r'C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\RPAInnovatech')
    print('')
    AutomationRpaAlphaProject1(r'C:\Users\JORGEMETRIMIRANDA\Downloads',r'C:\Users\JORGEMETRIMIRANDA\Innovatech Gestão Empresarial e Agroflorestal Ltda\AGENTE ALPHA - Documentos\Robo - RPA 0.3 v\dist',r'C:\Users\JORGEMETRIMIRANDA\Innovatech Gestão Empresarial e Agroflorestal Ltda\AGENTE ALPHA - Documentos\Robo - RPA 0.3 v\dist\chromedriver.exe')
#C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech
#C:\Users\JORGEMETRIMIRANDA\Desktop\Innovatech\RPAInnovatech\chromedriver.execls