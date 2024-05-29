from import_from_this import second_main
import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Player and bullet classes
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.height = 50
        self.width = 20
        self.speed = 5
        self.shield_count = 0
        self.fire_power = 1

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(min(self.x, WIDTH - self.width), 0)
        self.y = max(min(self.y, HEIGHT - self.height), 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.shield_count > 0:
            self.draw_shield(screen)

    def draw_shield(self, screen):
        shield_color = (0, 0, 255)
        for i in range(self.shield_count):
            pygame.draw.circle(screen, shield_color, (self.x + self.width // 2, self.y + self.height // 2), self.height // 2 + 10 * (i + 1), 2)

    def hit_by(self, bullet):
        return (
            bullet.x > self.x - bullet.width
            and bullet.x < self.x + self.width
            and bullet.y > self.y - bullet.height
            and bullet.y < self.y + self.height
        )

    def shoot(self):
        bullets = []
        if self.fire_power == 1:
            if self.color == RED:
                bullets.append(Bullet(self.x - 10, self.y + self.height // 2, -2 * self.speed))
            else:
                bullets.append(Bullet(self.x + self.width, self.y + self.height // 2, 2 * self.speed))
        elif self.fire_power == 3:
            if self.color == RED:
                bullets.append(Bullet(self.x - 10, self.y + self.height // 4, -2 * self.speed))
                bullets.append(Bullet(self.x - 10, self.y + self.height * 3 // 4, -2 * self.speed))
                bullets.append(Bullet(self.x - 10, self.y + self.height // 2, -2 * self.speed))
            else:
                bullets.append(Bullet(self.x + self.width, self.y + self.height // 4, 2 * self.speed))
                bullets.append(Bullet(self.x + self.width, self.y + self.height * 3 // 4, 2 * self.speed))
                bullets.append(Bullet(self.x + self.width, self.y + self.height // 2, 2 * self.speed))
        return bullets



class Bullet:
    def __init__(self, x, y, dx):
        self.x = x
        self.y = y
        self.dx = dx
        self.width = 10
        self.height = 5

    def move(self):
        self.x += self.dx

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.x < 0 or self.x > WIDTH

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.width = 15
        self.height = 15

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE if self.power_type == "shield" else GREEN, (self.x, self.y, self.width, self.height))

    def collected_by(self, player):
        return (
            self.x > player.x - self.width
            and self.x < player.x + player.width
            and self.y > player.y - self.height
            and self.y < player.y + player.height
        )


def show_restart_or_exit_message(screen, winner, score1, score2):


    comic_sans_font = pygame.font.Font("C:\Windows\Fonts\comic.ttf", 36)
    restart_text_surface = comic_sans_font.render("Restart", True, WHITE)
    exit_text_surface = comic_sans_font.render("Exit", True, WHITE)
    further_text_surface = comic_sans_font.render("Do you want to take it further?", True, WHITE)

    restart_text_x = WIDTH // 2 - restart_text_surface.get_width() - 20
    exit_text_x = WIDTH // 2 + 20
    further_text_x = WIDTH // 2 - further_text_surface.get_width() // 2
    text_y = HEIGHT // 2 + 50
    further_text_y = HEIGHT // 2 + 100

    selected_option = "restart"
    screen.fill(BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    selected_option = "exit" if selected_option == "restart" else "restart"
                    screen.fill(BLACK)
                    pygame.display.flip()

                if event.key == pygame.K_DOWN:
                    selected_option = "further"
                    screen.fill(BLACK)
                    pygame.display.flip()

                if event.key == pygame.K_UP:
                    selected_option = "restart"
                    screen.fill(BLACK)
                    pygame.display.flip()

                if event.key == pygame.K_RETURN:
                    return selected_option

        show_winner_message_and_scoreboard(screen, winner, score1, score2)

        if selected_option == "restart":
            pygame.draw.rect(screen, BLUE, (restart_text_x - 10, text_y - 10, restart_text_surface.get_width() + 20, restart_text_surface.get_height() + 20))
        elif selected_option == "exit":
            pygame.draw.rect(screen, BLUE, (exit_text_x - 10, text_y - 10, exit_text_surface.get_width() + 20, exit_text_surface.get_height() + 20))
        else:
            pygame.draw.rect(screen, BLUE, (further_text_x - 10, further_text_y - 10, further_text_surface.get_width() + 20, further_text_surface.get_height() + 20))

        screen.blit(restart_text_surface, (restart_text_x, text_y))
        screen.blit(exit_text_surface, (exit_text_x, text_y))
        screen.blit(further_text_surface, (further_text_x, further_text_y))
        pygame.display.flip()






def draw_scoreboard(screen, score1, score2):
    
    # Load Comic Sans MS font
    comic_sans_font = pygame.font.Font("C:\Windows\Fonts\comic.ttf", 36)

    # Create text surfaces
    text_surface1 = comic_sans_font.render(f"Player 1: {score1}", True, RED)
    text_surface2 = comic_sans_font.render(f"Player 2: {score2}", True, GREEN)

    # Calculate positions
    text1_x = WIDTH - text_surface1.get_width() - 10
    text1_y = 10
    text2_x = 10
    text2_y = 10

    # Draw text surfaces
    screen.blit(text_surface1, (text1_x, text1_y))
    screen.blit(text_surface2, (text2_x, text2_y))
    
def show_winner_message(screen, winner, score1, score2):
    # Load emoji-compatible font
    emoji_font = pygame.font.Font("C:\Windows\Fonts\seguiemj.ttf", 36)

    message = f"{'Player 1' if winner == 1 else 'Player 2'} is the Ultimate Space Duel Champion! 🏆"
    text_surface = emoji_font.render(message, True, WHITE)
    text_x = (WIDTH - text_surface.get_width()) // 2
    text_y = (HEIGHT - text_surface.get_height()) // 2

    screen.blit(text_surface, (text_x, text_y))
    pygame.display.flip()
    pygame.time.delay(3000)

    
    
def show_winner_message_and_scoreboard(screen, winner, score1, score2):
    # Load emoji-compatible font
    emoji_font = pygame.font.Font("C:\Windows\Fonts\seguiemj.ttf", 36)

    message = f"{'Player 1' if winner == 1 else 'Player 2'} is the Ultimate Space Duel Champion! 🏆"
    text_surface = emoji_font.render(message, True, WHITE)
    text_x = (WIDTH - text_surface.get_width()) // 2
    text_y = (HEIGHT - text_surface.get_height()) // 2

    screen.blit(text_surface, (text_x, text_y))
    pygame.display.flip()


    #pygame.time.delay(3000)

    player1_total_points = score1
    player2_total_points = score2
    
    
    player1_total_points_all_games = player1_total_points
    player2_total_points_all_games = player2_total_points


    
    # Determine ranking
    ranked_players = sorted([(1, player1_total_points_all_games), (2, player2_total_points_all_games)], key=lambda x: x[1], reverse=True)


    # Display scoreboard
    scoreboard_title = "Scoreboard:"
    scoreboard_title_surface = emoji_font.render(scoreboard_title, True, WHITE)
    title_x = (WIDTH - scoreboard_title_surface.get_width()) // 2

    text_y_above = text_y - 200
    screen.blit(scoreboard_title_surface, (title_x - 100, text_y_above))
    
    # Display ..........
    dots_title = "..............................................."
    dots_title_surface = emoji_font.render(dots_title, True, WHITE)
    title_yy = text_y_above + 10
    screen.blit(dots_title_surface, (title_x - 100, title_yy + 30))



    
    
    for i, (player, points) in enumerate(ranked_players):
        player_label = f"Player {player}: {points} Points"
        if player == 1:
            player_label_surface = emoji_font.render(player_label, True, RED)
        else:
            player_label_surface = emoji_font.render(player_label, True, GREEN) 

        label_y = title_yy + 70 + i * 40

        screen.blit(player_label_surface, (title_x - 100, label_y))

    # Show the messages on the screen
    pygame.display.flip()
    
    
    
    
    
    
    
    

def game_loop(score1, score2):
    clock = pygame.time.Clock()
    player1 = Player(WIDTH - 40, HEIGHT // 2 - 25, RED)
    player2 = Player(20, HEIGHT // 2 - 25, GREEN)
    bullets = []
    winner = None
    shield_count1 = 0
    shield_count2 = 0
    fire_start_time1 = None
    fire_start_time2 = None
    power_up = None
    next_power_up_time = time.time() + 5
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while winner is None:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                  bullets.extend(player1.shoot())
                if event.key == pygame.K_q:
                  bullets.extend(player2.shoot())


        keys = pygame.key.get_pressed()

        # Player 1 controls
        dx1 = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy1 = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # Player 2 controls
        dx2 = keys[pygame.K_d] - keys[pygame.K_a]
        dy2 = keys[pygame.K_s] - keys[pygame.K_w]

        player1.move(dx1, dy1)
        player2.move(dx2, dy2)

        # Update power-ups
        if power_up is None and current_time >= next_power_up_time:
            while True:
                x = random.randint(0, WIDTH - 15)
                y = random.randint(0, HEIGHT - 15)
                if not (player1.hit_by(PowerUp(x, y, "temp")) or player2.hit_by(PowerUp(x, y, "temp"))):
                    break

            power_type = random.choice(["shield", "fire"])
            power_up = PowerUp(x, y, power_type)

        if power_up is not None:
            if power_up.collected_by(player1):
                if power_up.power_type == "shield":
                   player1.shield_count = 3
                elif power_up.power_type == "fire":
                    player1.fire_power = 3
                    fire_start_time1 = current_time
                power_up = None
                next_power_up_time = current_time + random.randint(1, 10)
            elif power_up.collected_by(player2):
                if power_up.power_type == "shield":
                    player2.shield_count = 3
                elif power_up.power_type == "fire":
                    player2.fire_power = 3
                    fire_start_time2 = current_time
                power_up = None
                next_power_up_time = current_time + random.randint(1, 10)

        # Update fire power-up duration
        if fire_start_time1 is not None and current_time - fire_start_time1 >= 10:
            player1.fire_power = 1
            fire_start_time1 = None

        if fire_start_time2 is not None and current_time - fire_start_time2 >= 10:
            player2.fire_power = 1
            fire_start_time2 = None

        # Update bullets
        for bullet in bullets:
            bullet.move()
            if bullet.off_screen():
                bullets.remove(bullet)
            elif player1.hit_by(bullet):
                if player1.shield_count > 0:
                    player1.shield_count -= 1
                else:
                    score2 += 1
                    if score2 == 20:
                        winner = 2
                        break
                bullets.remove(bullet)
            elif player2.hit_by(bullet):
                if player2.shield_count > 0:
                    player2.shield_count -= 1
                else:
                    score1 += 1
                    if score1 == 20:
                        winner = 1
                        break
                bullets.remove(bullet)

        # Draw everything
        screen.fill(BLACK)
        player1.draw(screen)
        player2.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        if power_up is not None:
            power_up.draw(screen)
        draw_scoreboard(screen, score1, score2)
        pygame.display.flip()

        clock.tick(60)

    show_winner_message(screen, winner, score1, score2)
    return score1, score2, winner

def main():
    pygame.display.set_caption("Space Duel")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score1 = 0
    score2 = 0

    while True:
        score1, score2, winner = game_loop(score1, score2)  # Update here to get winner
        user_choice = show_restart_or_exit_message(screen, winner, score1, score2)  # Pass winner here
        if user_choice == "exit":
            pygame.quit()
            sys.exit()
        elif user_choice == "further":
            second_main(score1, score2)
        else:
            score1 = 0
            score2 = 0




if __name__ == "__main__":
    main()