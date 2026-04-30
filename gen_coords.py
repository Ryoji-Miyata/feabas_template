import os

# ==========================================================
# 修正が必要なのは以下の2箇所だけです！
# ==========================================================

# 1. 生データが入っているフォルダのパス
RAW_IMAGE_FOLDER = "/fileserver/raw/data/"

# 2. あなたが作成した「作業フォルダ（working_dir）」のフルパス
MY_WORKING_DIR = "/data/nips/feabas_template"

# ==========================================================
# ここから下はこのままでOK（feabas手順書内のプロンプト内容に従っています。）
# ==========================================================

COORD_DIR = os.path.join(MY_WORKING_DIR, "stitch/stitch_coord")

# 画像パラメータ
WIDTH = 5120
HEIGHT = 3840
OVERLAP = 0.1
RESOLUTION = 5.0
COLS = 7
ROWS = 7

# 次のタイルまでの距離を計算 (10%重なり)
X_STEP = int(WIDTH * (1 - OVERLAP))
Y_STEP = int(HEIGHT * (1 - OVERLAP))

# 保存先フォルダがなければ作成
os.makedirs(COORD_DIR, exist_ok=True)

# 1枚目〜20枚目の切片についてループ
for s_num in range(1, 21):
    section_id = f"{s_num:02d}"  # 01, 02...
    output_filename = os.path.join(COORD_DIR, f"s{s_num:04d}.txt")
    
    with open(output_filename, "w") as f:
        # ヘッダー情報の書き込み (タブ区切り \t )
        f.write(f"{{ROOT_DIR}}\t{RAW_IMAGE_FOLDER}\n")
        f.write(f"{{RESOLUTION}}\t{RESOLUTION}\n")
        f.write(f"{{TILE_SIZE}}\t{HEIGHT}\t{WIDTH}\n") # 高さ 幅 の順
        
        # 0番〜48番のタイルについて座標を計算
        for t_idx in range(ROWS * COLS):
            row = t_idx // COLS
            col = t_idx % COLS
            
            x_pos = col * X_STEP
            y_pos = row * Y_STEP
            
            # 実際のファイル名：Project_01_0000.tif など
            img_name = f"Project_{section_id}_{t_idx:04d}.tif"
            
            # 画像データ行の書き込み
            f.write(f"{img_name}\t{x_pos}\t{y_pos}\n")

print(f"完了！ {COORD_DIR} に20個のファイルができました。")