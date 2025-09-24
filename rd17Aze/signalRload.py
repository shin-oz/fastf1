from fastf1 import core # type: ignore
from fastf1.livetiming.data import LiveTimingData # type: ignore

# ライブデータをロード
livedata = LiveTimingData.from_file("o250919FP1.txt")

# セッションを作成（例: 2025年アゼルバイジャンGPのレース）
session = core.Session(2025, '17', 'FP1')  # 年、会場、セッションタイプ
session.load(livedata=livedata, telemetry=True)  # ライブデータ使用

# データアクセス例
laps = session.laps
telemetry = laps.pick_driver('VER').get_telemetry()
print(telemetry)  # テレメトリデータ表示