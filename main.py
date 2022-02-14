# Importamos los datos necesarios del archivo lifestore_file
from lifestore_file import (
    lifestore_products,
    lifestore_sales,
    lifestore_searches
)

import calendar

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

# Almacenar promedio de reseñas por productos
prod_con_reviews = {}
# Productos ordenados por sus reseñas
prod_reviews_ordenados = []

# Recorremos toda la lista de ventas
for venta in lifestore_sales:
    id_prod = venta[1]
    review = venta[2]
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

    # Si la review fue 0, no se cuenta
    if review != 0:
        # Sacamos las reviews
        # [promedio_reviews, total_reviews]
        if id_prod in prod_con_reviews:
            # Sacamos el promedio conforme vamos sumando
            prod_con_reviews[id_prod] = [(prod_con_reviews[id_prod][0] + review) / 2,
                                         prod_con_reviews[id_prod][1] + 1]

        else:
            prod_con_reviews[id_prod] = [review, 1]

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
    # {categoría: [[id_product, name, price, category, stock, total_sales, total_searches, reviews], [...]]}
    producto = producto + [0, 0, 0, 0]

    # Agregamos el número de ventas en caso de que tenga
    if id_prod in contadores_ventas:
        producto[5] = contadores_ventas[id_prod]

    # Agregamos el contador de busquedas
    if id_prod in contadores_busquedas:
        producto[6] = contadores_busquedas[id_prod]

    # Agregamos al producto el promedio de reviews y el contador de reviews
    if id_prod in prod_con_reviews:
        producto[7] = round(prod_con_reviews[id_prod][0], 2)
        producto[8] = prod_con_reviews[id_prod][1]

        # Lista fuera del dict para guardar los productos y sus reviews
        # Solo agregamos aquellos productos que tienen una cantidad de reviews mayor a 0
        prod_reviews_ordenados.append(producto)

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
print("\nProductos por categorias con menos búsquedas")
for categoria in categorias_por_busquedas:
    print(" ", categoria)
    for prod in categorias_por_busquedas[categoria][-10:]:
        print("   ", prod)


# 2: Mejores y peores reseñas
#############################
prod_reviews_ordenados = sorted(prod_reviews_ordenados,
                                # Si hay dos con el mismo número de promedio, se usa el total de reviews
                                key=lambda item: (item[7], item[8]),
                                reverse=True)

print("\nProductos con mejores reseñas")
for prod in prod_reviews_ordenados[:5]:
    print(" ", prod)

print("\nProductos con peor reseñas")
for prod in prod_reviews_ordenados[-5:]:
    print(" ", prod)

# 3: Separación de la ventas por fecha
####################################
# Diccionario que almacena las ventas de acuerdo al año y el mes
# Cada año es una entrada del dict
# Cada año es un dict, las entradas de este son los meses
ventas_por_fecha = {}

# Separamos las fechas de cada venta en el mes y el año
for venta in lifestore_sales:
    # Obtenemos la fecha de la venta
    fecha = venta[3]

    # Obtenemos el mes y el año del string de la fecha, el día no interesa
    # Dividiendo el string por el símbolo "/"
    _, mes, year = fecha.split("/")

    # Transformamos los strings a int
    year = int(year)
    mes = int(mes)

    # Ahora la fecha de las compras es una lista con el año y el mes
    venta[3] = [year, mes]

    # Checamos el año esté en el dict
    if year in ventas_por_fecha:
        # Vemos si el mes está en el dict del año
        if mes in ventas_por_fecha[year]:
            # En cada mes, vamos a ir guardando los demás resultados en diferentes campos
            # Agregamos la venta al campo "datos" del mes correspondiente
            # [id_sale, id_product, review, refund]
            ventas_por_fecha[year][mes]["Ventas"].append([venta[0],
                                                          venta[1],
                                                          venta[2],
                                                          venta[4]])
        else:
            # Si no está el mes agregamos un dict para el mes
            ventas_por_fecha[year][mes] = {"Ventas": [[venta[0], venta[1], venta[2], venta[4]]]}

    # Agregamos un dict inicial si no existe el dict dentro del dict
    else:
        ventas_por_fecha[year] = {mes: {"Ventas": [[venta[0], venta[1], venta[2], venta[4]]]}}

# Iteramos sobre cada año
for year in ventas_por_fecha:
    # Luego iteramos sobre cada mes
    for mes in ventas_por_fecha[year]:

        # Ventas por mes
        ##########################

        # Diccionario que lleva la cuenta de las ventas por cada producto
        contadores_ventas = {}
        # Lista con los productos más vendidos
        monto_por_producto = []

        # Recorremos toda la lista de ventas
        for venta in ventas_por_fecha[year][mes]["Ventas"]:
            # [id_sale, id_product, refund]
            id_prod = venta[1]
            reembolso = venta[3]

            # Contamos las ventas del producto en ese mes
            if id_prod in contadores_ventas:
                contadores_ventas[id_prod] += 1
            else:
                contadores_ventas[id_prod] = 1

            # Consideramos los reembolsos
            if reembolso == 1:  # Debería ser necesario con solo (if reembolso), pero lo pongo completo
                contadores_ventas[id_prod] -= 1

        # Ordenamos los elementos de mayor a menor
        ventas_ordenadas = sorted(contadores_ventas.items(),
                                  key=lambda item: item[1],
                                  reverse=True)

        costo_total_mensual = 0
        ventas_mensuales = 0
        # Recorremos toda la lista de ventas
        for venta in ventas_ordenadas:
            if venta[1] == 0:
                continue

            # Buscamos el nombre del producto
            for producto in lifestore_products:
                if producto[0] == venta[0]:
                    costo_total = int(venta[1]) * int(producto[2])

                    # [id, cantidad_ventas, precio_unitario, costo_total, el nombre del producto]
                    monto_por_producto.append([venta[0],
                                               venta[1],
                                               producto[2],
                                               costo_total,
                                               " ".join(list(producto[1].replace(",", "").split(" ", 8))[:8])])

                    costo_total_mensual += costo_total
                    ventas_mensuales += venta[1]

                    break

        ventas_por_fecha[year][mes]["Resumen Ventas"] = monto_por_producto
        ventas_por_fecha[year][mes]["Total de Ingresos"] = costo_total_mensual
        ventas_por_fecha[year][mes]["Productos vendidos"] = ventas_mensuales

# TODO: Mandar también a un JSON
# Imprimimos la cantidad de productos vendidos por mes de cada año
print("\nVentas por año y mes")
for year in ventas_por_fecha:
    print("Ventas año", year)

    # Por mes vamos imprimiendo el total de ingresos y la cantidad de productos vendidos
    for mes in ventas_por_fecha[year]:
        print("  Mes", calendar.month_name[mes])
        print("    Cantidad de productos vendidos", ventas_por_fecha[year][mes]["Productos vendidos"])
        print("    Total de ingresos mensuales", ventas_por_fecha[year][mes]["Total de Ingresos"])

    # Obtenemos el mes con más ventas
    mes_mas_ventas = sorted(ventas_por_fecha[year].items(),
                            key=lambda item: item[1]["Productos vendidos"],
                            reverse=True)

    print("  Mes con más ventas:", calendar.month_name[mes_mas_ventas[0][0]])

    # Obtenemos el total de ingresos por año
    suma_year = sum(item[1]["Total de Ingresos"] for item in ventas_por_fecha[year].items())
    print("  Total de ingresos en el año:", suma_year)

