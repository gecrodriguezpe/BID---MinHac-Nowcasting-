# Descripción del script: 

# Librerías de trabajo 
import time 
import os   # Funcionalidades que permiten trabajar con el sistema operativo directamente 
import pandas as pd  # Liberaría pandas para trabajar con "dataframes" en python
from pytrends.request import TrendReq 

# Especificar el directorio de trabajo principal 
main = f"{os.getcwd()}\../"

# Nota: Dentro del directorio de trabajo principal se encontrarán las siguientes tres carpetas: 
## input: Bases de datos que contienen las palabras de busqueda por google trends
## output: 
## scripts: 


# Se importan la bases de datos con las palabras de busqueda de google trends 

## Palabras originales ministerio haciendas
palabras_orig_min_hacienda = pd.read_excel(f"{main}inputs/inputs_gtrends_modified.xlsx", header=0)

## palabras dominicanos 
#palabras_dominicanos = pd.read_excel(f"{main}inputs/inputs_gtrends_extended_word_pool.xlsx", sheet_name = "palabras_dominicanos", header=0)

## palabras german 
#palabras_german = pd.read_excel(f"{main}inputs/inputs_gtrends_extended_word_pool.xlsx", sheet_name = "palabras_german", header=0)



# Función diseñada para descargar 
def busqueda_google_ternds(df_input, slp_time = 30, words_before_stop = 5): 
    '''

    Parameters
    ----------
    df_input: pandas dataframe 
        Base de datos de entrada, que contiene todas las palabras que van a ser buscadas por google trends 

    slp_time: int 
        Tiempo de espera, entre cada grupo de 5 palabras. Se usa para evitar problemas de "RateLimit" con google trends 

    Returns 
    -------
    None: La función no retorna nada 

    '''
    # 
    pytrends = TrendReq(tz=360, timeout=(10,25))

    # Base de datos que almacenará las variables recuperadas de google trends 
    df = pd.DataFrame()

    # Contador que permitirá saber en que palabra específica de la lista de palabras de google trends se encuentra el ciclo
    count = 0

    # Ciclo que permite descargar/recuperar información de "google trends" palabra por palabra 
    for index, row in df_input.iterrows():

        # Específica que palabra se está buscando en cada iteración 
        print(f"Buscando: {row['palabra']}")
        
        # 
        t = "all"
        pytrends.build_payload([row["palabra"]], cat=0, timeframe=t, geo=row["origen"])
        
        # 
        data = pd.DataFrame(pytrends.interest_over_time())
        data.drop("isPartial", axis=1, inplace=True)
        df = pd.merge(df, data, how='outer', left_index=True, right_index=True)
        
        # La base de datos se almacena o guarda en el archivo "GTrends.csv" en la carpeta 
        df.to_csv(f"{main}/output/GTrends.csv") # Creo que se puede mejorar esta parte, porque reescribe el archivo cada vez que genera una nueva palabra
        
        # Para evitar problemas de RateLimit, hacemos un "sleep" cada 5 palabras.

        ## Se actualiza la "variable contador" después de cada busqueda de google trends
        count = count+1
        ## Después de buscar 5 palabras, se espera "slp_time" antes de hacer la busqueda del siguiente grupo de variables
        if count == words_before_stop: print("Sleeping %d segs" %slp_time); time.sleep(slp_time); count=0

# Llamo a la función para "busqueda_google_ternds" recuperar de google trends las palabras en la base de datos "df_input", con un tiempo de latencia entre cada grupo de 5 palabras de "slp_time"

# Busqueda google trends: "Palabras originales ministerio haciendas"
busqueda_google_ternds(palabras_orig_min_hacienda, slp_time = 60, words_before_stop = 4)

# 
#busqueda_google_ternds(palabras_dominicanos, slp_time = 30)

# 
#busqueda_google_ternds(palabras_german, slp_time = 30)

