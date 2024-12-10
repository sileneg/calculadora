import pygame
import math
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO = 400
ALTO = 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Calculadora Científica")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_CLARO = (220, 220, 220)
NARANJA = (255, 165, 0)
AZUL_CLARO = (173, 216, 230)

# Fuente
FUENTE = pygame.font.Font(None, 35)

# Variables globales
entrada = ""
resultado = ""

# Configuración de botones
BOTON_ANCHO = 80
BOTON_ALTO = 70
BOTON_ESPACIO = 10  # Espacio entre botones

# Definir botones y posiciones
botones = [
    # Primera fila
    ("%", 20, 180), ("CE", 110, 180), ("C", 200, 180), ("⌫", 290, 180),
    # Segunda fila
    ("1/x", 20, 260), ("x²", 110, 260), ("√", 200, 260), ("/", 290, 260),
    # Tercera fila
    ("7", 20, 340), ("8", 110, 340), ("9", 200, 340), ("*", 290, 340),
    # Cuarta fila
    ("4", 20, 420), ("5", 110, 420), ("6", 200, 420), ("-", 290, 420),
    # Quinta fila
    ("1", 20, 500), ("2", 110, 500), ("3", 200, 500), ("+", 290, 500),
    # Sexta fila
    ("±", 20, 580), ("0", 110, 580), (".", 200, 580), ("=", 290, 580)
]

# Dibujar texto
def dibujar_texto(superficie, texto, x, y, tamaño, color):
    fuente = pygame.font.Font(None, tamaño)
    texto_superficie = fuente.render(texto, True, color)
    superficie.blit(texto_superficie, (x, y))

# Dibujar botones
def dibujar_botones():
    for texto, x, y in botones:
        color = NARANJA if texto == "=" else (AZUL_CLARO if texto in ["%", "CE", "C", "⌫"] else GRIS)
        pygame.draw.rect(VENTANA, color, (x, y, BOTON_ANCHO, BOTON_ALTO), border_radius=10)
        dibujar_texto(VENTANA, texto, x + 30, y + 20, 30, NEGRO)

# Procesar eventos
def manejar_eventos(evento):
    global entrada, resultado
    if evento.type == pygame.MOUSEBUTTONDOWN:
        x, y = evento.pos
        for texto, bx, by in botones:
            if bx < x < bx + BOTON_ANCHO and by < y < by + BOTON_ALTO:
                if texto == "C":  # Limpiar todo
                    entrada = ""
                    resultado = ""
                elif texto == "CE":  # Limpiar última entrada
                    entrada = entrada[:-1]
                elif texto == "=":  # Calcular resultado
                    try:
                        if "√" in entrada:
                            entrada = entrada.replace("√", "math.sqrt(") + ")"
                        if "x²" in entrada:
                            entrada = entrada.replace("x²", "**2")
                        resultado = str(eval(entrada))
                        entrada = resultado
                    except:
                        resultado = "Error"
                elif texto == "±":  # Cambiar signo
                    if entrada and entrada[0] == "-":
                        entrada = entrada[1:]
                    else:
                        entrada = "-" + entrada
                elif texto == "⌫":  # Borrar último carácter
                    entrada = entrada[:-1]
                elif texto == "1/x":  # Inverso
                    try:
                        resultado = str(1 / float(entrada))
                        entrada = resultado
                    except:
                        resultado = "Error"
                elif texto == "%":  # Calcular porcentaje
                    try:
                        numeros = entrada.split("*") if "*" in entrada else entrada.split("+")
                        if len(numeros) == 2:
                            base = float(numeros[0])
                            porcentaje = float(numeros[1]) / 100
                            entrada = f"{base * porcentaje}"
                        else:
                            resultado = "Error"
                    except:
                        resultado = "Error"
                else:
                    entrada += texto

# Actualizar pantalla
def actualizar_pantalla():
    VENTANA.fill(BLANCO)
    # Pantalla de resultados
    pygame.draw.rect(VENTANA, GRIS_CLARO, (20, 20, 360, 140), border_radius=10)
    dibujar_texto(VENTANA, entrada[:20], 30, 50, 40, NEGRO)
    dibujar_texto(VENTANA, resultado[:20], 30, 100, 30, NARANJA)

    # Dibujar botones
    dibujar_botones()
    pygame.display.flip()

# Bucle principal
def main():
    global entrada
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            manejar_eventos(evento)

        actualizar_pantalla()

# Ejecutar la calculadora
main()
