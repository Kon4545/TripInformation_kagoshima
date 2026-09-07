# 旅のしおり ワイヤーフレーム JPEG 生成スクリプト
# Usage: python generate_wireframe.py
# Output: C:/Users/ABC/Desktop/wireframe_01_sitemap.jpg など
from PIL import Image, ImageDraw, ImageFont
import os

# ===== Colors =====
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
BG         = (248, 249, 250)
PANEL      = (240, 241, 243)
LINE       = (180, 185, 192)
LINE_DARK  = (120, 125, 132)
BLUE       = (26,  107, 154)
BLUE_LIGHT = (210, 228, 242)
GOLD       = (200, 140,  0 )
GOLD_LIGHT = (255, 240, 190)
RED        = (200,  50,  50)
RED_LIGHT  = (255, 220, 220)
GREEN      = (50,  140,  50)
GREEN_LIGHT= (210, 240, 210)
GRAY       = (140, 145, 150)
GRAY_LIGHT = (210, 212, 215)
DARK       = (40,  45,  55 )

# ===== Fonts =====
FONT_JP_PATH = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
FONT_EN_PATH = "C:/Windows/Fonts/ARIALN.TTF"

def get_font(size, bold=False, jp=True):
    path = "C:/Windows/Fonts/BIZ-UDGothicB.ttc" if bold and jp else \
           "C:/Windows/Fonts/ARIALNB.TTF" if bold else \
           FONT_JP_PATH if jp else FONT_EN_PATH
    try:
        return ImageFont.truetype(path, size)
    except:
        try:
            return ImageFont.truetype(FONT_JP_PATH, size)
        except:
            return ImageFont.load_default()

def text_w(draw, text, font):
    bbox = draw.textbbox((0,0), text, font=font)
    return bbox[2] - bbox[0]

def text_h(draw, text, font):
    bbox = draw.textbbox((0,0), text, font=font)
    return bbox[3] - bbox[1]

def draw_rect(draw, x, y, w, h, fill, outline=None, radius=0):
    if radius > 0:
        draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill, outline=outline)
    else:
        draw.rectangle([x, y, x+w, y+h], fill=fill, outline=outline)

