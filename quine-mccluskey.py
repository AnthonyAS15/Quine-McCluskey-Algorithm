#Bibliotecas


########################################################

#Variables globales
Literales = { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F" } #Diccionario para la cantidad de casos expresiones de 4, 5 y 6 literales.

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

#Función que compara si dos minterminos solo difieren en un bit
def comparar(min1, min2):
    limite = 0 #Cantidad de bits en los que difiere.
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
    implicantes = [] #Almacena los implicantes que aún no se sabe si son primos.
    implicantes_primos = []
    posibles_implicantes_finales = [] #Almacena los implicantes del último que pueden ser implicantes primos.
    comprobacion_implicantes_primos = [] #Almacena una lista de booleanos que verifican si un mintermino no se pudo relacionar con ningún otro.
    cantidad_grupos = len(agrupacion_de_1s)-1 #Cuenta la cantidad de grupos por cantidad de 1s excepto el ultimo.

    if cantidad_grupos > 0: #Si la lista posee dos grupos o más.
        for contador1 in range(cantidad_grupos):
            for min1 in agrupacion_de_1s[contador1]: #Se inicia en 1 el contador para no tomar en cuenta el indicador de cada grupo.
                for contador2, min2 in enumerate(agrupacion_de_1s[contador1+1]):
                    difiere_1bit, nuevo_min = comparar(min1, min2) #Recibe True si los minterminos solo difieren en un 1 bit y el mintermino de la comparación.
                    if difiere_1bit == True:
                        implicantes.append(nuevo_min) #Añade el mintermino que difiere solo en 1 bit a la lista implicantes.
                        if contador1 == cantidad_grupos -1: #Si un mintermino del último grupo difiere en un solo bit
                            if min2 in posibles_implicantes_finales:#, se borra de la lista de posibles_implicantes_finales.
                                posibles_implicantes_finales.remove(min2)

                    else:
                        if contador1 == cantidad_grupos -1: #Si es del último grupo
                            if min2 not in posibles_implicantes_finales: #Si el mintermino no ha sido combinado y no está aún en la lista
                                posibles_implicantes_finales.append(min2) #Se va a insertar el mintermino del último grupo en posibles_implicantes_finales

                    comprobacion_implicantes_primos.append(difiere_1bit)
                for cant, comprobacion in enumerate(comprobacion_implicantes_primos): #Comprobar si el elemento es un implicante primo o no.
                     #Calcular la longitud del segundo grupo.
                    if isinstance(agrupacion_de_1s[contador1+1], str): #Si solo está un string en el segundo grupo
                        longitud_grupo2 = 0
                    else:
                        longitud_grupo2 = len(agrupacion_de_1s[contador1+1]) -1
                    if comprobacion == True:
                        break
                    elif comprobacion == False and cant == len(comprobacion_implicantes_primos) -1 and contador2 == longitud_grupo2 and not min_agrupado(min1):
                        implicantes_primos.append(min1) #Añadir el mintermino a los implicantes primos dado que no se pudo emparejar.
                    elif comprobacion == False and cant == len(comprobacion_implicantes_primos) -1 and min_agrupado(min1):
                        implicantes_primos.append(min1) #Añadir el mintermino a los implicantes primos dado que no se pudo emparejar.

                comprobacion_implicantes_primos = []
        
        grupos_implicantes = Agrupar_min_1s(implicantes)
        implicantes_primos += encontrar_implicantes_primos(grupos_implicantes)
        if posibles_implicantes_finales != []:
            for implicante in posibles_implicantes_finales:
                implicantes_primos.append(implicante)

        if implicantes_primos == [] and contador1 == cantidad_grupos -1: #Si no fue posible hacer alguna combinación de minterminos.
            for grupo in agrupacion_de_1s:
                for min in grupo:
                    implicantes_primos.append(min) #Almacenar todos los minterminos como implicantes primos.

    elif cantidad_grupos == 0: #Si la lista solo posee un grupo.
        for implicante in agrupacion_de_1s[0]:
            implicantes_primos.append(implicante)

    return implicantes_primos

#Función para eliminar los elementos repetidos de una lista.
def eliminar_repetidos(lista):
    for elemento in lista:
        cant = lista.count(elemento)
        while cant > 1:
            lista.remove(elemento)
            cant -= 1
    return lista

#Función para encontrar a los minterminos que conforman a los minterminos agrupados. Por ejemplo, 10X1 es obtenido al combinar 9(1001) y 11(1011)
def busca_minterminos(min): #Los minterminos se almacenan en su forma decimal.
    cant_xs = min.count('X')
    if cant_xs == 0:
        return [int(min, 2)]
    x = [bin(i)[2:].zfill(cant_xs) for i in range(pow(2, cant_xs))]
    minterminos = []

    for i in range(pow(2,cant_xs)):
        minterminos2,ind = min[:],-1
        for j in x[0]:
            if ind != -1:
                ind = ind+minterminos2[ind+1:].find('X')+1
            else:
                ind = minterminos2[ind+1:].find('X')
            minterminos2 = minterminos2[:ind]+j+minterminos2[ind+1:]
        minterminos.append(int(minterminos2, 2))
        x.pop(0)

    return minterminos

#Función para determinar los implicantes primos esenciales
def encontrar_implicantes_esenciales(implicantes_primos):
    implicantes_esenciales = []
    implicantes = [] #Almacena una lista de los minterminos relacionados con su respectivo implicante primo.
    comprobacion_implicantes_primos = [] #Almacena un valor booleano. True si el mintermino no se repite, False si se repite.
    restar_grupo = 0 #Compensa para evitar sobrepasar el límite de la lista. Resta 1 si se está iterando el segundo grupo, 2 si se está iterando el tercer grupo y así.

    for min in implicantes_primos:
        minterminos = busca_minterminos(min)
        implicantes.append(minterminos)

    cantidad_implicantes = len(implicantes)-1 #Cuenta los implicantes primos -1

    if cantidad_implicantes > 0: #Si la lista posee dos o más implicantes primos
        for contador1 in range(cantidad_implicantes+1):
            if contador1 != cantidad_implicantes: #Comprobar que los minterminos no sean del último grupo.
                for min1 in implicantes[contador1]:
                    for contador2 in range(1, len(implicantes) - restar_grupo):
                        for min2 in implicantes[contador1+contador2]:
                            if min1 == min2:
                                comprobacion_implicantes_primos.append(False)
                                break
                            else:
                                comprobacion_implicantes_primos.append(True)

                    for cant, comprobacion in enumerate(comprobacion_implicantes_primos): #Comprobar si el elemento es un implicante esencial o no.
                        if comprobacion == False:
                            break
                        elif comprobacion == True and cant == len(comprobacion_implicantes_primos) -1:
                            if implicantes_primos[contador1] not in implicantes_esenciales:
                                implicantes_esenciales.append(implicantes_primos[contador1]) #Añadir el mintermino a los implicantes esenciales dado que posee un mintermino que no se repite.

                    comprobacion_implicantes_primos = []

                restar_grupo += 1
                
            else: #Si solo queda por comparar el último grupo
                implicantes_invertidos = list(reversed(implicantes)) #Invertir la lista para poder comparar los últimos minterminos con los demás.
                implicantes_primos_invertidos = list(reversed(implicantes_primos)) #Invertir la lista de los implicantes primos.

                for min1 in implicantes_invertidos[0]:
                    if implicantes_primos_invertidos[0] not in implicantes_esenciales:
                        for contador2 in range(1, len(implicantes)):
                            for min2 in implicantes_invertidos[contador2]:
                                if min1 == min2:
                                    comprobacion_implicantes_primos.append(False)
                                    break
                                else:
                                    comprobacion_implicantes_primos.append(True)
                        
                        for cant, comprobacion in enumerate(comprobacion_implicantes_primos): #Comprobar si el elemento es un implicante esencial o no.
                            if comprobacion == False:
                                break
                            elif comprobacion == True and cant == len(comprobacion_implicantes_primos) -1:
                                implicantes_esenciales.append(implicantes_primos_invertidos[0]) #Añadir el mintermino a los implicantes esenciales dado que posee un mintermino que no se repite.

                        comprobacion_implicantes_primos = []                
        
    elif cantidad_implicantes == 0: #Si la lista solo tiene un implicante primo
        implicantes_esenciales.append(implicantes_primos[0])

    return implicantes_esenciales

#Función para convertir la ecuación Booleana
def Convertir_Booleana(expresiones):
    lista = []
    for termino in expresiones:
        a = " "
        for x in range(len(termino)): #Pasa por toda la lista para verificar si se encuentra una X la cual la quita y si hay un 0 niega la letra
            if termino[x] == "X":
                continue
            a += Literales[x]
            if termino[x] == "0":
                 a += "'"
        lista.append(a)
    return lista

#Función para convertir finalmente la ecuación booleana con forma de F= " " + " " + " " + ...
def Sumar_Booleana(lista):
    a = "F = " #pone el "F=" delante de la lista 
    for elemento in lista:
        a += elemento + " + " #pone los demás en la lista 
    print(a[:len(a)-3])

#Función que va a ejecutar el código principal del programa
def main():
    minterminos = [1, 4, 6, 15]
    minterminos.sort()

    num_binarios = min_binario(minterminos)
    print ("Minterminos:")
    print(num_binarios)
    num_binarios.sort()

    agrupacion_de_1s = Agrupar_min_1s(num_binarios)
    agrupacion_de_1s.sort(key=lambda x: x[0])
    print ("Minterminos agrupados:")
    print(agrupacion_de_1s)

    implicantes_primos = encontrar_implicantes_primos(agrupacion_de_1s)
    implicantes_primos = eliminar_repetidos(implicantes_primos)
    print("Implicantes primos:")
    print(implicantes_primos)

    implicantes_primos_esenciales = encontrar_implicantes_esenciales(implicantes_primos)
    print("Implicantes esenciales:")
    print(implicantes_primos_esenciales)

    terminos = Convertir_Booleana(implicantes_primos_esenciales)
    print("Solución:")
    Sumar_Booleana (terminos)

########################################################

#Main
main()