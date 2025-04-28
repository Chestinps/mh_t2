**José Agustín Pérez**
**Cristóbal Martínez**

Los aeropuertos exigen una coordinación precisa para garantizar la seguridad y7 eficiencia en los aterrizajes. 

Asegurar una secuencia eficiente que minimice costos.

Se debe coordinar la aproximación de aviones de distintas aerolíneas considerando los siguientes factores:
- Capacidad de pistas
- Separación entre vuelos
- Otros elementos.

Se cuenta con un **conjunto de D aviones**. Cada avión tendrá un:
- Tiempo más temprano de aterrizaje $E_k$,  
- Tiempo más tarde de aterrizaje $L_k$
- Tiempo preferente $P_k$
- Se respeta que $E_k < P_k < L_k$
- Se respeta un tiempo de separación mínimo $\tau_{ij}$ entre el aterrizaje del avión $i$ y el avión $j$ con $i \neq j$
- Si el avión $i$ aterriza en el tiempo $T_i$ y el avión $j$ aterriza en $T_j$ con $T_i < T_j$, entonces se debe cumplir que $T_j \geq T_i + \tau_{ij}$
- Por cada unidad **bajo el tiempo preferente** $P_k$, se penalizará con un costo lineal $C_i$.
- Por cada unidad **sobre el tiempo preferente** $P_k$, se penalizará con un costo lineal $C'_k$.
- Por cada archivo se tiene un caso de prueba distinto
- Se tienen 1 o 2 pistas de aterrizaje.

![[Pasted image 20250421052446.png]]

### Archivos TXT
Se adjuntan 4 archivos txt (representando cada caso) los cuales siguen el siguiente formato:
- Número de Aviones
- Por cada avión $k$
	- $E_k :$ No puede aterrizar antes de este tiempo
	- $P_k :$ Tiempo ideal
	- $L_k :$ No puede aterrizar después de este tiempo
	- $C_k :$ Costo por aterrizar antes del tiempo ideal
	- $C'_k :$ Costo por aterrizar después del tiempo ideal
	- Por cada avión $j$
		- $\tau_{kj}$


## Diseño de Greedy's

##### Greedy Determinista

| Ejecución | Lista |
|-----------|------|
| 1 | 2, 3, 4, 5, 7, 6, 8, 9, 0, 13, 12, 1, 11, 10, 14 |

##### Greedy Estocástico

| Ejecución | Lista |
|-----------|------|
|1 | 0, 8, 4, 5, 1, 3, 2, 7, 6, 9, 11, 14, 13, 12, 10 |
|2 | 8, 3, 6, 9, 2, 5, 4, 0, 12, 7, 14, 13, 10, 1, 11 |
|3 | 11, 0, 3, 4, 6, 2, 8, 5, 9, 7, 13, 14, 12, 1, 10 |
|4 | 3, 2, 11, 7, 4, 6, 5, 14, 13, 9, 8, 0, 12, 1, 10 |
|5 | 2, 3, 6, 4, 5, 8, 12, 9, 7, 0, 13, 1, 11, 14, 10 |
|6 | 4, 0, 3, 5, 1, 2, 7, 8, 6, 13, 9, 12, 10, 11, 14 |
|7 | 0, 8, 4, 10, 7, 11, 2, 12, 6, 1, 3, 9, 13, 5, 14 |
|8 | 4, 10, 2, 5, 13, 7, 6, 3, 12, 8, 0, 1, 9, 14, 11 |
|9 | 9, 14, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 0, 13, 1 |
|10 | 2, 7, 12, 5, 14, 3, 0, 4, 8, 9, 13, 6, 11, 10, 1|



## GRASP

### Hill Climbing

#### Mejora-Mejora

##### Greedy Determinista

##### Greedy Estocástico con Restart

#### Alguna-Mejora

##### Greedy Determinista

##### Greedy Estocástico con Restart


### 


## Tabu Search

### Greedy Determinista

### Greedy Estocástico

### Configuraciones: Tamaño Lista Tabu

##### Configuración 1

##### Configuración 2

##### Configuración 3

##### Configuración 4

##### Configuración 5


## Simulated Annealing

### Greedy Determinista

### Greedy Estocástico

### Configuraciones: Variaciones de Temperatura

##### Configuración 1

##### Configuración 2

##### Configuración 3

##### Configuración 4

##### Configuración 5