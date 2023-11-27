import numpy as np
from neo4j import GraphDatabase
from marcas import Marca

class Grafo:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("conectado")


    def crear_marca(self, tx , marca):
        tx.run("CREATE (:Nodo {nombre: $nombre , padre: $padre})" ,
                        nombre=(marca.nombre), padre=(marca.padre))

    def crear_marca_muerta(self, tx, marca):
        tx.run("CREATE (:Nodo {nombre: $nombre , padre: $padre})",
               nombre=(marca.nombre), padre=(marca.padre))



    def crear_relacion_hijo(self, tx, marca):
        tx.run("MATCH (a:Nodo {nombre: $nombre_nodo}) "
               "MATCH (b:Nodo {nombre: $nombre_padre}) "
               "MERGE (a)-[:HIJO]->(b)",
               nombre_nodo=(marca.nombre), nombre_padre=(marca.padre))



    def close(self):
        print("desconectado")
        self.driver.close()


global nodos
global transiciones
global matrizPrevia
global marcadores
global matrizIncidencia
global allMarcas
global nodosGrafo
#imprime en consola matriz nxm
def print_hi(matriz):
    print("matriz:  ")
    for filaIndice in range(transiciones):
        for columnaIndice in range(nodos):
                print(matriz[filaIndice][columnaIndice], end=" ")
        print()
    print("______")

#retorna la matriz de incidencia segun una matriz de entradas y salidas
def matriz_incidencia(matrizInput , matrizOutput ):
    matriz = []
    filaLista = []
    for filaIndice in range(transiciones):
        filaLista = []
        for columnas in range(nodos):
            filaLista.append(matrizInput[filaIndice][columnas] - matrizOutput[filaIndice][columnas])
            #print({filaLista[j]})
        matriz.append(filaLista)
    print_hi(matriz)
    return matriz

#verifica si la marca puede ssegun un vector de transiciones dispararse o no
def rama_habilitada( marca0, vector):
    d = np.dot(vector, matrizPrevia)
    r = (marca0 >= d)
    return r


def llenar_vector():
    vector = []
    #print(f"{vector} fuera")
    for i in range(transiciones):
        vector.append(0)
        #print(vector)
    #print(f"{vector} lleno")
    return vector


#Mo + e + MatrizIncidencia = MF
def marca_nueva(marca0, vector_e):
    marcaFinal = marca0 + np.dot(vector_e, matrizIncidencia)
    #print(f"{marcaFinal} marca final")
    #verificarMarca(marcaFinal)
    return marcaFinal


def verificarMarcaIgual(marcaNueva):

    marca = marcaNueva.flatten().tolist()
    bandera = False
    #print(f"{bandera} UN CICLO I ")
    for m in allMarcas:
        #print(f"{type(m)} tipo de m {type(marca)}  tipo de marcanueva" )
        igual = all(marcaNueva == m)
        if igual:
            #print(f" EXISTE RETORNO BANDERA {igual} {marcaNueva} {m}")
            bandera = igual

    #print(f"{bandera} UN CICLO F")
    return bandera




# Press the green button in the gutter to run the script.
def marcaInfinita(marcaNueva):
    bandera = []
    #print("------------")

    for listaMatrizMarcas in allMarcas:
        listaBandera = []

        if ((listaMatrizMarcas) != (marcaNueva.flatten().tolist())):
            for indice in range(len(listaMatrizMarcas)):
                if( (listaMatrizMarcas[indice]) <= (marcaNueva[indice]) ):
                    listaBandera.append(True)

                else:
                    listaBandera.append(False)



        else: print(f" no es igual {listaMatrizMarcas} {allMarcas} ")
        bandera.append(all(listaBandera))



    return any(bandera)


def crear_marcas(marca0, nodoViejo):
    print(f"{marca0} crear marcas Mo= {marca0}")
    hijos = []
    for i in range(transiciones):
        vector_e = llenar_vector()
        vector_e[i]=1

        #p cada vector veo rama habilitada

        # marcaNuevaes la marca a comprobar si esta en la matriz, si no esta => agregarla
        # si es mayor a una ya existente  => iNF
        if(all(rama_habilitada(marca0, vector_e))):

            marcaNueva = marca_nueva(marca0, vector_e)
            existe = verificarMarcaIgual(marcaNueva)
            #si existe es = a TRUE entonces la marca ya esta en la matriz

            if not existe:
                infinito = marcaInfinita(marcaNueva)

                if not infinito:
                    allMarcas.append(marcaNueva.flatten().tolist())
                    nueva = Marca(" ".join(str(x) for x in marcaNueva), nodoViejo.nombre)
                    print(f"MARCA NUEVA: {nueva.nombre} PADRE {nueva.padre} ")
                    hijos.append(crear_marcas(marcaNueva, nueva))
                    nueva.hijos = hijos
                    nodosGrafo.append(nueva)

                else:

                    muerta = Marca(" ".join(str(x) for x in marcaNueva), nodoViejo.nombre)
                    nodosGrafo.append(muerta)
                    print(f" MARCA INFINITA:  => tengo que matar la rama {marca0} marca nueva {marcaNueva}")


    print("______Termina Crear Marcas______")

    return hijos







if __name__ == '__main__':

    grafo = Grafo("bolt://localhost:7687", "neo4j", "arbolmurata")

    nodos = 2
    transiciones = 2
    allMarcas = []
    marcasInfinitas = []
    matrizPrevia = [[1, 0], [0, 1]]
    matrizPosterior = [[0, 2], [1, 0]]
    marca0 = [1, 1]
    allMarcas.append(marca0)
    nodosGrafo = []
    marcaCe = Marca(" ".join(str(x) for x in marca0), " ")
    nodosGrafo.append(marcaCe)

    matrizIncidencia = matriz_incidencia(matrizPosterior, matrizPrevia)
    crear_marcas(marca0, marcaCe)
    #print_hi(allMarcas)
    print(f"{allMarcas} all marcas")


    print(f"-------------------Grafo-----------------------------")



    with grafo.driver.session() as session:

        print("f ---------Creacion script----------")
        for marca in nodosGrafo:

            if len(marca.padre) == 0:
                print(f" RAIZ {marca.nombre} {len(marca.hijos)}")
                session.write_transaction(grafo.crear_marca, marca)

            else:
                #if (len(marca.hijos) == 0):
                session.write_transaction(grafo.crear_marca, marca)

                #print(f" MUERTA {marca.nombre} {len(marca.hijos)} ")

                #else:
                """    session.write_transaction(grafo.crear_marca, marca)
                    session.write_transaction(grafo.crear_relacion_hijo, marca)
                    print(f"RELACION {marca.nombre} {len(marca.hijos)}")"""

        for marca in nodosGrafo:
            session.write_transaction(grafo.crear_relacion_hijo, marca)


    grafo.close()


