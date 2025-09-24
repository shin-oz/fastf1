import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 設定
# =============================================================================
def setup_cache():
    """キャッシュ設定"""
    try:
        # キャッシュディレクトリのパスを指定（環境に合わせて変更）
        cache_path = './fastf1_cache'  # 相対パス例
        # cache_path = '/home/user/fastf1_cache'  # 絶対パス例
        
        fastf1.Cache.enable_cache(cache_path)
        print(f"✅ キャッシュ有効: {cache_path}")
        return True
    except Exception as e:
        print(f"⚠️  キャッシュ設定エラー: {e}")
        return False

# =============================================================================
# データ取得
# =============================================================================
def get_session_data(year, event_name, session_type='R', drivers=None):
    """
    セッションデータを取得
    
    Parameters:
    - year: int (例: 2024)
    - event_name: str (例: 'Monaco', 'Silverstone')
    - session_type: str ('R'=Race, 'Q'=Qualifying, 'P1'-'P3'=Practice)
    - drivers: list (例: ['VER', 'NOR', 'PIA'])
    """
    print(f"🔄 セッション取得中: {year} {event_name} {session_type}")
    
    try:
        # セッション取得
        session = fastf1.get_session(year, event_name, session_type)
        session.load(laps=True, telemetry=False, weather=False)  # laps=Trueでラップデータ取得
        
        # 全ラップデータ
        laps = session.laps
        
        # ドライバー指定がある場合フィルタリング
        if drivers:
            laps = laps.pick_drivers(drivers)
            print(f"📋 対象ドライバー: {', '.join(drivers)}")
        else:
            # デフォルトで上位4ドライバー
            drivers = list(laps['Driver'].unique())[:4]
            laps = laps.pick_drivers(drivers)
            print(f"📋 自動選択ドライバー: {', '.join(drivers)}")
        
        print(f"✅ データ取得完了: {len(laps)} ラップ, {len(drivers)} ドライバー")
        return session, laps, drivers
        
    except Exception as e:
        print(f"❌ セッション取得エラー: {e}")
        return None, None, None

# =============================================================================
# ドライバーマッピング
# =============================================================================
DRIVER_MAPPING = {
    'VER': 'Max Verstappen', 'HAM': 'Lewis Hamilton', 'NOR': 'Lando Norris',
    'LEC': 'Charles Leclerc', 'PIA': 'Oscar Piastri', 'RUS': 'George Russell',
    'SAI': 'Carlos Sainz', 'PER': 'Sergio Perez', 'ALO': 'Fernando Alonso',
    'STR': 'Lance Stroll', 'TSU': 'Yuki Tsunoda', 'LAW': 'Alex Albon'
}

