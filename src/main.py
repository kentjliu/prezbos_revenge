import pygame
import sys
import math
import random

# initialize font
pygame.font.init()

# load audio files
pygame.mixer.init(size=-16, channels=2)  # initialize sound mixer
pygame.mixer.set_num_channels(16)
jump = pygame.mixer.Sound('jump.ogg')
throw = pygame.mixer.Sound('throw.ogg')
studentsound = pygame.mixer.Sound('student.mp3')
pygame.mixer.Sound.set_volume(jump, .2)
pygame.mixer.Sound.set_volume(throw, .1)
pygame.mixer.Sound.set_volume(studentsound, .2)
pygame.mixer.music.load('music.mp3')

clock = pygame.time.Clock()

# screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png').convert_alpha()


class Player:
    def __init__(self):
        self.playerimg = pygame.image.load("prezbo.png").convert_alpha()
        self.playerimg = pygame.transform.scale(self.playerimg, (150, 150))
        self.player_x = 50
        self.player_y = 400
        self.player_velocity = 3
        self.is_jump = False
        self.jump_count = 10
        self.score = 0

    def move_player_in_screen(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.player_x < 720:
            self.player_x += 3
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= 3
        if keys[pygame.K_DOWN] and self.player_y < 500:
            self.player_y += 3
        if keys[pygame.K_UP] and self.player_y > 0:
            self.player_y -= 3


class Student:
    def __init__(self):
        self.studentimg = []
        self.student_pos_x = []
        self.student_pos_y = []
        self.num_of_students = 3
        self.student_pos = 450
        self.student_velocity = 1
        self.score = 0
        self.gameover = False

    def generate_students(self, player):  # Pass in player so when student hit, player score increases by 1
        for i in range(self.num_of_students):
            self.studentimg.append(pygame.image.load("studentpic.png").convert_alpha())
            self.student_pos_x.append(random.randint(750, 900))
            self.student_pos_y.append(self.student_pos)
            self.student_pos -= 90

        for i in range(student.num_of_students):
            student.student_pos_x[i] -= student.student_velocity
            screen.blit(student.studentimg[i], (student.student_pos_x[i], student.student_pos_y[i]))

        for i in range(student.num_of_students):
            # 2D distance formula --> square root ( (x2-x1)**2 + (y2-y1)**2 )
            distance = math.sqrt((student.student_pos_x[i] - machine.washing_machine_x) ** 2 +
                                 (student.student_pos_y[i] - machine.washing_machine_y) ** 2)
            player_distance = math.sqrt((student.student_pos_x[i] - player.player_x) ** 2 +
                                        (student.student_pos_y[i] - player.player_y) ** 2)

            # if player's position and washing machine position is lesser than 55
            if player_distance < 55:
                self.gameover = True

            # if machine throw is True than kill students
            if machine.throw is True:
                if distance < 40:
                    student.student_pos_y[i] = -500
                    screen.blit(student.studentimg[i], (student.student_pos_x[i], student.student_pos_y[i]))
                    self.score += 1
                    player.score += 1  # Increase player score by 1
                    studentsound.play()

    # if score hits 3 regenerate students at random position between 750-900
    def regenerate_students(self):
        if student.score // 3 == 1:
            self.score = 0
            self.student_velocity += 0.4
            self.studentimg = []
            self.student_pos_x = []
            self.student_pos_y = []
            self.student_pos = 450
            for i in range(self.num_of_students):
                self.studentimg.append(pygame.image.load("studentpic.png").convert_alpha())
                self.student_pos_x.append(random.randint(750, 900))
                self.student_pos_y.append(self.student_pos)
                self.student_pos -= 90

    # if student's position is lesser than 20
    def student_wins(self):
        for i in range(self.num_of_students):
            if self.student_pos_x[i] < 20:
                self.gameover = True


player = Player()
student = Student()


class Machine:
    def __init__(self):
        self.washing_machine = pygame.image.load("machine.png").convert_alpha()
        self.washing_machine_x = player.player_x + 40
        self.washing_machine_y = player.player_y + 50
        self.throw = False

    # throw machine
    def throw_machine(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.throw = True
            throw.play()

        # if machine is not thrown stick with the player
        if not self.throw:
            self.washing_machine_x = player.player_x + 40
            self.washing_machine_y = player.player_y + 50

        # if machine is thrown move the machine on x axis
        else:
            self.washing_machine_x += 20
            if self.washing_machine_x > 850:
                self.washing_machine_x = player.player_x + 40
                self.washing_machine_y = player.player_y + 50
                self.throw = False


# Death Screen
def death_screen(player):  # Pass in player object for access to final score

    # Death screen music start
    pygame.mixer.music.load('deathsong.mp3')  # Load in death screen song
    pygame.mixer.music.play(-1)  # Start playing theme song
    pygame.mixer.music.set_volume(.2)

    # Fonts initialized
    death_font = pygame.font.SysFont('comicsans', 30)
    death_option_font = pygame.font.SysFont('comicsans', 30)
    death_label = death_font.render('The SWC Won :( You must now sign the contract', True, (255, 0, 0))
    death_option = death_option_font.render('Press Space To Quit', True, (0, 0, 0))
    score_label = death_option_font.render(f'Final Score: {player.score}', True, (0, 0, 0))

    # Death Screen Loop
    running = True
    while running:
        clock.tick(80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        # Draw all text and background to screen
        screen.blit(background, (0, 0))
        screen.blit(death_label, (65, 200))
        screen.blit(death_option, (175, 350))
        screen.blit(score_label, (225, 75))
        pygame.display.update()


# Start Menu Loop
def start_menu():
    pygame.mixer.music.play(-1)  # Start playing theme song
    pygame.mixer.music.set_volume(.2)
    running = True
    title_font = pygame.font.SysFont('comicsans', 50)  # Create font object
    while running:
        screen.blit(background, (0, 0))  # Draw Background To Screen
        menu_label = title_font.render('Press Return To Begin...', True, (10, 10, 10))  # Create Text Label
        screen.blit(menu_label, (150, 150))  # Draw Label To Screen
        title_label = title_font.render("Prezbo's Union Buster", True, (10, 10, 10))
        screen.blit(title_label, (150, 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # If return is pressed, start game
                    main_loop()  # Starts main_loop
                    pygame.mixer.music.stop()
                    death_screen(player)
                    running = False  # After main_loop (player loses), the game quits


machine = Machine()


def main_loop():
    # Main game loop
    while not student.gameover:
        # Fps
        clock.tick(80)

        # Creating score tracker
        score_font = pygame.font.SysFont('comicsans', 50)
        score_tracker = score_font.render(f'Score: {player.score}', True, (255, 255, 255))

        # Handling Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # screen blits
        screen.blit(background, (0, 0))
        screen.blit(machine.washing_machine, (machine.washing_machine_x, machine.washing_machine_y))
        screen.blit(player.playerimg, (player.player_x, player.player_y))
        screen.blit(score_tracker, (15, 20))  # Draw score tracker to screen

        # Class functions
        player.move_player_in_screen()
        student.generate_students(player)
        machine.throw_machine()
        student.regenerate_students()
        student.student_wins()

        # refresh window
        pygame.display.update()


start_menu()  # Game starts from start menu, and the main_loop runs from within the start menu
