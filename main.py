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


# Dentro del script
df_EP1 = pq.read_table("../ProyectoSteam/0-DATA/1desarrollador.parquet").to_pandas()
df_EP2 = pq.read_table("../ProyectoSteam/0-DATA/2User_id.parquet").to_pandas()
df_EP3 = pq.read_table("../ProyectoSteam/0-DATA/3genero.parquet").to_pandas()
df_EP4 = pq.read_table("../ProyectoSteam/0-DATA/4año.parquet").to_pandas()
df_EP5 = pq.read_table("../ProyectoSteam/0-DATA/5desarrolladora.parquet").to_pandas()
modelo_games = pq.read_table("../ProyectoSteam/0-DATA/modelo_railway.parquet").to_pandas()



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
    # Tu lógica aquí

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
                     # 'Valve', 'Trion Worlds', 'Cryptic Studios', 'Grey Havens',
                                   #'Three Rings', 'Daybreak Game Company', 'Reloaded Productions',
                                   #'Splash Damage', 'CCP', 'Nimbly Games', 'Team Chivalry',
                                   #'PopCap Games, Inc.'otras empresas
    


# Pregunta 2
@app.get("/userdata/{usuario}", name="USERDATA", response_model=UserDataResponse)
async def UserData(usuario: str) -> UserDataResponse:

    user = df_EP2.user_id.unique()
    if usuario not in user:
        return {"message": "Mi base de datos no tiene registros de ese usuario"}
    
    lista = df_EP2.user_id.unique()
    dfusuario = df_EP2[df_EP2.user_id == usuario]
    maneyuser = f"{round(dfusuario.price.sum(), 2)} USD"
    recomend = f"{int(len(dfusuario[dfusuario.recommend == 1]) * 100 / len(dfusuario))}%"
    itemss = len(dfusuario)
    
    return UserDataResponse(
        User=usuario,
        Dinero_gastado=maneyuser,
        Porcentaje_de_recomendación=recomend,
        Cantidad_de_items=itemss
    )                 #'EizanAratoFujimaki', 'GamerFag', '76561198020928326', 'Bluegills',
                      #'76561198071955492', 'digfernandes', '76561197970812298',
                      #'meeeedie', 'phrostb', 'KewlKatzz', 'TheRealMeatyMate',
                      #'Auditore70', 'voaDs', '76561198060319088', '76561198085571748' u otros usuarios


# pregunta 3 no me sale en fastapi
@app.get("/userforgenre/{genero}", name="USERFORGENRE")
async def user_for_genre(genero: str):
    gender = df_EP3.genres_clean.unique()
    if genero not in gender:
        return {"message": "Mi base de datos no tiene registros de ese genero"}

    años = df_EP3.año.unique()
    usuario_total = None
    horas_totales_usuario = 0
    user_data = []

    for añi in años:
        # Filtrar datos para el género y año específico
        df_genero = df_EP3[(df_EP3.genres_clean == genero) & (df_EP3.año == añi)]

        # Encontrar usuario con más horas de juego
        if not df_genero.empty:
            usuario = df_genero.groupby('user_id')["playtime_hours"].sum().idxmax()
            horasT = df_genero[df_genero.user_id == usuario]["playtime_hours"].sum()

            # Actualizar usuario total si es necesario
            if horasT > horas_totales_usuario:
                usuario_total = usuario
                horas_totales_usuario = horasT

            # Añadir datos para este año
            user_data.append({"Año": añi, "Horas": horasT})
        else:
            # No se encontraron datos para este año
            user_data.append({"Año": añi, "Horas": 0})

    respuesta = {
        "Usuario con más horas jugadas para Género " + genero: usuario_total,
        "Horas jugadas": user_data,
    }

    return respuesta



    
                                #'Animation &amp; Modeling', 'Utilities', 'Massively Multiplayer',
                                #'Design &amp; Illustration', 'Video Production'
                                #'Action', 'Indie', 'Racing', 'Strategy', 'Casual', 'Simulation',
                                # Handle potential KeyError for missing data
                                #'Adventure', 'RPG', 'Sports', 'Free to Play',
                                                    


#Cuarta pregunta
@app.get("/bestdeveloperyear/{year}", name="BESTDEVELOPERYEAR")
async def BestDeveloperYear(year: int):

    rango_aceptado = range(2010, 2016)
    if year not in rango_aceptado:
        return {"message": "Mi base de datos solo tiene registros entre 2010 y 2015"}
    #year = int(year)
    recom = df_EP4[(df_EP4.recommend == 1) & (df_EP4.sentiment_analysis == 2) & (df_EP4.año == year)]
    developer_recommendations = recom.groupby("developer")["recommend"].sum()
    top_3_developers = developer_recommendations.nlargest(3)

    top_developers_list = []
    for rank, (developer, count) in enumerate(top_3_developers.items(), start=1):
        top_developers_list.append({"Puesto " + str(rank): developer})

    return top_developers_list                  # 2010,2011,2012,2013,2014,2015


#Quinta pregunta
@app.get("/developerreviewsanalysis/{desarrolladora}", name="DEVELOPERREVIEWSANALYSIS")
async def DeveloperReviewsAnalysis(desarrolladora: str) -> Union[str, Dict[str, Dict[str, int]]]:
    develo = df_EP1.developer.unique()
    if desarrolladora not in develo:
        return {"message": "Mi base de datos no tiene registros de ese desarrollador"}
    
    # Filtramos por desarrolladora
    df_filt_developer = df_EP5[(df_EP5['developer'] == desarrolladora) & (df_EP5['sentiment_analysis'] != 1)]
    # Verificamos que haya datos para la desarrolladora
    if not df_filt_developer.empty:
        # Contamos los sentimientos y mapeamos el número del sentimiento a su etiqueta correspondiente
        sentiment_counts = df_filt_developer['sentiment_analysis'].value_counts()
        sentiment_mapping = {0: 'Negative', 2: 'Positive'}
        sentiment_counts.index = sentiment_counts.index.map(sentiment_mapping)
        
        result = {desarrolladora: sentiment_counts.to_dict()}
    else:
        result = 'No cuento con los registros de esa empresa en mi base de datos'

    return result                               #'Valve', 'Outerlight Ltd.', 'GlyphX Games',
                                                #'Introversion Software', 'Facepunch Studios',
                                                #'Bugbear Entertainment', 'Funcom',
                                                #'Firaxis Games,Feral Interactive (Mac)',
                                                #'Crystal Dynamics,Feral Interactive (Mac)', 'CAPCOM Co., Ltd.',
                                                #'id Software', 'Gray Matter Studios', '2K Boston,2K Australia',
                                                #'Relic Entertainment', 'The Creative Assembly'


#Modelo de recomendacion item_item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id: int):
    
    # Verificamos si el juego con game_id existe en df_games
    game = modelo_games[modelo_games['item_id'] == id]

    if game.empty:
        return("El juego '{id}' no posee registros.")
    
    # Obtenemos el índice del juego dado
    idx = game.index[0]

    # Tomamos una muestra aleatoria del DataFrame df_games
    sample_size = 2000  # Definimos el tamaño de la muestra (ajusta según sea necesario)
    df_sample = modelo_games.sample(n=sample_size, random_state=42)  # Ajustamos la semilla aleatoria según sea necesario

    # Calculamos la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([modelo_games.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # Obtenemos las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # Ordenamos los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtenemos los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Listamos los juegos similares (solo nombres)
    similar_game_names = df_sample['app_name'].iloc[similar_game_indices].tolist()

    return {"similar_games": similar_game_names}

#uvicorn main:app --reload