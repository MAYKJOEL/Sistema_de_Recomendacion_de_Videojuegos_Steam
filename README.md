
# Hola, soy Mayk! 👋


# Sistema de Recomendación de Videojuegos
Este proyecto de Machine Learning se centra en desarrollar un sistema de recomendación de videojuegos basado en un modelo ítem-ítem. Utilizando Python y FastAPI, se ha creado una API que permite acceder a diversas funcionalidades relacionadas con la recomendación de videojuegos y análisis de datos.

![Logo](https://imgeucdn.gamespress.com/cdn/files/Games%20Press/2023/10/121359-c658b9a4/320976ec-3405-47ed-e665-5e71ffb995fa.gif?w=536&mode=max&otf=y&quality=90&format=gif&bgcolor=white&ex=2024-05-01+03%3A00%3A00&sky=4c93a0eab0eb938c645f39c6d4d33eabf7b387cb350a821a51240f1ac5794d31)

## Funcionalidades
### 1 -  Recomendación de Juegos Similares

* Método: `recomendacion_juego(id de producto)`
* Descripción: Recibe el ID de un juego y devuelve una lista de 5 juegos recomendados similares al ingresado.
### 2 - Análisis de Desarrollador

* Método: `developer(desarrollador: str)`
* Descripción: Proporciona la cantidad de items y el porcentaje de contenido gratuito por año según la empresa desarrolladora.
### 3 - Información de Usuario

* Método: `UserData(User_id: str)`
* Descripción: Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación basado en reviews, y la cantidad de items.
### 4 - Usuario por Género

* Método: `UserForGenre(genero: str)`
* Descripción: Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
### 5 - Mejores Desarrolladores por Año

* Método: `BestDeveloperYear(año: int)`
* Descripción: Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
### 6 - Análisis de Reseñas del Desarrollador

* Método: `DeveloperReviewsAnalysis(desarrolladora: str)`
* Descripción: Proporciona la cantidad total de registros de reseñas de usuarios categorizados con un análisis de sentimiento positivo o negativo para una desarrolladora específica.
## Implementación
El sistema está implementado en Python y utiliza FastAPI para crear una interfaz de programación de aplicaciones (API) que permite acceder a las funcionalidades mencionadas anteriormente.

## Cómo Usar
Clona este repositorio en tu máquina local.
Instala las dependencias requeridas.
Ejecuta la aplicación FastAPI.
Accede a la API a través de los endpoints especificados para realizar consultas y recibir respuestas según tus necesidades.

## Acceso al Proyecto
Para acceder al proyecto desplegado en Render, haz clic en el siguiente enlace: [Proyecto en Render](https://sistema-de-recomendacion-de-videojuegos.onrender.com/docs)

## Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, puedes hacer un fork del repositorio, implementar tus cambios y luego enviar un pull request. Se revisarán y fusionarán las contribuciones relevantes.

## Créditos
Este proyecto fue desarrollado por [MAYK JOEL QUISPE GASPAR](https://github.com/MAYKJOEL/) como parte del Primer Proyecto Individual del programa LABs **Data Science** del BootCamp ![`SOYHENRY`](data:image/png;base64,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)


## 🛠 Herramientas
Python, VisualCode, FastApi, Render


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/MAYKJOEL)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mayk-quispe-gaspar-42814a97/)


## Documentation

[Documentation](https://github.com/soyHenry/PI_ML_OPS/tree/FT?tab=readme-ov-file)

