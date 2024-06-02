import pygame
import sys

pygame.init()
window_width = 800
window_height = 400

window_size = (window_width, window_height)
white = (255, 255, 255)
black = (0, 0, 0)

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 10

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < window_height:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect)

class Ball:
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.speed_x = 5
        self.speed_y = 5
        self.radius = radius

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= window_height:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, white, self.rect)

    def auto_move(self):
        self.move()

class ComputerPaddle(Paddle):
    def __init__(self, x, y, width, height, ball):
        super().__init__(x, y, width, height)
        self.ball = ball

    def move(self):
        if self.ball.rect.y < self.rect.y + self.rect.height / 2:
            self.rect.y -= self.speed
        elif self.ball.rect.y > self.rect.y + self.rect.height / 2:
            self.rect.y += self.speed

font = pygame.font.Font(None, 74)

def main():
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    left_paddle = Paddle(30, (window_height - 100) // 2, 20, 100)
    ball = Ball(window_width // 2, window_height // 2, 15)

    score_left = 0
    score_right = 0

    mode_selected = False

    while not mode_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 320 <= mouse_pos[0] <= 320 + font.size("1 vs 1")[0] and 150 <= mouse_pos[1] <= 150 + font.size("1 vs 1")[1]:
                    right_paddle = Paddle(window_width - 50, (window_height - 100) // 2, 20, 100)  # Výběr režimu "1 vs 1"
                    mode_selected = True
                elif 320 <= mouse_pos[0] <= 320 + font.size("1 vs Pc")[0] and 250 <= mouse_pos[1] <= 250 + font.size("1 vs Pc")[1]:
                    right_paddle = ComputerPaddle(window_width - 50, (window_height - 100) // 2, 20, 100, ball)  # Výběr režimu "1 vs PC"
                    mode_selected = True

        screen.fill(black)
        text_mode = font.render("Chose mode", True, white)
        text_up = font.render("1 vs 1", True, white)
        text_down = font.render("1 vs Pc", True, white)
        screen.blit(text_mode, (230, 25))
        screen.blit(text_up, (320, 150))
        screen.blit(text_down, (320, 250))
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move_up()
        if keys[pygame.K_s]:
            left_paddle.move_down()

        ball.auto_move()

        if 'right_paddle' in locals():  
            if keys[pygame.K_UP]:
                right_paddle.move_up()
            if keys[pygame.K_DOWN]:
                right_paddle.move_down()
            if isinstance(right_paddle, ComputerPaddle):
                right_paddle.move()  # Pokud je druhý hráč počítač, posunujte ho automaticky

        if ball.rect.colliderect(left_paddle.rect) or ('right_paddle' in locals() and ball.rect.colliderect(right_paddle.rect)):
            ball.speed_x = -ball.speed_x

        if ball.rect.left <= 0:
            score_right += 1
            ball.rect.x = window_width // 2 - ball.radius
            ball.rect.y = window_height // 2 - ball.radius
            ball.speed_x = -ball.speed_x

        if ball.rect.right >= window_width:
            score_left += 1
            ball.rect.x = window_width // 2 - ball.radius
            ball.rect.y = window_height // 2 - ball.radius
            ball.speed_x = -ball.speed_x

        screen.fill(black)
        left_paddle.draw(screen)
        if 'right_paddle' in locals():
            right_paddle.draw(screen)
        ball.draw(screen)

        text_left = font.render(str(score_left), True, white)
        text_right = font.render(str(score_right), True, white)
        screen.blit(text_left, (250, 10))
        screen.blit(text_right, (510, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
