# turn off logging
import logging
from tableturf.ai.alpha.alpha import logger
logger.setLevel(logging.INFO)

import json
from tableturf_replica import bot
from tableturf.ai.alpha import Alpha
from fga401_bot_adapter.context import Context

ctx = Context()


@bot
class AlphaBot:
  meta = {
    'name': 'Alpha',
    'support': {
      'stages': [],
      'anyDeck': True,
    }
  }

  def __init__(self):
    self.ctx = Context()
    self.bot = Alpha()

  def initialize(self, params):
    self.player_id = params['player']
    self.update(params)

  def update(self, params):
    game_state = params['game']
    self.status = self.ctx.cvt_status_from_web(self.player_id, game_state)

  def query(self, params):
    step = self.bot.next_step(self.status)
    move = self.ctx.cvt_step_to_web(self.status, step)
    return move

  def finalize(self, params):
    pass

  @staticmethod
  def select_deck(params):
    print(params)
    return params['deck']


def main():
  AlphaBot().serve(5140)

