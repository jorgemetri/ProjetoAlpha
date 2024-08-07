import os
import shutil
import pandas as pd
import time
from DownloadPhotos import CorrigirLinhasVazias
def ReturnoDataframeComLinhasVazias(df):
    df = df[df['Cidade'].isna() | (df['Cidade'] == '')]
    return df

def remove_blank_city_rows_and_columns(file_path):
    """
    Remove linhas e colunas correspondentes onde a coluna 'cidade' possui valores em branco ou nulos em um arquivo Excel,
    e salva as alterações no mesmo arquivo.
    
    Parâmetros:
    file_path (str): Caminho do arquivo Excel de entrada.
    """
    # Carrega o dataset a partir de um arquivo Excel
    df = pd.read_excel(file_path, dtype={'ID Fazendas': str})

    # Remove as linhas onde a coluna 'cidade' está em branco ou nula
    df = df.dropna(subset=['Cidade'])
    df = df[df['Cidade'].str.strip() != '']

    # Remove as colunas correspondentes
    

    # Salva o DataFrame resultante no mesmo arquivo Excel
    df.to_excel(file_path, index=False)

    print(f"Linhas e colunas correspondentes removidas quando a coluna 'Cidade' possui valores em branco ou nulos. Alterações salvas no arquivo '{file_path}'")



def verificar_linhas_vazias_no_excel(file_path):
    """
    Solicita o caminho de um arquivo Excel, carrega o DataFrame e verifica
    se existem linhas vazias na coluna 'Cidade'.
    
    Retorna:
    bool: True se existirem linhas vazias na coluna 'cidade', False caso contrário.
    """

    
    # Carregar o DataFrame a partir do arquivo Excel
    df = pd.read_excel(file_path, dtype={'ID Fazendas': str})
    
    # Verificar se existem linhas vazias na coluna 'cidade'
    return df['Cidade'].isnull().any() or df['Cidade'].str.strip().eq('').any()


def excluir_arquivo_excel(nome_arquivo):
    """
    Exclui um arquivo Excel dado o nome do arquivo.
    
    Parâmetros:
    nome_arquivo (str): O nome do arquivo Excel a ser excluído.
    """
    try:
        os.remove(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' excluído com sucesso.")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro ao excluir o arquivo '{nome_arquivo}': {e}")


def renomear_arquivo_excel(nome_arquivo_atual, novo_nome_arquivo):
    """
    Renomeia um arquivo Excel.
    
    Parâmetros:
    nome_arquivo_atual (str): O nome atual do arquivo Excel.
    novo_nome_arquivo (str): O novo nome para o arquivo Excel.
    """
    try:
        os.rename(nome_arquivo_atual, novo_nome_arquivo)
        print(f"Arquivo '{nome_arquivo_atual}' renomeado com sucesso para '{novo_nome_arquivo}'.")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo_atual}' não encontrado.")
    except Exception as e:
        print(f"Erro ao renomear o arquivo '{nome_arquivo_atual}': {e}")


def criar_copia_arquivo_excel(origem, destino):
    """
    Cria uma cópia de um arquivo Excel.
    
    Parâmetros:
    origem (str): O caminho do arquivo Excel original.
    destino (str): O caminho onde a cópia do arquivo Excel será salva.
    """
    try:
        shutil.copyfile(origem, destino)
        print(f"Cópia criada com sucesso: {destino}")
    except Exception as e:
        print(f"Erro ao criar a cópia do arquivo: {e}")

def RetornoDataframeComLinhasVazias(df):
    df = df[df['Cidade'].isna() | (df['Cidade'] == '')]
    return df


def TratamentoLinhasVazias(driver):
    print('Tratamento de linhas  Vazias----------------------------------------------')
    df = pd.read_excel('raspagem.xlsx', sheet_name='Sheet1')
    tam = len(df)
    """
    Aqui iremos tentar resolver o problema de linhas vazias. Para isso equanto existirem linhas vazias iremos  tentar achar tais linhas e baixar novamente
    tais linhas vazias. Caso nesse processo o tamanho da dataframe diminua iremos retornar o dataframe inicial caso contrário o novo dataframe
    com a operação de consertar linhas vazias.
    """

    criar_copia_arquivo_excel('raspagem.xlsx', 'raspagem1.xlsx')

    while verificar_linhas_vazias_no_excel('raspagem.xlsx'):
        print('Retornand Dataframe com linhas vazias---------')
        df=RetornoDataframeComLinhasVazias(df)
        print('Corrigir Linhas Vazias ---------')
        CorrigirLinhasVazias(driver,df)
        print('Remover linhas em branco da coluna cidade------')
        remove_blank_city_rows_and_columns('raspagem.xlsx')
        df = pd.read_excel('raspagem.xlsx', sheet_name='Sheet1')
        if len(df) < tam:
            """
            Caso entrarmos aqui é porque algo deu erraod logo iremos excluir raspagem.xlsx (arquivo modificado) e retornaremos
            raspagem1.xlsx que sera renomeado para raspagem.xlsx
            """
            excluir_arquivo_excel('raspagem.xlsx')
            renomear_arquivo_excel('raspagem1.xlsx','raspagem.xlsx')
            print('Arquivo original com linhas vazias na coluna Cidade retornado retornado!')

            break
        else:
            excluir_arquivo_excel('raspagem1.xlsx')
            print('Arquivo raspagem modificado com linhas vazias resolvido retornado!')
    if verificar_linhas_vazias_no_excel('raspagem.xlsx') == False:
        print('Excluir Raspagem')
        excluir_arquivo_excel('raspagem1.xlsx')
    '''
    Remover coluna contador
    '''
    # Load the Excel file
    df = pd.read_excel('raspagem.xlsx', engine='openpyxl', dtype={'ID Fazendas': str}, sheet_name='Sheet1')

    # Drop the 'Contador' column
    df = df.drop('Contador', axis=1)

    # Save the modified DataFrame back to the Excel file
    df.to_excel('raspagem.xlsx', index=False)
    print('Tabela raspagem completa com as colunas: Cidade, ID Fazendas, Fotos das fazendas!')
  

    
    


    