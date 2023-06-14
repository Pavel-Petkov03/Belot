from collections import Counter

from sprites.preload_sprites.text_box_base import TextBox


class AnnouncementPopup(TextBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.announcement_popup_counter = Counter()



