import numpy as np
from typeguard import typechecked
from typing import Dict, Any
from tableturf.model import Grid


from_web_format = [
  {
    0: Grid.Empty,
    turn: Grid.MyInk,
    2*turn: Grid.MySpecial,
    -turn: Grid.HisInk,
    -2*turn: Grid.HisSpecial,
    3: Grid.Neutral,
    99: Grid.Wall,
  } \
  for turn in [1, -1]
]

to_web_format = [
  {
    v.value: k for k, v in lookup.items()
  } \
  for lookup in from_web_format
]


@typechecked
def cvt_rect_from_web_format(rect: Dict[str, Any], player_id: int = 0) -> np.ndarray:
  lookup = from_web_format[player_id]
  [w, h] = rect['size']
  values = rect['values']
  li = []
  for y in range(h):
    li_x = []
    for x in range(w):
      li_x.append(lookup[values[x+y*w]])
    li.append(li_x)
  return np.array(li)


@typechecked
def cvt_rect_to_web_format(li: np.ndarray, player_id: int = 0) -> Dict[str, Any]:
  lookup = to_web_format[player_id]
  h = len(li)
  w = len(li[0])
  values = []
  for y in range(h):
    for x in range(w):
      values.append(lookup[li[y][x]])
  return {
    'size': [w, h],
    'values': values,
  }
