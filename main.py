"""
FUNCIONES CREADAS PARA EL PROYECTO FINAL INDIVIDUAL 1 DE DATA SCIENCE DE SOY HENRY
                            - STEAM GAMES - 

FUNCIONES PARA ALIMENTAR LA API
"""

#uvicorn main:app --reload

#librerías
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, List, Union
import pandas as pd
import scipy as sp
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional
from pydantic import BaseModel

# Instanciamos la aplicación

app = FastAPI()


# Dentro del script3genero.csv
df_EP1 = pq.read_table("1desarrollador.parquet").to_pandas()
df_EP2 = pq.read_table("2User_id.parquet").to_pandas()
df_EP3 = pq.read_table("3genero.parquet").to_pandas()
df_EP4 = pq.read_table("4año.parquet").to_pandas()
df_EP5 = pq.read_table("5desarrolladora.parquet").to_pandas()
modelo_games = pq.read_table("modelo_render.parquet").to_pandas()



@app.get("/", response_class=HTMLResponse)
async def inicio():
    template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas sobre juegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam, su fuente confiable para consultas especializadas sobre la plataforma de videojuegos.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=template)


#uvicorn main:app --reload

# Antes de la definición de las funciónes
class DeveloperYearData(BaseModel):
    Año: int
    Cantidad_de_Items: int
    Contenido_Free: str

class DeveloperInfo(BaseModel):
    empresa_desarrolladora: str
    Lista_de_Años_y_porcentage_de_juegos_gratis: List[DeveloperYearData]

class UserDataResponse(BaseModel):
    User: str
    Dinero_gastado: str
    Porcentaje_de_recomendación: str
    Cantidad_de_items: int



#Pregunta 1
@app.get("/developer/{desarrollador}", name="DEVELOPER", response_model=DeveloperInfo)
async def developer(desarrollador: str) -> DeveloperInfo:

    """
    Obtiene la cantidad y porcentaje de juegos gratuitos por año para un desarrollador específico.

    Parámetros:

        Desarrollador (str): Ej: 'Valve', 'Trion Worlds', 'Cryptic Studios', 'Grey Havens', 'Three Rings', 'Daybreak Game Company', 'Reloaded Productions', 'Splash Damage', 'CCP', 'Nimbly Games', 'Team Chivalry', 'PopCap Games, Inc.'otras empresas
    
    Retorna:
    
         DeveloperInfo: Un objeto que contiene una lista de diccionarios, cada uno representando un año con la cantidad de juegos y el porcentaje de juegos gratuitos para ese año.
    """

    # Tu lógica aquí
    desarrollador = desarrollador.lower()
    # Validar que el desarrollador exista en el dataframe
    devel = df_EP1.developer.unique()
    if desarrollador not in devel:
        return {"message": "Mi base de datos no tiene registros de ese desarrollador"}

    # Obtener los años únicos y los nombres de desarrolladores únicos
    lista_años = df_EP1.año.unique()
    lista_desarrolladores = df_EP1.developer.unique()

    # Lista para almacenar la información
    lista = []

    # Recorrer los años
    for año in lista_años:

        # Obtener la cantidad total de items del desarrollador en ese año
        total = len(df_EP1[(df_EP1.año == año) & (df_EP1.developer == desarrollador)])

        # Obtener la cantidad de items gratuitos del desarrollador en ese año
        cantidad_items_free = len(df_EP1[(df_EP1.price == 0) & (df_EP1.año == año) & (df_EP1.developer == desarrollador)])

        # Calcular el porcentaje de contenido gratuito
        if total != 0 or cantidad_items_free != 0:
            porcentaje = f"{round(cantidad_items_free * 100 / total, 2)}%"
        else:
            porcentaje = "0%"

        # Agregar la información del año al modelo Pydantic
        diccionario_año = DeveloperYearData(Año=año, Cantidad_de_Items=cantidad_items_free, Contenido_Free=porcentaje)
        lista.append(diccionario_año)

    # Devolver el modelo Pydantic con la información del desarrollador
    return DeveloperInfo(empresa_desarrolladora=desarrollador, Lista_de_Años_y_porcentage_de_juegos_gratis=lista)
                     
    
