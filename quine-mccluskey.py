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
num_binarios = min_binario([1,3,5,8])

for num in num_binarios:
    print(num)

