# Descripción del script: 
## Realizar "Rolling Correlations" entre la series de tiempo de busquedas relativas de "google trends" y variables del DANE (PIB e ISE)

### Rolling correlations: 
#### 1) Metodología para encontrar la correlación entre dos series de tiempo a partir de una ventana móvil 
#### 2) Permite visualizar variaciones de la correlación a lo largo del tiempo

# 1. Importar librerías y especificar directorio de trabajo ----  

# Librerías de trabajo 
import time 
import os   # Funcionalidades que permiten trabajar con el sistema operativo directamente 
import pandas as pd  # Liberaría pandas para trabajar con "dataframes" en python
import matplotlib.pyplot as plt # Librería para graficar en "python"

# Especificar el directorio de trabajo principal 
main = f"{os.getcwd()}\../"

# 2. Especificar funciones dentro del script ----

# Función que transforma datos mensuales a trimestrales 
def mensual_a_trimestral(df_mensual):

    # Assuming the dataframe has a DateTimeIndex
    if not isinstance(df_mensual.index, pd.DatetimeIndex):
        raise ValueError("The DataFrame should have a DateTimeIndex.")

    # Resample to quarterly frequency
    df_trimestral = df_mensual.resample('Q', convention='end').mean()

    # If you want to keep the last quarter even if it's incomplete, use 'Q-DEC' as the frequency
    # quarterly_data = dataframe.resample('Q-DEC').mean()

    return df_trimestral

# 3. Importación y procesamiento de datos ----

# 3.1 Datos de Google Trends ----

# 3.1.1 Datos Mensuales de Google Trends ----

# Imporación base de datos con las "palabras de busqueda" en google trends
palabras_google_trends_mensual = pd.read_csv(f"{main}bases_datos/input/gtrends/GTrends_original.csv", header=0)

# Transformar la variale 'date' a tipo DateTimeIndex
palabras_google_trends_mensual['date'] = pd.to_datetime(palabras_google_trends_mensual['date'])

# Designar la variable 'date' como indice de la base de datos 
palabras_google_trends_mensual.set_index('date', inplace=True)

# Filtro la base de datos de gtrends para que empiece desde el año 2006 en adelante (y sea comparable con los datos de PIB y de ISE)
palabras_google_trends_mensual = palabras_google_trends_mensual[palabras_google_trends_mensual.index >= '2006-01-01']

# Visualizar los primero 10 datos de la base mensual
#print(palabras_google_trends_mensual.head(10))

# Visualizar los tipos de datos en la base 
#print(palabras_google_trends_mensual.dtypes)

# 3.1.2 Datos Trimestrales de Google Trends ----

# Transforma la base de palabras de google trends a datos trimestrales 
palabras_google_trends_trimestral = mensual_a_trimestral(palabras_google_trends_mensual)

# Nota: Extraer los nombres de la base de datos de "google trends"
colnames_google_trends = palabras_google_trends_mensual.columns

# Nota: Transformar los nombres de la base de datos de "google trends" en una lista de strings
colnames_google_trends_lst = colnames_google_trends.tolist()

# Visualizar los datos de la base de datos de google trends transformados a datos trimestrales 
# print(palabras_google_trends_mensual.head(10))
#print(palabras_google_trends_trimestral.head(10))

# 3.2 Datos del DANE ----

# 3.2.1 Datos mensuales del ISE ----

# Importación base de datos con el ISE desestacionalizado mensual 
ISE_desestac_mensual = pd.read_excel(f"{main}bases_datos/input/DANE/ISE_PIB_procesados.xlsx", header=0, sheet_name = "ISE_desesta_mensual")

# Transformar la variale 'fecha' a tipo DateTimeIndex
ISE_desestac_mensual['fecha'] = pd.to_datetime(ISE_desestac_mensual['fecha'])

# Designar la variable 'fecha' como indice de la base de datos 
ISE_desestac_mensual.set_index('fecha', inplace=True)

# Filtro la base de datos del ISE para que empiece desde el año 2006 en adelante 
ISE_desestac_mensual= ISE_desestac_mensual[ISE_desestac_mensual.index >= '2006-01-01']

#print(ISE_desestac_mensual.head(10))

# 3.2.2 Datos trimestrales del ISE ----

# Transforma la base del ISE a datos trimestrales 
ISE_desestac_trimestral = mensual_a_trimestral(ISE_desestac_mensual)

# print(ISE_desestac_trimestral.head(10))

