 # -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import pygame
import uuid



def publish_message(client, message):
    client.publish('testPepper', message)


direcction = {'forward':'fw','backward':'bw'}
head_position = {'up':'h_up','down':'h_dw','left':'h_lf','right':'h_rt','center':'h_ct'}
position = {'standart':'std','special1':'sp1','specia2':'sp2','special3':'sp3'}
gyro = ['g_lf','g_rt']
th_joystick = 0.5
broker_addres = "broker.hivemq.com"
client = mqtt.Client('PC', clean_session=False)
client.connect(broker_addres)

pygame.init()

hecho = False
 
# Lo usamos para gestionar cuán rápido de refresca la pantalla.
reloj = pygame.time.Clock()
 
# Inicializa los joysticks
pygame.joystick.init()
     
# Se prepara para imprimir

 
# -------- Bucle Principal del Programa -----------
while not hecho:
    # PROCESAMIENTO DEL EVENTO
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            hecho = True
         
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
        
    # Obtiene el nombre del Sistema Operativo del controlador/joystick
    nombre = joystick.get_name()
        
    # Habitualmente, los ejes van en pareja, arriba/abajo para uno, e izquierda/derecha
    # para el otro.
    ejes = joystick.get_numaxes()
    lateral_head = joystick.get_axis(2)
    vertical_head = joystick.get_axis(3)

    #head movements
    if(vertical_head>th_joystick):
        publish_message(client, head_position["down"])    
    if(vertical_head<-th_joystick):
        publish_message(client, head_position["up"])             
    if(lateral_head>th_joystick):
        publish_message(client, head_position["right"])    
    if(lateral_head<-th_joystick):
        publish_message(client, head_position["left"]) 
    if(joystick.get_button(11)):
        publish_message(client, head_position["center"]) 

    #Gyro movements
    if(joystick.get_button(4)):
        publish_message(client, gyro[0]) 
    if(joystick.get_button(5)):
        publish_message(client, gyro[1]) 

    # Hat switch. Todo o nada para la dirección, no como en los joysticks.
    # El valor vuelve en un array.
    hats = joystick.get_numhats()

    for i in range(hats):
        hat = joystick.get_hat(i)
        if hat[1]==1:
            publish_message(client,direcction['forward'])
        if hat[1]==-1:
            publish_message(client, direcction['backward'])

    for i in range(joystick.get_numbuttons()):
        if(joystick.get_button(i)):
            print('buton {} pess'.format(i))
 
    # Limitamos a 60 fotogramas por segundo.
    reloj.tick(5)
     
pygame.quit()