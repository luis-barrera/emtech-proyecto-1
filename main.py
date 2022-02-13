# Importamos los datos necesarios del archivo lifestore_file
from lifestore_file import (
    lifestore_products,
    lifestore_sales,
    lifestore_searches
)

# TODO: solo para cuestiones de desarrollo
import pprint

# Login
#######

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
        # usuario cuál ha sido su error
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

# 1: Productos vendidos y buscados por categorías
#############################
# Diccionario que lleva la cuenta de las ventas por cada producto
contadores_ventas = {}
# Lista con los productos más vendidos
prod_mas_vendidos = []

# Diccionario que lleva la cuenta de las busquedas por cada producto
contadores_busquedas = {}
# Lista con los productos más buscados
prod_mas_buscados = []

# Recorremos toda la lista de ventas
for venta in lifestore_sales:
    id_prod = venta[1]
    reembolso = venta[3]

    # Agregamos al dict el contador para el producto o lo incrementamos
    # en caso de que ya esté agregado
    if id_prod in contadores_ventas:
        contadores_ventas[id_prod] += 1
    else:
        contadores_ventas[id_prod] = 1

    # Consideramos los reembolsos
    if reembolso == 1:  # Debería ser necesario con solo (if reembolso), pero lo pongo completo
        contadores_ventas[id_prod] -= 1

# Recorremos toda la lista de busquedas
for busqueda in lifestore_searches:
    id_prod = busqueda[1]
    # El producto ya está en el dict
    if id_prod in contadores_busquedas:
        contadores_busquedas[id_prod] += 1
    # El producto no está en el dict
    else:
        contadores_busquedas[id_prod] = 1

# Diccionario que guarda las diferentes categorias y también los
# productos que pertenecen a cada una
prod_por_categorias = {}

# Agregamos los productos a un diccionario donde la key es la categoría
for producto in lifestore_products:
    id_prod = producto[0]
    prod_categoria = producto[3]

    # prod_por_categorias =
    # {categoría: [[id_product, name, price, category, stock, total_sales, total_searches], [...]]}
    producto = producto + [0, 0]

    # Agregamos el número de ventas en caso de que tenga
    if id_prod in contadores_ventas:
        producto[5] = contadores_ventas[id_prod]

    # Agregamos el contador de busquedas
    if id_prod in contadores_busquedas:
        producto[6] = contadores_busquedas[id_prod]

    # Guardamos los productos en una lista fuera del dict
    prod_mas_vendidos.append(producto)
    prod_mas_buscados.append(producto)

    # Agregamos el producto a su categoría
    if prod_categoria in prod_por_categorias:
        prod_por_categorias[prod_categoria].append(producto)
    else:
        # Si no existe la categoría, se crea una
        prod_por_categorias[prod_categoria] = [producto]


# Productos ordenados por total de ventas
categorias_por_ventas = {}
# Productos ordenados por total de busquedas
categorias_por_busquedas = {}

# Por cada categoría ordenamos los productos
for categoria in prod_por_categorias.keys():
    # Ordenamos a partir de la cantidad de ventas
    categorias_por_ventas[categoria] = sorted(prod_por_categorias[categoria],
                                              key=lambda item: item[5],
                                              reverse=True)

for categoria in prod_por_categorias.keys():
    # Ordenamos a partir de la cantidad de busquedas
    categorias_por_busquedas[categoria] = sorted(prod_por_categorias[categoria],
                                                 key=lambda item: item[6],
                                                 reverse=True)

# Ordenamos los productos por su total de ventas
prod_mas_vendidos = sorted(prod_mas_vendidos,
                           # Si hay dos con el mismo número de ventas, se usa su total de búsquedas
                           key=lambda item: (item[5], item[6]),
                           reverse=True)

# Ordenamos los productos por su total de busquedas
prod_mas_buscados = sorted(prod_mas_buscados,
                           # Si hay dos con el mismo número de busquedas, se usa su total de ventas
                           key=lambda item: (item[6], item[5]),
                           reverse=True)