# =============================================================================
# グラフ作成
# =============================================================================
def create_comparison_plots(session, laps, drivers, figsize=(16, 12)):
    """
    複数ドライバー比較グラフ作成
    """
    session_name = f"{session.event['EventName']} {session.event.year} {session.name}"
    
    # タイヤコンパウンドの色設定（F1公式カラー）
    compound_colors = {
        'SOFT': '#FF0000',      # 赤
        'MEDIUM': '#FFFF00',    # 黄色
        'HARD': '#FFFFFF',      # 白
        'INTERMEDIATE': '#00FF00',  # 緑
        'WET': '#00BFFF',       # 水色
        'UNKNOWN': '#808080'    # グレー
    }
    
    # ドライバーごとのカラー設定
    driver_colors = {
        'VER': '#FF2800', 'NOR': '#FF8C00', 'PIA': '#0066CC', 'RUS': '#00A3E0',
        'LEC': '#DC143C', 'HAM': '#00D2BE', 'SAI': '#FF1F37', 'PER': '#1A8BFF',
        'ALO': '#009E49', 'STR': '#005555', 'TSU': '#4463C7', 'LAW': '#FF8E00'
    }
    
    # コンパウンドごとのマーカースタイル
    compound_markers = {
        'SOFT': 'o', 'MEDIUM': 's', 'HARD': '^',
        'INTERMEDIATE': 'D', 'WET': 'p', 'UNKNOWN': 'x'
    }
    
    # 図の作成
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.8], hspace=0.3, wspace=0.3)
    
    # グラフ1: ラップタイム推移（コンパウンド色分け）
    ax1 = fig.add_subplot(gs[0, :])
    handles1, labels1 = [], []
    
    for driver in drivers:
        driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
        
        # 各ドライバーのラップをプロット
        for compound in driver_laps['Compound'].unique():
            compound_laps = driver_laps[driver_laps['Compound'] == compound]
            if len(compound_laps) >= 1:  # 1ラップ以上
                times_sec = compound_laps['LapTime'].dt.total_seconds()
                color = compound_colors.get(compound, '#808080')
                marker = compound_markers.get(compound, 'o')
                
                # ドライバー固有のエッジカラー
                edge_color = driver_colors.get(driver, '#000000')
                
                line, = ax1.plot(compound_laps['LapNumber'], times_sec, 
                               color=color, marker=marker, markersize=4, 
                               linewidth=2, markeredgecolor=edge_color, 
                               markeredgewidth=1, alpha=0.8,
                               label=f"{DRIVER_MAPPING.get(driver, driver)}-{compound}")
                
                if driver == drivers[0]:  # 最初のドライバーでラベル追加
                    handles1.append(line)
                    labels1.append(f"{compound}")
    
    # 平均ラップタイムの基準線
    avg_time = laps['LapTime'].dt.total_seconds().mean()
    ax1.axhline(y=avg_time, color='black', linestyle='--', alpha=0.5, 
                label=f'Avg: {avg_time:.2f}s')
    
    ax1.set_xlabel('Lap Number')
    ax1.set_ylabel('Lap Time (seconds)')
    ax1.set_title(f'{session_name}\nLap Time Progression by Compound', fontsize=12, pad=20)
    ax1.legend(handles=handles1, labels=labels1, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Y軸の範囲調整（最速-最遅の範囲に収める）
    times = laps['LapTime'].dt.total_seconds()
    y_min, y_max = times.min() - 0.5, times.max() + 0.5
    ax1.set_ylim(y_min, y_max)
    
    # グラフ2: コンパウンド別最速ラップ比較
    ax2 = fig.add_subplot(gs[1, 0])
    fastest_per_compound = []
    
    for compound in compound_colors.keys():
        compound_laps = laps[laps['Compound'] == compound]
        if len(compound_laps) > 0:
            fastest_lap = compound_laps.loc[compound_laps['LapTime'].idxmin()]
            fastest_per_compound.append({
                'Compound': compound,
                'FastestTime': fastest_lap['LapTime'].total_seconds(),
                'Driver': fastest_lap['Driver'],
                'LapNumber': fastest_lap['LapNumber'],
                'Position': fastest_lap['Position']
            })
    
    if fastest_per_compound:
        fastest_df = pd.DataFrame(fastest_per_compound).sort_values('FastestTime')
        bars = ax2.bar(range(len(fastest_df)), fastest_df['FastestTime'], 
                      color=[compound_colors[c] for c in fastest_df['Compound']],
                      alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # 各バーの上にドライバー名とラップ番号を表示
        for i, bar in enumerate(bars):
            height = bar.get_height()
            driver_name = DRIVER_MAPPING.get(fastest_df.iloc[i]['Driver'], 
                                           fastest_df.iloc[i]['Driver'])
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f"{driver_name}\nLap {fastest_df.iloc[i]['LapNumber']}",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        ax2.set_ylabel('Fastest Lap Time (seconds)')
        ax2.set_title('Fastest Lap by Compound')
        ax2.set_xticks(range(len(fastest_df)))
        ax2.set_xticklabels([c[:3] for c in fastest_df['Compound']], rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 最小値のライン
        ax2.axhline(y=fastest_df['FastestTime'].min(), color='red', 
                   linestyle='-', alpha=0.7, linewidth=1)
    
    # グラフ3: ドライバー別平均ラップタイム
    ax3 = fig.add_subplot(gs[1, 1])
    driver_stats = []
    
    for driver in drivers:
        driver_laps = laps[laps['Driver'] == driver]
        if len(driver_laps) > 0:
            avg_time = driver_laps['LapTime'].mean().total_seconds()
            std_time = driver_laps['LapTime'].std().total_seconds()
            lap_count = len(driver_laps)
            
            driver_stats.append({
                'Driver': driver,
                'AvgTime': avg_time,
                'StdTime': std_time,
                'LapCount': lap_count
            })
    
    if driver_stats:
        stats_df = pd.DataFrame(driver_stats)
        x_pos = np.arange(len(drivers))
        width = 0.35
        
        bars = ax3.bar(x_pos, stats_df['AvgTime'], 
                      yerr=stats_df['StdTime'], capsize=5, 
                      color=[driver_colors[d] for d in stats_df['Driver']],
                      alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # 各バーの上にラップ数と平均タイムを表示
        for i, bar in enumerate(bars):
            height = bar.get_height()
            driver_name = DRIVER_MAPPING.get(stats_df.iloc[i]['Driver'], 
                                           stats_df.iloc[i]['Driver'])
            ax3.text(bar.get_x() + bar.get_width()/2., height + stats_df.iloc[i]['StdTime'] + 0.1,
                    f"{driver_name}\n{stats_df.iloc[i]['LapCount']} laps\n{stats_df.iloc[i]['AvgTime']:.2f}s",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        ax3.set_ylabel('Average Lap Time (seconds)')
        ax3.set_title('Driver Performance Summary')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels([DRIVER_MAPPING.get(d, d) for d in drivers], rotation=45)
        ax3.grid(True, alpha=0.3, axis='y')
    
    # グラフ4: タイヤ使用統計テーブル
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('tight')
    ax4.axis('off')
    
    # 統計テーブル作成
    table_data = []
    headers = ['Driver', 'SOFT', 'MEDIUM', 'HARD', 'Total', 'Fastest Lap']
    
    for driver in drivers:
        driver_laps = laps[laps['Driver'] == driver]
        row = [DRIVER_MAPPING.get(driver, driver)]
        
        # コンパウンド別ラップ数
        for compound in ['SOFT', 'MEDIUM', 'HARD']:
            count = len(driver_laps[driver_laps['Compound'] == compound])
            row.append(str(count) if count > 0 else '-')
        
        total_laps = len(driver_laps)
        row.append(str(total_laps))
        
        # 最速ラップ
        if total_laps > 0:
            fastest = driver_laps.loc[driver_laps['LapTime'].idxmin()]
            fastest_time = fastest['LapTime'].total_seconds()
            fastest_compound = fastest['Compound']
            row.append(f"{fastest_time:.2f}s ({fastest_compound})")
        else:
            row.append('-')
        
        table_data.append(row)
    
    # テーブル描画
    table = ax4.table(cellText=table_data, colLabels=headers, 
                     cellLoc='center', loc='center', colWidths=[0.15, 0.1, 0.1, 0.1, 0.1, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # ヘッダー行のスタイル
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(weight='bold', color='white')
        table[(0, i)].set_height(0.1)
    
    # ドライバー行の交互色
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
    
    ax4.set_title('Tire Compound Usage Summary', fontsize=12, pad=20)
    
    # 全体タイトル
    plt.suptitle(f'{session_name} - Multiple Driver & Compound Analysis', 
                fontsize=16, y=0.95)
    
    plt.tight_layout()
    plt.show()
    
    return fig

# =============================================================================
# 統計表示
# =============================================================================
def print_session_stats(session, laps, drivers):
    """セッション統計を表示"""
    print("\n" + "="*60)
    print(f"📊 {session.event['EventName']} {session.event.year} {session.name} 分析結果")
    print("="*60)
    
    # 全体統計
    total_laps = len(laps)
    unique_compounds = laps['Compound'].unique()
    avg_lap_time = laps['LapTime'].mean().total_seconds()
    
    print(f"📈 総ラップ数: {total_laps}")
    print(f"🔴 使用コンパウンド: {', '.join(unique_compounds)}")
    print(f"⏱️  平均ラップタイム: {avg_lap_time:.2f}秒")
    
    # ドライバー別統計
    print(f"\n👨‍💼 ドライバー別統計:")
    print("-" * 40)
    driver_stats = []
    
    for driver in drivers:
        driver_laps = laps[laps['Driver'] == driver]
        if len(driver_laps) > 0:
            avg_time = driver_laps['LapTime'].mean().total_seconds()
            best_time = driver_laps['LapTime'].min().total_seconds()
            lap_count = len(driver_laps)
            best_compound = driver_laps.loc[driver_laps['LapTime'].idxmin()]['Compound']
            
            driver_stats.append({
                'Driver': DRIVER_MAPPING.get(driver, driver),
                'Laps': lap_count,
                'Avg': f"{avg_time:.2f}s",
                'Best': f"{best_time:.2f}s",
                'BestTire': best_compound
            })
    
    # 統計テーブル表示
    print(f"{'ドライバー':<15} {'ラップ':<6} {'平均':<8} {'最速':<8} {'最速タイヤ':<10}")
    print("-" * 50)
    for stat in driver_stats:
        print(f"{stat['Driver']:<15} {stat['Laps']:<6} {stat['Avg']:<8} {stat['Best']:<8} {stat['BestTire']:<10}")
    
    # コンパウンド統計
    print(f"\n🛞 コンパウンド別統計:")
    print("-" * 40)
    compound_stats = laps.groupby('Compound').agg({
        'LapTime': ['count', 'mean', 'min'],
        'Driver': 'nunique'
    }).round(2)
    
    compound_stats.columns = ['ラップ数', '平均タイム', '最速タイム', 'ドライバー数']
    compound_stats['平均タイム'] = compound_stats['平均タイム'].apply(lambda x: f"{x:.2f}s")
    compound_stats['最速タイム'] = compound_stats['最速タイム'].apply(lambda x: f"{x:.2f}s")
    
    print(compound_stats[['ラップ数', '平均タイム', '最速タイム', 'ドライバー数']])

# =============================================================================
# メイン実行関数
# =============================================================================
def main():
    """メイン実行関数"""
    print("🏎️  FastF1 複数ドライバー比較分析ツール")
    print("="*50)
    
    # キャッシュ設定
    setup_cache()
    
    # セッション設定（例）
    YEAR = 2024
    EVENT = 'Silverstone'  # イギリスGP
    SESSION_TYPE = 'R'     # 決勝
    
    # 分析対象ドライバー（変更可能）
    TARGET_DRIVERS = ['VER', 'NOR', 'PIA', 'RUS']  # Verstappen, Norris, Piastri, Russell
    
    # データ取得
    session, laps, drivers = get_session_data(YEAR, EVENT, SESSION_TYPE, TARGET_DRIVERS)
    
    if session is None or laps is None:
        print("❌ データ取得に失敗しました。")
        return
    
    # 統計表示
    print_session_stats(session, laps, drivers)
    
    # グラフ作成
    print(f"\n📈 グラフ作成中...")
    fig = create_comparison_plots(session, laps, drivers)
    
    print("✅ 分析完了！")
    
    # グラフ保存（オプション）
    save_path = f"{EVENT}_{YEAR}_{SESSION_TYPE}_analysis.png"
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"💾 グラフ保存: {save_path}")

# =============================================================================
# 実行
# =============================================================================
if __name__ == "__main__":
    main()