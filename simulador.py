# Inicialização e importação das bibliotecas
import pygame
import math
pygame.init()

# Definições da simulação
rate = 60  # FPS (Frames por segundo)
dt = 1 / rate  # Intervalo entre frames
espaco_janela = 600  # Altura da janela
largura_janela = 1000  # Largura da janela para incluir o texto e botões

# Configuração da janela de exibição
screen = pygame.display.set_mode([largura_janela, espaco_janela])
clock = pygame.time.Clock()


# Lista para armazenar as partículas
particulas = []

# Definir 10 partículas usando um loop
for i in range(10):
    raio_massa = (i + 1) * 5  # Raio e massa variam de 5 a 50
    particulas.append({
        'x': 400 + i * 40,  # Distribuir partículas ao longo do espaço à direita
        'y': 50 + i * 40,  # Distribuir partículas ao longo do espaço
        'vx': (-1)**i * (50 + i * 10),  # Alternar direções e variar velocidades
        'vy': (-1)**(i + 1) * (30 + i * 10),
        'r': raio_massa,
        'm': raio_massa,
        'c': (255 - i * 25, i * 25, 128)  # Cores variadas
    })

# Inicialização de variáveis de controle
tipo_colisao = "elastica"  # Tipo inicial de colisão
coeficiente = 1.0  # Coeficiente para ajustar energias e velocidades
input_ativo = False  # Controle do campo de entrada
input_texto = "1.0"  # Texto inicial no campo de entrada

# Função para calcular energia cinética de uma partícula
def calcular_energia_cinetica(p):
    velocidade_quadrada = p['vx']**2 + p['vy']**2
    return 0.5 * p['m'] * velocidade_quadrada

