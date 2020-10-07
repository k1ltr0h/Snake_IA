# Snake-IA

![Menu Background](imgs/snake_bg.png)

Juego Snake con agente que ejecuta algoritmos de búsqueda.

* Escrito en python
* Greedy
* Greedy DFS con cola de prioridad
* RRT


## Instalación

* Descargar python3 desde la [página oficial](https://www.python.org/downloads/).

* Descargar biblioteca `pygame` por medio de `pip` en la terminal.

```
pip3 install pygame
```

## Ejecutar aplicación
Descargar el código desde el repositorio y correr el archivo como cualquier otro script python.
```
python Snake_Game.py
```

## Botones y configuraciones

![Controles](imgs/controles.png)

En la pantalla de inicio(Menú principal), podemos seleccionar entre jugar o iniciar la simulación con nuestro agente ejecutando los algoritmos de búsqueda.

![Menú](imgs/menu.png)

Para elegir un algoritmo para nuestro agente, debemos iniciar la simulación seleccionando `simulación` en el menú principal y luego presionar `Espacio` para pausar y elegir el algoritmo a gusto.

Por defecto viene `Greedy_Priority`

![Algoritmo](imgs/algoritmo.png)

Basta con presionar `Espacio` nuevamente para volver a la simulación y que nuestro agente ajecute en su próxima búsqueda el algoritmo seleccionado.

## Greedy clásico
Elige el nodo inmediatamente menos costoso en cada iteración. Si no llega a su objetivo con su actual ruta(atrapado) finaliza la búsqueda.

![Greedy](imgs/greedy.png)

## Greedy DFS con prioridad
Elige el nodo inmediatamente menos costoso del punto de vista de la `Distancia euclediana` y recorre ese camino siguiendo la misma lógica. Si no encuentra un camino en la ruta actual, es decir no hay más nodos, retrocede al nodo anterior y sigue la búsqueda en el siguiente nodo más barato(guardado en la cola de prioridad) que se enlaza al de la pocisión actual, viendolo de esta forma tiene una similitud con `DFS`(Depth First Search), ya que analiza los caminos a profundidad en cada búsqueda. **El costo de los enlaces no está contemplado en la heurística**. Si no encuentra ruta posible(atrapado), llama a `Greedy clásico` para despejar una posible salida, si esto no sucede finaliza la búsqueda, en otro caso se ejecuta el algoritmo nuevamente tomando como punto inicial el último nodo recorrido con `Greedy clásico`.


![Greedy DFS Priority](imgs/greedy_priority_dfs.png)

Cada nodo tiene 4 enlaces posibles, si de alguna manera el costo hacia el objetivo fuera el mismo para las 4 posiciones(o las que esten disponibles, es decir no hay obstaculos) el orden de elección para la selección del proximo nodo está dada por `Up, Down, Left, Right`.

[Greedy DFS con cola de prioridad en acción](https://www.youtube.com/watch?v=Wb_aUWTxIuA)


## Gracias a

* [Snake simple, código base](python-game-development-creating-a-snake-game-from-scratch/learn/v4/overview)
