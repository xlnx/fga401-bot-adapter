import numpy as np

# turn off logging
import logging
from tableturf.ai.alpha.alpha import logger
logger.setLevel(logging.INFO)

from tableturf_replica import bot, api
from tableturf.ai.alpha import Alpha
import os
import json
from fga401_bot_adapter.context import Context
from fga401_bot_adapter.utils import cvt_rect_to_web_format

ctx = Context()
cur_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_path, "data/MiniGameCardInfo.json"), "r") as f:
  ctx.import_minigame_card_info(json.load(f))

def main():
  status = ctx.cvt_status_from_web(0, {
    'round': 12,
    'board': api.getStageById(0)['board'],
    'players': [
      {
        'deck': [
          30,
          52,
          65,
          50,
          66,
          64,
          53,
          58,
          28,
          74,
          69
        ],
        'hand': [
          33,
          159,
          92,
          25,
        ],
        'count': {
          'area': 1,
          'special': 0,
        }
      },
      {
        'deck': [
          53,
          118,
          125,
          69,
          109,
          20,
          143,
          44,
          12,
          113,
          75
        ],
        'hand': {
          86,
          110,
          105,
          161,
        },
        'count': {
          'area': 1,
          'special': 0,
        }
      }
    ],
  })
  rect = cvt_rect_to_web_format(status.stage.grid)
  print(api.printRect(rect))
  step = Alpha().next_step(status)
  print(step)
  
