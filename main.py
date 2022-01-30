# Importamos los datos necesarios del archivo lifestore_file
from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

##################
## Login #########
##################
# Credenciales correctas
usuarios = {'jimmy':'ymmij'}
max_intentos = 3

# Mensaje de bienvenida y primera petición de las credenciales
mensaje_bienvenida = 'Bienvenide al sistema!\nAccede con tus credenciales'
print(mensaje_bienvenida)

# Variables de control
usuario_autenticado = False # El usuario está autenticado?
intentos = 0 # Contador de los intentos

# Ciclo para controlar el acceso hasta que el usuario dé las credenciales correctas
# TODO: recordar quitar esta madre
# while not usuario_autenticado:
while usuario_autenticado:
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



#####################################
## Productos con más ventas #########
#####################################
# Diccionario que lleva la cuenta de las ventas por cada producto
contadores_ventas = {}
# Lista con los productos más vendidos
prod_mas_vendidos = []

# Recorremos toda la lista de ventas
for venta in lifestore_sales:
    if venta[1] in contadores_ventas:
        contadores_ventas[venta[1]] += 1
    else:
        contadores_ventas[venta[1]] = 1

# Ordenamos los elementos de mayor a menor
ventas_ordenadas = dict(sorted(contadores_ventas.items(),
                               key = lambda item: item[1],
                               reverse = True))

# Agregamos a cada venta el nombre del producto y mostramos los productos
contador = 0

print("Mostrando productos más vendidos")
# Recorremos toda la lista
for contador_ventas in ventas_ordenadas.items():
    for producto in lifestore_products:
        if producto[0] == contador_ventas[0]:
            prod_mas_vendidos.append([*contador_ventas, producto[1]])
            break

    if contador == 5: break

    contador += 1


# TODO: mostrar los productos de mejor manera
print(prod_mas_vendidos, "\n\n")


# Diccionario que lleva la cuenta de las ventas por cada producto
contadores_busquedas = {}
# Lista con los productos más vendidos
prod_mas_buscados = []

# Recorremos toda la lista de ventas
for busqueda in lifestore_searches:
    if busqueda[1] in contadores_busquedas:
        contadores_busquedas[busqueda[1]] += 1
    else:
        contadores_busquedas[busqueda[1]] = 1

# Ordenamos los elementos de mayor a menor
busquedas_ordenadas = dict(sorted(contadores_busquedas.items(),
                               key = lambda item: item[1],
                               reverse = True))

# Agregamos a cada busqueda el nombre del producto y mostramos los productos
contador = 0
print("Mostrando productos más buscados")
# Recorremos toda la lista
for contador_busquedas in busquedas_ordenadas.items():
    for producto in lifestore_products:
        if producto[0] == contador_busquedas[0]:
            prod_mas_buscados.append([*contador_busquedas, producto[1]])
            break

    if contador == 10: break

    contador += 1


# TODO: mostrar los productos de mejor manera
print(prod_mas_buscados)


# print(ventas_ordenadas.items())
###################################
## Productos más buscados #########
###################################
#lifestore_searches = [id_search, id product]
# print(lifestore_searches[0])

#lifestore_products = [id_product, name, price, category, stock]
# print(lifestore_products[0])

# lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
# print(lifestore_sales[0])
