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

    def set_current_state(self, new_state):
        self.current_state = new_state

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
    def socket_get_players(self):
        return self.send("get_players")


class PreloadClient(Game, PreloadClientConnector):
    MAX_PLAYERS = 4

    def __init__(self):
        super().__init__()
        self.all_start_boxes = self.load_boxes()

    def render_start_dialog(self, event_list):
        self.all_start_boxes.update(event_list)
        self.all_start_boxes.draw(self.screen)

    def render_waiting_screen(self, event_list):
        reply = self.socket_get_players()

        current_players_length = len(reply["data"])
        if current_players_length == self.MAX_PLAYERS:
            self.set_current_state("render_game")
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
    def socket_check_announcements_order(self):
        return self.send("check_announcements_order")

    def socket_get_announcement(self):
        return self.send("get_announcement")

    def socket_get_pass_list_len(self):
        return self.send("get_pass_counter")

    def socket_set_announcement(self, announcement):
        return self.send("set_announcement", params={"announced_game": announcement})

    def socket_get_loading_bar_info(self):
        return self.send("get_loading_bar_info")


class AnnouncementsClient(Game, AnnouncementClientConnector):
    def __init__(self):
        super().__init__()
        self.announcements_modal = AnnounceModal()
        self.time_remaining_bar = TimeRemainingBar()
        self.announcements_done = False

    def announcements(self, event_list):
        pass_list_len = self.socket_get_pass_list_len()["data"]
        if pass_list_len == 4:
            self.set_current_state("render_game")
            self.announcements_done = True
            return
        self.render_cards()
        response = self.socket_check_announcements_order()
        on_move = response["data"]

        if on_move:
            self.announcements_modal.load(
                self.calculate_available_dict(
                    self.socket_get_announcement()
                )
            )
            self.set_current_state("render_announcements_modal")
        self.load_time_remaining_bar()

    def render_announcements_modal(self, event_list):
        self.render_cards()
        self.announcements_modal.draw(self.screen)

        is_clicked = self.announcements_modal.click_event_listener(event_list)
        if is_clicked:

            self.socket_set_announcement(self.announcements_modal.announced_game)
            self.set_current_state("announcements")
            return
        self.load_time_remaining_bar()

    def load_time_remaining_bar(self):
        response = self.socket_get_loading_bar_info()
        position = response["data"]["position"]
        counter = response["data"]["counter"]
        self.time_remaining_bar.draw(self.screen, counter / 100, position)
        if self.time_remaining_bar.time_is_up(counter / 100):
            self.socket_set_announcement("Pass")

    def calculate_available_dict(self, top_argument):
        available_array = []
        return {}


class DealCardsClientConnector(ClientConnector):
    def socket_deal_cards(self, wanted_cards):
        return self.send("deal_cards", params={"wanted_cards": wanted_cards})


class DealCardsClient(Game, DealCardsClientConnector):
    FIRST_ROW_CARDS_MAX_LEN = 20
    SECOND_ROW_CARDS_MAX_LEN = 32

    def render_game(self, event_list):
        if len(self.cards) == self.SECOND_ROW_CARDS_MAX_LEN:
            self.set_current_state("gameplay")
            return
        elif len(self.cards) == self.FIRST_ROW_CARDS_MAX_LEN and not self.announcements_done:
            self.set_current_state("announcements")
            return
        response = self.socket_deal_cards(self.calculate_wanted_cards())
        all_cards = response["data"]
        self.add_cards(all_cards)
        self.set_current_state("animation")

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
                    self.set_current_state("render_game")
            card.blit(self.screen)


class BoardClientConnector(ClientConnector):
    pass


class BoardClient(Game, BoardClientConnector):
    def gameplay(self, event_list):
        self.render_cards()


class MainClient(PreloadClient, AnnouncementsClient, DealCardsClient, BoardClient):
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
