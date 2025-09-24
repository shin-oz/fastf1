import fastf1 # type: ignore
# import os

# キャッシュフォルダを作成（例: カレントディレクトリの'fastf1_cache'）
# cache_dir = os.path.join(os.getcwd(), 'fastf1_cache')
# os.makedirs(cache_dir, exist_ok=True)

# キャッシュを有効化（初回のみインターネット接続が必要）
# fastf1.Cache.enable_cache(cache_dir)


# セッションを取得（年、ラウンド、セッションタイプ）
# session = fastf1.get_session(2021, 7, 'Q')  # 7はフランスGPのラウンド番号、'Q'は予選
# session = fastf1.get_session(2025, 15, 'R')  # 7はフランスGPのラウンド番号、'Q'は予選
# 決勝後にこれを実行しておくこと
# session = fastf1.get_session(2025, 16, 'R')  # 7はフランスGPのラウンド番号、'Q'は予選
# session = fastf1.get_session(2025, 17, 'FP2')  # 7はフランスGPのラウンド番号、'Q'は予選
session = fastf1.get_session(2025, 17, 'Q') #アゼルバイジャンGPの予選 

# データをロード（キャッシュに保存。初回はダウンロード）
session.load()  # telemetry=True, laps=True, weather=True などで詳細データを指定可能

print(session.results)  # 結果を表示（キャッシュ確認）