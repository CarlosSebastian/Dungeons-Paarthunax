#GRUPO 2
#Sofía Valeria García Quintana
#Davi Magalhaes Eler
#Leonardo Mormontoy Cabrera
#Carlos Sebastian Sobenes Obregon


import sys
import pygame
import random
import os.path

pygame.init()
clock = pygame.time.Clock()
fps = 150
game_over = False

# Fuentes
fuente = pygame.font.SysFont("Consolas", 75, 1)  # fuente, tamaño, grueso
fuente2 = pygame.font.SysFont("Consolas", 50, 1)
fuente3 = pygame.font.SysFont("Consolas", 22, 1)

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
color_menu = (50, 50, 50)
rojo = (220, 50, 50)
amarillo = (220, 200, 30)
verde = (50, 180, 50)
marron = (150, 100, 50)

# Pantalla
pygame.display.set_caption("Dungeon's Paarthurnax")
tamanho_panel_accion = 150
tamanho_pantalla_x = 1024
tamanho_pantalla_y = 426 + tamanho_panel_accion
pantalla = pygame.display.set_mode((tamanho_pantalla_x, tamanho_pantalla_y))
pantalla.fill(negro)

# Escenarios y música
escenario1 = pygame.image.load('imagenes/Fondo.png').convert_alpha()
escenario_menu = pygame.image.load("imagenes/menu4.png")


# Función para el escenario
def dibujar_esc(escenario):
    pantalla.blit(escenario, (0, 0))


