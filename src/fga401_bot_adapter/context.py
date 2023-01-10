__all__ = ['Context']


from functools import cache
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from typeguard import typechecked
from tableturf.model import Status, Stage, Card, Grid, Step
from tableturf_replica import api
from fga401_bot_adapter.utils import *


@typechecked
@dataclass
class CardMeta:
  web: Dict[str, Any]
  offset: Tuple[int, int]


@cache
@typechecked
def get_default_cards() -> Dict[int, Card]:
  cards = {}
  for info in api.getCards():
    i = info['id']
    li = cvt_rect_from_web_format(info)

    if isinstance(li[0][0], Grid):
      li = np.vectorize(lambda x: x.value)(li)
    li1 = li != Grid.Empty.value
    [x, y] = map(lambda i: list(np.any(li1, axis=i)).index(True), range(2))

    card = cards[i] = Card(li, info['count']['special'])
    card.meta = CardMeta(web=info, offset=(x, y))
    
  return cards


@typechecked
class Context:
  def __init__(self) -> None:
    self._cards = get_default_cards()

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
      hands=[
        self.get_card(card_id) \
        for card_id in my_state['hand'] \
        if card_id is not None
      ],
      round=state['round'],
      my_sp=my_state['count']['special'],
      his_sp=his_state['count']['special'],
      my_deck=[self.get_card(card_id) for card_id in my_state['deck']],
      his_deck=[self.get_card(card_id) for card_id in his_state['deck']],
    )

  def cvt_step_to_web(self, status: Status, step: Step) -> Dict[str, Any]:
    move = {
      'action': {
        Step.Action.Skip: 'discard',
        Step.Action.Place: 'trivial',
        Step.Action.SpecialAttack: 'special',
      } [step.action],
      'hand': status.hands.index(step.card),
    }
    if step.action != Step.Action.Skip:
      rotation = (4 - step.rotate) % 4
      pattern = step.card.get_pattern(step.rotate)
      dy, dx = map(int, np.amin(pattern.offset, axis=0))
      y, x = map(int, step.pos)
      x, y = x + dx, y + dy
      pattern = step.card.get_pattern()
      w, h = pattern.width, pattern.height
      dx, dy = step.card.meta.offset
      rdx, rdy = 8 - w - dx, 8 - h - dy
      x, y = [
        [x-dx, y-dy],
        [x-rdy, y-dx],
        [x-rdx, y-rdy],
        [x-dy, y-rdx],
      ] [rotation]
      move['params'] = {
        'rotation': rotation,
        'position': {'x':x,'y':y},
      }
    return move
