# Importamos los datos necesarios del archivo lifestore_file
from lifestore_file import (
    lifestore_products,
    lifestore_sales,
    lifestore_searches
)

#################
# Login #########
#################
# Credenciales correctas
usuarios = {"jimmy": "python"}
max_intentos = 3

# Mensaje de bienvenida y primera petición de las credenciales
mensaje_bienvenida = 'Bienvenide al sistema!\nAccede con tus credenciales'
print(mensaje_bienvenida)

# Variables de control
# TODO: recordar cambiar esta madre
usuario_autenticado = True  # El usuario está autenticado
intentos = 0  # Contador de los intentos

# Ciclo para controlar el acceso hasta que el usuario instroduzca las
# credenciales correctas
while not usuario_autenticado:
    # Pedir al usuario que ingrese sus credenciales
    input_usuario = input('Usuario: ')
    input_pass = input('Contraseña: ')

    # Aumentamos el contador
    intentos += 1

    # Comprobamos las credenciales
    if input_usuario in usuarios and input_pass == usuarios[input_usuario]:
        # Si las credenciales son correcta cambiamos la variable de
        # control para salir del ciclo while
        usuario_autenticado = True
        # También damos un saludo de entrada al programa
        print(f'Hola de nuevo {input_usuario}!')
    else:
        # Si alguna de las dos credenciales es erronea le avisamos al
        # usuario cual ha sido su error
        print("Error: ", end="")
        if input_usuario in usuarios:
            print('Te equivocaste en la contraseña')
        else:
            print(f'Usuario "{input_usuario}" no esta registrado')
        # Avisamos los intentos disponibles
        print(f'Tienes {3 - intentos} intentos restantes')

    # Si supera el número de intentos permitidos, terminamos el programa
    if intentos == max_intentos:
        print("Demasiados intentos fallidos, terminando programa")
        exit()


# TODO: Empezar a comentar desde aquí
# TODO: separar las ventas por fechas y luego correr todo esto que está abajo por cada mes
for venta in lifestore_sales:
    fecha = venta[3]

    _, mes, year = fecha.split("/")

####################################
# Productos con más ventas #########
####################################
# Diccionario que lleva la cuenta de las ventas por cada producto
contadores_ventas = {}
# Lista con los productos más vendidos
prod_mas_vendidos = []
# Reseñas por productos
prod_con_reviews = {}

# Recorremos toda la lista de ventas
for venta in lifestore_sales:
    id_prod = venta[1]
    reembolso = venta[4]
    review = venta[2]

    if id_prod in contadores_ventas:
        contadores_ventas[id_prod] += 1
    else:
        contadores_ventas[id_prod] = 1

    # Consideramos los reembolsos
    if reembolso == 1:  # Debería ser necesario con solo (if reembolso), pero lo pongo completo
        contadores_ventas[id_prod] -= 1

    # Sacamos las reviews
    if id_prod in prod_con_reviews:
        prod_con_reviews[id_prod] = [(prod_con_reviews[id_prod][0] + review) / 2,
                                     prod_con_reviews[id_prod][1] + 1]
    else:
        prod_con_reviews[id_prod] = [review, 1]


# Ordenamos los elementos de mayor a menor
ventas_ordenadas = dict(sorted(contadores_ventas.items(),
                               key=lambda item: item[1],
                               reverse=True))

# Agregamos a cada venta el nombre del producto y mostramos los productos
contador = 0

# print("Mostrando productos más vendidos")
# Recorremos toda la lista de ventas
for contador_ventas in ventas_ordenadas.items():
    # Buscamos el nombre del producto
    for producto in lifestore_products:
        if producto[0] == contador_ventas[0]:
            # [id, la cantidad de ventas, el nombre del producto]
            prod_mas_vendidos.append([*contador_ventas, producto[1]])
            break

    if contador == 5:
        break

    contador += 1


# TODO: mostrar los productos de mejor manera
# print(prod_mas_vendidos, "\n\n")


##################################
# Productos más buscados #########
##################################
# Diccionario que lleva la cuenta de las busquedas por cada producto
contadores_busquedas = {}
# Lista con los productos más buscados
prod_mas_buscados = []

# Recorremos toda la lista de busquedas
for busqueda in lifestore_searches:
    if busqueda[1] in contadores_busquedas:
        contadores_busquedas[busqueda[1]] += 1
    else:
        contadores_busquedas[busqueda[1]] = 1

