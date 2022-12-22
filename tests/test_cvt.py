import textwrap
import numpy as np
from tableturf_replica import api
from tableturf.model import Step
from fga401_bot_adapter.context import Context
from fga401_bot_adapter.utils import cvt_rect_to_web_format


ctx = Context()


def test_cvt_status():
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


def test_cvt_step():
  board = textwrap.dedent('''\
    Aa.
    aB.
    @..
  ''')
  game_state = {
    "round":0,
    "board":api.parseRect(board),
    "players":[
      {
        "deck":[],
        # splat bomb
        "hand":[56],
        "count":{"area":0,"special":99}
      },
      {
        "deck":[],
        "hand":[],
        "count":{"area":0,"special":0}
      }
    ],
  }
  status = ctx.cvt_status_from_web(0, game_state)
  steps = status.get_possible_steps()
  moves = [
    ctx.cvt_step_to_web(status, step) \
    for step in steps \
    if step.action != Step.Action.Skip
  ]
  moves.sort(
    key=lambda x:(x['action'], x['params']['rotation']),
    reverse=True,
  )
  assert moves == [
    {
      "action": "trivial",
      "hand": 0,
      "params": {
        "rotation": 0,
        "position": {"x":-2, "y":-2}
      }
    },
    {
      "action": "special",
      "hand": 0,
      "params": {
        "rotation": 3,
        "position": {"x":-2, "y":-3}
      }
    },
  ]

def test_case_1():
  game_state = {
    "round": 12, 
    "board": {
      "size": [17, 25], 
      "values": [99, 99, 99, 99, 99, 99, 99, 99, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 0, 99, 99, 99, 99, 99, 99, 99, 99], 
      "count": {"area": [1, 1], "special": [0, 0]}
    }, 
    "players": [
      {
        "deck": [40, 92, 34, 22, 6, 13, 56, 137, 159, 103, 28], 
        "hand": [52, 55, 141, 45], 
        "count": {"area": 0, "special": 0}
      }, 
      {
        "deck": [6, 55, 141, 52, 56, 92, 45, 40, 137, 103, 34], 
        "hand": [13, 159, 28, 22], 
        "count": {"area": 0, "special": 0}
      }
    ], 
    "prevMoves": []
  }
  status = ctx.cvt_status_from_web(1, game_state)
  step = Step(
    action=Step.Action.Place, 
    card=status.hands[3],
    rotate=3,
    pos=np.array([6, 9])
  )
  move = ctx.cvt_step_to_web(status, step)
  assert move == {
    'action': 'trivial', 
    'hand': 3, 'params': {
      'rotation': 1, 
      'position': {'x': 4, 'y': 5}
    }
  }