# Imprimimos los resultados dando un poco de formato
print("\nProductos más vendidos")
for prod in prod_mas_vendidos[:5]:
    print(" ", prod)

print("\nProductos más buscados")
for prod in prod_mas_buscados[:10]:
    print(" ", prod)

print("\nProductos por categorias")
# {categoría: [[id_product, name, price, category, stock, total_sales, total_searches], [...]]}
print("Productos por categorias con menos ventas")
for categoria in categorias_por_ventas:
    print(" ", categoria)
    for prod in categorias_por_ventas[categoria][-5:]:
        print("   ", prod)
print("\nProductos por categorias con menos búsquedas busquedas")
for categoria in categorias_por_busquedas:
    print(" ", categoria)
    for prod in categorias_por_busquedas[categoria][-10:]:
        print("   ", prod)

# # Separación de la ventas por fecha
# ###################################
#
# # Diccionario que almacena las ventas de acuerdo al año y el mes
# # Cada año es una entrada del dict
# # Cada año es un dict, las entradas de este son los meses
# ventas_por_fecha = {}
#
# # Separamos las fechas de cada venta en el mes y el año
# for venta in lifestore_sales:
#     # Obtenemos la fecha de la venta
#     fecha = venta[3]
#
#     # Obtenemos el mes y el año del string de la fecha, el día no interesa
#     # Dividiendo el string por el símbolo "/"
#     _, mes, year = fecha.split("/")
#
#     # Transformamos los strings a int
#     year = int(year)
#     mes = int(mes)
#
#     # Ahora la fecha de las compras es una lista con el año y el mes
#     venta[3] = [year, mes]
#
#     # Checamos el año esté en el dict
#     if year in ventas_por_fecha:
#         # Vemos si el mes está en el dict del año
#         if mes in ventas_por_fecha[year]:
#             # En cada mes, vamos a ir guardando los demás resultados en diferentes campos
#             # Agregamos la venta al campo "datos" del mes correspondiente
#             # [id_sale, id_product, review, refund]
#             ventas_por_fecha[year][mes]["ventas"].append([venta[0],
#                                                           venta[1],
#                                                           venta[2],
#                                                           venta[4]])
#         else:
#             # Si no está el mes agregamos un dict para el mes
#             ventas_por_fecha[year][mes] = {"ventas": [[venta[0], venta[1], venta[2], venta[4]]]}
#
#     # Agregamos un dict vacio si no está el año en el dict de ventas
#     else:
#         ventas_por_fecha[year] = {mes: {"ventas": [[venta[0], venta[1], venta[2], venta[4]]]}}
#
#
# # Iteramos sobre cada año
# for year in ventas_por_fecha:
#     # Luego iteramos sobre cada mes
#     for mes in ventas_por_fecha[year]:
#
#         # Ventas y reseñas por mes
#         ##########################
#
#         # Diccionario que lleva la cuenta de las ventas por cada producto
#         contadores_ventas = {}
#         # Lista con los productos más vendidos
#         prod_mas_vendidos = []
#
#         # Almacenar promedio de reseñas por productos
#         prod_con_reviews = {}
#         # Productos ordenados por sus reseñas
#         prod_reviews_ordenados = []
#
#         # Recorremos toda la lista de ventas
#         for venta in ventas_por_fecha[year][mes]["ventas"]:
#             # [id_sale, id_product, review, refund]
#             id_prod = venta[1]
#             review = venta[2]
#             reembolso = venta[3]
#
#             # Contamos las ventas del producto en ese mes
#             if id_prod in contadores_ventas:
#                 contadores_ventas[id_prod] += 1
#             else:
#                 contadores_ventas[id_prod] = 1
#
#             # Consideramos los reembolsos
#             if reembolso == 1:  # Debería ser necesario con solo (if reembolso), pero lo pongo completo
#                 contadores_ventas[id_prod] -= 1
#
#             # Si la review fue 0, no se cuenta
#             if review != 0:
#                 # Sacamos las reviews
#                 if id_prod in prod_con_reviews:
#                     # Sacamos el promedio conforme vamos sumando
#                     prod_con_reviews[id_prod] = [(prod_con_reviews[id_prod][0] + review) / 2,
#                                                  prod_con_reviews[id_prod][1] + 1]
#                 else:
#                     prod_con_reviews[id_prod] = [review, 1]
#
#         # Ordenamos los elementos de mayor a menor
#         ventas_ordenadas = sorted(contadores_ventas.items(),
#                                   key=lambda item: item[1],
#                                   reverse=True)
#
#         # Recorremos toda la lista de ventas
#         for venta in ventas_ordenadas:
#             # Buscamos el nombre del producto
#             for producto in lifestore_products:
#                 if producto[0] == venta[0]:
#                     # [id, la cantidad de ventas, el nombre del producto]
#                     prod_mas_vendidos.append([venta[0], venta[1], producto[1]])
#                     break
#
#         # Mandamos los resultados al dict
#         ventas_por_fecha[year][mes]["mas vendidos"] = prod_mas_vendidos[:5]
#         # ventas_por_fecha[year][mes]["menos vendidos"] = prod_mas_vendidos[-5:]
#
#         # Ordenamos por el promedio de reseñas
#         prod_con_reviews = sorted(prod_con_reviews.items(),
#                                   # Ordena el diccionario, basándose primero en el promedio
#                                   # de reviews, luego en la cantidad de reviews y después
#                                   # por id del producto.
#                                   key=lambda item: (item[1], item[0]),
#                                   reverse=True)
#
#         # Recorremos toda la lista de ventas
#         for prod in prod_con_reviews:
#             # Buscamos el nombre del producto
#             for producto in lifestore_products:
#                 if producto[0] == prod[0]:
#                     # [id, la cantidad de ventas, el nombre del producto]
#                     prod_reviews_ordenados.append([prod[0], prod[1][0], producto[1]])
#                     break
#
#         # Mandamos los resultados al dict
#         ventas_por_fecha[year][mes]["mejores reseñas"] = prod_reviews_ordenados[:5]
#         ventas_por_fecha[year][mes]["peores reseñas"] = prod_reviews_ordenados[-5:]
#
#
# # TODO: Mandar también a un JSON
# pprint.pprint(ventas_por_fecha, width=200, indent=1)
#
#
# # Productos más buscados
# ########################
# # Diccionario que lleva la cuenta de las busquedas por cada producto
# contadores_busquedas = {}
# # Lista con los productos más buscados
# prod_mas_buscados = []
#
# # Recorremos toda la lista de busquedas
# for busqueda in lifestore_searches:
#     id_prod = busqueda[1]
#     # El producto ya está en el dict
#     if id_prod in contadores_busquedas:
#         contadores_busquedas[id_prod] += 1
#     # El producto no está en el dict
#     else:
#         contadores_busquedas[id_prod] = 1
#
# # Ordenamos los elementos de mayor a menor usando la cantidad de veces que fue buscado
# busquedas_ordenadas = sorted(contadores_busquedas.items(),
#                              key=lambda item: item[1],
#                              reverse=True)
#
# # Agregamos a cada busqueda el nombre del producto y mostramos los productos
# # Recorremos todas la busquedas ordenadas
# for contador_busquedas in busquedas_ordenadas:
#     # Recorremos la lista de producto
#     for producto in lifestore_products:
#         # Encontramos el nombre del producto a partir del id
#         if producto[0] == contador_busquedas[0]:
#             # [id_prod, total_busquedas, nombre_prod
#             prod_mas_buscados.append([*contador_busquedas, producto[1]])
#             break
#
# print(prod_mas_buscados[:10])
#


# print("\n\nMostrando los 10 productos menos buscados por categoría")
# for categoria in busq_prod_por_categorias.keys():
#     print(f"\nCategoría: {categoria}")
#     for producto in busq_prod_por_categorias[categoria][-10:]:
#         print(" ", producto)


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
