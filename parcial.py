import math

# --- configuraciones 

MAX_RETIRO = 5000#la cantidad maxima que puede retirar por sesion
MULT_OPERACION = 50#el multiplo
COMISION = 9.50

# --- variables para los usuarios

#estas variables son para identificar que dato pertenece a cada lugar de la matriz
i_numTarjeta = 0
i_pin = 1
i_dinero = 2
i_bloqueo = 3
i_banco = 4

usuarioInfo = [
    # [numero tarjeta, pin, dinero, bloqueo, banco]
    [123456, 2552, 1000, 0, 'BANMAS'],
    [991199, 0000, 2550, 0, 'BANCOR'],
    [559463, 0000, 3500, 0, 'MACRO']
]


billetes = [
    [500, 0],
    [200, 0],
    [100, 0],
    [50, 0]
]#los billetes con sus cantidades


# --- informacion del cajero
# [veces usado, cantidad bloqueos, total entregado, total depositado, total comisiones, cantidad de billetes, importe mayor retiro, importe mayor deposito]
infoCajero = [0, 0, 0, 0, 0, [0, 0, 0, 0], 0, 0]

#cargamos la cantidad de cada billete
for i in range(len(billetes)):
    billetes[i][1] = int(input(f"Ingresa la cantidad de billetes de {billetes[i][0]}: "))

#limpiamos un poco el log
for i in range(15):
    print("")


def cobrarComision(userid):
    if(usuarioInfo[userid][i_banco] != 'BANMAS'):
        usuarioInfo[userid][i_dinero] -= COMISION#cobramos comision
        infoCajero[4] += COMISION

userid = -1

