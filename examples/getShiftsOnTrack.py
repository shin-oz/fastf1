import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
from matplotlib import colormaps # type: ignore
from matplotlib.collections import LineCollection # type: ignore

import fastf1 # type: ignore

fastf1.Cache.offline_mode(True)

session = fastf1.get_session(2025, 16, 'R')
session.load()

# fastestlapのみ取得→NOR
lap = session.laps.pick_fastest()
tel = lap.get_telemetry()

x = np.array(tel['X'].values)
y = np.array(tel['Y'].values)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
gear = tel['nGear'].to_numpy().astype(float)

cmap = colormaps['Paired']
lc_comp = LineCollection(segments, norm = plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(gear)
lc_comp.set_linewidth(4)

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft = False, left = False, labelbottom = False, bottom = False)

title = plt.suptitle(
  f"Fastest Lap Gear Shift Visualization\n"
  f"{lap['Driver']} - {session.event['EventName']} {session.event.year}"
)

cbar = plt.colorbar(mappable=lc_comp, label = "Gear",
                    boundaries = np.arange(1, 10))
cbar.set_ticks(np.arange(1.5, 9.5))
cbar.set_ticklabels(np.arange(1, 9))

plt.show()