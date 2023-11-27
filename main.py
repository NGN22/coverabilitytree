import numpy as np



global nodos
global transiciones
global matrizPrevia
global marcadores
global matrizIncidencia
global allMarcas
#imprime en consola matriz nxm
def print_hi(matriz, nombre):
    print(f"matriz: {nombre} ")
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
    print_hi(matriz, "incidencia")
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
    #print(f"{bandera} UN CICLO I verificar marca igual {marcaNueva} ")
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



def crear_marcas(marca0):
    print(f"{marca0} crear marcas Mo= {marca0}")

    for i in range(transiciones):
        vector_e = llenar_vector()
        vector_e[i]=1
        #print(f"{vector_e} VECTOR E {i}")
        #p cada vector veo rama habilitada

        # marcaNuevaes la marca a comprobar si esta en la matriz, si no esta => agregarla
        # si es mayor a una ya existente  => iNF
        if(all(rama_habilitada(marca0, vector_e))):
            #print(f"RAMA HABILITADA UN CICLO {vector_e} VECTOR E {i}")

            marcaNueva = marca_nueva(marca0, vector_e)
            existe = verificarMarcaIgual(marcaNueva)
            #si existe es = a TRUE entonces la marca ya esta en la matriz

            if not existe:
                infinito = marcaInfinita(marcaNueva)

                if not infinito:
                    allMarcas.append(marcaNueva.flatten().tolist())
                    print(f"MARCA NUEVA NO EXISTE {existe} NO ES INFINITA {marcaNueva}")
                    crear_marcas(marcaNueva)
                else:
                    print(f"infinita => tengo que matar la rama {marcaNueva} {infinito} {existe}")
            #print(f"{marcaNueva} marca nueva - existe: {existe} ")

    print("______Termina Crear Marcas______")









if __name__ == '__main__':


    nodos = 4
    transiciones = 3
    allMarcas =[]
    matrizPrevia = [[1, 0,0,0], [0, 1,0,0],[0, 1,0,0]]
    matrizPosterior = [[0, 1,0,0], [0,0,0,1], [0,0,1,0]]
    marca0 = [5,0,0,0]
    allMarcas.append(marca0)


    print("matrices")
    print_hi(matrizPrevia, "Previa")

    print_hi(matrizPosterior, "Posterior")
    matrizIncidencia = matriz_incidencia(matrizPosterior, matrizPrevia)
    crear_marcas(marca0)

    print(f"{allMarcas} all marcas")


