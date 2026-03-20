# ¡Hola! Bienvenidos a este pequeño experimento con Ollama

¿Sabes qué es lo más fascinante de estas "cajas de pensamiento" que llamamos LLMs? No es solo lo que *saben*, sino lo que *pueden llegar a hacer* cuando les damos las herramientas adecuadas. 

Imagina que estás intentando explicarle a alguien cómo funciona un reloj. Puedes contárselo (teoría), puedes darle un destornillador (herramientas), o puedes darle el manual de instrucciones (contexto). Este repositorio es exactamente eso: una demostración de cómo un modelo local de Ollama se comporta en cuatro escenarios distintos, evolucionando en cada paso.

---

### 1. Rama `main`: "El Pensador Solitario"
Aquí tenemos al modelo en su estado más puro. Imagina a un genio encerrado en una habitación sin ventanas. Le haces una pregunta y él rebusca en sus recuerdos de entrenamiento.
- **Propósito:** Demostrar el razonamiento puro y sus límites.
- **Lo nuevo:** Hemos añadido **Persistencia de Memoria** para que el genio no olvide de qué estás hablando.

### 2. Rama `feature/tools`: "El Artesano con Herramientas"
¡Aquí la cosa se pone divertida! Le hemos dado al modelo un cinturón de herramientas (scripts de Python). Ahora, cuando le pides un cálculo, el modelo dice: *"Espera, no tengo que adivinar esto, ¡puedo usar mi calculadora!"*.
- **Propósito:** Mostrar la ejecución de herramientas exactas.
- **Lo nuevo:** Un motor de **Extracción Robusta (Regex)** que entiende a la IA aunque se equivoque al escribir el formato técnico.

### 3. Rama `feature/markdown`: "El Investigador con Biblioteca"
¿Y si el modelo necesita saber algo que no está en sus recuerdos? En esta rama le damos una biblioteca de archivos Markdown. Pero no se los leemos todos, sino que le enseñamos a ir a la estantería y sacar el libro correcto.
- **Propósito:** Demostrar la Recuperación Dinámica de Conocimiento (RAG).
- **Lo nuevo:** **Transparencia Total**. La IA ahora cita el archivo que leyó y confirma cuánta información recuperó.

### 4. Rama `feature/expert`: "El Agente de Operaciones" (La Cúspide)
Esta es la unión de todo lo anterior. Aquí el modelo es un Soporte Técnico Autónomo. No solo sabe leer el manual, sino que puede tomar acciones reales basándose en lo que ha investigado.
- **Propósito:** Mostrar el ciclo completo de Razonamiento y Acción (ReAct).
- **Lo nuevo:** **Guía de Estado Activa**. Un director de orquesta que asegura que la IA siga el protocolo sin saltarse pasos.

---

### ¿Por qué hacemos esto?
Porque para entender algo de verdad, hay que construirlo. La inteligencia no es solo memoria; es saber qué herramienta usar y dónde buscar la información que te falta. 

¡Explora las ramas, corre el código y observa cómo cambia la "personalidad" de la IA!
