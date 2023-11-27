
# Coverability tree

El proyecto muestra la implementacion de las reglas para la obtencion de todas las marcas de una red de petri dada segun Tadao Murata:  paper: Petri nets: Propieties, Analysis and Applications (1989).



El codigo echo en python muestra todas las marcas alcanzables, de la red se tienen que entregar las matrices de entrada y salida . 

el codico en python se le agrego un adicional de [neo4j](https://neo4j.com/) (base de datos orientada a grafos) que crea un arbol de cobertura visual con todas las marcas encontradas generando una relacion (HIJO) que marca de quien es hijo el nodo dado (caso infinito marca todos los posibles padres).
La raiz es el unico nodo sin padre 

## Authors

- [@Nadia Nohely Gonzalez](https://github.com/NGN22/)


## Documentation

[Presentacion del proyecto](https://github.com/NGN22/coverabilitytree/blob/bd55910bd11594720c4a9d495df031f06ab21d2e/Presentaci%C3%B3n%20proyecto.pdf)

**en el archivo se muestran las explicaciones teoricas para la aplicacion asi como ejemplos (matriz de 2x2) del algoritmo dde estado final de una red de petri, con todas las caracteristicas de la herramienta para el analisis de la red usada y una breve descripcion del marco teorico del proyecto
