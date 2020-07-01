 # -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import pygame
import uuid

# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
 
class TextPrint(object):
    def __init__(self):
        """Constructor"""
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
    
    def printf(self, mi_pantalla, text_string):
        textBitmap = self.font.render(text_string, True, NEGRO)
        mi_pantalla.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
         
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
         
    def indent(self):
        self.x += 10
         
    def unindent(self):
        self.x -= 10
     
direcction = ['FW','BW']


broker_addres = "broker.hivemq.com"
client = mqtt.Client('PC'.join(str(uuid.uuid4())))
client.connect(broker_addres)

pygame.init()
  
# Establecemos el largo y alto de la pantalla [largo,alto]
dimensiones = [500, 700]
pantalla = pygame.display.set_mode(dimensiones)
 
pygame.display.set_caption("Mi Juego")
 
#Iteramos hasta que el usuario pulsa el botón de salir.
hecho = False
 
# Lo usamos para gestionar cuán rápido de refresca la pantalla.
reloj = pygame.time.Clock()
 
# Inicializa los joysticks
pygame.joystick.init()
     
# Se prepara para imprimir
text_print = TextPrint()
 
# -------- Bucle Principal del Programa -----------
while not hecho:
    # PROCESAMIENTO DEL EVENTO
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            hecho = True
         
        # Acciones posibles del joystick: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if evento.type == pygame.JOYBUTTONDOWN:
            print("Botón presionado del joystick.")
        if evento.type == pygame.JOYBUTTONUP:
            print("Botón liberado del joystick.")
             
  
    # DIBUJAMOS
    # Primero, limpiamos la pantalla con color blanco. No pongas otros comandos de dibujo 
    # encima de esto, de lo contrario serán borrados por el comando siguiente.
    pantalla.fill(BLANCO)
    text_print.reset()
 
    # Contamos el número de joysticks
    joystick_count = pygame.joystick.get_count()
 
    text_print.printf(pantalla, "Número de joysticks: {}".format(joystick_count) )
    text_print.indent()
     
    # Para cada joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
     
        text_print.printf(pantalla, "Joystick {}".format(i) )
        text_print.indent()
     
        # Obtiene el nombre del Sistema Operativo del controlador/joystick
        nombre = joystick.get_name()
        text_print.printf(pantalla, "Nombre del joystick: {}".format(nombre))
         
        # Habitualmente, los ejes van en pareja, arriba/abajo para uno, e izquierda/derecha
        # para el otro.
        ejes = joystick.get_numaxes()
        text_print.printf(pantalla, "Número de ejes: {}".format(ejes))
        text_print.indent()
         
        for i in range(ejes):
            eje = joystick.get_axis(i)
            text_print.printf(pantalla, "Eje {} valor: {:>6.3f}".format(i, eje))
        text_print.unindent()
             
        botones = joystick.get_numbuttons()
        text_print.printf(pantalla, "Número de botones: {}".format(botones))
        text_print.indent()
 
        for i in range(botones):
            boton = joystick.get_button(i)
            text_print.printf(pantalla, "Botón {:>2} valor: {}".format(i,boton))
        text_print.unindent()
             
        # Hat switch. Todo o nada para la dirección, no como en los joysticks.
        # El valor vuelve en un array.
        hats = joystick.get_numhats()
        text_print.printf(pantalla, "Número de hats: {}".format(hats))
        text_print.indent()
 
        for i in range(hats):
            hat = joystick.get_hat(i)
            if hat[1]==1:
                client.publish('testPepper', direcction[0])
            if hat[1]==-1:
                client.publish('testPepper', direcction[1])


            text_print.printf(pantalla, "Hat {} valor: {}".format(i, str(hat)))
        text_print.unindent()
         
        text_print.unindent()
 
     
    # TODO EL CÓDIGO DE DIBUJO DEBERÍA IR ENCIMA DE ESTE COMENTARIO
     
    # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
 
    # Limitamos a 60 fotogramas por segundo.
    reloj.tick(5)
     
pygame.quit()