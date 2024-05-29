import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 1200
HEIGHT = 1200

# Constants
PLAYER_SPEED = 5 

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
LIGHT_GREY = (192, 192, 192)



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
        self.lives = 5
        self.score = 0

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

    def hit_by(self, meteor):  # Update the parameter name
        return (
            meteor.x < self.x + self.width and
            meteor.x + meteor.size > self.x and
            meteor.y < self.y + self.height and
            meteor.y + meteor.size > self.y
        )
        
    def hit_powerup(self, powerup): 
        return (
            powerup.x < self.x + self.width and
            powerup.x + powerup.width > self.x and
            powerup.y < self.y + self.height and
            powerup.y + powerup.height > self.y
        )    
        
        

    def shoot(self):
        bullets = []
        if self.fire_power == 1:
            if self.color == RED:
                #bullets.append(Bullet(self.x - 10, self.y + self.height // 2, -2 * self.speed))
                bullets.append(Bullet(self.x + self.width  // 2 - 2, self.y - 10, -2 * self.speed, self))
            else:
                bullets.append(Bullet(self.x + self.width  // 2 - 2, self.y - 10, -2 * self.speed, self))
        elif self.fire_power == 3:
            if self.color == RED:
                #bullets.append(Bullet(self.x - 10, self.y + self.height // 4, -2 * self.speed))
                bullets.append(Bullet(self.x + self.width // 2 - 15, self.y - 10, -2 * self.speed, self))
                bullets.append(Bullet(self.x + self.width // 2, self.y - 10, -2 * self.speed, self))
                bullets.append(Bullet(self.x + self.width // 2 + 15, self.y - 10, -2 * self.speed, self))
            else:
                bullets.append(Bullet(self.x + self.width // 2 - 15, self.y - 10, - 2 * self.speed, self))
                bullets.append(Bullet(self.x + self.width // 2, self.y - 10, - 2 * self.speed, self))
                bullets.append(Bullet(self.x + self.width // 2 + 15, self.y - 10, -2 * self.speed, self))
        return bullets


class Bullet:
    def __init__(self, x, y, dy, shooter):
        self.x = x
        self.y = y
        self.dy = dy
        self.width = 5
        self.height = 10
        self.shooter = shooter

    def move(self):
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.x < 0 or self.x > WIDTH


# Meteor, Explosion, AlienBoss and Alien_Bullet classes
class Meteor:
    def __init__(self, image):
        self.image = image
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = 0
        self.dy = random.uniform(0.5, 3) * PLAYER_SPEED
        self.size = random.randint(50, 200)
        self.scaled_image = pygame.transform.scale(self.image, (self.size, self.size))

    def move(self):
        self.y += self.dy

    def draw(self, screen):
        screen.blit(self.scaled_image, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT


# When a meteor is hit, the explosion class is called
class Explosion:
    def __init__(self, x, y, size, images):
        self.x = x
        self.y = y
        self.size = size
        self.images = [pygame.transform.scale(img, (size, size)) for img in images]  # Scale images
        self.image_index = 0
        self.last_image_time = time.time()

    def draw(self, screen):
        if self.image_index < len(self.images):
            image = self.images[self.image_index]
            rect = image.get_rect()
            rect.center = (self.x, self.y)
            screen.blit(image, rect)
        return self.image_index < len(self.images)

    def update(self):
        current_time = time.time()
        if current_time - self.last_image_time >= 0.1:
            self.image_index += 1
            self.last_image_time = current_time




class AlienBoss:
    def __init__(self, image):
        self.x = WIDTH // 2
        self.y = 50
        self.dx = random.uniform(-0.5, 0.5) * PLAYER_SPEED
        self.width = 400
        self.height = 300
        self.shoot_interval = 1.5  # Seconds between each shot
        self.last_shoot_time = time.time()
        self.image = image
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        self.next_direction_change = time.time() + random.uniform(1, 3)
        self.lives = 100

    def move(self):
        self.x += self.dx
        if self.x < 0 or self.x + self.width > WIDTH:
            self.dx = -self.dx

    def draw(self, screen):
        screen.blit(self.scaled_image, (self.x, self.y))

    def shoot(self, alien_bullet_image):
        current_time = time.time()
        if current_time - self.last_shoot_time >= self.shoot_interval:
            self.last_shoot_time = current_time
            return [Alien_bullet(self.x + self.width // 2 - 30, self.y + self.height, 0, 2 * PLAYER_SPEED, alien_bullet_image)]
        return []

    def hit_by(self, bullet):
        return (bullet.x >= self.x and bullet.x <= self.x + self.width) and \
               (bullet.y >= self.y and bullet.y <= self.y + self.height)

    def random_direction_and_speed(self):
        self.dx = random.uniform(-0.5, 0.5) * PLAYER_SPEED
        
        
    def lose_life(self):
        self.lives -= 1    

               
class Alien_bullet:
    def __init__(self, x, y, dx, dy, image_alienbullet):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image_alienbullet = image_alienbullet
        self.size = 50
        self.scaled_image_alienbullet = pygame.transform.scale(self.image_alienbullet, (self.size, self.size))



    def reset(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = 0
        self.dy = 2 * PLAYER_SPEED
        self.size = random.randint(50, 200)
        self.scaled_image_alienbullet = pygame.transform.scale(self.image_alienbullet, (self.size, self.size))

    def move(self):
        self.y += self.dy

    def draw(self, screen):
        screen.blit(self.scaled_image_alienbullet, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT 



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


def draw_alien_boss_health_bar(screen, alien_boss):
    bar_width = 200
    bar_height = 20
    border_thickness = 2
    health_percentage = alien_boss.lives / 100

    # Draw health bar border
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - bar_width // 2 - border_thickness, 20 - border_thickness, bar_width + 2 * border_thickness, bar_height + 2 * border_thickness))

    # Draw health bar
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2 - bar_width // 2, 20, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (WIDTH // 2 - bar_width // 2, 20, bar_width * health_percentage, bar_height))
    
    

def show_restart_or_exit_message(screen, player1, player2, winner):
    pygame.time.delay(100)

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

        show_small_winner_message(screen, player1, player2, winner)

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
        
        
def show_small_winner_message(screen, player1, player2, winner):
    # Load emoji-compatible font
    emoji_font = pygame.font.Font("C:\Windows\Fonts\seguiemj.ttf", 36)
    comic_sans_font = pygame.font.Font("C:\Windows\Fonts\comic.ttf", 24)

    player1_total_points = player1.lives * 10 + player1.score
    player2_total_points = player2.lives * 10 + player2.score


    # Displaying player scores
    player1_message = [f"Player 1, you have {player1.lives} lives left,"
                       ,f" and successfully hit {player1.score} objects,",
                       f"{player1.lives}x10❤️ + {player1.score}🎯 = {player1_total_points} Points"]
    player2_message = [f"Player 2, you have {player2.lives} lives left, ",
                       f"and successfully hit {player2.score} objects:",
                       f"{player2.lives}x10❤️ + {player2.score}🎯 = {player2_total_points} Points"]
    
    player1_text_x = WIDTH // 2
    player2_text_x = 20
    text_y = HEIGHT // 2 - 300


    for i in range(3):
        player1_text_surface = emoji_font.render(player1_message[i], True, RED)
        player2_text_surface = emoji_font.render(player2_message[i], True, GREEN)
        screen.blit(player1_text_surface, (player1_text_x, text_y + i * 30))
        screen.blit(player2_text_surface, (player2_text_x, text_y + i * 30))


    if winner == 0:
        if player1_total_points > player2_total_points:
            winner_text_surface = emoji_font.render("Players 1 is the Ultimate Space Force Ranger!🏆", True, WHITE)
        elif player1_total_points < player2_total_points:
            winner_text_surface = emoji_font.render("Players 2 is the Ultimate Space Force Ranger!🏆", True, WHITE)
        else:
            winner_text_surface = emoji_font.render("Both players are Ultimate Space Force Rangers!🏆", True, WHITE)  
    else:
        winner_text_surface = emoji_font.render(f"Player {winner} is the Ultimate Space Force Ranger!🏆", True, WHITE)

    text_x = WIDTH // 2 - winner_text_surface.get_width() // 2
    text_y = HEIGHT // 2 - winner_text_surface.get_height() // 2 - 50 - 300

    screen.blit(winner_text_surface, (text_x, text_y))


def show_winner_message(screen, player1, player2, winner):
    # Load emoji-compatible font
    emoji_font = pygame.font.Font("C:\Windows\Fonts\seguiemj.ttf", 36)
    comic_sans_font = pygame.font.Font("C:\Windows\Fonts\comic.ttf", 24)

    player1_total_points = player1.lives * 10 + player1.score
    player2_total_points = player2.lives * 10 + player2.score

    screen.fill(BLACK)

    # Displaying the first message
    first_message = "You have defeated Eldho The Evil, Congratulations!"
    first_text_surface = comic_sans_font.render(first_message, True, WHITE)
    first_text_x = (WIDTH - first_text_surface.get_width()) // 2
    first_text_y = HEIGHT // 2 - 100
    screen.blit(first_text_surface, (first_text_x, first_text_y))
    pygame.display.flip()
    pygame.time.delay(5000)

    # Displaying the second message
    second_message = "The galaxy is now a safer place thanks to your excellent team work!"
    second_text_surface = comic_sans_font.render(second_message, True, WHITE)
    second_text_x = (WIDTH - second_text_surface.get_width()) // 2
    second_text_y = HEIGHT // 2 - 60
    screen.fill(BLACK)
    screen.blit(second_text_surface, (second_text_x, second_text_y))
    pygame.display.flip()
    pygame.time.delay(3000)


    # Displaying player scores
    player1_message = [f"Player 1, you have {player1.lives} lives left,"
                       ,f" and successfully hit {player1.score} objects,",
                       f"{player1.lives}x10❤️ + {player1.score}🎯 = {player1_total_points} Points"]
    player2_message = [f"Player 2, you have {player2.lives} lives left, ",
                       f"and successfully hit {player2.score} objects:",
                       f"{player2.lives}x10❤️ + {player2.score}🎯 = {player2_total_points} Points"]
    
    player1_text_x = WIDTH // 2
    player2_text_x = 20
    text_y = HEIGHT // 2 - 300

    screen.fill(BLACK)

    for i in range(3):
        player1_text_surface = emoji_font.render(player1_message[i], True, RED)
        player2_text_surface = emoji_font.render(player2_message[i], True, GREEN)
        screen.blit(player1_text_surface, (player1_text_x, text_y + i * 30))
        screen.blit(player2_text_surface, (player2_text_x, text_y + i * 30))

    #pygame.display.flip()

    if winner == 0:
        if player1_total_points > player2_total_points:
            winner_text_surface = emoji_font.render("Players 1 is the Ultimate Space Force Ranger!🏆", True, WHITE)
        elif player1_total_points < player2_total_points:
            winner_text_surface = emoji_font.render("Players 2 is the Ultimate Space Force Ranger!🏆", True, WHITE)
        else:
            winner_text_surface = emoji_font.render("Both players are Ultimate Space Force Rangers!🏆", True, WHITE)  
    else:
        winner_text_surface = emoji_font.render(f"Player {winner} is the Ultimate Space Force Ranger!🏆", True, WHITE)
        

    text_x = WIDTH // 2 - winner_text_surface.get_width() // 2
    text_y = HEIGHT // 2 - winner_text_surface.get_height() // 2 - 50 - 300

    screen.blit(winner_text_surface, (text_x, text_y))
    pygame.time.delay(5000)
    pygame.display.flip()




def draw_scoreboard(screen, player1, player2):
    # Load Comic Sans MS font
    comic_sans_font = pygame.font.Font("C:\Windows\Fonts\seguiemj.ttf", 36)

    # Create text surfaces
    text_surface1 = comic_sans_font.render(f"Player 1 ❤️: {player1.lives} 🎯: {player1.score}", True, RED)
    text_surface2 = comic_sans_font.render(f"Player 2 ❤️: {player2.lives} 🎯: {player2.score}", True, GREEN)

    # Calculate positions
    text1_x = WIDTH - text_surface1.get_width() - 10
    text1_y = 10
    text2_x = 10
    text2_y = 10

    # Draw text surfaces
    screen.blit(text_surface1, (text1_x, text1_y))
    screen.blit(text_surface2, (text2_x, text2_y))
    




def show_message(screen, message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)
    
    
def game_loop(lives1, lives2):
    
    
    
    
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
    meteors = []
    explosions = []
    next_meteor_time = time.time() + 1
    
    meteor_images = []
    meteor_filenames = [
        "Meteor_Comets/Meteor1.jpg", "Meteor_Comets/Meteor2.jpg", "Meteor_Comets/Meteor3.jpg",
        "Meteor_Comets/Meteor4.jpg", "Meteor_Comets/Meteor5.jpg", "Meteor_Comets/Meteor6.jpg",
        "Meteor_Comets/Meteor7.jpg", "Meteor_Comets/Meteor8.jpg", "Meteor_Comets/Meteor9.jpg",
        "Meteor_Comets/Meteor10.jpg"
    ]

    BLACK = (0, 0, 0)
    for filename in meteor_filenames:
        image = pygame.image.load(filename).convert()
        image.set_colorkey(BLACK)
        meteor_images.append(image)
        
    # Add explosion images
    explosion_images = []
    explosion_filenames = [
        "Explosion/Explosion1.jpg",
        "Explosion/Explosion2.jpg",
        "Explosion/Explosion3.jpg",
        "Explosion/Explosion4.jpg",
        "Explosion/Explosion5.jpg",
        "Explosion/Explosion6.jpg",
        "Explosion/Explosion7.jpg",
        "Explosion/Explosion8.jpg",
        "Explosion/Explosion9.jpg",
        "Explosion/Explosion10.jpg",
    ]

    explosion_images = []
    for filename in explosion_filenames:
        image = pygame.image.load(filename).convert()
        image.set_colorkey(BLACK)
    explosion_images.append(image)


    
    # Load alien boss and alien bullet image and remove black background
    alien_bullet_image = pygame.image.load("Alien/Alien_Fire.jpg").convert()
    alien_boss_image = pygame.image.load("Alien/Alien_boss.jpg").convert()
    alien_bullet_image.set_colorkey(BLACK)
    alien_boss_image.set_colorkey(BLACK)
    
    #alien_boss = AlienBoss(alien_boss_image)
    alien_bullets = []
    
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    game_start_time = time.time()


    last_message_time = game_start_time
    show_message_time = game_start_time - 11
    
    messages = [
        "Seems like its getting worse comrad!",
        "The worst is yet to come",
        "I've seen smaller swarms",
        "Looks like the final swarm, or? Shit..",
        "More ahead, keep focused!",
     ]
    
    
    alien_boss = None
    boss_spawn_time = 10
    
    
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
                if not (player1.hit_powerup(PowerUp(x, y, "temp")) or player2.hit_powerup(PowerUp(x, y, "temp"))):
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
        bullets = [bullet for bullet in bullets if not bullet.off_screen()]

        for bullet in bullets:
            bullet.move()
            if bullet.off_screen():
                bullets.remove(bullet)
                
            if alien_boss is not None:
                if alien_boss.hit_by(bullet):
                    explosions.append(Explosion(bullet.x, bullet.y, 60, explosion_images)) # Add explosion when alien boss is hit
                    bullets.remove(bullet)
                    alien_boss.lose_life()
                    bullet.shooter.score += 1
                    if alien_boss.lives <= 0:
                        winner = 0  # 0 means both players won by defeating the alien boss
                    break
                
                
                
        # Add meteor logic
        elapsed_time = current_time - game_start_time
        meteors_to_spawn = int(elapsed_time // 10) + 1

        if current_time >= next_meteor_time:
            for _ in range(meteors_to_spawn):
                meteor_image = random.choice(meteor_images)
                meteors.append(Meteor(meteor_image))
            next_meteor_time = current_time + random.uniform(1, 3)
            
            
        meteor_hit = None
        for meteor in meteors:
            meteor.move()
            if meteor.off_screen():
                meteors.remove(meteor)
            else:
                for bullet in bullets:
                    dist = ((bullet.x - meteor.x)**2 + (bullet.y - meteor.y)**2)**0.5
                    if dist <= meteor.size:
                        meteors.remove(meteor)
                        bullets.remove(bullet)
                        bullet.shooter.score += 1
                        meteor_hit = meteor
                        break
                else:
                    if player1.hit_by(meteor):  
                        if player1.shield_count > 0:
                            meteors.remove(meteor)
                            player1.shield_count -= 1
                        else:
                            player1.lives -= 1
                            meteors.remove(meteor)
                            if player1.lives == 0:
                                winner = 2
                            break

                    if player2.hit_by(meteor):  
                        if player2.shield_count > 0:
                            meteors.remove(meteor)
                            player2.shield_count -= 1
                        else:
                            player2.lives -= 1
                            meteors.remove(meteor)
                            if player2.lives == 0:
                                winner = 1
                            break
                if meteor_hit is not None:
                    explosions.append(Explosion(meteor_hit.x, meteor_hit.y, meteor_hit.size, explosion_images))
                    meteor_hit = None

                        
        
        # Add Alien Boss logic       
        if alien_boss is None and time.time() - game_start_time >= boss_spawn_time:
            alien_boss = AlienBoss(alien_boss_image)


        if alien_boss:
            alien_boss.move()
            alien_boss.draw(screen)
            
            if current_time >= alien_boss.next_direction_change:
                alien_boss.random_direction_and_speed()
                alien_boss.next_direction_change = current_time + random.uniform(1, 3)

            alien_bullets += alien_boss.shoot(alien_bullet_image)
            for bullet in alien_bullets:
                bullet.move()
                bullet.draw(screen)

                if bullet.off_screen():
                    alien_bullets.remove(bullet)

                if player1.hit_by(bullet):
                    if player1.shield_count > 0:
                        player1.shield_count -= 1
                    else:
                        player1.lives -= 1
                        if player1.lives == 0:
                            winner = 2
                    alien_bullets.remove(bullet)

                if player2.hit_by(bullet):
                    if player2.shield_count > 0:
                        player2.shield_count -= 1
                    else:
                        player2.lives -= 1
                        if player2.lives == 0:
                            winner = 1
                    alien_bullets.remove(bullet)
                
                
        # Display message every 10 seconds
        if current_time - last_message_time >= 10:
            last_message_time = current_time
            message = random.choice(messages)
            show_message_time = current_time + 1

        # Draw everything
        screen.fill(BLACK)
        
        
        explosions = [explosion for explosion in explosions if explosion.draw(screen)]
        for explosion in explosions:
            explosion.update()
        
        player1.draw(screen)
        player2.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        if power_up is not None:
            power_up.draw(screen)
            
        draw_scoreboard(screen, player1, player2)
        if alien_boss is not None:
            draw_alien_boss_health_bar(screen, alien_boss)
        
        for meteor in meteors:
            meteor.draw(screen)
            
        # Draw and move alien bullets
        for alien_bullet in alien_bullets:
            alien_bullet.move()
            alien_bullet.draw(screen)    
            
        if alien_boss:
            alien_boss.draw(screen)    
            
            
        if current_time <= show_message_time:
           show_message(screen, message)
        
        pygame.display.flip()

        clock.tick(60)

    show_winner_message(screen, player1, player2, winner)
    return player1, player2, player1.lives, player2.lives, winner

def main():
    pygame.display.set_caption("Space Duel")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    lives1 = 5
    lives2 = 5

    while True:
        player1, player2, lives1, lives2, winner = game_loop(lives1, lives2)  # Update here to get winner
        user_choice = show_restart_or_exit_message(screen, player1, player2, winner)  # Pass winner here
        if user_choice == "exit":
            pygame.quit()
            sys.exit()
        #elif user_choice == "further":
        #    second_game_main()
        else:
            lives1 = 5
            lives2 = 5




if __name__ == "__main__":
    main()