class Personaje:
    def __init__(self, x, y, nombre, max_hp, atk, dfa, max_sta, tipo_esp, flip=True, mag=False):
        self.nombre = nombre
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.dfa = dfa
        self.max_sta = max_sta
        self.sta = max_sta
        self.tipo_esp = tipo_esp
        self.esp = 0
        self.dmg = 0
        self.total_dmg = 0
        self.max_dfa = False
        self.vivo = True
        self.lista_animacion = []
        self.frame = 0
        self.action = 0  # 0:reposo, 1:ataque, 2:herido, 3:muerto, 4:heal
        self.update = pygame.time.get_ticks()
        # reposo
        lista_temporal = []
        for i in range(1, 4):
            img = pygame.image.load(f"sprites/{self.nombre}/Idle{i}.png")
            if flip:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if mag:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            lista_temporal.append(img)
        self.lista_animacion.append(lista_temporal)
        # ataque
        lista_temporal = []
        for i in range(1, 7):
            img = pygame.image.load(f"sprites/{self.nombre}/Attack{i}.png")
            if flip:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if mag:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            lista_temporal.append(img)
        self.lista_animacion.append(lista_temporal)
        # herido
        lista_temporal = []
        for i in range(1, 4):
            img = pygame.image.load(f"sprites/{self.nombre}/Hurt{i}.png")
            if flip:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if mag:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            lista_temporal.append(img)
        self.lista_animacion.append(lista_temporal)
        # muerto
        lista_temporal = []
        for i in range(1, 7):
            img = pygame.image.load(f"sprites/{self.nombre}/Death{i}.png")
            if flip:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if mag:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            lista_temporal.append(img)
        self.lista_animacion.append(lista_temporal)
        # heal
        lista_temporal = []
        for i in range(1, 4):
            img = pygame.image.load(f"sprites/{self.nombre}/Heal{i}.png")
            if flip:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if mag:
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            lista_temporal.append(img)
        self.lista_animacion.append(lista_temporal)

        self.imagen = self.lista_animacion[self.action][self.frame]
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)

    def dibujo(self):
        pantalla.blit(self.imagen, self.rect)

    def idle(self):
        self.action = 0
        self.frame = 0
        self.update = pygame.time.get_ticks()

    def attack(self, target): #añadir target
        # daño a los enemigos
        if self.sta >= 10:
            self.sta -= 10
            rand = random.randint(1, 6)
            bloq = random.randint(0, target.dfa//2)
            self.dmg = self.atk + rand - bloq
            if target.max_dfa == True:
                self.dmg = 0
                target.max_dfa = False
            target.hp -= self.dmg #agregar el tema de DEF
            target.hurt()
            if target.hp < 1:
                target.hp = 0
                target.vivo = False
                target.death()
            # set variables to attack animation
            self.action = 1
            self.frame = 0
            self.update = pygame.time.get_ticks()
            self.esp += 1

    def restaurar(self):
        self.action = 4
        self.frame = 0
        self.update = pygame.time.get_ticks()
        self.hp += random.randint(5, 15)
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.sta += random.randint(5, 10)
        if self.sta > self.max_sta:
            self.sta = self.max_sta

    def especial(self, target):
        if self.sta >= 20:
            self.sta -= 20
            if self.tipo_esp == 1:
                rand = random.randint(15, 25)
                self.dmg = self.atk + rand
                target.hp -= self.dmg
                target.hurt()
                if target.hp < 1:
                    target.hp = 0
                    target.vivo = False
                    target.death()
                # set variables to attack animation
                self.action = 1
                self.frame = 0
                self.update = pygame.time.get_ticks()
            if self.tipo_esp == 2:
                self.dmg = 0
                self.hp += random.randint(25, 35)
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                self.sta += random.randint(20, 30)
                if self.sta > self.max_sta:
                    self.sta = self.max_sta
                #animacion
                self.action = 4
                self.frame = 0
                self.update = pygame.time.get_ticks()
            if self.tipo_esp == 3:
                self.dmg = 0
                self.attack(target)
                self.max_dfa = True
            self.esp = 0

    def hurt(self):
        self.action = 2
        self.frame = 0
        self.update = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame = 0
        self.update = pygame.time.get_ticks()

    def scores(self):
        self.total_dmg += self.dmg
        return self.total_dmg

    def update_img(self):
        cooldown = 200
        # update frame
        self.imagen = self.lista_animacion[self.action][self.frame]
        #revisar tiempo
        if pygame.time.get_ticks() - self.update > cooldown:
            self.update = pygame.time.get_ticks()
            self.frame += 1
        #reiniciar animación
        if self.frame >= len(self.lista_animacion[self.action]):
            if self.action == 3:
                self.frame = len(self.lista_animacion[self.action]) - 1
            else:
                self.idle()

# Funcion para panel de accion
class Panel():

    def __init__(self, jugador, enemigo):
        # Panel de accion
        self.paneldeac = pygame.image.load('imagenes/Panelbueno.png').convert_alpha()
        #crear texto del panel
        self.fuente_panel_accion = pygame.font.SysFont("Consolas", 30, True)
        self.Texto1 = self.fuente_panel_accion.render("1.ATACAR", 0, blanco)
        self.Texto2 = self.fuente_panel_accion.render("2.RESTABLECER", 0, blanco)
        self.Texto3 = self.fuente_panel_accion.render("3.ATAQUE ESPECIAL", 0, rojo)
        self.fuente_p_e_e = pygame.font.SysFont("Consolas", 20, True)
        self.jugador_e = self.fuente_p_e_e.render("Tu:", 0, blanco)
        self.enemigo_e = self.fuente_p_e_e.render("Enemigo:", 0, blanco)
        self.fuente_panel_estadisticas = pygame.font.SysFont("Consolas", 35, True)
        #data obtenida de los perfiles
        self.vida_jugador = self.fuente_panel_estadisticas.render(f"HP: {jugador.hp}/{jugador.max_hp}", 0, blanco)
        self.stamina_jugador = self.fuente_panel_estadisticas.render(f"STM: {jugador.sta}/{jugador.max_sta}", 0, blanco)
        self.vida_enemigo = self.fuente_panel_estadisticas.render(f"HP: {enemigo.hp}/{enemigo.max_hp}", 0, blanco)
        self.stamina_enemigo = self.fuente_panel_estadisticas.render(f"STM: {enemigo.sta}/{enemigo.max_sta}", 0, blanco)
        #mostrar que acciones no están disponibles
        if jugador.esp >= 3 and jugador.sta >= 20:
            self.Texto3 = self.fuente_panel_accion.render("3.ATAQUE ESPECIAL", 0, blanco)
        if jugador.sta < 10:
            self.Texto1 = self.fuente_panel_accion.render("1.ATACAR", 0, rojo)

    def acciones_panel(self, x, y):
        #posición acciones
        pantalla.blit(self.Texto1, (x, y))
        pantalla.blit(self.Texto2, (x, y + 30))
        pantalla.blit(self.Texto3, (x, y + 60))

    def positions(self, x, y):
        #posición datos jugador
        pantalla.blit(self.jugador_e, (x + 20, y - 20))
        pantalla.blit(self.vida_jugador, (x + 20, y+10))
        pantalla.blit(self.stamina_jugador, (x + 20, y + 50))
        #posición datos enemigos
        pantalla.blit(self.enemigo_e, (x + 280, y - 20))
        pantalla.blit(self.vida_enemigo, (x + 280, y+10))
        pantalla.blit(self.stamina_enemigo, (x + 280, y + 50))

    def dibujar_panel(self):
        #imprimir texto
        pantalla.blit(self.paneldeac, (0, tamanho_pantalla_y - tamanho_panel_accion))
        self.acciones_panel(tamanho_pantalla_x - 305, tamanho_pantalla_y - 120)
        self.positions(10, tamanho_pantalla_y - 110)

class Juego():
    def __init__(self):
        self.nivel = 1
        self.cdw = 0
        self.accion_wait_time = 15
        self.acto = False
        self.manejo_estado = "menu"
        self.score = 0
        self.nombre_jugador = ""
        self.stop = False
        pygame.mixer.music.load("sonidos/terraria.mp3")
        pygame.mixer.music.play(loops=4,start=0.0, fade_ms=100)
        pygame.mixer.music.set_volume(0.2)

    def estado(self):
        if self.manejo_estado == "menu":
            self.menu()
        elif self.manejo_estado == "nombre":
            self.elegir_nombre()
        elif self.manejo_estado == "eleccion":
            self.eleccion_personaje()
        elif self.manejo_estado == "highscores":
            self.highscores()
        elif self.manejo_estado == "nivel":
            self.cambio_nivel(self.nivel)
        elif self.manejo_estado == "juego":
            self.juego_principal(self.jugador, self.nivel)

    def menu(self):
        dibujar_esc(escenario_menu)
        texto_menu = ["1.JUGAR", "2.HIGHSCORES", "3.SALIR"]
        altura = 330
        for i in texto_menu:
            render_menu = fuente2.render(i, True, color_menu)
            retc_texto = render_menu.get_rect(center=(tamanho_pantalla_x // 2, altura))
            pantalla.blit(render_menu, retc_texto)
            altura += 70
        titulo = pygame.image.load(f"imagenes/titulo.png")
        rect = titulo.get_rect(center=(tamanho_pantalla_x // 2 + 50, 180))
        pantalla.blit(titulo, rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.manejo_estado = "nombre"
                elif event.key == pygame.K_2:
                    self.manejo_estado = "highscores"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

    def elegir_nombre(self):
        dibujar_esc(escenario_menu)
        texto_elegir = fuente2.render("Elige tu nombre:", True, color_menu)  # color_menu
        salir = fuente3.render("(PRESIONE ENTER PARA CONTINUAR)", True, color_menu)
        rect_e = texto_elegir.get_rect(center=(tamanho_pantalla_x // 2, 200))
        rect_s = salir.get_rect(center=(tamanho_pantalla_x // 2, 255))
        pantalla.blit(texto_elegir, rect_e)
        pantalla.blit(salir, rect_s)
        pygame.display.update()
        while True:
            event = pygame.event.poll()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if len(key) == 1:  # Teclas alfanumericas
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.nombre_jugador += key.upper()
                    else:
                        self.nombre_jugador += key
                elif key == "backspace":
                    self.nombre_jugador = self.nombre_jugador[:len(self.nombre_jugador) - 1]
                elif event.key == pygame.K_RETURN:  #terminar.
                    self.manejo_estado = "eleccion"
                    break

                dibujar_esc(escenario_menu)
                mostrar_nombre = fuente2.render(self.nombre_jugador, 1, color_menu)
                rect_nom = mostrar_nombre.get_rect(center=(tamanho_pantalla_x // 2, 325))
                pantalla.blit(mostrar_nombre, rect_nom)
                texto_elegir = fuente2.render("Elige tu nombre:", True, color_menu)  # color_menu
                salir = fuente3.render("(PRESIONE ENTER PARA CONTINUAR)", True, color_menu)
                rect_e = texto_elegir.get_rect(center=(tamanho_pantalla_x // 2, 200))
                rect_s = salir.get_rect(center=(tamanho_pantalla_x // 2, 255))
                pantalla.blit(texto_elegir, rect_e)
                pantalla.blit(salir, rect_s)
                pygame.display.update()

    def eleccion_personaje(self):
        pygame.draw.rect(pantalla, marron, (10, 10, 1004, 556))
        a = tamanho_pantalla_x // 5
        b = tamanho_pantalla_x // 2
        c = tamanho_pantalla_x - tamanho_pantalla_x // 5
        eje_x = [a, b, c]
        i = -1

        eleccion = [["1. CABALLERO", f"HP: {caballero.max_hp}", f"ATK: {caballero.atk}", f"DEF: {caballero.dfa}", f"STA: {caballero.max_sta}", "", "ESPECIAL:", "SUPER ATAQUE"],
             ["2. MAGO", f"HP: {mago.max_hp}", f"ATK: {mago.atk}", f"DEF: {mago.dfa}", f"STA: {mago.max_sta}", "", "ESPECIAL:", "RECUPERACIÓN"],
             ["3. ARQUERO", f"HP: {arquero.max_hp}", f"ATK: {arquero.atk}", f"DEF: {arquero.dfa}", f"STA: {arquero.max_sta}", "", "ESPECIAL:", "BLOQUEO MAXIMO"]]
        for personaje in eleccion:
            i += 1
            altura = 310
            for linea in personaje:
                stats = fuente3.render(linea, True, blanco)
                stats_rect = stats.get_rect(center=(eje_x[i], altura))
                pantalla.blit(stats, stats_rect)
                altura += 25
        especial = fuente3.render("¡Ataca 3 veces para desbloquar el especial!", True, blanco)
        esp_rect = especial.get_rect(center=(tamanho_pantalla_x//2, 530))
        pantalla.blit(especial, esp_rect)
        personajes = pygame.image.load(f"imagenes/personajes.png")
        rect = personajes.get_rect(center=(tamanho_pantalla_x//2, 180))
        pantalla.blit(personajes, rect)

        empezar = fuente3.render("ESCOGE UN PERSONAJE PRESIONANDO LAS TECLAS 1, 2 Y 3:", 0, blanco)
        pantalla.blit(empezar, (50, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.jugador = caballero
                    self.manejo_estado = "nivel"
                elif event.key == pygame.K_2:
                    self.jugador = mago
                    self.manejo_estado = "nivel"
                elif event.key == pygame.K_3:
                    self.jugador = arquero
                    self.manejo_estado = "nivel"

    def highscores(self):
        # self.score es el puntaje de la partida
        pantalla.fill(negro)
        high_scores = []
        if self.nivel == 1:
            regresar = fuente3.render("PARA REGRESAR PRESIONA ENTER", 0, blanco)
            rect_r = regresar.get_rect(center=(tamanho_pantalla_x // 2 + 50, 80))
            pantalla.blit(regresar, rect_r)
        elif self.nivel == 0:
            while self.stop == False:
                self.score = str(self.score)
                self.score = self.score.zfill(5)
                puntos = f"{self.score} - {self.nombre_jugador}"
                archivo = open("highscores.txt", "a")
                archivo.write(puntos)
                archivo.write("\n")
                archivo.close()
                self.stop = True
                break
            gracias = fuente3.render("¡GRACIAS POR JUGAR!", 0, blanco)
            pantalla.blit(gracias, (375, 30))
            puntaje = fuente3.render(f"{self.nombre_jugador}, tu puntaje es {self.score}.", 0, blanco)
            pantalla.blit(puntaje, (375, 60))
            elaborado = fuente3.render("Elaborado por: Sofía G., Leo M., Davi M. & Carlos S.", 0, blanco)
            pantalla.blit(elaborado, (375, 530))

        if os.path.exists("highscores.txt"):
            scores = open("highscores.txt", "r")
            scores = scores.readlines()
            sortedData = sorted(scores, reverse=True)
            for line in range(5):
                high_scores.append("#" + str(line + 1) + " " + sortedData[line][:-1])
        else:
            puntaje = fuente3.render("PUNTAJES INSUFICIENTES PARA MOSTRAR HIGHSCORES", 0, blanco)
            rect_p = puntaje.get_rect(center=(tamanho_pantalla_x // 2, 120))
            pantalla.blit(puntaje, rect_p)

        self.p1 = fuente.render(high_scores[0], 0, blanco)
        self.p2 = fuente.render(high_scores[1], 0, blanco)
        self.p3 = fuente.render(high_scores[2], 0, blanco)
        self.p4 = fuente.render(high_scores[3], 0, blanco)
        self.p5 = fuente.render(high_scores[4], 0, blanco)
        pantalla.blit(self.p1, (180, 120))
        pantalla.blit(self.p2, (180, 200))
        pantalla.blit(self.p3, (180, 280))
        pantalla.blit(self.p4, (180, 360))
        pantalla.blit(self.p5, (180, 440))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.nivel == 1:
                    self.manejo_estado = "menu"

    def cambio_nivel(self, nivel):
        if nivel == 1:
            pygame.mixer.music.load("sonidos/batalla.mp3")
            pygame.mixer.music.play(loops=4,start=0.0, fade_ms=100)
            pygame.mixer.music.set_volume(0.2)
        if nivel == 1 or nivel == 2:
            pantalla.fill(verde)
        if nivel == 3 or nivel == 4:
            pantalla.fill(amarillo)
        if nivel == 5:
            pantalla.fill(rojo)
        if nivel == 3 or nivel == 5:
            reg = fuente3.render("¡REGENERACIÓN DE HP Y STA!", 0, blanco)
            pantalla.blit(reg, (375, 480))
        level_text = fuente.render(f"NIVEL {nivel}", 0, blanco)
        pantalla.blit(level_text, (370, 240))
        empezar = fuente3.render("¡PRESIONA ENTER PARA SEGUIR!", 0, blanco)
        pantalla.blit(empezar, (375, 180))
        for tecla in pygame.event.get():
            if tecla.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if tecla.type == pygame.KEYDOWN:
                if tecla.key == pygame.K_RETURN:
                    self.manejo_estado = "juego"

    def juego_principal(self, jugador, nivel=1):
        if nivel == 1:
            enemigo = lagarto
        if nivel == 2:
            enemigo = dragon_bb
        if nivel == 3:
            enemigo = demonio
        if nivel == 4:
            enemigo = medusa
        if nivel == 5:
            enemigo = dragon

        # mostrar escenario y panel
        dibujar_esc(escenario1)
        panel_juego = Panel(jugador, enemigo)
        panel_juego.dibujar_panel()
        # mostrar luchadores
        jugador.update_img()
        jugador.dibujo()
        enemigo.update_img()
        enemigo.dibujo()

        events = pygame.event.get()
        # acción del jugador
        if jugador.vivo == True:
            if self.acto == False:
                for turno in events:
                    if turno.type == pygame.KEYDOWN:
                        if turno.key == pygame.K_1 and jugador.sta >= 10:
                            jugador.attack(enemigo)
                            self.score += jugador.scores()
                            self.acto = True
                        if turno.key == pygame.K_2:
                            jugador.restaurar()
                            self.acto = True
                        if turno.key == pygame.K_3 and jugador.esp == 3 and jugador.sta >= 20:
                            jugador.especial(enemigo)
                            self.score += jugador.scores()
                            self.acto = True
        else:
            pygame.mixer.music.stop()
            self.cdw += 1
            game_over_text = fuente.render("GAME OVER", 0, blanco)
            pantalla.blit(game_over_text, (340, 100))
            if self.cdw > 2 * self.accion_wait_time:
                self.nivel = 0
                self.manejo_estado = "highscores"

        # acción del enemigo (IA)
        if enemigo.vivo == True:
            if self.acto == True:
                self.cdw += 1
                if self.cdw > self.accion_wait_time:
                    opcion = random.randint(0, 5)
                    if opcion == 0 or opcion == 1 or opcion == 2:
                        if enemigo.sta >= 10:
                            enemigo.attack(jugador)
                        else:
                            enemigo.restaurar()
                    if opcion == 3 or opcion == 4:
                        enemigo.restaurar()
                    if opcion == 5:
                        if enemigo.sta >= 20 and enemigo.esp >= 3:
                            enemigo.especial(jugador)
                        elif enemigo.sta >= 10:
                            enemigo.attack(jugador)
                        else:
                            enemigo.restaurar()
                    self.acto = False
                    self.cdw = 0
        else:
            jugador.esp = 0
            self.cdw += 1
            tiempo = 20
            if self.cdw > tiempo:
                if nivel == 2 or nivel == 4:
                    jugador.hp = jugador.max_hp
                    jugador.sta = jugador.max_sta
                self.nivel += 1
                self.cdw = 0
                jugador.idle()
                self.acto = False
                if self.nivel < 6:
                    self.manejo_estado = "nivel"
                else:
                    self.nivel = 0
                    self.manejo_estado = "highscores"

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # para salir del juego al presionar esc
                    pygame.quit()
                    sys.exit()  # temporal

mostrar = Juego()

# CREACIÓN DE PERSONAJES
# Personaje(x, y, carpeta con sprites, max vida, ataque, defensa, max estamina, tipo de especial, girar y aumentar 3, aumentar 2):
# jugador
caballero = Personaje(320, 340, "knight", 100, 18, 20, 100, 1, False)
mago = Personaje(320, 310, "wizard", 120, 16, 18, 140, 2, False, True)
arquero = Personaje(320, 370, "archer", 110, 20, 16, 120, 3, False)

# enemigos
lagarto = Personaje(750, 350, "lizard", 40, 10, 13, 80, 3)
dragon_bb = Personaje(700, 390, "small_dragon", 40, 15, 20, 100, 1)
demonio = Personaje(650, 270, "demon", 60, 15, 15, 100, 2)
medusa = Personaje(650, 340, "medusa", 80, 20, 10, 120, 2)
dragon = Personaje(790, 250, "dragon", 120, 25, 20, 150, 1)

# LOOP DEL JUEGO
while not game_over:
    mostrar.estado()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
