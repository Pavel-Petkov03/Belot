import pygame

from cards import CardSprite
from variables import DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_WIDTH, window


class Animation:

    def deal_cards_animation(self, players):
        distance_between_cards = 50
        for player in players:
            player_x, player_y = player.x_y_position_on_board
            add_tup, reduce_tup = self.define_movement_axis(player, distance_between_cards)
            add_x, add_y = add_tup
            reduce_x, reduce_y = reduce_tup
            next_card_x = player_x + add_x - reduce_x
            next_card_y = player_y + add_y - reduce_y
            for card in sorted(player.cards, key=lambda obj: (obj.suit, obj.rank)):
                animation_card = CardSprite(card.suit, card.rank, next_card_x, next_card_y,
                                            player.rotation_degrees_of_own_cards)
                next_card_x += add_x
                next_card_y += add_y
                animation_card.update()

    @staticmethod
    def define_movement_axis(player, distance_between_cards):
        not_moving = 0

        player_x, player_y = player.x_y_position_on_board
        reduce_value = len(player.cards) / 2 * distance_between_cards
        if player_x in (DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_WIDTH - DISTANCE_BETWEEN_PLAYER_AND_WINDOW):
            reduce_tup = (not_moving, reduce_value)
            add_tup = (not_moving, distance_between_cards)
        else:
            add_tup = (distance_between_cards, not_moving)
            reduce_tup = (reduce_value, not_moving)
        return add_tup, reduce_tup

    @staticmethod
    def rotate_sprite(image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    @staticmethod
    def toggle_rect(announce_string, pos, degrees):
        font = pygame.font.SysFont(None, 50)
        i = font.render(announce_string, True, "black", "white")
        i = pygame.transform.rotate(i, degrees)
        window.blit(i, pos)
