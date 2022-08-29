#Bibliotecas



########################################################

#Funciones

#Función para transformar los minterminos a su forma binaria
def min_binario(minterminos):
    min_binarios = []
    for min in minterminos:
        mintermino = format(min, "b") #Transforma un número entero a uno binario. int -> string
        min_binarios.append(mintermino)
    return min_binarios #Retorna una lista con los minterminos en su forma binaria.

#Función para agrupar miniterminos 1s 
def Agrupar_min_1s (min_binario): #Recibe una lista implementada por min_binarios e itera por cada elemento de la lista 
    Lista_de_lista = []
    for num in min_binario:
        contador = 0 #Se asigna un contador en 0 
        for buscar_1_min in num:
            if buscar_1_min == "1": #Verifica si en el la lista de los binarios se encuentran 1s 
                contador+=1
        Lista_de_lista.append(contador)
    return Lista_de_lista

def main():
    num_binarios = min_binario([1, 2, 3, 4, 11, 12, 13, 14])
    print ("Función def min_binario(minterminos): =")
    for num in num_binarios:
        print(num)
    num_binarios.sort()
    Agrupacion_de_1s = Agrupar_min_1s(num_binarios)
    print ("Función def Agrupar_min_1s (min_binario): ")
    for i in range(len(num_binarios)):
        print(num_binarios[i],"|", Agrupacion_de_1s[i])

########################################################

#Main
main()
    
