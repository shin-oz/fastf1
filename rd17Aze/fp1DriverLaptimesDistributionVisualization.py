import seaborn as sns # type: ignore
from matplotlib import pyplot as plt # type: ignore

import fastf1 # type: ignore
import fastf1.plotting # type: ignore

from fastf1.livetiming.data import LiveTimingData # type: ignore
# オフラインモードを有効化（キャッシュのみ使用）
fastf1.Cache.offline_mode(True)

livedata = LiveTimingData("o250919FP1.txt")
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_schme='fastf1')

# セッションの取得
session = fastf1.get_session(2025, 17, 'FP1')
# セッションを読み込み
session.load(livedata=livedata)  # ライブデータ使用

point_finishers = session.drivers[:20]
driver_laps = session.laps.pick_drivers(point_finishers).pick_quicklaps()
driver_laps = driver_laps.reset_index()

finishing_order = [session.get_driver(i)["Abbreviation"] for i in point_finishers]
# print(finishing_order)

fig, ax = plt.subplots(figsize=(10, 5))

driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

sns.violinplot(data=driver_laps,
               x="Driver",
               y="LapTime(s)",
               inner=None,
               density_norm="area",
               order=finishing_order,
               palette=fastf1.plotting.get_driver_color_mapping(session=session)
               )

sns.swarmplot(data=driver_laps,
              x="Driver",
              y="LapTime(s)",
              order=finishing_order,
              hue="Compound",
              palette=fastf1.plotting.get_compound_mapping(session=session),
              hue_order=["SOFT","MEDIUM", "HARD"],
              linewidth=0,
              size=4,
              )

ax.set_xlabel("Driver")
ax.set_ylabel("Lap Time (s)")
plt.suptitle("2023 Azerbaijan Grand Prix Lap Time Distributions")
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()