# 3.3.1 Datos trimestrales del PIB ----

# Importación base de datos PIB Trimestral 
PIB_trimestral = pd.read_excel(f"{main}bases_datos/input/DANE/ISE_PIB_procesados.xlsx", header=0, sheet_name = "PIB_trimestral")

# Filtro la base de datos del PIB para que empiece desde el año 2006 en adelante 
PIB_trimestral = PIB_trimestral.drop(PIB_trimestral.index[:4])

# Designar la variable 'fecha' de la base "ISE_desestac_trimestral" como indice de la base de datos PIB_trimestral
PIB_trimestral.set_index(ISE_desestac_trimestral.index, inplace=True)

#print(PIB_trimestral.head(10))

# 4. Ejercicio de correlaciones ----

# 4.1 Correlaciones simples entre series de tiempo ----

# 4.1.1 Correlación entre el PIB y el ISE 
PIB_ISE_corr = PIB_trimestral["PIB_crec_anual"].corr(ISE_desestac_trimestral["ISE_crec_anual"])
print(PIB_ISE_corr)

# 4.1.2 Correlación entre las variables del DANE y las palabras extraidas de Google Trends 

# Función que me genera la correlación entre las variables del DANE y las variables de Google Trends 
def simple_correlations(df_DANE, df_google_tends, nomb_variable_df_DANE):
    
    # Lista que almacenará los objetos "numpy.float64" que resultan de la correlación entre alguna variable del DANE con alguna palabra de google trends
    simple_correl_list = []
    
    # Ciclo que itera a través de las columnas de la base de datos de google trends para poder hacer la correlación entre dichas variables y la variable del DANE de interés
    for variable in range(df_google_tends.shape[1]): 
        
        # Genero la correlación entre cada palabra de google trends con alguna variable del DANE 
        nueva_simple_correl = df_DANE[nomb_variable_df_DANE].corr(df_google_tends.iloc[:, variable])
        
        # Voy agregando a la lista cada una de los "numpy.float64" que guardan la correlación entre la correspondiente palabra de google trends y la variable del DANE de interés
        simple_correl_list.append(nueva_simple_correl)
    
    # Concateno o junto cada uno de los "numpy.float64" guradados en la lista "simple_correl_list" en un solo dataframe 
    #simple_corr_df = pd.concat(simple_correl_list, axis = 1)
    
    # Retorno el dataframe que almacena las rolling correlations entre las palabras de google trends y las variables del DANE
    return(simple_correl_list)

# Correlaciones ISE

# Simple correlation ISE vs palabras google trends (Frecuencia mensual)
ISE_mensual_simple_corr_lst = simple_correlations(ISE_desestac_mensual, palabras_google_trends_mensual, nomb_variable_df_DANE= "ISE_crec_anual")
ISE_mensual_simple_corr_dict = dict(zip(colnames_google_trends_lst, ISE_mensual_simple_corr_lst))
ISE_mensual_simple_corr_df = pd.DataFrame([ISE_mensual_simple_corr_dict], index = ["Correlaciones"])

# Simple correlation ISE vs palabras google trends (Frecuencia trimestral)
ISE_trimestral_simple_corr_lst = simple_correlations(ISE_desestac_trimestral, palabras_google_trends_trimestral, nomb_variable_df_DANE= "ISE_crec_anual")
ISE_trimestral_simple_corr_dict = dict(zip(colnames_google_trends_lst, ISE_trimestral_simple_corr_lst))
ISE_trimestral_simple_corr_df = pd.DataFrame([ISE_trimestral_simple_corr_dict], index = ["Correlaciones"])

# Correlaciones PIB

# Simple correlation PIB vs palabras google trends (Frecuencia trimestral)
PIB_trimestral_simple_corr_lst = simple_correlations(PIB_trimestral, palabras_google_trends_trimestral, nomb_variable_df_DANE= "PIB_crec_anual")
PIB_trimestral_simple_corr_dict = dict(zip(colnames_google_trends_lst, PIB_trimestral_simple_corr_lst))
PIB_trimestral_simple_corr_df = pd.DataFrame([PIB_trimestral_simple_corr_dict], index = ["Correlaciones"])

# 4.2 Rolling correlations: Correlaciones en ventana móvil de las dos series de tiempo ----

