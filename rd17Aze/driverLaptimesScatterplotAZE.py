import seaborn as sns # type: ignore

import matplotlib.pyplot as plt # type: ignore

import fastf1.plotting # type: ignore
import fastf1 # type: ignore

fastf1.Cache.offline_mode(True)

# なんでtrueにするかは不明
fastf1.plotting.setup_mpl(mpl_timedeta_support= True, color_scheme= 'fastf1')

race = fastf1.get_session(2025, 16, 'R')
race.load()

driver_laps = race.laps.pick_driver("TSU").pick_quicklaps().reset_index()

fix, ax = plt.subplots(figsize=(8, 8))

sns.scatterplot(data = driver_laps,
                      x = "LapNumber",
                      y = "LapTime",
                      ax = ax,
                      hue = "Compound",
                      palette = fastf1.plotting.get_compound_mapping(session=race),
                      s=80,
                      linewidth = 0,
                      legend = "auto")

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

ax.invert_yaxis()

plt.suptitle("Tsunoda Laptime in the 2025 Italian Grand prix")

plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()