# Ordenamos los elementos de mayor a menor
busquedas_ordenadas = dict(sorted(contadores_busquedas.items(),
                                  key=lambda item: item[1],
                                  reverse=True))

# Agregamos a cada busqueda el nombre del producto y mostramos los productos
contador = 0
# print("Mostrando productos más buscados")
# Recorremos toda la lista
for contador_busquedas in busquedas_ordenadas.items():
    for producto in lifestore_products:
        if producto[0] == contador_busquedas[0]:
            prod_mas_buscados.append([*contador_busquedas, producto[1]])
            break

    if contador == 10:
        break

    contador += 1

# TODO: mostrar los productos de mejor manera
# print(prod_mas_buscados)


####################################
# Productos por categorías #########
####################################
# Diccionario que guarda las diferentes categorias y también los productos que
# pertenecen a cada una
ventas_prod_por_categorias = {}

# Agregamos los productos a un diccionario donde la key es la categoría
for producto in lifestore_products:
    prod_categoria = producto[3]

    id_product = producto[0]

    if id_product in contadores_ventas:
        prod_con_ventas = producto + [contadores_ventas[id_product]]
    else:
        prod_con_ventas = producto + [0]

    # prod_por_categorias =
    # {cateforia: [[id_product, name, price, category, stock, total_sales], [...]]}
    if prod_categoria in ventas_prod_por_categorias:
        ventas_prod_por_categorias[prod_categoria].append(prod_con_ventas)
    else:
        ventas_prod_por_categorias[prod_categoria] = [prod_con_ventas]

for categoria in ventas_prod_por_categorias.keys():
    ventas_prod_por_categorias[categoria] = sorted(ventas_prod_por_categorias[categoria],
                                                   key=lambda item: item[5],
                                                   reverse=True)


# print("\n\nMostrando los 5 productos menos vendidos por categorías")
# for categoria in ventas_prod_por_categorias.keys():
#     print(f"\nCategoría: {categoria}")
#     for producto in ventas_prod_por_categorias[categoria][-5:]:
#         print(" ", producto)


# Diccionario que guarda las diferentes categorias y también los productos que
# pertenecen a cada una, con sus búsquedas
busq_prod_por_categorias = {}

# Agregamos los productos a un diccionario donde la key es la categoría
for producto in lifestore_products:
    prod_categoria = producto[3]

    id_product = producto[0]

    if id_product in contadores_busquedas:
        prod_con_busquedas = producto + [contadores_busquedas[id_product]]
    else:
        prod_con_busquedas = producto + [0]

    # prod_por_categorias =
    # {cateforia: [[id_product, name, price, category, stock, total_sales], [...]]}
    if prod_categoria in busq_prod_por_categorias:
        busq_prod_por_categorias[prod_categoria].append(prod_con_busquedas)
    else:
        busq_prod_por_categorias[prod_categoria] = [prod_con_busquedas]

for categoria in busq_prod_por_categorias.keys():
    busq_prod_por_categorias[categoria] = sorted(busq_prod_por_categorias[categoria],
                                                 key=lambda item: item[5],
                                                 reverse=True)


# print("\n\nMostrando los 10 productos menos buscados por categoría")
# for categoria in busq_prod_por_categorias.keys():
#     print(f"\nCategoría: {categoria}")
#     for producto in busq_prod_por_categorias[categoria][-10:]:
#         print(" ", producto)


#################################
# Reseñas por productos #########
#################################
prod_con_reviews_ord = sorted(prod_con_reviews.items(),
                              # Ordena el diccionario, basándose primero en el promedio
                              # de reviews, luego en la canidad de reviews y después por id del producto.
                              key=lambda item: (item[1], item[0]),
                              reverse=True)

for prod in prod_con_reviews_ord[:5]:
    print(prod)

for prod in prod_con_reviews_ord[-5:]:
    print(prod)

# print(prod_por_categorias)
# print(ventas_ordenadas.items())
# lifestore_searches = [id_search, id product]
# print(lifestore_searches[0])

# lifestore_products = [id_product, name, price, category, stock]
# print(lifestore_products[0])

# lifestore_sales = [
#     id_sale,
#     id_product,
#     score (from 1 to 5),
#     date,
#     refund (1 for true or 0 to false)
# ]
# print(lifestore_sales[0])

# DONE: TODO: Aquí mismo hacer un ordenamiento de las más vendidos