#uvicorn main:app --reload


# Pregunta 2
@app.get("/userdata/{usuario}", name="USERDATA", response_model=UserDataResponse)
async def UserData(usuario: str) -> UserDataResponse:

    """
    Información del usuario, incluyendo cantidad de dinero gastado, porcentaje de recomendación y cantidad de items, o un mensaje de error si el usuario no existe.
    
    Parámetros:

        Usuario (str): El ID del usuario a consultar. Ej: 'EizanAratoFujimaki', 'GamerFag', '76561198020928326', 'Bluegills', '76561198071955492', 'digfernandes', '76561197970812298', 'meeeedie', 'phrostb', 'KewlKatzz', 'TheRealMeatyMate', 'Auditore70', 'voaDs', '76561198060319088', '76561198085571748' u otros usuarios

    Retorna:
    
        Obtiene información sobre el usuario especificado.
    """

    # Convertimos el nombre de usuario a minúsculas para evitar errores de coincidencia de mayúsculas y minúsculas
    usuario = usuario.lower()

    # Obtenemos la lista de usuarios únicos en la columna "user_id" del DataFrame
    user = df_EP2.user_id.unique()

    # Verificamos si el usuario proporcionado está en la lista de usuarios del DataFrame
    if usuario not in user:
        # Si el usuario no está en la lista, devolvemos un mensaje indicando que no hay registros para ese usuario
        return {"message": "Mi base de datos no tiene registros de ese usuario"}

    # Filtramos el DataFrame para obtener los datos del usuario proporcionado
    dfusuario = df_EP2[df_EP2.user_id == usuario]

    # Calculamos la cantidad de dinero gastado por el usuario, redondeado a 2 decimales, y lo representamos en formato USD
    maneyuser = f"{round(dfusuario.price.sum(), 2)} USD"

    # Calculamos el porcentaje de recomendación del usuario (es decir, el porcentaje de reseñas positivas sobre el total de reseñas)
    # y lo representamos como un porcentaje entero
    recomend = f"{int(len(dfusuario[dfusuario.recommend == 1]) * 100 / len(dfusuario))}%"

    # Contamos la cantidad de items que ha adquirido el usuario
    itemss = len(dfusuario)

    # Creamos y devolvemos un objeto UserDataResponse con la información del usuario
    return UserDataResponse(
        User=usuario,
        Dinero_gastado=maneyuser,
        Porcentaje_de_recomendación=recomend,
        Cantidad_de_items=itemss
    )



#uvicorn main:app --reload


