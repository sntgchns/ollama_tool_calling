# ¡Hola! Bienvenidos a este pequeño experimento con Ollama

¿Sabes qué es lo más fascinante de estas "cajas de pensamiento" que llamamos LLMs? No es solo lo que *saben*, sino lo que *pueden llegar a hacer* cuando les damos las herramientas adecuadas. 

Imagina que estás intentando explicarle a alguien cómo funciona un reloj. Puedes contárselo (teoría), puedes darle un destornillador (herramientas), o puedes darle el manual de instrucciones (contexto). Este repositorio es exactamente eso: una demostración de cómo un modelo local de Ollama (el pequeño pero valiente `qwen2.5:3b`) se comporta en cuatro escenarios distintos.

---

### 1. Rama `main`: "El Pensador Solitario"
Aquí tenemos al modelo en su estado más puro. Imagina a un genio encerrado en una habitación sin ventanas. Le haces una pregunta y él rebusca en sus recuerdos (lo que aprendió durante su entrenamiento).
- **Propósito:** Demostrar el razonamiento puro del modelo.
- **Lo que verás:** Si le pides una suma compleja o un dato muy específico, el modelo hará su mejor esfuerzo, pero podría alucinar. Es brillante, pero está aislado.

### 2. Rama `feature/tools`: "El Artesano con Herramientas"
¡Aquí la cosa se pone divertida! Le hemos dado al modelo un cinturón de herramientas (scripts de Python). Ahora, cuando le pides calcular el área de un círculo o convertir bases numéricas, el modelo dice: *"Espera, no tengo que adivinar esto, ¡puedo usar mi calculadora!"*.
- **Propósito:** Mostrar la **ejecución de herramientas algorítmicas**.
- **Lo que verás:** El modelo detecta qué herramienta necesita y usa lógica matemática exacta para responderte.

### 3. Rama `feature/markdown`: "El Investigador con Biblioteca"
¿Y si el modelo necesita saber algo que no está en sus recuerdos ni es una fórmula? En esta rama le damos una biblioteca: archivos `.md`. Pero no se los leemos todos a la vez, sino que le enseñamos a ir a la estantería y sacar el libro correcto cuando lo necesite.
- **Propósito:** Demostrar la **Recuperación Dinámica de Conocimiento**.
- **Lo que verás:** El modelo consultará documentos (como el de Computación Cuántica) para darte respuestas basadas en hechos reales y documentados.

### 4. Rama `feature/expert`: "El Agente de Operaciones" (La Cúspide)
Esta es la unión de todo lo anterior. Aquí el modelo es un **Soporte Técnico Autónomo**. No solo sabe leer el manual, sino que puede tomar acciones reales en el sistema basándose en lo que ha investigado.
- **Propósito:** Mostrar el **ciclo completo de Razonamiento, Investigación y Acción (ReAct)**.
- **Lo que verás:** Ante un problema, el modelo verificará el estado del servidor, buscará el error en el manual y ejecutará el reinicio del servicio correcto. Es la IA actuando como un ingeniero.

---

### ¿Por qué hacemos esto?
Porque la inteligencia no es solo memoria; es saber qué herramienta usar y dónde buscar la información que te falta. ¡Explora las ramas, corre el código y observa cómo cambia la "personalidad" de la IA!

*— Richard (a través de este código)*
