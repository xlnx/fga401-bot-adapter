__all__ = ['Context']


import numpy as np
from typing import Dict, Any, List
from typeguard import typechecked
from tableturf.model import Status, Stage, Card, Grid
from fga401_bot_adapter.utils import *


@typechecked
class Context:
  def __init__(self) -> None:
    self._cards: Dict[int, Card] = {}

  # getters
  def get_card(self, card_id: int) -> Card:
    return self._cards[card_id]

  # converters
  def cvt_status_from_web(self, player_id: int, state: Dict[str, Any]) -> Status:
    players = state['players']
    board = state['board']
    my_state = players[player_id]
    his_state = players[1 - player_id]
    return Status(
      stage=Stage(cvt_rect_from_web_format(board, player_id)),
      hands=[self.get_card(card_id) for card_id in my_state['hand']],
      round=state['round'],
      my_sp=my_state['count']['special'],
      his_sp=his_state['count']['special'],
      my_deck=[self.get_card(card_id) for card_id in my_state['deck']],
      his_deck=[self.get_card(card_id) for card_id in his_state['deck']],
    )

  # data importers
  def import_minigame_card_info(self, card_infos):
    """
    Args:
        card_infos (_type_): format = minigame_card_info.json
    """
    self._cards = {}
    for info in card_infos:
      card_id = info['Number']
      sp_cost = info['SpecialCost']
      values = info['Square']
      li = []
      for y in range(8):
        li_x = []
        for x in range(8):
          v0 = values[x+(7-y)*8]
          v = Grid.Empty
          if v0 == "Fill":
            v = Grid.MyInk
          elif v0 == "Special":
            v = Grid.MySpecial
          li_x.append(v)
        li.append(li_x)
      self._cards[card_id] = Card(np.array(li), sp_cost)