# pregunta 3 no me sale en fastapi
@app.get("/userforgenre/{genero}", name="USERFORGENRE")
async def user_for_genre(genero: str) -> Dict[str, Union[str, List[Dict[str, Union[float, str]]]]]:

    """
    Devuelve el usuario con más horas jugadas para un género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

    Parámetros:

        Genero del juego (str). Ej: 'Video Production', 'Action', 'Indie', 'Racing', 'Strategy', 'Casual', 'Simulation', 'Adventure', 'RPG', 'Sports', 'Free to Play',

    Retorna:

        Un diccionario con la información del usuario con más horas jugadas por año de lanzamiento.
    """

    # Convertimos la primera letra del género en mayúscula y el resto en minúscula
    generoO = genero.capitalize()
    genero = genero.lower()

    # Obtenemos la lista de géneros únicos en la columna "genres_clean" del DataFrame
    gender = df_EP3.genres_clean.unique()

    # Verificamos si el género proporcionado está en la lista de géneros del DataFrame
    if genero not in gender:
        # Si el género no está en la lista, devolvemos un mensaje indicando que no hay registros para ese género
        return {"message": "Mi base de datos no tiene registros de ese genero"}

    # Obtenemos la lista de años únicos en la columna "año" del DataFrame
    años = df_EP3.año.unique()

    # Inicializamos las variables para almacenar al usuario con más horas jugadas y las horas totales
    usuario_total = None
    horas_totales_usuario = 0
    user_data = []

    # Iteramos sobre los años únicos
    for añi in años:
        # Filtramos el DataFrame para obtener los datos del género específico y el año actual
        df_genero = df_EP3[(df_EP3.genres_clean == genero) & (df_EP3.año == añi)]

        # Verificamos si hay datos para el género y año actuales
        if not df_genero.empty:
            # Encontramos al usuario con más horas de juego para el género y año actuales
            usuario = df_genero.groupby('user_id')["playtime_hours"].sum().idxmax()
            horasT = df_genero[df_genero.user_id == usuario]["playtime_hours"].sum()

            # Actualizamos el usuario con más horas jugadas si es necesario
            if horasT > horas_totales_usuario:
                usuario_total = usuario
                horas_totales_usuario = horasT

            # Añadimos los datos de horas jugadas para este año al usuario_data
            user_data.append({"Año": añi, "Horas": horasT})
        else:
            # Si no hay datos para este año, añadimos un diccionario con horas igual a cero al usuario_data
            user_data.append({"Año": añi, "Horas": 0})

    # Creamos el diccionario de respuesta con el usuario con más horas jugadas y las horas jugadas por año
    respuesta = {
        f"Usuario con más horas jugadas para el Género {generoO} solicitado es": usuario_total,
        "Horas jugadas": user_data,
    }

    # Devolvemos la respuesta
    return respuesta    
                                
                                                    
#uvicorn main:app --reload


#Cuarta pregunta
@app.get("/bestdeveloperyear/{year}", name="BESTDEVELOPERYEAR")
async def BestDeveloperYear(year: int):

    """
    La siguiente función devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
    
    Parametros de entrada: 

        Ej: 2010, 2011, 2012, 2013, 2014 y 2015
    """

    # Definimos el rango de años aceptado en la base de datos
    rango_aceptado = range(2010, 2016)

    # Verificamos si el año proporcionado está dentro del rango aceptado
    if year not in rango_aceptado:
        # Si no está dentro del rango, devolvemos un mensaje indicando el rango válido de años en la base de datos
        return {"message": "Mi base de datos solo tiene registros entre 2010 y 2015"}

    # Filtramos el DataFrame para obtener las recomendaciones positivas y el análisis de sentimientos igual a 2 para el año proporcionado
    recom = df_EP4[(df_EP4.recommend == 1) & (df_EP4.sentiment_analysis == 2) & (df_EP4.año == year)]

    # Agrupamos por desarrollador y sumamos las recomendaciones para cada uno
    developer_recommendations = recom.groupby("developer")["recommend"].sum()

    # Seleccionamos los 3 mejores desarrolladores con más recomendaciones
    top_3_developers = developer_recommendations.nlargest(3)

    # Creamos una lista para almacenar los 3 mejores desarrolladores
    top_developers_list = []

    # Iteramos sobre los 3 mejores desarrolladores y sus cantidades de recomendaciones
    for rank, (developer, count) in enumerate(top_3_developers.items(), start=1):
        # Añadimos el desarrollador y su posición a la lista
        top_developers_list.append({"Puesto " + str(rank): developer})

    # Devolvemos la lista de los 3 mejores desarrolladores
    return top_developers_list


#uvicorn main:app --reload

