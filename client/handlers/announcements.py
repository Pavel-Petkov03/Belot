from client.connectors.announcements import AnnouncementClientConnector
from client.handlers.base import Game
from sprites.announcements.announce_modal import AnnounceModal
from sprites.loading_bar import TimeRemainingBar


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
                    self.socket_get_announcement_info()["data"]
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

    def calculate_available_dict(self, data):
        available_array = ["Pass", "Clubs", "Diamonds", "Hearts", "No Trumps", "All Trumps"]
        top_announcement = data["top_announcement"]
        top_announcer_not_in_team = data["top_announcer_in_same_team"]
        points_multiply_coefficient = data["points_multiply_coefficient"]
        if top_announcement:
            top_announcement_index = available_array.index(top_announcement)
            available_fields = available_array[top_announcement_index:]
            if top_announcer_not_in_team:
                if points_multiply_coefficient == 1:
                    available_fields.append("Double")
                elif points_multiply_coefficient == 2:
                    available_fields.append("Redouble")
            return available_fields
        return available_array