def draw_text_center(draw, text, cx, y, font, color=DARK):
    w = text_w(draw, text, font)
    draw.text((cx - w//2, y), text, font=font, fill=color)

def draw_text_left(draw, text, x, y, font, color=DARK):
    draw.text((x, y), text, font=font, fill=color)

def draw_arrow(draw, x1, y1, x2, y2, color=BLUE, width=2):
    draw.line([(x1,y1),(x2,y2)], fill=color, width=width)
    # Arrowhead
    import math
    angle = math.atan2(y2-y1, x2-x1)
    al = 12
    aa = 0.4
    ax1 = int(x2 - al*math.cos(angle-aa))
    ay1 = int(y2 - al*math.sin(angle-aa))
    ax2 = int(x2 - al*math.cos(angle+aa))
    ay2 = int(y2 - al*math.sin(angle+aa))
    draw.polygon([(x2,y2),(ax1,ay1),(ax2,ay2)], fill=color)


# ====================================================
# PAGE WIREFRAME DEFINITIONS
# ====================================================
PAGES = [
    {
        "id": "index",
        "title": "① index.html",
        "subtitle": "トップページ",
        "sections_pc": [
            ("HEADER / NAV", BLUE, 0.08),
            ("ヒーローバナー（ツアータイトル・概要）", BLUE_LIGHT, 0.18),
            ("お客様情報カード", PANEL, 0.10),
            ("添乗員ご挨拶", PANEL, 0.10),
            ("集合・解散情報（2カラム）", GRAY_LIGHT, 0.12),
            ("含まれるもの / 含まれないもの（2カラム）", GRAY_LIGHT, 0.12),
            ("FOOTER", LINE, 0.06),
        ],
        "sections_mob": [
            ("HEADER / ☰", BLUE, 0.07),
            ("ヒーローバナー", BLUE_LIGHT, 0.16),
            ("お客様情報", PANEL, 0.10),
            ("ご挨拶", PANEL, 0.10),
            ("集合情報", GRAY_LIGHT, 0.10),
            ("解散情報", GRAY_LIGHT, 0.10),
            ("含む/含まない", GRAY_LIGHT, 0.11),
            ("FOOTER", LINE, 0.05),
        ],
    },
    {
        "id": "route",
        "title": "② route.html",
        "subtitle": "全体行程",
        "sections_pc": [
            ("HEADER / NAV", BLUE, 0.08),
            ("全体行程タイムライン（Day1・Day2）", GOLD_LIGHT, 0.22),
            ("ハイライト（3〜4カラムカード）", PANEL, 0.16),
            ("宿泊施設情報", GRAY_LIGHT, 0.14),
            ("FOOTER", LINE, 0.06),
        ],
        "sections_mob": [
            ("HEADER / ☰", BLUE, 0.07),
            ("行程タイムライン", GOLD_LIGHT, 0.22),
            ("ハイライト（1列）", PANEL, 0.20),
            ("宿泊施設情報", GRAY_LIGHT, 0.16),
            ("FOOTER", LINE, 0.05),
        ],
    },
    {
        "id": "day1",
        "title": "③ itinerary_day1.html",
        "subtitle": "Day1 詳細行程",
        "sections_pc": [
            ("HEADER / NAV", BLUE, 0.08),
            ("Day1 タイムライン（詳細）", GOLD_LIGHT, 0.30),
            ("Google Maps 埋め込み", BLUE_LIGHT, 0.20),
            ("FOOTER", LINE, 0.06),
        ],
        "sections_mob": [
            ("HEADER / ☰", BLUE, 0.07),
            ("Day1 タイムライン", GOLD_LIGHT, 0.34),
            ("Google Maps", BLUE_LIGHT, 0.22),
            ("FOOTER", LINE, 0.05),
        ],
    },
    {
        "id": "day2",
        "title": "④ itinerary_day2.html",
        "subtitle": "Day2 詳細行程",
        "sections_pc": [
            ("HEADER / NAV", BLUE, 0.08),
            ("Day2 タイムライン（詳細）", GOLD_LIGHT, 0.30),
            ("Google Maps 埋め込み", BLUE_LIGHT, 0.20),
            ("FOOTER", LINE, 0.06),
        ],
        "sections_mob": [
            ("HEADER / ☰", BLUE, 0.07),
            ("Day2 タイムライン", GOLD_LIGHT, 0.34),
            ("Google Maps", BLUE_LIGHT, 0.22),
            ("FOOTER", LINE, 0.05),
        ],
    },
    {
        "id": "caution",
        "title": "⑤ caution.html",
        "subtitle": "持ち物・注意事項",
        "sections_pc": [
            ("HEADER / NAV", BLUE, 0.08),
            ("持ち物リスト（必須・推奨チェックボックス）", GREEN_LIGHT, 0.18),
            ("Travel Tips（アコーディオン）", PANEL, 0.14),
            ("事故・緊急時の対応手順（ステップ）", RED_LIGHT, 0.20),
            ("FOOTER", LINE, 0.06),
        ],
        "sections_mob": [
            ("HEADER / ☰", BLUE, 0.07),
            ("持ち物リスト", GREEN_LIGHT, 0.20),
            ("Travel Tips", PANEL, 0.16),
            ("緊急対応手順", RED_LIGHT, 0.22),
            ("FOOTER", LINE, 0.05),
        ],
    },
    {
        "id": "company",
        "title": "⑥ company_information.html",
        "subtitle": "会社情報",
        "sections_pc": [
            ("HEADER / NAV", BLUE, 0.08),
            ("オリジナルグッズ紹介（カード）", GOLD_LIGHT, 0.18),
            ("SNS紹介（Instagram・X・YouTube・LINE）", PANEL, 0.14),
            ("緊急連絡先（大きく表示）", RED_LIGHT, 0.20),
            ("FOOTER", LINE, 0.06),
        ],
        "sections_mob": [
            ("HEADER / ☰", BLUE, 0.07),
            ("グッズ紹介（1列）", GOLD_LIGHT, 0.20),
            ("SNS リンク（1列）", PANEL, 0.18),
            ("緊急連絡先", RED_LIGHT, 0.20),
            ("FOOTER", LINE, 0.05),
        ],
    },
]

ADMIN_PAGE = {
    "id": "admin",
    "title": "⑦ admin.html",
    "subtitle": "管理画面",
}

# ====================================================
# DRAW FUNCTIONS
# ====================================================

def draw_page_wireframe_pc(draw, ox, oy, w, h, page):
    """Draw a PC-style wireframe for the given page at (ox,oy) with size (w,h)."""
    f_small  = get_font(13)
    f_tiny   = get_font(11)
    f_label  = get_font(14, bold=True)

    # Outer border
    draw_rect(draw, ox, oy, w, h, WHITE, LINE_DARK, radius=4)

    # Title bar above
    title_h = 28
    draw_rect(draw, ox, oy-title_h-4, w, title_h, BLUE, None, radius=4)
    draw_text_center(draw, page["title"], ox+w//2, oy-title_h-4+5, f_label, WHITE)

    # Browser chrome
    chrome_h = 22
    draw_rect(draw, ox, oy, w, chrome_h, PANEL, LINE)
    draw.ellipse([ox+6, oy+6, ox+14, oy+14], fill=(220,80,80))
    draw.ellipse([ox+18, oy+6, ox+26, oy+14], fill=(240,200,0))
    draw.ellipse([ox+30, oy+6, ox+38, oy+14], fill=(80,200,80))
    url_x = ox+48
    draw_rect(draw, url_x, oy+5, w-60, 12, WHITE, LINE_DARK)
    draw_text_left(draw, "localhost:3000/" + page["id"] + ".html", url_x+4, oy+6, get_font(8), GRAY)

    # Sections
    content_y = oy + chrome_h
    content_h = h - chrome_h
    total_ratio = sum(s[2] for s in page["sections_pc"])

    for sec_label, sec_color, sec_ratio in page["sections_pc"]:
        sec_h = int(content_h * sec_ratio / total_ratio)
        draw_rect(draw, ox+1, content_y, w-2, sec_h, sec_color, LINE)
        # Center text vertically
        th = text_h(draw, sec_label, f_small)
        ty = content_y + sec_h//2 - th//2
        draw_text_center(draw, sec_label, ox+w//2, ty, f_small, DARK)
        content_y += sec_h


def draw_page_wireframe_mobile(draw, ox, oy, w, h, page):
    """Draw a Mobile-style wireframe for the given page at (ox,oy) with size (w,h)."""
    f_small = get_font(11)
    f_tiny  = get_font(9)
    f_label = get_font(12, bold=True)

    # Outer border + phone shape
    draw_rect(draw, ox, oy, w, h, WHITE, LINE_DARK, radius=8)

    # Title bar above
    title_h = 24
    draw_rect(draw, ox, oy-title_h-4, w, title_h, BLUE, None, radius=4)
    draw_text_center(draw, page["title"], ox+w//2, oy-title_h-4+4, f_label, WHITE)

    # Phone notch
    notch_w = w//3
    draw_rect(draw, ox + w//2 - notch_w//2, oy, notch_w, 10, DARK, None, radius=3)

    # Status bar
    draw_rect(draw, ox, oy+10, w, 14, DARK)
    draw_text_center(draw, "9:41  ●●●●  WiFi", ox+w//2, oy+12, get_font(7), WHITE)

    # Sections
    content_y = oy + 24
    content_h = h - 24
    total_ratio = sum(s[2] for s in page["sections_mob"])

    for sec_label, sec_color, sec_ratio in page["sections_mob"]:
        sec_h = int(content_h * sec_ratio / total_ratio)
        draw_rect(draw, ox+1, content_y, w-2, sec_h, sec_color, LINE)
        th = text_h(draw, sec_label, f_tiny)
        ty = content_y + sec_h//2 - th//2
        draw_text_center(draw, sec_label, ox+w//2, ty, f_tiny, DARK)
        content_y += sec_h


# ====================================================
# IMAGE 1: SITE MAP
# ====================================================
def create_sitemap_image():
    W, H = 2400, 1600
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title  = get_font(48, bold=True)
    f_h2     = get_font(32, bold=True)
    f_h3     = get_font(24, bold=True)
    f_body   = get_font(22)
    f_small  = get_font(18)
    f_tiny   = get_font(16)
    f_badge  = get_font(14)

    # ---- Title ----
    draw_rect(draw, 0, 0, W, 90, BLUE)
    draw_text_center(draw, "旅のしおり  サイト構造図（サイトマップ）", W//2, 22, f_title, WHITE)
    draw_text_center(draw, "MOTO TOURS JAPAN  |  内部資料", W//2, 62, f_small, GOLD_LIGHT)

    # ---- Section label ----
    draw_text_left(draw, "【 データフロー 】", 60, 110, f_h2, DARK)
    draw.line([(60,148),(W-60,148)], fill=LINE_DARK, width=2)

    # ---- Data store box (center) ----
    ds_x, ds_y, ds_w, ds_h = W//2-160, 200, 320, 110
    draw_rect(draw, ds_x, ds_y, ds_w, ds_h, GOLD_LIGHT, GOLD, radius=8)
    draw_text_center(draw, "tour-data.js", W//2, ds_y+14, f_h3, DARK)
    draw_text_center(draw, "（デフォルトデータ）", W//2, ds_y+44, f_small, DARK)
    draw_rect(draw, ds_x+20, ds_y+70, ds_w-40, 26, WHITE, LINE, radius=4)
    draw_text_center(draw, "localStorage（編集データ上書き）", W//2, ds_y+76, f_tiny, GRAY)

    # ---- admin.html box (left) ----
    adm_x, adm_y, adm_w, adm_h = 80, 200, 260, 110
    draw_rect(draw, adm_x, adm_y, adm_w, adm_h, RED_LIGHT, RED, radius=8)
    draw_text_center(draw, "admin.html", adm_x+adm_w//2, adm_y+14, f_h3, DARK)
    draw_text_center(draw, "管理画面", adm_x+adm_w//2, adm_y+44, f_body, DARK)
    draw_text_center(draw, "（データ編集・保存）", adm_x+adm_w//2, adm_y+68, f_small, DARK)

    # Arrow: admin → datastore
    draw_arrow(draw, adm_x+adm_w, adm_y+adm_h//2, ds_x-6, ds_y+ds_h//2, RED, 3)
    draw_text_center(draw, "保存", adm_x+adm_w+50, adm_y+adm_h//2-22, f_tiny, RED)

    # ---- User pages (right side) ----
    pages_short = [
        ("index.html",            "トップページ",      BLUE_LIGHT),
        ("route.html",            "全体行程",          GOLD_LIGHT),
        ("itinerary_day1.html",   "Day1 詳細",         GOLD_LIGHT),
        ("itinerary_day2.html",   "Day2 詳細",         GOLD_LIGHT),
        ("caution.html",          "注意事項",          GREEN_LIGHT),
        ("company_information.html","会社情報",        PANEL),
    ]
    pg_w, pg_h = 280, 80
    pg_cols = 2
    pg_start_x = W - 80 - pg_w*pg_cols - 30
    pg_start_y = 170

    pg_positions = []
    for i, (fname, label, color) in enumerate(pages_short):
        col = i % pg_cols
        row = i // pg_cols
        px = pg_start_x + col*(pg_w+30)
        py = pg_start_y + row*(pg_h+20)
        draw_rect(draw, px, py, pg_w, pg_h, color, BLUE, radius=8)
        draw_text_center(draw, fname, px+pg_w//2, py+12, f_small, DARK)
        draw_text_center(draw, label, px+pg_w//2, py+40, f_body, DARK)
        pg_positions.append((px, py, pg_w, pg_h))
        # Arrow from data store to page
        tx = px
        ty = py + pg_h//2
        sx = ds_x + ds_w + 6
        sy = ds_y + ds_h//2
        draw_arrow(draw, sx, sy, tx, ty, BLUE, 2)

    draw_text_center(draw, "getData()\n読み込み", ds_x+ds_w+80, ds_y+ds_h//2-22, f_tiny, BLUE)

    # ---- Navigation links between user pages ----
    nav_y_base = pg_start_y + 3*(pg_h+20) + pg_h + 50
    draw.line([(60, nav_y_base-20),(W-60, nav_y_base-20)], fill=LINE, width=1)

    # ---- Section 2: Navigation structure ----
    draw_text_left(draw, "【 ナビゲーション構造 】", 60, nav_y_base, f_h2, DARK)

    nav_pages = ["index", "route", "day1", "day2", "caution", "company"]
    nav_labels = ["トップ", "行程概要", "Day1", "Day2", "注意事項", "会社情報"]
    nav_colors = [BLUE_LIGHT, GOLD_LIGHT, GOLD_LIGHT, GOLD_LIGHT, GREEN_LIGHT, PANEL]

    nw, nh = 300, 70
    nx_start = (W - len(nav_pages)*(nw+20) + 20) // 2
    ny = nav_y_base + 50

    for i, (pid, plabel, pcolor) in enumerate(zip(nav_pages, nav_labels, nav_colors)):
        nx = nx_start + i*(nw+20)
        draw_rect(draw, nx, ny, nw, nh, pcolor, BLUE, radius=8)
        draw_text_center(draw, pid+".html", nx+nw//2, ny+8, f_small, DARK)
        draw_text_center(draw, plabel, nx+nw//2, ny+34, f_body, DARK)
        # Arrow to next
        if i < len(nav_pages)-1:
            draw_arrow(draw, nx+nw, ny+nh//2, nx+nw+20, ny+nh//2, BLUE, 2)

    # Mutual navigation note
    draw_text_center(draw, "← 全ページ共通ナビゲーションバーで相互移動可能 →", W//2, ny+nh+18, f_small, BLUE)

    # ---- Section 3: Admin structure ----
    adm2_y = ny + nh + 80
    draw.line([(60, adm2_y-20),(W-60, adm2_y-20)], fill=LINE, width=1)
    draw_text_left(draw, "【 管理画面（admin.html）タブ構成 】", 60, adm2_y, f_h2, DARK)

    tabs = [
        ("基本情報タブ", "ツアー名・日程・\nお客様名・担当者", BLUE_LIGHT),
        ("行程タブ", "Day1/Day2 の\nスケジュール編集", GOLD_LIGHT),
        ("持ち物タブ", "持ち物リスト・\nTips・緊急手順", GREEN_LIGHT),
        ("会社情報タブ", "グッズ・SNS・\n緊急連絡先", PANEL),
        ("宿泊タブ", "ホテル情報\nチェックイン/アウト", GOLD_LIGHT),
        ("ハイライトタブ", "ツアー見どころ\nカード管理", BLUE_LIGHT),
    ]
    tw = 340
    th = 100
    tx_start = (W - len(tabs)*(tw+20) + 20) // 2
    ty = adm2_y + 50

    for i, (tname, tdesc, tcolor) in enumerate(tabs):
        tx = tx_start + i*(tw+20)
        draw_rect(draw, tx, ty, tw, th, tcolor, LINE_DARK, radius=8)
        draw_text_center(draw, tname, tx+tw//2, ty+10, f_body, DARK)
        for j, line in enumerate(tdesc.split("\n")):
            draw_text_center(draw, line, tx+tw//2, ty+40+j*24, f_small, GRAY)

    # Footer
    draw_rect(draw, 0, H-40, W, 40, DARK)
    draw_text_center(draw, "MOTO TOURS JAPAN  旅のしおり ワイヤーフレーム資料  ©2026", W//2, H-30, f_tiny, GRAY_LIGHT)

    return img


# ====================================================
# IMAGE 2: PC WIREFRAMES
# ====================================================
def create_pc_wireframes_image():
    COLS = 3
    ROWS = 2
    PW, PH = 580, 500  # wireframe box size
    PAD_X, PAD_Y = 60, 80
    TITLE_H = 50
    HEADER_H = 100

    W = PAD_X*2 + COLS*PW + (COLS-1)*PAD_X
    H = HEADER_H + ROWS*(TITLE_H + PH + PAD_Y) + 60

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title  = get_font(40, bold=True)
    f_small  = get_font(16)
    f_sub    = get_font(20)

    # Header
    draw_rect(draw, 0, 0, W, HEADER_H, BLUE)
    draw_text_center(draw, "旅のしおり  ワイヤーフレーム  ─  PC レイアウト（デスクトップ表示）", W//2, 18, f_title, WHITE)
    draw_text_center(draw, "画面幅 1280px 基準  |  MOTO TOURS JAPAN", W//2, 65, f_small, GOLD_LIGHT)

    for i, page in enumerate(PAGES):
        col = i % COLS
        row = i // COLS
        ox = PAD_X + col*(PW + PAD_X)
        oy = HEADER_H + PAD_Y//2 + row*(PH + TITLE_H + PAD_Y)
        draw_page_wireframe_pc(draw, ox, oy + TITLE_H, PW, PH, page)
        # subtitle below
        draw_text_center(draw, page["subtitle"], ox+PW//2, oy + TITLE_H + PH + 8, f_sub, GRAY)

    # Footer
    draw_rect(draw, 0, H-36, W, 36, DARK)
    draw_text_center(draw, "MOTO TOURS JAPAN  旅のしおり ワイヤーフレーム資料  ©2026", W//2, H-26, get_font(14), GRAY_LIGHT)

    return img


# ====================================================
# IMAGE 3: MOBILE WIREFRAMES
# ====================================================
def create_mobile_wireframes_image():
    COLS = 3
    ROWS = 2
    PW, PH = 260, 520  # mobile wireframe size
    PAD_X, PAD_Y = 60, 80
    TITLE_H = 50
    HEADER_H = 100

    W = PAD_X*2 + COLS*PW + (COLS-1)*PAD_X
    H = HEADER_H + ROWS*(TITLE_H + PH + PAD_Y) + 60

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title  = get_font(38, bold=True)
    f_small  = get_font(16)
    f_sub    = get_font(18)

    # Header
    draw_rect(draw, 0, 0, W, HEADER_H, BLUE)
    draw_text_center(draw, "旅のしおり  ワイヤーフレーム  ─  モバイル レイアウト（スマートフォン表示）", W//2, 18, f_title, WHITE)
    draw_text_center(draw, "画面幅 375px 基準  |  MOTO TOURS JAPAN", W//2, 65, f_small, GOLD_LIGHT)

    for i, page in enumerate(PAGES):
        col = i % COLS
        row = i // COLS
        ox = PAD_X + col*(PW + PAD_X)
        oy = HEADER_H + PAD_Y//2 + row*(PH + TITLE_H + PAD_Y)
        draw_page_wireframe_mobile(draw, ox, oy + TITLE_H, PW, PH, page)
        draw_text_center(draw, page["subtitle"], ox+PW//2, oy + TITLE_H + PH + 8, f_sub, GRAY)

    # Footer
    draw_rect(draw, 0, H-36, W, 36, DARK)
    draw_text_center(draw, "MOTO TOURS JAPAN  旅のしおり ワイヤーフレーム資料  ©2026", W//2, H-26, get_font(14), GRAY_LIGHT)

    return img


# ====================================================
# IMAGE 4: ADMIN PAGE WIREFRAME
# ====================================================
def create_admin_image():
    W, H = 2400, 1400
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title  = get_font(44, bold=True)
    f_h2     = get_font(30, bold=True)
    f_h3     = get_font(24, bold=True)
    f_body   = get_font(20)
    f_small  = get_font(17)
    f_tiny   = get_font(14)

    # Header
    draw_rect(draw, 0, 0, W, 90, BLUE)
    draw_text_center(draw, "旅のしおり  ワイヤーフレーム  ─  管理画面（admin.html）", W//2, 18, f_title, WHITE)
    draw_text_center(draw, "MOTO TOURS JAPAN  管理者専用", W//2, 62, f_small, GOLD_LIGHT)

    # ---- Login Screen ----
    sec_x = 60
    sec_y = 120
    draw_text_left(draw, "【 ログイン画面 】", sec_x, sec_y, f_h2, DARK)

    login_x, login_y, login_w, login_h = 60, sec_y+50, 500, 380
    draw_rect(draw, login_x, login_y, login_w, login_h, WHITE, LINE_DARK, radius=8)
    draw_rect(draw, login_x, login_y, login_w, 50, BLUE, None, radius=8)
    draw_text_center(draw, "MOTO TOURS JAPAN 管理画面", login_x+login_w//2, login_y+14, f_small, WHITE)

    logo_y = login_y + 70
    draw_rect(draw, login_x+150, logo_y, 200, 50, BLUE_LIGHT, LINE, radius=8)
    draw_text_center(draw, "ロゴ", login_x+login_w//2, logo_y+14, f_body, DARK)

    for j, (label, ftype) in enumerate([("管理者パスワード", "password"), ("", "")]):
        if not label: continue
        ly = logo_y + 80 + j*70
        draw_text_left(draw, label, login_x+30, ly, f_small, DARK)
        draw_rect(draw, login_x+30, ly+26, login_w-60, 34, WHITE, LINE_DARK, radius=4)
        draw_text_left(draw, "••••••••", login_x+42, ly+32, f_body, GRAY)

    btn_y = logo_y + 220
    draw_rect(draw, login_x+80, btn_y, login_w-160, 44, BLUE, None, radius=6)
    draw_text_center(draw, "ログイン", login_x+login_w//2, btn_y+10, f_h3, WHITE)

    draw_text_center(draw, "※ パスワードは社内システムで管理", login_x+login_w//2, btn_y+60, f_tiny, GRAY)

    # ---- Main Admin UI ----
    main_x = 620
    main_y = sec_y + 50
    main_w = W - main_x - 60
    main_h = H - main_y - 80

    draw_text_left(draw, "【 管理画面メイン 】", main_x, sec_y, f_h2, DARK)
    draw_rect(draw, main_x, main_y, main_w, main_h, WHITE, LINE_DARK, radius=8)

    # Top bar
    topbar_h = 52
    draw_rect(draw, main_x, main_y, main_w, topbar_h, BLUE, None, radius=8)
    draw_text_left(draw, "MOTO TOURS JAPAN  管理画面", main_x+20, main_y+14, f_h3, WHITE)
    draw_rect(draw, main_x+main_w-180, main_y+10, 150, 32, RED_LIGHT, RED, radius=6)
    draw_text_center(draw, "ログアウト", main_x+main_w-105, main_y+16, f_small, RED)

    # Sidebar
    sidebar_w = 220
    sidebar_x = main_x
    sidebar_y = main_y + topbar_h
    sidebar_h = main_h - topbar_h
    draw_rect(draw, sidebar_x, sidebar_y, sidebar_w, sidebar_h, DARK, None)

    sidebar_items = [
        ("基本情報", "fa-circle-info", BLUE_LIGHT),
        ("行程（Day1）", "fa-calendar", GOLD_LIGHT),
        ("行程（Day2）", "fa-calendar", GOLD_LIGHT),
        ("持ち物・注意", "fa-triangle-exclamation", GREEN_LIGHT),
        ("会社情報", "fa-building", PANEL),
        ("宿泊施設", "fa-hotel", GOLD_LIGHT),
        ("ハイライト", "fa-star", BLUE_LIGHT),
    ]
    for j, (name, icon, color) in enumerate(sidebar_items):
        item_y = sidebar_y + j*58
        is_active = (j == 0)
        bg = BLUE if is_active else DARK
        draw_rect(draw, sidebar_x, item_y, sidebar_w, 58, bg, None)
        if is_active:
            draw_rect(draw, sidebar_x, item_y, 4, 58, GOLD, None)
        draw_text_left(draw, "  " + name, sidebar_x+16, item_y+18, f_body, WHITE if not is_active else GOLD_LIGHT)

    # Content area
    content_x = sidebar_x + sidebar_w + 1
    content_y = main_y + topbar_h
    content_w = main_w - sidebar_w - 1
    content_h = main_h - topbar_h
    draw_rect(draw, content_x, content_y, content_w, content_h, BG, None)

    # Form area
    form_pad = 24
    draw_text_left(draw, "基本情報 編集", content_x+form_pad, content_y+form_pad, f_h2, DARK)

    fields = [
        ("ツアー名", "京都・大阪 歴史と食の旅 2日間"),
        ("出発日", "2026年4月10日"),
        ("帰着日", "2026年4月11日"),
        ("お客様名", "山田 太郎 様"),
        ("参加人数", "2名"),
        ("担当添乗員", "佐藤 花子"),
    ]
    for j, (flabel, fval) in enumerate(fields):
        fx = content_x + form_pad
        fy = content_y + form_pad + 60 + j*68
        if fy + 50 > content_y + content_h - 80: break
        draw_text_left(draw, flabel, fx, fy, f_small, GRAY)
        draw_rect(draw, fx, fy+22, content_w-form_pad*2, 36, WHITE, LINE_DARK, radius=4)
        draw_text_left(draw, fval, fx+10, fy+30, f_body, DARK)

    # Save button
    save_y = content_y + content_h - 70
    draw_rect(draw, content_x+form_pad, save_y, 200, 44, BLUE, None, radius=6)
    draw_text_center(draw, "保存する", content_x+form_pad+100, save_y+10, f_h3, WHITE)
    draw_rect(draw, content_x+form_pad+220, save_y, 200, 44, GRAY_LIGHT, LINE, radius=6)
    draw_text_center(draw, "リセット", content_x+form_pad+320, save_y+10, f_h3, DARK)

    # Footer
    draw_rect(draw, 0, H-40, W, 40, DARK)
    draw_text_center(draw, "MOTO TOURS JAPAN  旅のしおり ワイヤーフレーム資料  ©2026", W//2, H-30, f_tiny, GRAY_LIGHT)

    return img


# ====================================================
# MAIN
# ====================================================
if __name__ == "__main__":
    out_dir = r"C:\Users\ABC\Desktop"

    print("生成中: ① サイトマップ...")
    img1 = create_sitemap_image()
    img1.save(os.path.join(out_dir, "wireframe_01_sitemap.jpg"), "JPEG", quality=92)
    print(f"  → 保存: {out_dir}\\wireframe_01_sitemap.jpg  ({img1.width}x{img1.height})")

    print("生成中: ② PC レイアウト...")
    img2 = create_pc_wireframes_image()
    img2.save(os.path.join(out_dir, "wireframe_02_pc.jpg"), "JPEG", quality=92)
    print(f"  → 保存: {out_dir}\\wireframe_02_pc.jpg  ({img2.width}x{img2.height})")

    print("生成中: ③ モバイル レイアウト...")
    img3 = create_mobile_wireframes_image()
    img3.save(os.path.join(out_dir, "wireframe_03_mobile.jpg"), "JPEG", quality=92)
    print(f"  → 保存: {out_dir}\\wireframe_03_mobile.jpg  ({img3.width}x{img3.height})")

    print("生成中: ④ 管理画面...")
    img4 = create_admin_image()
    img4.save(os.path.join(out_dir, "wireframe_04_admin.jpg"), "JPEG", quality=92)
    print(f"  → 保存: {out_dir}\\wireframe_04_admin.jpg  ({img4.width}x{img4.height})")

    print("\n✓ 完了！デスクトップに4枚のJPEGファイルを保存しました。")