# Función que me genera la rolling correlation entre las variables del DANE y las variables de google trends
def roll_correlations(df_DANE, df_google_tends, nomb_variable_df_DANE, roll_window):
    
    # Lista que almacenará los objetos Series (de pandas) que resultan de la rolling correlation entre alguna variable del DANE con alguna palabra de google trends
    roll_correl_list = []
    
    # Ciclo que itera a través de las columnas de la base de datos de google trends para poder hacer la rolling correlation entre dichas variables y la variable del DANE de interés
    for variable in range(df_google_tends.shape[1]): 
        
        # Genero la rolling correlation entre cada palabra de google trends con alguna variable del DANE 
        nueva_roll_correl = df_DANE[nomb_variable_df_DANE].rolling(roll_window).corr(df_google_tends.iloc[:, variable])
        
        # Voy agregando a la lista cada una de las Pandas Series que guardan la rolling correlation entre la correspondiente palabra de google trends y la variable del DANE de interés
        roll_correl_list.append(nueva_roll_correl)
    
    # Concateno o junto cada uno de los pandas Series guradados en la lista "roll_correl_list" en un solo dataframe 
    roll_corr_df = pd.concat(roll_correl_list , axis = 1)
    
    # Retorno el dataframe que almacena las rolling correlations entre las palabras de google trends y las variables del DANE
    return(roll_corr_df)


# Rolling correlation ISE vs PIB (Frecuencia trimestral)
PIB_ISE_trimestral_roll_corr = PIB_trimestral["PIB_crec_anual"].rolling(12).corr(ISE_desestac_trimestral["ISE_crec_anual"])

# Correlaciones ISE

# Rolling correlation ISE vs palabras google trends (Frecuencia mensual)
ISE_mensual_roll_corr_df = roll_correlations(ISE_desestac_mensual, palabras_google_trends_mensual, nomb_variable_df_DANE= "ISE_crec_anual", roll_window = 36)
ISE_mensual_roll_corr_df.columns = colnames_google_trends 

# Rolling correlation ISE vs palabras google trends (Frecuencia trimestral)
ISE_trimestral_roll_corr_df = roll_correlations(ISE_desestac_trimestral, palabras_google_trends_trimestral, nomb_variable_df_DANE= "ISE_crec_anual", roll_window = 12)
ISE_trimestral_roll_corr_df.columns = colnames_google_trends 

# Correlaciones PIB
PIB_trimestral_roll_corr_df = roll_correlations(PIB_trimestral, palabras_google_trends_trimestral, nomb_variable_df_DANE= "PIB_crec_anual", roll_window = 12)
PIB_trimestral_roll_corr_df.columns = colnames_google_trends 



# 5. Visualización de las correlaciones móviles ----

# 5.1 Visualización de las correlaciones móviles entre el PIB y el ISE ----

def plot_roll_ISE_PIB(roll_corr, PIB_ISE_corr):
        
    # Visualizar graficamente las rolling correlations
    plt.plot(roll_corr, label='Rolling Correlation ISE + PIB')
    plt.title('Rolling Correlation ISE + PIB')
    plt.xlabel('Tiempo')
    plt.ylabel('Correlación')
    
    # Correlación de cero
    plt.axhline(y=PIB_ISE_corr, color='red', linestyle='--', label='corr simple')
    
    plt.legend()
    plt.show()    



plot_roll_ISE_PIB(PIB_ISE_trimestral_roll_corr, PIB_ISE_corr)


# 5.2 Visualización de las correlaciones móviles entre las variables del DANE y las palabras de Google Trends ----

def plot_roll_correlations(roll_corr_df):

    # Lista con los nombres en el orden que se gr�fica
    colnames_lst = roll_corr_df.columns.tolist()

    for variable in range(roll_corr_df.shape[1]):
        
        # 
        roll_corr = roll_corr_df.iloc[:, variable]
        
        # Visualizar graficamente las rolling correlations
        plt.plot(roll_corr, label='Rolling Correlation' + ' ' + colnames_lst[variable])
        plt.title('Rolling Correlation'+ ' ' + colnames_lst[variable])
        plt.xlabel('Tiempo')
        plt.ylabel('Correlación')
        
        # Correlación de cero
        plt.axhline(y=0, color='red', linestyle='--', label='corr = 0')
        
        plt.legend()
        plt.show()    
        
        
# ISE: Gráficas Rolling Correlations 
        
#plot_roll_correlations(ISE_mensual_roll_corr_df)

# plot_roll_correlations(ISE_trimestral_roll_corr_df)

# PIB: Gráficas Rolling Correlations 

plot_roll_correlations(PIB_trimestral_roll_corr_df)


