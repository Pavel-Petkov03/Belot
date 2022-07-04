import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FPS = 30


class Card(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WINDOW_WIDTH / 12, WINDOW_HEIGHT / 8))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.position = "dealer"

    def update(self, *args, **kwargs) -> None:
        pass


class AnnounceRect(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, image, rect_title):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.rect_title = rect_title
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, win):
        win.blit(self.image, self.rect)


def run_game():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    sprites = pygame.sprite.Group()
    sprites.add(Card(50, 60))
    clock = pygame.time.Clock()
    margin = 400
    r = pygame.Rect(margin, margin, WINDOW_WIDTH - margin, WINDOW_HEIGHT - margin)
    r.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                print(r.left, r.top, r.width, r.height, r.x, r.right, r.bottom)
        sprites.update()

        window.fill("black")
        pygame.draw.rect(window, "green", r)
        for x_axis in range(2):
            for y_axis in range(4):
                middle_x = (r.width / 2)
                divided_y_axis = r.height / 16*3
                y_pos = r.top + divided_y_axis * y_axis
                x_pos = r.left + middle_x * x_axis

                rect = AnnounceRect(x_pos, y_pos, middle_x, divided_y_axis, "random.jpg", "")
                rect.draw(window)

        b = AnnounceRect(r.left,  r.top+r.height/4*3, r.width, r.height/4, "random.jpg", "")
        b.draw(window)
        sprites.draw(window)
        pygame.display.flip()


class Player:
    def __init__(self, cards):
        self.cards = cards


class Bot(Player):
    def generate_random_announcements_algorythm(self):
        pass


class Row:
    def __init__(self, players_deque, cards):
        self.players_deque = players_deque  # [, next , next , next, current dealer]
        self.cards = cards
        self.announced_game = None

    def card_dealing_before_announcements(self):
        first_row_dealing = 3
        second_row_dealing = 2
        self.make_dealing_row(first_row_dealing)
        self.make_dealing_row(second_row_dealing)

    def make_announcements(self):
        available_announcements = {
            "Pass": 0,
            "Spades": 1,
            "Diamonds": 2,
            "Hearts": 3,
            "Clubs": 4,
            "No trumps": 5,
            "All trumps": 6,
        }
        current_announcer = self.players_deque[0]
        if not isinstance(current_announcer, Bot):
            self.toggle_modal_for_announcements()
        else:
            current_announcer.generate_random_announcements_algorythm()

    def toggle_modal_for_announcements(self):
        pass

    def card_dealing_after_announcements(self):
        third_row_dealing = 3
        self.make_dealing_row(third_row_dealing)

    def make_dealing_row(self, dealing_row, ):
        for player in self.players_deque:
            self.pop_n_cards_and_give_to_player(dealing_row, player)

    def pop_n_cards_and_give_to_player(self, n, player):
        for pop_card in range(n):
            taken_card = self.cards.pop()
            taken_card.position = "player"
            player.cards.append()

    def taking_hand(self):
        pass

    def run_row(self):
        self.card_dealing_before_announcements()


class Game:
    pass


if __name__ == "__main__":
    run_game()
