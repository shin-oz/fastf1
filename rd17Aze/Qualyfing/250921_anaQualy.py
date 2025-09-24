# 全てドライバーの位置変動
# 特定のドライバーのラップタイム変動とタイヤコンパウンド
# 特定のドライバーのラップタイム比較

import seaborn as sns # type: ignore
import pandas as pd # type: ignore

import matplotlib.pyplot as plt # type: ignore

import fastf1 # type: ignore
import fastf1.plotting # type: ignore


# オフラインモードを有効化（キャッシュのみ使用）
fastf1.Cache.enable_cache('./cache')
fastf1.Cache.offline_mode(True)

# なんでtrueにするかは不明
fastf1.plotting.setup_mpl(mpl_timedeta_support= True, color_scheme= 'fastf1')

session = fastf1.get_session(2025, 17, 'Q')
session.load(telemetry = True, laps = True)

laps = session.laps

# 指定ドライバーのラップデータを取得
driver = "TSU"
driver_laps = laps.pick_drivers(driver)
# print("=== 指定ドライバーのラップタイム===")
# print(driver_laps[['LapNumber', 'Driver', 'LapTime', 'Position', 'Compound']])

# plt.figure(figsize=(10, 6))
# plt.plot(driver_laps['LapNumber'], driver_laps['LapTime'], marker = 'o')
# plt.xlabel('Lap Number')
# plt.ylabel('Lap Time(seconds)')
# plt.title('Driver Lap Times')
# plt.grid(True)
# plt.show()

# 複数のドライバーのラップデータを取得
drivers = ['VER', 'TSU','NOR']
multi_driver_laps = laps.pick_drivers(drivers)
# print("=== 複数ドライバーのラップタイム===")
# print(multi_driver_laps[['LapNumber', 'Driver', 'LapTime', 'Position', 'Compound']])

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15, 6))

for driver in drivers:
  driver_data = multi_driver_laps[multi_driver_laps['Driver'] == driver]
  times = driver_data['LapTime']
  ax2.plot(driver_data['LapNumber'], times, marker = 'o', label = driver, linewidth = 2)

ax2.set_xlabel('Lap Number')
ax2.set_ylabel('Lap Time')
ax2.set_title('Lap Time Progression')
ax2.legend()
ax2.grid(True, alpha = 0.3)

plt.tight_layout()
plt.show()