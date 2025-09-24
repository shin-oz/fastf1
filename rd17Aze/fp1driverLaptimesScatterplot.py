import seaborn as sns # type: ignore

import matplotlib.pyplot as plt # type: ignore

import fastf1.plotting # type: ignore
import fastf1 # type: ignore

fastf1.Cache.enable_cache('./rd17cache')

# なんでtrueにするかは不明
fastf1.plotting.setup_mpl(mpl_timedeta_support= True, color_scheme= 'fastf1')

race = fastf1.get_session(2025, 17, 'FP2')
race.load()

# 複数のドライバーをリストで指定
drivers = ['VER', 'LEC', 'NOR', 'HAM']  # Verstappen, Leclerc, Norris, Hamilton
drivers = ['VER', 'TSU','NOR']
laps = race.laps

# 複数のドライバーのラップデータを取得
multi_driver_laps = laps.pick_drivers(drivers)

print("=== 指定ドライバーのラップタイム===")
print(multi_driver_laps[['LapNumber', 'Driver', 'LapTime', 'Position', 'Compound']])

# ドライバーごとの最速ラップを可視化
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 棒グラフ: 最速ラップ比較
# fastest_times = fastest_per_driver['LapTime'].dt.total_seconds()
# ax1.bar(fastest_per_driver['Driver'], fastest_times, color=['red', 'yellow', 'orange', 'green'])
# ax1.set_ylabel('Lap Time (seconds)')
# ax1.set_title('Fastest Lap Comparison')
# ax1.grid(True, alpha=0.3)

# 折れ線グラフ: 全ラップの推移
for driver in drivers:
    driver_data = multi_driver_laps[multi_driver_laps['Driver'] == driver]
    times_sec = driver_data['LapTime'].dt.total_seconds()
    ax2.plot(driver_data['LapNumber'], times_sec, marker='o', label=driver, linewidth=2)

ax2.set_xlabel('Lap Number')
ax2.set_ylabel('Lap Time (seconds)')
ax2.set_title('Lap Time Progression')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# driver_laps_TSU = race.laps.pick_driver("TSU").pick_quicklaps().reset_index()
# driver_laps_VER = race.laps.pick_driver("VER").pick_quicklaps().reset_index()
# print(driver_laps_TSU)
# print(driver_laps_VER)

# driver_laps = race.laps.pick_driver("TSU").pick_quicklaps().reset_index()

# fix, ax = plt.subplots(figsize=(8, 8))

# sns.scatterplot(data = driver_laps,
#                       x = "LapNumber",
#                       y = "LapTime",
#                       ax = ax,
#                       hue = "Compound",
#                       palette = fastf1.plotting.get_compound_mapping(session=race),
#                       s=80,
#                       linewidth = 0,
#                       legend = "auto")

# ax.set_xlabel("Lap Number")
# ax.set_ylabel("Lap Time")

# ax.invert_yaxis()

# plt.suptitle("Tsunoda Laptime in the 2025 Italian Grand prix")

# plt.grid(color='w', which='major', axis='both')
# sns.despine(left=True, bottom=True)

# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(10, 6))
# plt.plot(driver_laps['LapNumber'], driver_laps['LapTime'].dt.total_seconds(), marker='o')
# plt.xlabel('Lap Number')
# plt.ylabel('Lap Time (seconds)')
# plt.title('Verstappen Lap Times')
# plt.grid(True)
# plt.show()