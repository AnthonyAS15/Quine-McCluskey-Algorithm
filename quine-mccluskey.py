#Bibliotecas



########################################################

#Funciones

def min_binario(minterminos):
    min_binarios = []
    for min in minterminos:
        mintermino = format(min, "b")
        min_binarios.append(mintermino)
    return min_binarios

########################################################

#Main
print("help")