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

# Recorremos toda la lista de ventas
for venta in lifestore_sales:
    if venta[1] in contadores_ventas:
        contadores_ventas[venta[1]] += 1
    else:
        contadores_ventas[venta[1]] = 1

print(contadores_ventas)


###################################
## Productos más buscados #########
###################################
# print(lifestore_searches[0])
# print(lifestore_products[0])
# lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
# print(lifestore_sales[0])
