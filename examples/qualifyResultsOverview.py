import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
from timple.timedelta import strftimedelta # type: ignore

import fastf1 # type: ignore
import fastf1.plotting # type: ignore
from fastf1.core import Laps # type: ignore

fastf1.Cache.offline_mode(True)

# Enable Matplotlib patches for plotting timedelta values
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

# qualifyingのデータって取得していなかったっけ...?
session = fastf1.get_session(2025, 16, 'Q')
session.load()

drivers = pd.unique(session.laps['Driver'])

list_fastest_laps = list()
for drv in drivers:
  drvs_fastestlap = session.laps.pick_driver(drv).pick_fastest()
  list_fastest_laps.append(drvs_fastestlap)
fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

team_colors = list()
for index, lap in fastest_laps.iterlaps():
  color = fastf1.plotting.get_team_color(lap['Team'], session = session)
  team_colors.append(color)

fig, ax = plt.subplots()
ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])

ax.invert_yaxis()

ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

plt.show()