# Loop principal da simulação
running = True
while running:
    # Checar eventos do usuário
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar clique do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Detectar clique nos botões
            if 10 <= x <= 60 and 450 <= y <= 490:
                tipo_colisao = "elastica"
            elif 70 <= x <= 120 and 450 <= y <= 490:
                tipo_colisao = "super-elastica"

            # Detectar clique no campo de entrada
            if 10 <= x <= 200 and 500 <= y <= 530:
                input_ativo = True
            else:
                input_ativo = False

        # Detectar entrada de texto e atualizar valor da variável coeficiente
        if event.type == pygame.KEYDOWN and input_ativo:
            if event.key == pygame.K_RETURN:
                try:
                    coeficiente = float(input_texto)
                except ValueError:
                    coeficiente = 1.0
                input_texto = f"{coeficiente:.1f}"
            elif event.key == pygame.K_BACKSPACE:
                input_texto = input_texto[:-1]
            else:
                input_texto += event.unicode

    # Preencher o fundo da janela com preto
    screen.fill((0, 0, 0))

    # Desenhar partículas
    for p in particulas:
        pygame.draw.circle(screen, p['c'], (int(p['x']), int(p['y'])), p['r'])

    # Exibir energia cinética de cada partícula
    font = pygame.font.SysFont(None, 24)
    energia_total = 0
    texto_x = 10  # Posição inicial do texto na esquerda
    texto_y = 140  # Espaçamento inicial abaixo do cabeçalho

    # Exibir informações adicionais no cabeçalho
    cabecalho1 = font.render("Simulador de Colisões", True, (255, 255, 255))
    cabecalho2 = font.render("Física 1 - Engenharia da Computação - UTFPR", True, (255, 255, 255))
    cabecalho3 = font.render("Aluno: Sergio Roncato Maccari", True, (255, 255, 255))
    cabecalho4 = font.render("Professor: Rafael Barreto", True, (255, 255, 255))
    screen.blit(cabecalho1, (texto_x, 10))
    screen.blit(cabecalho2, (texto_x, 30))
    screen.blit(cabecalho3, (texto_x, 50))
    screen.blit(cabecalho4, (texto_x, 70))

    for index, p in enumerate(particulas):
        energia_cinetica = calcular_energia_cinetica(p)
        energia_total += energia_cinetica
        texto = font.render(f"E{index+1}: {energia_cinetica:.2f}", True, (255, 255, 255))
        screen.blit(texto, (texto_x, texto_y + index * 20))

    # Exibir energia total do sistema
    texto_total = font.render(f"Energia Total: {energia_total:.2f}", True, (255, 255, 255))
    screen.blit(texto_total, (texto_x, texto_y + len(particulas) * 20 + 10))

    # Exibir o tipo de colisão atual
    if tipo_colisao == "elastica":
        texto_colisao = "Colisão: Elástica"
    else:
        if coeficiente > 1.0:
            texto_colisao = "Colisão: Super-Elástica"
        else:
            texto_colisao = "Colisão: Parcialmente Elástica"

    texto_colisao_render = font.render(texto_colisao, True, (255, 255, 255))
    screen.blit(texto_colisao_render, (texto_x, texto_y + len(particulas) * 20 + 40))

    # Verificar colisões entre partículas
    for i in range(len(particulas)):
        for j in range(i + 1, len(particulas)):
            p1 = particulas[i]
            p2 = particulas[j]

            # Calcular distância entre as partículas
            dx = p2['x'] - p1['x']
            dy = p2['y'] - p1['y']
            distance = math.sqrt(dx**2 + dy**2)

            # Verificar colisão
            if distance < (p1['r'] + p2['r']):
                # Vetores normal e tangencial
                nx = dx / distance
                ny = dy / distance
                tx = -ny
                ty = nx

                # Decompor velocidades
                v1n = p1['vx'] * nx + p1['vy'] * ny
                v1t = p1['vx'] * tx + p1['vy'] * ty
                v2n = p2['vx'] * nx + p2['vy'] * ny
                v2t = p2['vx'] * tx + p2['vy'] * ty

                # Calcular novas velocidades normais após colisão
                if tipo_colisao == "elastica":
                    v1n_new = (v1n * (p1['m'] - p2['m']) + 2 * p2['m'] * v2n) / (p1['m'] + p2['m'])
                    v2n_new = (v2n * (p2['m'] - p1['m']) + 2 * p1['m'] * v1n) / (p1['m'] + p2['m'])
                else:  # Super-elástica ou parcialmente elástica
                    v1n_new = coeficiente * ((v1n * (p1['m'] - p2['m']) + 2 * p2['m'] * v2n) / (p1['m'] + p2['m']))
                    v2n_new = coeficiente * ((v2n * (p2['m'] - p1['m']) + 2 * p1['m'] * v1n) / (p1['m'] + p2['m']))

                # Atualizar velocidades
                p1['vx'] = v1n_new * nx + v1t * tx
                p1['vy'] = v1n_new * ny + v1t * ty
                p2['vx'] = v2n_new * nx + v2t * tx
                p2['vy'] = v2n_new * ny + v2t * ty

                # Resolver sobreposição
                overlap = p1['r'] + p2['r'] - distance
                p1['x'] -= overlap * nx / 2
                p1['y'] -= overlap * ny / 2
                p2['x'] += overlap * nx / 2
                p2['y'] += overlap * ny / 2

    # Verificar colisões com as paredes
    for p in particulas:
        if (p['x'] - p['r']) < 400 or (p['x'] + p['r']) > largura_janela:
            p['vx'] = -p['vx']
        if (p['y'] - p['r']) < 0 or (p['y'] + p['r']) > espaco_janela:
            p['vy'] = -p['vy']

    # Atualizar posições
    for p in particulas:
        p['x'] += p['vx'] * dt
        p['y'] += p['vy'] * dt

    # Desenhar botões
    pygame.draw.rect(screen, (255, 0, 0), (10, 450, 50, 40))  # Botão 1 - Elastica
    pygame.draw.rect(screen, (0, 255, 0), (70, 450, 50, 40))  # Botão 2 - Parcialmente Elaática ou super-elástica
    botao1_texto = font.render("1", True, (255, 255, 255))
    botao2_texto = font.render("2", True, (255, 255, 255))
    screen.blit(botao1_texto, (25, 460))
    screen.blit(botao2_texto, (85, 460))

    # Desenhar campo de entrada
    cor_campo = (255, 255, 255) if input_ativo else (200, 200, 200)
    pygame.draw.rect(screen, cor_campo, (10, 500, 200, 30))
    input_surface = font.render(input_texto, True, (0, 0, 0))
    screen.blit(input_surface, (15, 505))

    # Atualizar exibição
    pygame.display.flip()

    # Limitar taxa de quadros
    clock.tick(rate)

# Encerrar pygame
pygame.quit()
