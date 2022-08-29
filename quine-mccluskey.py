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
            nuevo_min += "-" #Sustituye el bit que difiere por "-"
        else:
            nuevo_min += bit1 
    if limite < 2:
        return True, nuevo_min
    else:
        return False, nuevo_min


#Función para encontrar los implicantes primos
def encontrar_implicantes_primos(agrupacion_de_1s):
    implicantes_primos = []
    cantidad_grupos = len(agrupacion_de_1s) -1 #Cuenta la cantidad de grupos formados -1 a partir de la cantidad de unos de cada uno.

    for contador1 in range(cantidad_grupos):
        longitud_grupo = len(agrupacion_de_1s[contador1])

        for contador2 in range (1, longitud_grupo): #Se inicia en 1 el contador para no tomar en cuenta el indicador de cada grupo.
            for min1 in agrupacion_de_1s[contador1][contador2]:
                for min2 in agrupacion_de_1s[contador1+1][contador2]: #Se suma uno para poder tomar al grupo siguiente del actual.
                    difiere_1bit, nuevo_min = comparar(min1, min2) #Recibe True si los minterminos solo difieren en un 1 bit.
                    if difiere_1bit == True:
                        implicantes_primos.append(nuevo_min)
    
    return implicantes_primos

#Función para determinar los implicantes primos esenciales
#def encontrar_implicantes_esenciales ():


#Función que va a ejecutar el código principal del programa
def main():
    minterminos = [1, 2, 3, 4, 11, 12, 13, 14]
    minterminos.sort()
    num_binarios = min_binario(minterminos)
    print ("Función def min_binario(minterminos): =")
    print(num_binarios)
    num_binarios.sort()
    agrupacion_de_1s = Agrupar_min_1s(num_binarios)
    agrupacion_de_1s.sort(key=lambda x: x[0])
    print ("Función def Agrupar_min_1s (min_binario): ")
    print(agrupacion_de_1s)
    comparacion, nuevo_min = comparar("1101","1111")
    print(comparacion)
    print(nuevo_min)

########################################################

#Main
main()