#Quinta pregunta
@app.get("/developerreviewsanalysis/{desarrolladora}", name="DEVELOPERREVIEWSANALYSIS")
async def DeveloperReviewsAnalysis(desarrolladora: str) -> Union[str, Dict[str, Dict[str, int]]]:

    """
    La siguiente función devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentran categorizados con un análisis de sentimiento como valor positivo o negativo.

    Parametros de entrada:

        Nombre de empresas desarrolladoras de juegos. Ej: Ejemplos de entrada: Valve, Outerlight Ltd., GlyphX Games, Introversion Software, Facepunch Studios, Bugbear Entertainment, Funcom, Firaxis Games, Feral Interactive (Mac)
                                                                     
    """  

    # Convertimos el nombre de la desarrolladora a minúsculas para evitar errores de coincidencia de mayúsculas y minúsculas
    desarrolladora = desarrolladora.lower()
    
    # Obtenemos la lista única de desarrolladoras en el DataFrame proporcionado
    develo = df_EP1.developer.unique()
    
    # Comprobamos si la desarrolladora proporcionada está en la lista de desarrolladoras del DataFrame
    if desarrolladora not in develo:
        # Si no está en la lista, devolvemos un mensaje indicando que no hay registros para esa desarrolladora
        return {"message": "Mi base de datos no tiene registros de ese desarrollador"}
    
    # Filtramos el DataFrame para obtener solo las reseñas de la desarrolladora proporcionada
    df_filt_developer = df_EP5[(df_EP5['developer'] == desarrolladora) & (df_EP5['sentiment_analysis'] != 1)]
    
    # Verificamos si hay datos para la desarrolladora proporcionada
    if not df_filt_developer.empty:
        # Contamos los diferentes sentimientos y mapeamos el número del sentimiento a su etiqueta correspondiente
        sentiment_counts = df_filt_developer['sentiment_analysis'].value_counts()
        sentiment_mapping = {0: 'Negative', 2: 'Positive'}
        sentiment_counts.index = sentiment_counts.index.map(sentiment_mapping)
        
        # Creamos un diccionario con el nombre de la desarrolladora y los recuentos de sentimientos
        result = {desarrolladora: sentiment_counts.to_dict()}
    else:
        # Si no hay datos disponibles para la desarrolladora, devolvemos un mensaje indicando que no hay registros
        result = 'No cuento con los registros de esa empresa en mi base de datos'

    # Devolvemos el resultado
    return result                            



#uvicorn main:app --reload

#Modelo de recomendacion item_item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id: int):

    """La siguiente función genera un diccionario de 5 juegos similares como recomendación al juego introducido mediante su codigo de identificación.
    
    Parametros de entrada:
    
        'id' de un juego. Ej: 10, 3260, 100980, 207340, 2520, 1700, 4230 

    Retorna:
    
        Un diccionario con la recomendación de 5 juegos similares 
    """
    
    # Filtrar el DataFrame 'modelo_games' para obtener el juego con el ID especificado
    game = modelo_games[modelo_games['item_id'] == id]

    # Verificar si el DataFrame resultante está vacío
    if game.empty:
        return("El juego '{id}' no posee registros.")

    # Obtener el índice del primer registro del juego seleccionado
    idx = game.index[0]

    # Tamaño de la muestra para calcular la similitud
    sample_size = 2000  

    # Tomar una muestra aleatoria del DataFrame 'modelo_games'
    df_sample = modelo_games.sample(n=sample_size, random_state=42)  

    # Calcular la similitud coseno entre el juego seleccionado y la muestra aleatoria
    sim_scores = cosine_similarity([modelo_games.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # Extraer los puntajes de similitud
    sim_scores = sim_scores[0]

    # Crear una lista de tuplas de juegos similares con su puntaje de similitud
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]

    # Ordenar los juegos similares por puntaje de similitud en orden descendente
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtener los índices de los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Obtener los nombres de los juegos más similares
    similar_game_names = df_sample['app_name'].iloc[similar_game_indices].tolist()

    # Devolver un diccionario que contiene los nombres de los juegos similares
    return {"similar_games": similar_game_names}


#uvicorn main:app --reload