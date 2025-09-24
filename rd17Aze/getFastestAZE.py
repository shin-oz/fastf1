import fastf1 # type: ignore
# なんでfastf1でなくてplotting選択まで必要か不明
import fastf1.plotting # type: ignore
import matplotlib.pyplot as plt # type: ignore


# オフラインモードを有効化（キャッシュのみ使用）
fastf1.Cache.offline_mode(True)

# load dark color scheme
fastf1.plotting.setup_mpl(color_scheme='fastf1')

# セッションの取得
session = fastf1.get_session(2025, 16, 'R')
# セッションを読み込み
session.load()
# print(session.results.columns)
# トップ10ドライバーとQ3結果
# print(session.results.iloc[0:10].loc[:, ['Abbreviation', 'Q3']])

# ドライバーのラップタイムを取得
laps = session.laps
# Tsunodaのラップを取得
tsunoda_laps = laps.pick_drivers('TSU')
# ラップ番号、タイム、タイヤ　
# print(tsunoda_laps[['LapNumber', 'LapTime', 'Compound']])
# print(tsunoda_laps)
# print(tsunoda_laps.columns)
# print(tsunoda_laps['PitOutTime'])

# Tsunodaのfastestlapを取得　
fastest_lap = tsunoda_laps.pick_fastest()
telemetry = fastest_lap.get_telemetry()
# 速度と距離
# print(telemetry)
# print(telemetry[['Speed', 'Distance']])

# テスト中
# print(session.date)
# print(session.event)
# print(session.event)

# プロット（Matplotlib使用）
plt.plot(telemetry['Distance'], telemetry['Speed'])
plt.title('Tsunoda Fastest Lap Speed')
plt.xlabel('Distance (m)')
plt.ylabel('Speed (km/h)')
# plt.show()