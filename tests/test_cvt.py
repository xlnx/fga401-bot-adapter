import os
import json
import textwrap
from tableturf_replica import api
from fga401_bot_adapter.context import Context
from fga401_bot_adapter.utils import cvt_rect_to_web_format

ctx = Context()
cur_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_path, "../src/fga401_bot_adapter/data/MiniGameCardInfo.json"), "r") as f:
  ctx.import_minigame_card_info(json.load(f))

def test_cvt():
  game_state = {
    "round":0,
    "board":{
      "size":[16,22],
      "values":[99,99,99,99,99,99,99,99,0,0,-2,0,-1,-1,-1,0,99,99,99,99,99,99,99,99,0,0,0,-1,-1,-1,-1,-1,99,99,99,99,99,99,99,99,-1,-1,-1,-1,-1,-1,-1,0,99,99,99,99,99,99,99,99,-1,-1,-1,-2,-2,-1,0,0,99,99,99,99,99,99,99,99,-1,-1,2,1,-1,0,0,0,99,99,99,99,99,99,99,99,-1,-2,1,1,-1,-1,-1,0,99,99,99,99,99,99,99,99,-1,1,1,-1,-1,-1,-1,-1,0,1,1,1,0,1,-1,2,1,1,1,-1,-2,-1,-2,-1,1,1,2,-1,-1,1,2,1,1,1,1,1,-2,-1,0,-1,1,1,-1,-1,-1,-1,-2,-1,-1,1,1,0,0,-1,-1,0,0,0,-1,-1,-1,-1,0,0,1,-2,-1,1,-2,-1,0,0,0,1,2,-1,-1,1,1,1,-1,-1,-1,-1,0,-1,0,0,1,1,1,1,0,1,1,0,1,1,-1,0,-1,-1,-1,0,1,1,0,0,0,1,1,1,2,1,0,0,0,-1,-1,-1,1,0,1,0,1,1,1,1,1,0,1,0,0,-2,0,0,1,2,1,1,1,2,1,1,99,99,99,99,99,99,99,99,1,1,1,1,0,1,0,1,99,99,99,99,99,99,99,99,1,1,1,1,1,1,1,0,99,99,99,99,99,99,99,99,0,0,2,2,1,1,0,0,99,99,99,99,99,99,99,99,0,0,1,1,1,1,1,0,99,99,99,99,99,99,99,99,1,1,1,1,1,1,1,0,99,99,99,99,99,99,99,99,0,0,2,0,0,0,0,0,99,99,99,99,99,99,99,99],
      "count":{
        "area":[96,79],"special":[5,4]
      }
    },
    "players":[
      {
        "deck":[],
        "hand":[66,65,69],
        "count":{"area":96,"special":0}
      },
      {
        "deck":[],
        "hand":[110,105,161],
        "count":{"area":79,"special":2}
      }
    ],
    "prevMoves":[
      [
        {"rotation":3,"position":{"x":6,"y":4},"player":0,"card":74},
        {"rotation":0,"position":{"x":0,"y":6},"player":1,"card":75}
      ]
    ]
  }
  expected = textwrap.dedent("""\
    @@@@@@@@..B.bbb.
    @@@@@@@@...bbbbb
    @@@@@@@@bbbbbbb.
    @@@@@@@@bbbBBb..
    @@@@@@@@bbAab...
    @@@@@@@@bBaabbb.
    @@@@@@@@baabbbbb
    .aaa.abAaaabBbBb
    aaAbbaAaaaaaBb.b
    aabbbbBbbaa..bb.
    ..bbbb..aBbaBb..
    .aAbbaaabbbb.b..
    aaaa.aa.aab.bbb.
    aa...aaaAa...bbb
    a.a.aaaaa.a..B..
    aAaaaAaa@@@@@@@@
    aaaa.a.a@@@@@@@@
    aaaaaaa.@@@@@@@@
    ..AAaa..@@@@@@@@
    ..aaaaa.@@@@@@@@
    aaaaaaa.@@@@@@@@
    ..A.....@@@@@@@@
    """)
  for player_id in [0, 1]:
    status = ctx.cvt_status_from_web(player_id, game_state)
    rect = cvt_rect_to_web_format(status.stage.grid, player_id)
    actual = api.printRect(rect)
    assert actual == expected
