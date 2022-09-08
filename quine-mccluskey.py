#Bibliotecas
import copy
from pylatex import Document, LongTable, Section, Command, NewPage
from pylatex.utils import bold, NoEscape

########################################################

#Variables globales

Literales = { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F" } #Diccionario para la cantidad de casos expresiones de 4, 5 y 6 literales.

archivo = open("problema.txt", "r") #Abre el archivo txt a utilizar
literalentrada= archivo.readlines(1)
NumLiterales=int(literalentrada[0]) #Se crea la cantidad de Literales a utilizar

########################################################

#Funciones

#Funciones del algoritmo:

#Función para transformar los minterminos a su forma binaria
def min_binario(minterminos):
    min_binarios = []
    cantidad_bits = NumLiterales #Mayor cantidad de bits de los minterminos disponibles.

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
    return a

########################################################

#Funciones para la creación del documento:

#Crea la portada del documento.
def portada(doc):
    with doc.create(Section('Portada')):
        doc.preamble.append(Command('title', 'Algoritmo de Quine-McCluskey'))
        doc.preamble.append(Command('author', 'Anthony Artavia Salazar \n Diego Huertas Solorzano \n Justin Segura Rodríguez'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

#Crea una diapositiva con los datos del archivo de texto.
def archivo_texto(literal, minterminos,doc):
    with doc.create(Section('Entrada: Archivo de Texto')):
        doc.append(bold('Entrada: Archivo de Texto\n'))
        doc.append('\nCantidad de literales: ')
        doc.append(literal)
        doc.append('\n')
        doc.append('\nMinterminos: ')
        for indice, min in enumerate(minterminos):
            doc.append(min)
            if indice != len(minterminos)-1:
                doc.append(', ')
        doc.append('\n')
    doc.append(NewPage())

#Crea una diapositiva con una tabla con los minterminos con su respectiva representación en binario.
def minterminos_inicio(minterminos, num_binarios, doc):
    with doc.create(Section('Minterminos')):
        doc.append(bold('Minterminos'))
        with doc.create(LongTable("c c")) as data_table:
            encabezado = ["Mintermino en Decimal", "Mintermino en Binario"]
            data_table.add_row(encabezado, mapper=[bold])
            data_table.add_hline()
            data_table.end_table_header()

            for indice in range(len(minterminos)):
                fila = [minterminos[indice], num_binarios[indice]]
                data_table.add_row(fila)
            data_table.add_hline()

    doc.append(NewPage())

#Crea una tabla con los minterminos agrupados según la cantidad de unos que poseen.
def minterminos_agrupados(agrupacion_de_1s, doc):
    with doc.create(Section('Minterminos Agrupados')):
        doc.append(bold('Minterminos Agrupados'))
        with doc.create(LongTable("c c c")) as data_table:
            encabezado = ["Cantidad de Unos", "Minterminos en Decimal","Minterminos en Binario"]
            data_table.add_row(encabezado)
            data_table.add_hline()
            data_table.end_table_header()

            cant_unos = []
            for lista in agrupacion_de_1s:
                cant_unos.append(lista[0])
            
            grupos_minterminos = eliminar_indicador(agrupacion_de_1s)
            minterminos = []

            for grupo in grupos_minterminos:
                for min in grupo:
                    minterminos.append(busca_minterminos(min)[0])
            
            num_mintermino = 0
            for num_grupo, grupo in enumerate(grupos_minterminos):
                for indice in range(len(grupo)):
                    fila = [cant_unos[num_grupo], minterminos[num_mintermino], grupo[indice]]
                    data_table.add_row(fila)
                    num_mintermino += 1
            data_table.add_hline()

    doc.append(NewPage())

#Crea una tabla con los implicantes primos.
def implicantes_primos_documento(implicantes, doc):
    with doc.create(Section('Implicantes Primos')):
        doc.append(bold('Implicantes Primos'))
        with doc.create(LongTable("c c")) as data_table:
            encabezado = ["Minterminos en Decimal", "Minterminos en Binario"]
            data_table.add_row(encabezado)
            data_table.add_hline()
            data_table.end_table_header()

            minterminos = []
            for implicante in implicantes:
                minterminos.append(busca_minterminos(implicante))
            
            minterminos_agrupados = []
            mintermino_agrupado = ""
            for min in minterminos:
                for m in min:
                    mintermino_agrupado += str(m)
                    if m == min[-1]:
                        break
                    else:
                        mintermino_agrupado += ", "
                minterminos_agrupados.append(mintermino_agrupado)
                mintermino_agrupado = ""
            
            for indice, implicante in enumerate(implicantes):
                    fila = [minterminos_agrupados[indice], implicante]
                    data_table.add_row(fila)
            data_table.add_hline()

    doc.append(NewPage())

#Crea una tabla con los implicantes primos esenciales.
def implicantes_esenciales(implicantes_primos_esenciales,doc):
    with doc.create(Section('Implicantes Primos Esenciales')):
        doc.append(bold('Implicantes Primos Esenciales'))
        with doc.create(LongTable("c c")) as data_table:
            encabezado = ["Minterminos en Decimal", "Minterminos en Binario"]
            data_table.add_row(encabezado)
            data_table.add_hline()
            data_table.end_table_header()

            minterminos = []
            for implicante in implicantes_primos_esenciales:
                minterminos.append(busca_minterminos(implicante))
            
            minterminos_agrupados = []
            mintermino_agrupado = ""
            for min in minterminos:
                for m in min:
                    mintermino_agrupado += str(m)
                    if m == min[-1]:
                        break
                    else:
                        mintermino_agrupado += ", "
                minterminos_agrupados.append(mintermino_agrupado)
                mintermino_agrupado = ""
            
            for indice, implicante in enumerate(implicantes_primos_esenciales):
                    fila = [minterminos_agrupados[indice], implicante]
                    data_table.add_row(fila)
            data_table.add_hline()

    doc.append(NewPage())

#Crea una diapositiva con la solucion del algoritmo.
def solucion(terminos, doc):
    with doc.create(Section("Solución")):
         doc.append(bold("Solución\n"))
         doc.append('\nSimplificacion obtenida: ')
         doc.append('\n')
         a = Sumar_Booleana(terminos)
         doc.append(a[:len(a)-3])

    doc.append(NewPage())

#Crea el documento pdf resultante.
def creacion_documento(doc):
    doc.generate_pdf('Solución del problema', clean_tex=False, clean=True)

#####################################

#Función que va a ejecutar el código principal del programa
def main():
    
    #Toma de los datos del documento txt.
    archivo = open("problema.txt", "r") #Utiliza el archivo txt a utilizar

    littexto= archivo.readlines(1) #Lo volvemos a tomar, para poner tomar la lista completa
    literal=int(littexto[0])

    mintexto = archivo.readlines(2)
    lista1=[]

    for line in mintexto:
        line_strip= line.strip()
        line_split= line_strip.split(',') #divide cada elemento de la lista por un ','
        lista1.append(line_split)
    archivo.close()

    lista2=[]

    for i in lista1:
        for j in i:
            lista2.append(j)
    lista2 = [c.replace(',', '') for c in lista2]

    for i in range(len(lista2)): #crea la funcion que convierte la funcion en un int
        lista2[i] = int(lista2[i])

   #/////////////////////////////////////////////////////////////////////////////

    print("El número de literales a utilizar, es:",literal)

    print("La lista que ahora se va a utilizar es:",lista2, "\n")

    #Creación del documento
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm", "margin": "1cm"}
    doc = Document(page_numbers=True, geometry_options=geometry_options, documentclass="beamer",)
    
    #Creación de la portada
    portada(doc)
    
    #Ejecución del algoritmo y añadido al documento a retornar.
    minterminos = lista2
    minterminos.sort()

    num_binarios = min_binario(minterminos)
    print ("Minterminos:")
    print(num_binarios)
    num_binarios.sort()

    #Añadir al documento lo recibido del archivo de texto y los minterminos.
    archivo_texto(literal, minterminos, doc)
    minterminos_inicio(minterminos, num_binarios, doc)

    agrupacion_de_1s = Agrupar_min_1s(num_binarios)
    agrupacion_de_1s.sort(key=lambda x: x[0])
    print ("Minterminos agrupados:")
    print(agrupacion_de_1s)

    grupos_unos = copy.deepcopy(agrupacion_de_1s) #Crear una copia de lista antes de que sea modificada por la siguiente función
    #Añadir a la presentación una tabla con los minterminos agrupados.
    minterminos_agrupados(agrupacion_de_1s, doc)

    implicantes_primos = encontrar_implicantes_primos(grupos_unos)
    implicantes_primos = eliminar_repetidos(implicantes_primos)
    print("Implicantes primos:")
    print(implicantes_primos)

    #Añadir una tabla con los implicantes primos al documento.
    implicantes_primos_documento(implicantes_primos, doc)

    implicantes_primos_esenciales = encontrar_implicantes_esenciales(implicantes_primos)
    print("Implicantes esenciales:")
    print(implicantes_primos_esenciales)

    #Añadir una tabla con los implicantes primos esenciales al documento.
    implicantes_esenciales(implicantes_primos_esenciales, doc)

    terminos = Convertir_Booleana(implicantes_primos_esenciales)
    print("Solución:")

    #Añadir la solución al documento.
    solucion(terminos, doc)
    
	#Crear el pdf
    creacion_documento(doc)

########################################################

#Main
if __name__ == '__main__':
    main()