while(userid == -1):#iniciamos la sesion
    user = int(input("Ingresa tu numero de tarjeta: "))
    if(user == 0):#terminar el sistema si ingresa un numero de tarjeta 0
        break

    for t in range(len(usuarioInfo)):
        if(usuarioInfo[t][i_numTarjeta] == user):#verifica si encuentra algun usuario con ese numero de tarjeta
            userid = t

    if(userid == -1):#no se encontro usuario con numero de tarjeta
        print("ERROR: No se encontro ninguna cuenta con ese numero de tarjeta.")
    elif(usuarioInfo[userid][i_bloqueo] != 0):#si esta la cuenta bloqueada
            print("ERROR: Esta cuenta se encuentra bloqueada.")
            userid = -1
    else:
            intentos = 0#reseteamos la variable de intentos
            while(True):
                pin = int(input("Ingresa el PIN:"))
                if(pin != usuarioInfo[userid][i_pin]):#clave PIN incorrecta
                    print("EROR: PIN incorrecto, intenta de nuevo.")
                    intentos += 1#sumamos el contador de intentos fallidos
                    if(intentos == 3):#si los intentos llega a 3
                        print("ALERTA: Se bloqueo tu tarjeta por 24h.")
                        usuarioInfo[userid][i_bloqueo] = 1#bloqueamos la cuenta
                        userid = -1
                        infoCajero[1] += 1#cantidad de bloqueos
                        break
                else:
                    infoCajero[0] += 1#cantidad de usos
                    print("****")
                    print("*                              *")
                    print("*    BIENVENIDO AL BANCO       *")
                    print("*                              *")
                    print("****")
                    while(True):
                        #mostramos las opciones
                        print("MENU DE OPCIONES:")
                        print("1. VER SALDO")
                        print("2. DEPOSITO")
                        print("3. RETIRO")
                        print("4. SALIR")
                        opcion = int(input("OPCION: "))
                        if(opcion == 1):#ver saldo
                            cobrarComision(userid)#cobramos la comision
                            print("--------------------------------------------------------")
                            print(f"INFO: Tu saldo es: ${usuarioInfo[userid][i_dinero]}.")
                            print("--------------------------------------------------------")
                        elif(opcion == 2):#deposito
                            dinero = int(input("Ingresa la cantidad a depositar: "))
                            if(dinero%MULT_OPERACION != 0):#si no es multiplo del valor de la variable MULT_OPERACION
                                print(F"ERROR: Solo puedes depositar ${MULT_OPERACION}, ${MULT_OPERACION * 2}, etc")
                            else:
                                usuarioInfo[userid][i_dinero] += dinero#a la variable del dinero en banco le sumamos
                                infoCajero[3] += dinero#dinero depositado
                                if(dinero > infoCajero[7]):#para obtener el mayor deposito
                                    infoCajero[7] = dinero
                                print("--------------------------------------------------------")
                                print(f"INFO: Depositaste ${dinero}.")
                                print("--------------------------------------------------------")
                                cobrarComision(userid)
                        elif(opcion == 3):#retiro
                            dinero = int(input("Ingresa la cantidad a retirar: "))
                            if(dinero > usuarioInfo[userid][i_dinero]):#si no tiene el dinero ingresado en su cuenta
                                print("ERROR: No hay esa cantidad en tu cuenta bancaria.")
                            elif(dinero > MAX_RETIRO):#si excede la cantidad maxima de retiro por sesion
                                print(f"ERROR: Solo podes retirar {MAX_RETIRO} por operacion.")
                            elif(dinero%MULT_OPERACION != 0):#si no es multiplo
                                print(f"ERROR: Solo puedes retirar ${MULT_OPERACION}, ${MULT_OPERACION * 2}, etc")
                            else:        
                                dinerobuscar = dinero

                                #recorremos los billetes
                                for i in range(len(billetes)):
                                    if(billetes[i][1] > 0 and dinerobuscar > 0):#si hay billetes y el dinero a entregar es mayor a 0
                                            
                                        cantidadb = math.floor(dinerobuscar / billetes[i][0])#vemos cuantos billetes podemos entregar segun la cantidad a dar
                                        if(cantidadb > billetes[i][1]):#si la cantidad de billetes a dar es mayor a la cantidad disponible
                                            cantidadb = billetes[i][1]#actualizamos a la cantidad disponible

                                        billetes[i][1] -= cantidadb#desconetamos la cantidad de billetes disponible
                                        dinerobuscar -= billetes[i][0] * cantidadb#restamos a la cantidad de dinero a dar
                                        if(cantidadb > 0):
                                            infoCajero[5][i] += cantidadb
                                            print(f"Se entrego {cantidadb} billetes de ${billetes[i][0]}")
                               
                                if(dinerobuscar == dinero):#si no encontro billetes para entregar
                                    print(f"ERROR: El cajero no puede entregar el monto solicitado.")  
                                else:#encontro dinero para entregar
                                    if((dinero - dinerobuscar) > infoCajero[6]):#para obtener el mayor retiro
                                        infoCajero[6] = (dinero - dinerobuscar)

                                    infoCajero[2] += dinero - dinerobuscar#dinero entregado
                                    print("--------------------------------------------------------")
                                    if(dinerobuscar > 0):#faltan billetes para dar
                                        print(f"Disculpe, por falta de billetes solo te pudimos entregar ${dinero - dinerobuscar}.")
                                    else:#no falto billetes para dar
                                        print(f"INFO: Retiraste ${dinero}.")
                                    print("--------------------------------------------------------")
                                    usuarioInfo[userid][i_dinero] -= (dinero - dinerobuscar)
                                    cobrarComision(userid) 
                        elif(opcion == 4):#salir
                            print("Por favor retire su tarjeta.")
                            print("Recuerde usar alcohol en sus manos despues de operar.")
                            userid = -1
                            break
                    break

#imprimimos los datos
print("----------------------------------------------")
print("-------------------TICKET---------------------")
print(f"Cantidad de veces usado: {infoCajero[0]}")
print(f"Cantidad de usuarios bloqueados: {infoCajero[1]}")
print(f"Importe total entregado: ${infoCajero[2]}")
print(f"Importe total depositado: ${infoCajero[3]}")
print(f"Importe total por comisiones: {infoCajero[4]}")
for i in range(len(billetes)):
    print(f"Billetes de {billetes[i][0]} entregados: {infoCajero[5][i]}")
print(f"Importe del mayor retiro: ${infoCajero[6]}")
print(f"Importe del mayor deposito: ${infoCajero[7]}")
