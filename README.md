
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
Este proyecto fue desarrollado por [MAYK JOEL QUISPE GASPAR](https://github.com/MAYKJOEL/) como parte del Primer Proyecto Individual del programa LABs **Data Science** del BootCamp ![`SOYHENRY`](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)


## 🛠 Herramientas
Python, VisualCode, FastApi, Render


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/MAYKJOEL)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mayk-quispe-gaspar-42814a97/)


## Documentation

[Documentation](https://github.com/soyHenry/PI_ML_OPS/tree/FT?tab=readme-ov-file)

