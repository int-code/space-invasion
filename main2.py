import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Invasion")
        icon = pygame.image.load('resources/icon.png')
        pygame.display.set_icon(icon)
        self.height = 700
        self.width = 500
        self.surface = pygame.display.set_mode((self.height, self.width))
        self.bg = pygame.image.load('resources/background.png')
        self.bulletlist = []
        self.enemylist = []
        self.rocket = Rocket(self)
        self.font = pygame.font.SysFont('cambria', 32)
        self.font2 = pygame.font.Font('resources/PixelEmulator-xq08.ttf', 20)
        self.running = True
        self.game = False
        self.menu = Menu(self)
        self.btime = pygame.time.get_ticks()
        self.result = False
        self.score = 0
        self.dangerlist = []

    def startgame(self):
        self.bulletlist = []
        self.enemylist = []
        self.dangerlist = []
        self.score = 0
        self.rocket.life = 3
        self.surface.blit(self.bg, (0, 0))
        self.surface.blit(self.rocket.image, (self.rocket.rx, self.rocket.ry))
        startx = 50
        starty = 100
        for i in range(3):
            for j in range(10):
                alien = Enemy(self.surface, startx + 60 * j, starty + 60 * i)
                self.enemylist.append(alien)
                alien.draw()

    def scoreshow(self):
        sctext = self.font2.render("Score: "+str(self.score), True, (255, 255, 255), (0, 0, 0))
        sctextrect = sctext.get_rect()
        sctextrect.center = (self.height//8, 25)
        self.surface.blit(sctext, sctextrect)

    def lifeshow(self):
        lifetext = self.font2.render("Lives: " + str(self.rocket.life), True, (255, 255, 255), (0, 0, 0))
        lifetextrect = lifetext.get_rect()
        lifetextrect.center = (self.height *5// 8, 25)
        self.surface.blit(lifetext, lifetextrect)

    def resultshow(self, s):
        if s == 0:
            t = "DEFEAT"
        else:
            t = "VICTORY"
        vtext = self.font.render(t, True, (255, 255, 255), (0, 0, 0))
        vtextrect = vtext.get_rect()
        vtextrect.center = (self.height // 2, self.width // 2)
        self.surface.blit(vtext, vtextrect)

        sctext = self.font.render("Score: " + str(self.score + self.rocket.life * 50), True, (255, 255, 255), (0, 0, 0))
        sctextrect = sctext.get_rect()
        sctextrect.center = (self.height // 2, self.width // 2 + 50)
        self.surface.blit(sctext, sctextrect)

    def run(self):
        while self.running:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if (not self.game):
                    if self.result:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            self.result = False
                    else:
                        self.menu.show()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mpos = pygame.mouse.get_pos()
                            if self.menu.quittextrect.collidepoint(mpos):
                                self.running = False
                            if self.menu.playtextrect.collidepoint(mpos):
                                self.startgame()
                                self.game = True
            if self.game:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]: self.rocket.move('up')
                if pressed[pygame.K_s]: self.rocket.move('down')
                if pressed[pygame.K_a]: self.rocket.move('left')
                if pressed[pygame.K_d]: self.rocket.move('right')
                if pressed[pygame.K_SPACE]:
                    if pygame.time.get_ticks() - self.btime > 200:
                        t = Bullet(self.rocket.rx + 20, self.rocket.ry)
                        self.bulletlist.append(t)
                        self.btime = pygame.time.get_ticks()

                self.surface.blit(self.bg, (0, 0))
                self.surface.blit(self.rocket.image, (self.rocket.rx, self.rocket.ry))
                if len(self.bulletlist) > 0:
                    for bullet in self.bulletlist:
                       bullet.checkboundary(self)

                if len(self.dangerlist) > 0:
                    for bullet in self.dangerlist:
                        bullet.checkboundary(self)

                for x in self.enemylist:
                    if x.boundary(self):
                        self.resultshow(0)
                        self.result = True
                        self.game = False
                        break
                    elif not x.collision(self.bulletlist, self):
                        x.draw()
                        x.fire(self)
                if len(self.enemylist) == 0:
                    self.resultshow(1)
                    pygame.time.delay(50)
                    self.result = True
                    self.game = False

                self.rocket.checkcollision(self.dangerlist)
                if self.rocket.life == 0:
                    self.resultshow(0)
                    self.result = True
                    self.game = False

                self.scoreshow()
                self.lifeshow()

            pygame.display.flip()


class Menu:
    def __init__(self, game):
        self.quittext = game.font.render("Quit", True, (255, 255, 255), (0, 0, 0))
        self.quittextrect = self.quittext.get_rect()
        self.quittextrect.center = (game.height // 2, game.width // 2 + 100)

        self.playtext = game.font.render("Play", True, (255, 255, 255), (0, 0, 0))
        self.playtextrect = self.playtext.get_rect()
        self.playtextrect.center = (game.height // 2, game.width // 2)

        self.title = pygame.image.load('resources/title1.png')
        self.trect = self.title.get_rect()
        self.trect.center = (game.height // 2, game.width // 4)
        self.game = game

    def show(self):
        self.game.surface.blit(self.game.bg, (0, 0))
        self.game.surface.blit(self.title, self.trect)
        self.game.surface.blit(self.playtext, self.playtextrect)
        self.game.surface.blit(self.quittext, self.quittextrect)


class Rocket:
    def __init__(self,game):
        self.image = pygame.image.load('resources/rocket.png')
        self.rx = game.height // 2
        self.ry = game.width - 60
        self.rv = 5
        self.game = game
        self.life = 3

    def move(self, dir):
        if dir == 'up' and self.ry > 0: self.ry -= self.rv
        elif dir == 'down' and self.ry < self.game.width - 60: self.ry += self.rv
        elif dir == 'left' and self.rx > 0: self.rx -= self.rv
        elif dir == 'right' and self.rx < self.game.height - 50: self.rx += self.rv

    def checkcollision(self, dangerlist):
        for d in dangerlist:
            if d.x>self.rx  and d.x<self.rx+50 and d.y>self.ry and d.y<self.ry+60:
                dangerlist.remove(d)
                self.life-=1

class Danger:
    def __init__(self, x, y):
        self.image = pygame.image.load('resources/danger.png')
        self.x = x
        self.y = y
        self.v = 5

    def checkboundary(self, game):
        if self.y > game.width:
            game.dangerlist.remove(self)
        else:
            game.surface.blit(self.image, (self.x, self.y))
            self.y += self.v


class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load('resources/bullet.png')
        self.x = x
        self.y = y
        self.v = 5

    def checkboundary(self, game):
        if self.y < 0:
            game.bulletlist.remove(self)
        else:
            game.surface.blit(self.image, (self.x, self.y))
            self.y -= self.v



class Enemy:
    def __init__(self, surface, x, y):
        self.image = pygame.image.load('resources/enemy.png')
        self.surface = surface
        self.x = x
        self.y = y
        self.num = random.randint(20,50)
        self.fired = pygame.time.get_ticks() - self.num * 100

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))
        self.y += 0.2

    def fire(self, game):
        if pygame.time.get_ticks() - self.fired > self.num*150:
            t = Danger(self.x + 20, self.y)
            game.dangerlist.append(t)
            self.fired = pygame.time.get_ticks()

    def collision(self, bullet, game):
        for b in bullet:
            if b.x>self.x  and b.x<self.x+60 and b.y>self.y and b.y<self.y+30:
                bullet.remove(b)
                game.enemylist.remove(self)
                game.score += 10
                return True
        return False

    def boundary(self, game):
        if self.y>=game.width-30:
            return True
        return False



game = Game()
game.run()