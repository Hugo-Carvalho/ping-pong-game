import sys, os, pygame, time, random
from pygame.locals import *

# posiciona janela do jogo no centro
os.environ['SDL_VIDEO_CENTERED'] = '1'

## configuracao das cores
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## configuracoes da GUI
FPS = 50
W_SIZE = W_WIDTH, W_HEIGHT = 850, 500

## configuracoes do jogo
BALL_RADIUS = 20 # raio da bolinha
PAD_WIDTH = 5 # largura dos bastoes
PAD_HEIGHT = 80 # altura dos bastoes
HALF_PAD_WIDTH = PAD_WIDTH / 2 # metade da largura dos bastoes
HALF_PAD_HEIGHT = PAD_HEIGHT / 2 # metade da altura dos bastoes
speed_increase = 0.1 # velocidade de aumento da bolinha (10%)
ball_pos = [] # posicao da bolinha
ball_vel = [] # velocidade da bolinha
ball_vel_cop = [0,0] # copia da velocidade da bolinha
paddle1_pos = [] # posicao do bastao 1
paddle2_pos = [] # posicao do bastao 2
paddle1_vel = [] # velocidade do bastao 1
paddle2_vel = [] # velocidade do bastao 1
score1 = 0 # pontuacao 1
score2 = 0 # pontuacao 1
pause = False # guarda status do jogo
pause_text = "" # texto de jogo pausado
color = BLACK # cor de fundo

#MARIO
marioBoll = False
luigiBoll = False
mario_pos = []
luigi_pos = []
mario = pygame.image.load("./marioiconL.png")
luigi = pygame.image.load("./marioiconR.png")
mario = pygame.transform.scale(mario,(100,100))
luigi = pygame.transform.scale(luigi,(100,100))
mariorect = mario.get_rect()
luigirect = luigi.get_rect()

def main():
        """ funcao principal """

        global SCREEN, CLOCK, sound_beep, sound_boop, sound_gool, sound_mario_jump, color
        pygame.mixer.pre_init(44100, 16, 2, 4096) # inicia dispositivo de som
        pygame.init() # inicia pygame

        pygame.display.set_icon(pygame.image.load('gameicon.png'))
        SCREEN = pygame.display.set_mode(W_SIZE)

        pygame.display.set_caption("PING-PONG")

        CLOCK = pygame.time.Clock()

        font_score = pygame.font.Font('freesansbold.ttf', 50)

        sound_beep = pygame.mixer.Sound('./pong_beep.wav')
        sound_boop = pygame.mixer.Sound('./pong_boop.wav')
        sound_gool = pygame.mixer.Sound('./pong_gool.wav')
        sound_mario_jump = pygame.mixer.Sound('./mario_Jump.wav')

        pygame.mixer.music.load("./pong_bottom.wav")
        pygame.mixer.music.play(-1, 0.0)


        
        init()
        while True:
                SCREEN.fill(color)

                pressed = pygame.key.get_pressed()
        
                # verifica eventos
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.mixer.music.stop()
                                pygame.quit()
                                sys.exit()
                        elif event.type == pygame.KEYDOWN:
                                keydown(event.key)
                        elif event.type == pygame.KEYUP:
                                keyup(event.key)
                        
                draw(font_score) # desenha os objetos
                pygame.display.update()  # atualiza a tela com os objetos
                CLOCK.tick(FPS) # velocidade de atualizacao


