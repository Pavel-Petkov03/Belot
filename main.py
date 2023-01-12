import pygame

from announcements import AnnounceModal
from client_connector import ClientConnector
from sprites.entry_text_box import TextBoxesGroup, SCREENSIZE, AllBoxes, TextBox
from loading_bar import TimeRemainingBar


class Game:
    background_image_location = "cool_belot_background.jpg"

    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = self.get_screen()
        self.current_state = "render_start_dialog"
        self.cards = {}
        self.announcements_done = False

    def gameplay(self, event_list):
        self.render_cards()

    def render_cards(self):
        for sprite in (self.cards.values()):
            sprite.blit(self.screen)

    def dispatch(self, *args, **kwargs):
        func = getattr(self, self.current_state)
        func(*args, **kwargs)

    @staticmethod
    def get_screen():
        return pygame.display.set_mode(SCREENSIZE)

    def blit_background(self):
        image = self.render_image(self.background_image_location)
        image = self.scale_image(image, SCREENSIZE)
        self.screen.blit(image, (0, 0))

    @staticmethod
    def render_image(image_location, ):
        return pygame.image.load(image_location).convert()

    def scale_image(self, image, scale_cord):
        return pygame.transform.scale(image, scale_cord)


class PreloadClientConnector(ClientConnector):
    pass


class PreloadClient(Game, PreloadClientConnector):
    def __init__(self):
        super().__init__()
        self.all_start_boxes = self.load_boxes()

    def render_start_dialog(self, event_list):
        self.all_start_boxes.update(event_list)
        self.all_start_boxes.draw(self.screen)

    def render_waiting_screen(self, event_list):
        reply = self.current_player.net.send({
            "action": "get_players"
        })

        current_players_length = len(reply["data"])
        if current_players_length == 4:
            self.current_state = "render_game"
            return

        text_box = TextBox(100, 100, 200, 200, font="Sans Serif", font_size=50, backcolor="green",
                           text=f"Waiting for other {4 - current_players_length} to join")
        text_box.update(event_list)
        text_box.draw(self.screen)

    def load_boxes(self):
        all_sprites = TextBoxesGroup()
        instance_of_all_boxes = AllBoxes(self)
        all_boxes = instance_of_all_boxes.all_boxes
        all_sprites.add(*all_boxes)
        return all_sprites


class AnnouncementClientConnector(ClientConnector):
    pass


class AnnouncementsClient(Game, AnnouncementClientConnector):
    def __init__(self):
        super().__init__()
        self.announcements_modal = AnnounceModal()
        self.time_remaining_bar = TimeRemainingBar()
        self.pass_list = []
        self.announcements_done = False

    def announcements(self, event_list):
        self.render_cards()
        response = self.current_player.net.send({
            "action": "check_announcements_order"
        })
        on_move = response["data"]
        if on_move:
            self.announcements_modal.toggle_modal(
                self.calculate_available_dict(
                    self.current_player.net.send({
                        "action": "get_announcement"
                    })
                )
            )
            self.current_state = "render_announcements_modal"

    def render_announcements_modal(self, event_list):
        pass_list_len = self.current_player.net.send({
            "action": "get_pass_list_len"
        })
        if pass_list_len == 4:
            self.current_state = "render_game"
            self.announcements_done = True
            return
        self.render_cards()
        self.announcements_modal.draw(self.screen)

        is_clicked = self.announcements_modal.click_event_listener(event_list)
        if is_clicked:
            self.current_player.net.send({
                "action": "set_announcement",
                "params": {
                    "announcement": self.announcements_modal.announced_game
                }
            })
            self.current_state = "render_announcements_modal"
            return

        response = self.current_player.net.send({
            "action": "loading_bar"
        })
        position = response["data"]["position"]
        counter = response["data"]["counter"]
        self.time_remaining_bar.draw(self.screen, counter / 100, position)
        if self.time_remaining_bar.time_is_up(counter / 100):
            self.current_player.net.send({
                "action": "set_announcement",
                "params": {
                    "announcement": self.announcements_modal.announced_game
                }
            })

    def calculate_available_dict(self, top_argument):
        return {}


class DealCardsClientConnector(ClientConnector):
    pass


class DealCardsClient(Game, DealCardsClientConnector):
    def render_game(self, event_list):
        if len(self.cards) == 32:
            self.current_state = "gameplay"
            return
        elif len(self.cards) == 20 and not self.announcements_done:
            self.current_state = "announcements"
            return
        response = self.current_player.net.send({
            "action": "deal_cards",
            "params": {
                "wanted_cards": self.calculate_wanted_cards()
            }
        })
        all_cards = response["data"]
        self.add_cards(all_cards)
        self.current_state = "animation"

    def add_cards(self, all_cards):
        for card in all_cards:
            key = f'suit:{card.suit}rank:{card.rank}'
            if key not in self.cards:
                self.cards[key] = card
            else:
                self.cards[key].rect.center = card.destination_pos

    def calculate_wanted_cards(self):
        if len(self.cards) < 12 or len(self.cards) >= 20:
            return 3
        return 2

    def animation(self, event_list):
        for card in self.cards.values():
            if not card.given:
                if card.rect is None:
                    card.load_image()
                card.calculate_destination_of_movement()
                if card.on_wanted_position():
                    card.given = True
                    self.current_state = "render_game"
            card.blit(self.screen)


class BoardClientConnector(ClientConnector):
    pass


class BoardClient(Game, BoardClientConnector):
    pass


class MainClient(PreloadClient, AnnouncementsClient, DealCardsClient):
    def run(self):

        running = True

        while running:
            self.blit_background()
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False

            self.dispatch(event_list)
            pygame.display.flip()


game = MainClient()
game.run()
