import matplotlib.pyplot as plt # type: ignore

import fastf1 # type: ignore
from fastf1 import plotting # type: ignore

fastf1.Cache.offline_mode(True)

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

race = fastf1.get_session(2025, 16, 'R')
race.load()

my_styles = [
  {'color': 'auto', 'linestyle': 'solid', 'linewidth': 10, 'alpha':0.3},
  {'color': 'auto', 'linestyle': 'solid', 'linewidth': 1, 'alpha':0.7},
]

# Basic driver-specific plot styling
fig, ax = plt.subplots(figsize=(8,5))

for driver in ('HAM', 'TSU', 'VER', 'RUS'):
  laps = race.laps.pick_drivers(driver).pick_quicklaps().reset_index()
  # style = plotting.get_driver_style(identifier = driver, style = ['color', 'linestyle'],
                                    # session = race)
  style = plotting.get_driver_style(identifier=driver,
                                      style=my_styles,
                                      session=race)
  ax.plot(laps['LapTime'], **style, label = driver)

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

# 二つの違いがわからん
# ax.legend()
plotting.add_sorted_driver_legend(ax, race)

plt.show()