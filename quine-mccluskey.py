#Bibliotecas



########################################################

#Funciones

#Función para transformar los minterminos a su forma binaria
def min_binario(minterminos):
    min_binarios = []
    cantidad_bits = len(format(minterminos[-1], "b")) #Mayor cantidad de bits de los minterminos disponibles.

    for min in minterminos:
        mintermino = format(min, "b") #Transforma un número entero a uno binario. int -> string.
        mintermino = mintermino.zfill(cantidad_bits)
        min_binarios.append(mintermino)
    
    return min_binarios #Retorna una lista con los minterminos en su forma binaria.

#Función para agrupar miniterminos 1s 
def Agrupar_min_1s (min_binario): #Recibe una lista implementada por min_binarios e itera por cada elemento de la lista 
    Lista_de_lista = []
    for num in min_binario:
        contador = 0 #Se asigna un contador en 0 
        for buscar_1_min in num:
            if buscar_1_min == "1": #Verifica si en la lista de los binarios se encuentran 1s 
                contador+=1
        
        if len(Lista_de_lista) == 0:
            Lista_de_lista.append([contador, num])

        else:
            numero = 0
            for lista in Lista_de_lista:
                if lista[0] == contador:
                    lista.append(num)
                    break
                numero += 1
                if len(Lista_de_lista) == numero:
                    Lista_de_lista.append([contador, num])
                    break
    return Lista_de_lista

#Función para eliminar el indicador al inicio de las agrupaciones de 1s
def eliminar_indicador(agrupacion_de_1s):
    cant_grupos = len(agrupacion_de_1s) #Cantidad de agrupaciones de 1s que tiene la lista de listas.

    for num in range(cant_grupos):
        agrupacion_de_1s[num].pop(0)

    return agrupacion_de_1s

#Función para elimintar listas vacías
def eliminar_vacias(lista_de_listas):
    lista_sin_vacias = []
    for lista in lista_de_listas:
        if lista != [""]:
            lista_sin_vacias.append(lista)
    
    return lista_sin_vacias

#Función que compara si dos minterminos solo difieren en un bit
def comparar(min1, min2):
    limite = 0
    cantidad_bits = len(min1)
    nuevo_min = ""

    for contador1 in range(cantidad_bits):
        bit1 = min1[contador1]
        bit2 = min2[contador1]
        if bit1 != bit2:
            limite +=1
            nuevo_min += "X" #Sustituye el bit que difiere por "-"
        else:
            nuevo_min += bit1 
    if limite < 2:
        return True, nuevo_min
    else:
        return False, nuevo_min

#Función para comprobar si el mintermino ya ha sido agrupado con anterioridad o no.
def min_agrupado(min):
    for bit in min:
        if bit == "X":
            return True
    return False

#Función para encontrar los implicantes primos
#Esta función va a hacer uso de la recursividad para cumplir con su propósito
def encontrar_implicantes_primos(agrupacion_de_1s):
    agrupacion_de_1s = eliminar_indicador(agrupacion_de_1s) #Eliminar el indicador de 1s al comienzo de la lista
    agrupacion_de_1s = eliminar_vacias(agrupacion_de_1s) #Elimina las listas vacías que existan dentro de la lista.
    implicantes = [] #Almacena los implicantes que aún no se sabe si son primos.
    implicantes_primos = [] 
    posibles_implicantes_primos = [] #Almacena los implicantes del último que pueden ser implicantes primos.
    comprobacion_implicantes_primos = [] #Almacena una lista de booleanos que verifican si un mintermino no se pudo relacionar con ningún otro.
    cantidad_grupos = len(agrupacion_de_1s)-1 #Cuenta la cantidad de grupos por cantidad de 1s excepto el ultimo.

    if cantidad_grupos > 0: #Si la lista posee dos grupos o más.
        for contador1 in range(cantidad_grupos):
            for contador2, min1 in enumerate(agrupacion_de_1s[contador1]): #Se inicia en 1 el contador para no tomar en cuenta el indicador de cada grupo.
                for contador3, min2 in enumerate(agrupacion_de_1s[contador1+1]):
                    difiere_1bit, nuevo_min = comparar(min1, min2) #Recibe True si los minterminos solo difieren en un 1 bit y el mintermino de la comparación.
                    if difiere_1bit == True:
                        implicantes.append(nuevo_min) #Añade el mintermino que difiere solo en 1 bit a la lista implicantes.
                        if contador1 == cantidad_grupos -1: #Si un mintermino del último grupo difiere en un solo bit
                            if min2 in posibles_implicantes_primos and min_agrupado(min2):#, se borra de la lista de posibles_implicantes_primos.
                                posibles_implicantes_primos.remove(min2)
                    else:
                        if contador1 == cantidad_grupos -1: #Si es del último grupo
                            if min2 not in posibles_implicantes_primos and min_agrupado(min2): #Si el mintermino no ha sido combinado y no está aún en la lista
                                posibles_implicantes_primos.append(min2) #Se va a insertar el mintermino del último grupo en posibles_implicantes_primos
                    comprobacion_implicantes_primos.append(difiere_1bit)
                for cant, comprobacion in enumerate(comprobacion_implicantes_primos): #Comprobar si el elemento es un implicante primo o no.
                    if comprobacion == True:
                        break
                    elif comprobacion == False and cant == len(comprobacion_implicantes_primos) -1 and min_agrupado(min1):
                        implicantes_primos.append(min1) #Añadir el mintermino a los implicantes primos dado que no se pudo emparejar.

                comprobacion_implicantes_primos = []
        
        grupos_implicantes = Agrupar_min_1s(implicantes)
        implicantes_primos += encontrar_implicantes_primos(grupos_implicantes)
        if posibles_implicantes_primos != []:
            for implicante in posibles_implicantes_primos:
                implicantes_primos.append(implicante)
    elif cantidad_grupos == 0: #Si la lista solo posee un grupo.
        for implicante in agrupacion_de_1s:
            implicantes_primos.append(implicante)

    return implicantes_primos

#Función para determinar los implicantes primos esenciales
def encontrar_implicantes_esenciales ():
    pass


#Función que va a ejecutar el código principal del programa
def main():
    minterminos = [4, 8, 11, 12, 15]
    minterminos.sort()

    num_binarios = min_binario(minterminos)
    print ("Función def min_binario(minterminos): =")
    print(num_binarios)
    num_binarios.sort()

    agrupacion_de_1s = Agrupar_min_1s(num_binarios)
    agrupacion_de_1s.sort(key=lambda x: x[0])
    print ("Función def agrupar_min_1s (min_binario): ")
    print(agrupacion_de_1s)

    comparacion, nuevo_min = comparar("1101","1111")
    print ("Función comparar(min1, min2): ")
    print(comparacion, nuevo_min)

    implicantes_primos = encontrar_implicantes_primos(agrupacion_de_1s)
    print("Función encontrar_implicantes_primos(agrupacion_de_1s): ")
    print(implicantes_primos)

########################################################

#Main
main()
