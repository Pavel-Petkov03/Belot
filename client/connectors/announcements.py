from client.connectors.base import ClientConnector


class AnnouncementClientConnector(ClientConnector):
    def socket_check_announcements_order(self):
        return self.send("check_announcements_order")

    def socket_get_announcement_info(self):
        return self.send("get_announcement_info")

    def socket_get_pass_list_len(self):
        return self.send("get_pass_counter")

    def socket_set_announcement(self, announcement):
        return self.send("set_announcement", params={"announced_game": announcement})

    def socket_get_loading_bar_info(self):
        return self.send("get_loading_bar_info")