def init():
        """ inicia parametros do jogo """
        global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
        global ball_pos, ball_vel, pause_text, pause
        global score1, score2

        #MARIO
        global luigi_pos, mario_pos

        mario_pos = [50,W_HEIGHT - 50]
        luigi_pos = [W_WIDTH - 50,W_HEIGHT - 50]
        
        mariorect.center = mario_pos
        luigirect.center = luigi_pos
        #/MARIO
        
        score1 = 0
        score2 = 0
        paddle1_pos = [0, W_HEIGHT/2]
        paddle2_pos = [W_WIDTH-1, W_HEIGHT/2]
        paddle1_vel = [0, 0]
        paddle2_vel = [0, 0]
        ball_pos = [W_WIDTH//2, W_HEIGHT//2]
        ball_vel = [0, 0]
        pause = False
        pause_text = "" 

def start():
        """ inicia a movimentacao da bolinha """

        global pause, pause_text
        if not pause:
                ball_init(random.choice([True, False]))


def pause_game():
        """ define se jogo esta em pausa """
        # TODO: vc devera encontrar a logica para jogo em pausa ou nao.
        # Se estiver em pausa, coloque o texto PAUSE, guarde a velocidade
        # da bolinha e altere a velocidade da bolinha para zero.
        # Se o jogo nao estiver em pausa, o texto altera para "" (string
        # vazia), volte com a velocidade da bolinha.

        global pause_text, pause, ball_vel_cop, ball_vel, paddle1_vel, marioBoll
        
        if pause == True:
              pause_text = "PAUSE"
              ball_vel_cop = ball_vel
              ball_vel = (0,0)
        else:
              pause_text = ""
              ball_vel = ball_vel_cop

def ball_init(right):
        """ escolhe uma direcao para a bolinha """
        global ball_pos, ball_vel
    
        ball_pos = [W_WIDTH//2, W_HEIGHT//2] # TODO: bola inicia no meio da tela
        ball_vel = [random.randrange(120, 240), -random.randrange(60, 180)] # velocidade inicial (não alterar!)
        if not right:
                ball_vel[0] = -ball_vel[0] # move bola para a esquerda dependendo do parametro 'right'


def draw(font_score):
        """ desenha os objetos """

        global paddle1_pos, paddle2_pos, ball_pos, ball_vel, SCREEN
        
        update_paddle()

        # desenha as linhas (posicao fixa)
        pygame.draw.line(SCREEN, WHITE, (W_WIDTH/2, 0), (W_WIDTH/2, W_HEIGHT), 2)
        pygame.draw.line(SCREEN, WHITE, (PAD_WIDTH, 0), (PAD_WIDTH, W_HEIGHT), 1)
        pygame.draw.line(SCREEN, WHITE, (W_WIDTH-PAD_WIDTH, 0), (W_WIDTH-PAD_WIDTH, W_HEIGHT), 1)

        # desenha os bastoes (posicao varia de acordo com as teclas pressionadas)
        pygame.draw.line(SCREEN, WHITE, (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT), 
                                                 (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT), PAD_WIDTH)

        pygame.draw.line(SCREEN, WHITE, (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), 
                                                 (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT), PAD_WIDTH)

        # desenha o score (varia qndo ha pontuacao) e texto para pausa
        text_surf_p1 = font_score.render(str(score1), True, WHITE, BLACK)
        text_surf_p2 = font_score.render(str(score2), True, WHITE, BLACK)
        text_surf_pause = font_score.render(pause_text, True, WHITE, BLACK)
        text_rect_p1 = text_surf_p1.get_rect()
        text_rect_p2 = text_surf_p2.get_rect()
        text_rect_pause = text_surf_pause.get_rect()
        text_rect_p1.center = (W_WIDTH//5, 50)
        text_rect_p2.center = (W_WIDTH//5 + (3*W_WIDTH//5), 50)
        text_rect_pause.center = (W_WIDTH//2, W_HEIGHT//2)
        SCREEN.blit(text_surf_p1, text_rect_p1)
        SCREEN.blit(text_surf_p2, text_rect_p2)
        SCREEN.blit(text_surf_pause, text_rect_pause)

        # desenha a bolinha (varia com a velocidade e posicao)
        update_ball()
        pygame.draw.circle(SCREEN, WHITE, ball_pos, BALL_RADIUS, 0)

        #MARIO
        if marioBoll == True:
                        SCREEN.blit(mario, mariorect)
                        print (mariorect.center)
        if luigiBoll == True:
                        SCREEN.blit(luigi, luigirect)
        #/MARIO

def update_paddle():
        """ atualiza os bastoes """

        paddle1_pos[1] =  paddle1_pos[1] + paddle1_vel[1] # TODO: mudar a posicao do bastao 1: posicao somada a velocidade
        paddle2_pos[1] =  paddle2_pos[1] + paddle2_vel[1] # TODO: mudar a posicao do bastao 2: posicao somada a velocidade
    
        # TODO: matenha os bastoes na tela
        
        # bastao 1
        if paddle1_pos[1] - HALF_PAD_HEIGHT <= 0:
                   paddle1_pos[1] = HALF_PAD_HEIGHT
        elif paddle1_pos[1] + HALF_PAD_HEIGHT >= W_HEIGHT:
                paddle1_pos[1] = W_HEIGHT - HALF_PAD_HEIGHT
   # bastao 2
        if paddle2_pos[1] - HALF_PAD_HEIGHT <= 0:
                paddle2_pos[1] = HALF_PAD_HEIGHT
        elif paddle2_pos[1] + HALF_PAD_HEIGHT >= W_HEIGHT:
                paddle2_pos[1] = W_HEIGHT - HALF_PAD_HEIGHT


def update_ball():
        """ atualiza posicao da bolinha assim como a pontuacao """
        global score1, score2, marioBoll, luigiBoll, mariorect, luigirect, mario_pos, luigi_pos
    
        # TODO: atualiza posicao da bolinha (60 FPS)
        # Dica: cada coordenada da posicao da bolinha vai ser adicionada a 
        # parcela int(round(ball_vel[]/FPS))
        ball_pos[0] = ball_pos[0] + int(round(ball_vel[0]/FPS))
        ball_pos[1] = ball_pos[1] + int(round(ball_vel[1]/FPS))

        #MARIO
        if marioBoll == True:
                mario_pos[0] = mario_pos[0] + 10
                mario_pos[1] = mario_pos[1] - 10
                mariorect.center = ([mario_pos[0], mario_pos[1]])
                print (mariorect.center)
        if luigiBoll == True:
                luigi_pos[0] = luigi_pos[0] - 10
                luigi_pos[1] = luigi_pos[1] - 10
                luigirect.center = ([luigi_pos[0], luigi_pos[1]])

        if mario_pos[1] <= 0:
                marioBoll = False
                mario_pos = [50,W_HEIGHT - 50]
        if luigi_pos[1] <= 0:
                luigiBoll = False
                luigi_pos = [W_WIDTH - 50,W_HEIGHT - 50]
                
        if (mario_pos[0] + 50 >= ball_pos[0] - BALL_RADIUS and ball_pos[0] - BALL_RADIUS >= mario_pos[0]) and (ball_pos[1] + BALL_RADIUS <= mario_pos[1] + 50 and ball_pos[1] - BALL_RADIUS >= mario_pos[1] - 50):
                if marioBoll == True:
                        ball_vel[0] = -ball_vel[0]
                        ball_vel[1] = -ball_vel[1]
                        ball_vel[0] = ball_vel[0] + 400 + speed_increase
                        ball_vel[1] = ball_vel[1] + 400 + speed_increase
                        ball_vel[1] = -ball_vel[1]
        elif (mario_pos[1] + 50 >= ball_pos[1] - BALL_RADIUS and ball_pos[1] - BALL_RADIUS >= mario_pos[1]) and (ball_pos[0] + BALL_RADIUS <= mario_pos[0] + 50 and ball_pos[0] - BALL_RADIUS >= mario_pos[0] - 50):
                if marioBoll == True:
                        ball_vel[0] = -ball_vel[0]
                        ball_vel[1] = -ball_vel[1]
                        ball_vel[0] = ball_vel[0] + 400 + speed_increase
                        ball_vel[1] = ball_vel[1] + 400 + speed_increase
                        ball_vel[1] = -ball_vel[1]

        if (luigi_pos[0] + 50 >= ball_pos[0] - BALL_RADIUS and ball_pos[0] - BALL_RADIUS >= luigi_pos[0]) and (ball_pos[1] + BALL_RADIUS <= luigi_pos[1] + 50 and ball_pos[1] - BALL_RADIUS >= luigi_pos[1] - 50):
                if luigiBoll == True:
                        ball_vel[0] = -ball_vel[0]
                        ball_vel[1] = -ball_vel[1]
                        ball_vel[0] = ball_vel[0] + 400 + speed_increase
                        ball_vel[1] = ball_vel[1] + 400 + speed_increase
                        ball_vel[1] = -ball_vel[1]
        elif (luigi_pos[1] + 50 >= ball_pos[1] - BALL_RADIUS and ball_pos[1] - BALL_RADIUS >= luigi_pos[1]) and (ball_pos[0] + BALL_RADIUS <= luigi_pos[0] + 50 and ball_pos[0] - BALL_RADIUS >= luigi_pos[0] - 50):
                if luigiBoll == True:
                        ball_vel[0] = -ball_vel[0]
                        ball_vel[1] = -ball_vel[1]
                        ball_vel[0] = ball_vel[0] + 400 + speed_increase
                        ball_vel[1] = ball_vel[1] + 400 + speed_increase
                        ball_vel[1] = -ball_vel[1]
        #/MARIO

    
        # TODO: bola rebate no bastao 1 (refleccao do bastao 1): 
        # tocar som boop;
        # aumentar velocidade da bolinha em (1 + 10/100) (use a variavel speed_increase)
        # cuidado com a direcao
        if (ball_pos[0] - BALL_RADIUS <= paddle1_pos[0] + HALF_PAD_WIDTH and (ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT)):
                
                sound_boop.play(0)

                print ("bastao 1 inicio ", ball_vel)
                ball_vel[0] = -ball_vel[0]
                ball_vel[1] = -ball_vel[1]
                ball_vel[0] = ball_vel[0] + 10 + speed_increase
                ball_vel[1] = ball_vel[1] + 10 + speed_increase
                ball_vel[1] = -ball_vel[1]
                print ("bastao 1 fim ", ball_vel)

        # TODO: bola rebate no bastao 2 (refleccao do bastao 2): 
        # tocar som boop;
        # aumentar velocidade da bolinha em (1 + 10/100) (use a variavel speed_increase)
        # cuidado com a direcao
        elif (ball_pos[0] + BALL_RADIUS >= paddle2_pos[0] - HALF_PAD_WIDTH and (ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT)):
                
                sound_boop.play(0)

                print ("bastao 2 inicio ", ball_vel)

                ball_vel[0] = -ball_vel[0]
                ball_vel[1] = -ball_vel[1]
                ball_vel[0] = ball_vel[0] - 10 - speed_increase
                ball_vel[1] = ball_vel[1] - 10 - speed_increase
                ball_vel[1] = -ball_vel[1]
                print ("bastao 2 fim ", ball_vel)
                
        # TODO: bola acerta a parede (esquerda) do jogador 1 (mas nao no bastao):
        # atualizar score e iniciar bolinha a partir do centro: use funcao ball_init()   
        elif (ball_pos[0] - BALL_RADIUS <= 0):

                sound_gool.play(0)
                score2 = score2 + 1
                ball_init(random.choice([True, False]))

        # TODO: bola acerta a parede (direita) do jogador 2 (mas nao no bastao) 
        # atualizar score e iniciar bolinha a partir do centro: use funcao ball_init() 
        elif (ball_pos[0] + BALL_RADIUS >= W_WIDTH):

                sound_gool.play(0)
                score1 = score1 + 1
                ball_init(random.choice([True, False]))

        # TODO: bola acerta as paredes laterais (rebater):
        # rebater a bolinha: mude a velocidade;
        # tocar som beep
        elif (ball_pos[1] + BALL_RADIUS >= W_HEIGHT or ball_pos[1] - BALL_RADIUS <= 0):
                
                ball_vel[1] = -ball_vel[1]

                sound_beep.play(0)

                
def keydown(key):
        """ verifica qual tecla foi pressionada """
        global paddle1_vel, paddle2_vel, pause, color, marioBoll, luigiBoll
        
        if key == pygame.K_SPACE:
                init()
                start()
        elif key == pygame.K_p:
                marioBoll = False
                luigiBoll = False
                if pause == True:
                        pause = False
                        pause_game()
                else:
                        pause = True
                        pause_game()
        elif key == pygame.K_q:
                if pygame.mixer.music.get_busy() == True:
                        pygame.mixer.music.stop()
                else:
                        pygame.mixer.music.play(-1)
        elif key == pygame.K_1:
                color = BLUE
        elif key == pygame.K_2:
                color = RED
        elif key == pygame.K_3:
                color = GREEN
        elif key == pygame.K_0:
                color = BLACK
        elif not pause:

                if key == pygame.K_UP:
                        paddle2_vel[1] = -10
                elif key == pygame.K_w:
                        paddle1_vel[1] = -10
                elif key == pygame.K_DOWN:
                        paddle2_vel[1] = 10
                elif key == pygame.K_s:
                        paddle1_vel[1] = 10
                
                #MARIO
                if key == pygame.K_m:
                        if marioBoll == False:
                                sound_mario_jump.play(0)
                                marioBoll = True
                elif key == pygame.K_l:
                        if luigiBoll == False:
                                sound_mario_jump.play(0)
                                luigiBoll = True
                #/MARIO


def keyup(key):
        """ verifica qual tecla foi soltada """
        global paddle1_vel, paddle2_vel
        
        if key == pygame.K_UP:
                paddle2_vel[1] = 0
        elif key == pygame.K_w:
                paddle1_vel[1] = 0
        elif key == pygame.K_DOWN:
                paddle2_vel[1] = 0
        elif key == pygame.K_s:
                paddle1_vel[1] = 0


# inicio
if __name__ == '__main__':
        main()
