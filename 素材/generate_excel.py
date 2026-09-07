import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
import os

OUT = r"C:\Users\ABC\Desktop\旅のしおり_編集シート.xlsx"

# ===== Color palette =====
C_NAVY   = "1A3A5C"   # ヘッダー背景（濃紺）
C_BLUE   = "2E6DA4"   # セクション背景
C_GOLD   = "C89B2A"   # アクセント
C_YELLOW = "FFF9C4"   # 入力セル背景
C_INPUT  = "FFFDE7"   # サブ入力
C_GRAY   = "F5F5F5"   # 奇数行
C_WHITE  = "FFFFFF"
C_RED    = "C0392B"   # 必須ラベル
C_GREEN  = "27AE60"
C_LABEL  = "E8F4FD"   # ラベル行

# ===== Fonts =====
def fnt(size=10, bold=False, color="000000", italic=False):
    return Font(name="Arial", size=size, bold=bold, color=color, italic=italic)

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def border_all(thin=True):
    s = Side(style="thin" if thin else "medium", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def aln(h="left", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def set_cell(ws, row, col, value, font=None, bg=None, align=None, border=None):
    c = ws.cell(row=row, column=col, value=value)
    if font:   c.font = font
    if bg:     c.fill = fill(bg)
    if align:  c.alignment = align
    if border: c.border = border
    return c

def header_row(ws, row, cols_data, bg=C_NAVY):
    for col, (val, width) in enumerate(cols_data, 1):
        c = set_cell(ws, row, col, val,
                     font=fnt(10, bold=True, color="FFFFFF"),
                     bg=bg,
                     align=aln("center"),
                     border=border_all())
        ws.column_dimensions[get_column_letter(col)].width = width

def section_title(ws, row, col_start, col_end, text, bg=C_BLUE):
    ws.merge_cells(start_row=row, start_column=col_start,
                   end_row=row, end_column=col_end)
    c = ws.cell(row=row, column=col_start, value=text)
    c.font = fnt(11, bold=True, color="FFFFFF")
    c.fill = fill(bg)
    c.alignment = aln("left", "center")
    c.border = border_all()

def input_row(ws, row, label, value, note="", row_bg=C_WHITE):
    set_cell(ws, row, 1, label,
             font=fnt(10, bold=True),
             bg=C_LABEL,
             align=aln("left", "center"),
             border=border_all())
    c = set_cell(ws, row, 2, value,
                 font=fnt(10),
                 bg=C_YELLOW,
                 align=aln("left", "center", wrap=True),
                 border=border_all())
    if note:
        set_cell(ws, row, 3, note,
                 font=fnt(9, italic=True, color="666666"),
                 bg=C_WHITE,
                 align=aln("left", "center", wrap=True))
    ws.row_dimensions[row].height = 22

def sheet_title(ws, title, subtitle=""):
    ws.merge_cells("A1:J1")
    c = ws["A1"]
    c.value = title
    c.font = fnt(14, bold=True, color="FFFFFF")
    c.fill = fill(C_NAVY)
    c.alignment = aln("center")
    ws.row_dimensions[1].height = 34
    if subtitle:
        ws.merge_cells("A2:J2")
        c2 = ws["A2"]
        c2.value = subtitle
        c2.font = fnt(9, italic=True, color="FFFFFF")
        c2.fill = fill(C_BLUE)
        c2.alignment = aln("center")
        ws.row_dimensions[2].height = 18
        return 3
    return 2

def notice_row(ws, row, text, cols=10):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=cols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = fnt(9, color=C_RED)
    c.fill = fill("FFF3E0")
    c.alignment = aln("left", "center")
    ws.row_dimensions[row].height = 18

# ============================================================
# SHEET 1: 基本情報
# ============================================================
def build_basic(wb):
    ws = wb.create_sheet("①基本情報")
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 36

    r = sheet_title(ws, "①  基本情報", "ツアー名・お客様情報・日程などの基本情報を入力してください")
    notice_row(ws, r, "  ★ 黄色のセルに入力してください。グレーのセルはラベルです（編集不要）。", 3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ ツアー情報"); r += 1
    input_row(ws, r, "ツアー名（大）", "HondaGO TOUR in 伊豆箱根", "例：HondaGO TOUR in 北海道"); r += 1
    input_row(ws, r, "ツアー名（サブ）", "富士を望み、名道を駆ける3日間", "キャッチコピー・サブタイトル"); r += 1
    input_row(ws, r, "エリア", "伊豆・箱根", "例：北海道・道東"); r += 1
    input_row(ws, r, "ツアー期間", "2026年4月10日（金）〜 4月12日（日）", "例：2026年7月10日（金）〜 7月12日（日）"); r += 1

    section_title(ws, r, 1, 3, "  ■ お客様情報"); r += 1
    input_row(ws, r, "お客様名", "近藤 一聖", "フルネームで入力（例：田中 花子）"); r += 1
    input_row(ws, r, "参加人数", "1名様", "例：2名様、3名様"); r += 1

    section_title(ws, r, 1, 3, "  ■ ヒーロー画像"); r += 1
    input_row(ws, r, "ヒーロー画像", "（admin.htmlのヒーロー画像アップロードから設定）", "トップページの背景画像。管理画面からアップロード。"); r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 2: 集合・解散情報
# ============================================================
def build_meeting(wb):
    ws = wb.create_sheet("②集合・解散")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 36

    r = sheet_title(ws, "②  集合・解散情報", "集合場所・時間・解散情報・送迎シャトルの設定")
    notice_row(ws, r, "  ★ Google Maps の埋め込みURLはGoogleマップで「共有」→「地図を埋め込む」からコピーしてください。", 3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ 集合情報"); r += 1
    input_row(ws, r, "集合場所", "バイカーズパラダイス南箱根", "施設名・店名"); r += 1
    input_row(ws, r, "集合場所詳細（住所）", "静岡県駿東郡小山町桑木1348-2", "住所・フロア・建物名など"); r += 1
    input_row(ws, r, "集合日", "2026年4月10日（金）", "例：2026年7月10日（金）"); r += 1
    input_row(ws, r, "集合時間", "午前 10:00", "例：午前 9:30"); r += 1
    input_row(ws, r, "集合場所 地図URL", "https://www.google.com/maps/embed?pb=...", "Googleマップのiframe src属性のURLをコピー"); r += 1
    ws.row_dimensions[r-1].height = 28

    section_title(ws, r, 1, 3, "  ■ 解散情報"); r += 1
    input_row(ws, r, "解散場所", "バイカーズパラダイス南箱根", "施設名"); r += 1
    input_row(ws, r, "解散日時", "2026年4月12日（日）17:00 頃", "例：2026年7月12日（日）16:00頃"); r += 1
    input_row(ws, r, "解散場所 地図URL", "https://www.google.com/maps/embed?pb=...", "Googleマップのiframe src属性のURLをコピー"); r += 1
    ws.row_dimensions[r-1].height = 28
    input_row(ws, r, "集合に関する注意事項", "集合時間の10分前にはお集まりください。また解散後はバイカーズパラダイス南箱根から小山町への送迎がございます。", "注意事項・補足情報"); r += 1
    ws.row_dimensions[r-1].height = 40

    section_title(ws, r, 1, 3, "  ■ シャトル送迎（あり / なし）"); r += 1
    input_row(ws, r, "シャトル送迎", "あり", "「あり」または「なし」"); r += 1
    input_row(ws, r, "シャトル案内文", "集合場所まで送迎希望の方は、午前9:00までに小山町コミュニティーバスまでお集まりください。", ""); r += 1
    ws.row_dimensions[r-1].height = 36

    section_title(ws, r, 1, 3, "  ■ シャトル乗車地点（複数ある場合は行を追加）"); r += 1
    header_row(ws, r, [("乗車地点名", 28), ("乗車時間", 14), ("備考・メモ", 36), ("地図URL", 36)], bg=C_BLUE); r += 1

    pickups = [
        ("小山町コミュニティーバス", "9:00", "北口早川駐車場付近", "https://www.google.com/maps/embed?pb=..."),
    ]
    for i, (place, time, note, url) in enumerate(pickups):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([place, time, note, url], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "center", wrap=True)
            c.border = border_all()
        r += 1
    ws.freeze_panes = "A4"

# ============================================================
# SHEET 3: 添乗員情報
# ============================================================
def build_guide(wb):
    ws = wb.create_sheet("③添乗員情報")
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 36

    r = sheet_title(ws, "③  添乗員情報", "担当添乗員のプロフィール・連絡先・ご挨拶文を入力してください")
    notice_row(ws, r, "  ★ 添乗員が複数いる場合は、admin.htmlの「担当添乗員」タブから追加してください。", 3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ 担当添乗員（1人目）"); r += 1
    input_row(ws, r, "氏名", "鈴木 花子", "フルネーム"); r += 1
    input_row(ws, r, "役職・所属", "ガイド添乗員 / MOTO TOURS JAPAN アテンダントスタッフ", "例：ガイド / MOTO TOURS JAPAN スタッフ"); r += 1
    input_row(ws, r, "電話番号", "050-1742-3855", "ハイフンあり"); r += 1
    input_row(ws, r, "メールアドレス", "inquiry@mototoursjapan.com", ""); r += 1
    input_row(ws, r, "LINE ID", "@638nrfza", "@から始まるLINE公式アカウントID"); r += 1

    section_title(ws, r, 1, 3, "  ■ ご挨拶文"); r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=1)
    set_cell(ws, r, 1, "ご挨拶文（本文）",
             font=fnt(10, bold=True), bg=C_LABEL, align=aln("left", "top"), border=border_all())
    greeting = (
        "お客様\n\n"
        "このたびは「HondaGO TOUR in 伊豆箱根」にご参加いただき\\\nありがとうございます。\n\n"
        "今回の旅では、ライダーに人気の日本のシンボル「富士山」を眺める"
        "絶景ルートを走り、伊豆の山々も楽しみます。\n\n"
        "MOTO TOURS JAPAN\nスタッフ一同"
    )
    c = ws.cell(row=r, column=2, value=greeting)
    c.font = fnt(10)
    c.fill = fill(C_YELLOW)
    c.alignment = aln("left", "top", wrap=True)
    c.border = border_all()
    set_cell(ws, r, 3, "改行は Ctrl+Enter で入力できます。",
             font=fnt(9, italic=True, color="666666"),
             bg=C_WHITE, align=aln("left", "top", wrap=True))
    ws.row_dimensions[r].height = 120
    r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 4: 含む・含まない
# ============================================================
def build_includes(wb):
    ws = wb.create_sheet("④含む・含まない")
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 46
    ws.column_dimensions["C"].width = 46

    r = sheet_title(ws, "④  含むもの・含まないもの", "ツアーに含まれるもの・含まれないものを箇条書きで入力してください")
    notice_row(ws, r, "  ★ 行を追加・削除してください。含む項目は B列、含まない項目は C列に1行1項目で入力。", 3)
    r += 1

    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=2)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=3)
    set_cell(ws, r, 2, "含まれるもの ✔", font=fnt(11, bold=True, color="FFFFFF"),
             bg=C_GREEN, align=aln("center"), border=border_all())
    set_cell(ws, r, 3, "含まれないもの ✗", font=fnt(11, bold=True, color="FFFFFF"),
             bg=C_RED, align=aln("center"), border=border_all())
    r += 1

    includes = [
        "2泊宿泊費（各ホテル・1室1泊朝食付）",
        "食費 (朝食2回・昼食3回・夕食2回)",
        "旅行傷害保険（全期間）",
        "おみやげ代（本ページ）",
        "バイク代含む損害保険（3日間）",
    ]
    excludes = [
        "夕食時のドリンク代",
        "個人的土産・任意な保険料",
        "集合地までの交通費",
        "追加オプション（オプションでご購入可）",
    ]

    max_rows = max(len(includes), len(excludes))
    for i in range(max_rows):
        inc_val = includes[i] if i < len(includes) else ""
        exc_val = excludes[i] if i < len(excludes) else ""
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        set_cell(ws, r, 1, i+1, font=fnt(9, color="999999"), bg=bg, align=aln("center"))
        set_cell(ws, r, 2, inc_val, font=fnt(10), bg=C_YELLOW, align=aln("left", "center", wrap=True), border=border_all())
        set_cell(ws, r, 3, exc_val, font=fnt(10), bg=C_YELLOW, align=aln("left", "center", wrap=True), border=border_all())
        ws.row_dimensions[r].height = 22
        r += 1

    ws.freeze_panes = "B4"

# ============================================================
# SHEET 5-7: Day行程
# ============================================================
def build_day(wb, day_num, date_val, theme_val, items):
    ws = wb.create_sheet(f"⑤Day{day_num}行程" if day_num == 1 else
                          f"⑥Day{day_num}行程" if day_num == 2 else f"⑦Day{day_num}行程")
    ws.column_dimensions["A"].width = 10  # 時刻
    ws.column_dimensions["B"].width = 26  # 場所名
    ws.column_dimensions["C"].width = 18  # 場所
    ws.column_dimensions["D"].width = 44  # 説明
    ws.column_dimensions["E"].width = 14  # バッジ
    ws.column_dimensions["F"].width = 14  # バッジ種別
    ws.column_dimensions["G"].width = 14  # ハイライト

    r = sheet_title(ws, f"⑤  Day{day_num} 行程スケジュール" if day_num == 1 else
                        f"⑥  Day{day_num} 行程スケジュール" if day_num == 2 else
                        f"⑦  Day{day_num} 行程スケジュール",
                    "各スポットの時刻・場所・説明を入力してください")
    notice_row(ws, r, "  ★ バッジ種別：red（赤）/ gold（金）/ blue（青）/ green（緑）/ 空白（なし）。ハイライト：yes/no", 7)
    r += 1

    section_title(ws, r, 1, 7, "  ■ Day基本情報"); r += 1
    input_row(ws, r, "日付", date_val, "例：2026年7月10日（金）"); r += 1
    ws.merge_cells(start_row=r-1, start_column=2, end_row=r-1, end_column=7)

    input_row(ws, r, "テーマ（サブタイトル）", theme_val, "例：富士山を眺めながら名道を駆ける"); r += 1
    ws.merge_cells(start_row=r-1, start_column=2, end_row=r-1, end_column=7)

    input_row(ws, r, "Googleマップ URL", "https://www.google.com/maps/embed?pb=...", "Day全体のルートマップのiframe src URL"); r += 1
    ws.merge_cells(start_row=r-1, start_column=2, end_row=r-1, end_column=7)
    ws.row_dimensions[r-1].height = 28

    section_title(ws, r, 1, 7, "  ■ スケジュール一覧"); r += 1
    header_row(ws, r, [
        ("時刻", 10), ("スポット名", 26), ("場所・施設名", 18),
        ("説明・詳細", 44), ("バッジ表示", 14), ("バッジ種別", 14), ("ハイライト", 14)
    ], bg=C_BLUE)
    r += 1

    for i, item in enumerate(items):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([
            item.get("time",""), item.get("title",""), item.get("place",""),
            item.get("desc",""), item.get("badge",""), item.get("badgeType",""),
            "yes" if item.get("isHighlight") else "no"
        ], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 26
        r += 1

    ws.freeze_panes = "A7"

# ============================================================
# SHEET 8: ハイライト
# ============================================================
def build_highlights(wb):
    ws = wb.create_sheet("⑧ハイライト")
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 46
    ws.column_dimensions["D"].width = 28

    r = sheet_title(ws, "⑧  ツアー ハイライト", "ツアーの見どころカード（route.htmlに表示）を設定してください")
    notice_row(ws, r, "  ★ 画像はadmin.htmlのハイライトタブから各カードにアップロードしてください。アイコンはFont Awesomeクラス名。", 4)
    r += 1

    section_title(ws, r, 1, 4, "  ■ ハイライト一覧"); r += 1
    header_row(ws, r, [("No.", 4), ("見出し", 28), ("説明文", 46), ("Font Awesomeアイコン", 28)], bg=C_BLUE)
    r += 1

    highlights = [
        ("伊豆スカイライン", "富士山や駿河湾を眺めながら爽快な大空を楽しめる、伊豆随一の絶景ルート", "fa-solid fa-motorcycle"),
        ("内浦 (木負 大村屋)", "昔ながらの木造建物で大村屋の雰囲気が、老舗の技とともに迎えてくれるお店", "fa-solid fa-house"),
        ("わさび屋 峰の家", "伊豆の特産物であるわさびを使ったわさびづくし料理で、幸の思い出として喜べる人気", "fa-solid fa-cart-shopping"),
        ("グラスカイウォーク", "かんざんじ湖周辺の上から、浜松・伊豆エリアの麓の田園風景を眺められる魅惑的な場所", "fa-solid fa-bridge"),
        ("わなかいとところ", "丁寧に仕上げた肴とともに料理を楽しんで、和の味わいを演じられる人気のお店", "fa-solid fa-utensils"),
    ]
    for i, (title, desc, icon) in enumerate(highlights):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([i+1, title, desc, icon], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW) if col > 1 else fill(bg)
            c.alignment = aln("left" if col > 1 else "center", "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 26
        r += 1

    ws.freeze_panes = "B4"

# ============================================================
# SHEET 9: 宿泊施設
# ============================================================
def build_hotels(wb):
    ws = wb.create_sheet("⑨宿泊施設")
    cols = [("宿泊夜", 18), ("ホテル名", 26), ("住所", 32), ("星数(1-5)", 10),
            ("電話番号", 16), ("チェックイン", 14), ("チェックアウト", 14),
            ("WiFi(yes/no)", 12), ("説明文", 36), ("公式サイトURL", 32)]
    for i, (_, w) in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    r = sheet_title(ws, "⑨  宿泊施設情報", "ツアー中の宿泊ホテル情報を入力してください（写真はadmin.htmlからアップロード）")
    notice_row(ws, r, "  ★ 宿泊夜は「1泊目（Day1→Day2）」のように記載。写真はadmin.htmlの宿泊タブからアップロード。", 10)
    r += 1

    header_row(ws, r, cols, bg=C_BLUE); r += 1

    hotels = [
        ("1泊目（Day1→Day2）", "ホテルニューアカオ", "〒413-0033 静岡県熱海市熱海1993-250",
         4, "0557-83-6161", "15:00〜", "〜10:00", "yes",
         "伊豆に馴染むような景色と海辺、美食と温泉を満喫できる人気の老舗リゾートホテル",
         "https://hotel-new-akao.com/"),
        ("2泊目（Day2→Day3）", "ホテルニュー銀水", "〒410-3514 静岡県伊豆市堂ヶ島2977-1",
         3, "0558-52-2211", "14:00〜", "〜10:00", "yes",
         "伊豆の美しい海岸を眺めながら、穏やかと上質な温泉でゆったりくつろげる人気の宿",
         "https://www.dougashima-newginsui.jp/"),
    ]
    for i, row_data in enumerate(hotels):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate(row_data, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 30
        r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 10: 持ち物リスト
# ============================================================
def build_checklist(wb):
    ws = wb.create_sheet("⑩持ち物リスト")
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 20

    r = sheet_title(ws, "⑩  持ち物リスト", "caution.htmlに表示する持ち物チェックリストを入力してください")
    notice_row(ws, r, "  ★ カテゴリを追加する場合はadmin.htmlの持ち物タブから行ってください。", 3)
    r += 1

    categories = [
        ("必須持ち物（赤ラベル）", [
            "身分証明書・免許証（バイク乗車時）",
            "ツアーバウチャー（本しおり）",
            "現金・クレジットカード",
            "クレジットカード",
            "スマートフォン・充電器",
            "モバイルバッテリー",
            "常備薬",
            "歩きやすいシューズ",
            "着替え（2泊分）",
            "雨具・防寒着",
        ]),
        ("あると便利なもの（黒ラベル）", [
            "まとめられる雨衣・ライトコート",
            "折りたたみ傘",
            "サングラス",
            "カメラ・予備バッテリー",
            "エコバッグ",
            "ウェットティッシュ・ハンカチ",
            "マスク（任意含む）",
            "軽量アウター",
            "ネックポーチ",
            "花粉・虫刺され防止パッド",
        ]),
    ]

    for cat_name, items in categories:
        section_title(ws, r, 1, 3, f"  ■ {cat_name}"); r += 1
        header_row(ws, r, [("持ち物名", 22), ("補足説明（任意）", 50), ("カテゴリ区分", 20)], bg=C_BLUE); r += 1
        for i, item in enumerate(items):
            bg = C_GRAY if i % 2 == 0 else C_WHITE
            set_cell(ws, r, 1, item, font=fnt(10), bg=C_YELLOW, align=aln("left", "center", wrap=True), border=border_all())
            set_cell(ws, r, 2, "", font=fnt(10), bg=C_YELLOW, align=aln("left", "center", wrap=True), border=border_all())
            set_cell(ws, r, 3, cat_name.split("（")[1].replace("）",""), font=fnt(9), bg=C_LABEL, align=aln("center"), border=border_all())
            ws.row_dimensions[r].height = 22
            r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 11: Travel Tips
# ============================================================
def build_tips(wb):
    ws = wb.create_sheet("⑪Travel Tips")
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 60
    ws.column_dimensions["C"].width = 24

    r = sheet_title(ws, "⑪  Travel Tips（アコーディオン）", "caution.htmlのTravel Tipsアコーディオン内容を設定してください")
    notice_row(ws, r, "  ★ 各Tipをクリックで展開する仕様。本文内で改行したい場合は「\\n」と入力してください（システムが改行に変換）。", 3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ Tips一覧"); r += 1
    header_row(ws, r, [("見出し（タイトル）", 28), ("本文", 60), ("Font Awesomeアイコン", 24)], bg=C_BLUE)
    r += 1

    tips = [
        ("4月の気象と服装",
         "寒さと雨の可能性が大きい季節です。特に伊豆・箱根では、集合時間や場所は冷えやすいところも多く暖かくしやすい防寒をお勧めします。\n4月10日〜12日 伊豆エリアの最高気温:16度 /最低気温:7度 推定3/25現在",
         "fa-solid fa-cloud-sun"),
        ("走行中",
         "ツアー中はグループ走行になります。全員のペースで無理なく走行していただきます。グループ外での追い越しは禁止となります。\nまた走行中、食事に立ち寄っている間どこに停車してる間もどうぞご安心ください。どうぞの際は前の人が走っていたく前から見て安全を確認してから行なっていただきます。",
         "fa-solid fa-motorcycle"),
        ("旅行傷害保険",
         "転倒・軽傷（約8km以内）の場合、「旅行保険」として補償します。走行中の重大転倒・事故の起こる事のは該当しませんのでご注意ください。",
         "fa-solid fa-person-biking"),
        ("サポート車両",
         "サポート車両は万能兼用車両台数を確保します。基本的にバイクの見守りをメインにします。",
         "fa-solid fa-truck"),
    ]
    for i, (title, content, icon) in enumerate(tips):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([title, content, icon], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "top" if col == 2 else "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 56
        r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 12: 緊急連絡先・対応手順
# ============================================================
def build_emergency(wb):
    ws = wb.create_sheet("⑫緊急連絡先")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 46
    ws.column_dimensions["C"].width = 30

    r = sheet_title(ws, "⑫  緊急連絡先・対応手順", "caution.htmlの緊急時情報・対応ステップを入力してください")
    notice_row(ws, r, "  ★ 赤帯のアラート文・対応手順ステップ・その他緊急連絡先をすべてここで管理します。", 3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ 会社緊急連絡先"); r += 1
    input_row(ws, r, "緊急連絡 電話番号", "050-1742-3855", ""); r += 1
    input_row(ws, r, "対応時間", "平日　10:00〜18:00（土日祝日除く）", ""); r += 1
    input_row(ws, r, "会社住所", "〒145-0062 東京都大田区北千束一丁目5-七 2F", ""); r += 1
    input_row(ws, r, "メールアドレス", "inquiry@mototoursjapan.com", ""); r += 1

    section_title(ws, r, 1, 3, "  ■ アラートメッセージ（赤帯）"); r += 1
    set_cell(ws, r, 1, "アラート文",
             font=fnt(10, bold=True), bg=C_LABEL, align=aln("left", "top"), border=border_all())
    alert_text = (
        "緊急の場合はまず 119番（救急・消防） または 110番（警察） に通報してください。\n"
        "その後、必ず 担当添乗員または弊社緊急連絡先 にご連絡をお願いいたします。"
    )
    c = ws.cell(row=r, column=2, value=alert_text)
    c.font = fnt(10)
    c.fill = fill(C_YELLOW)
    c.alignment = aln("left", "top", wrap=True)
    c.border = border_all()
    ws.row_dimensions[r].height = 56
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ 対応手順ステップ（順番通りに入力）"); r += 1
    header_row(ws, r, [("手順タイトル", 24), ("説明文", 46), ("タグ表示（任意）", 20)], bg=C_BLUE)
    r += 1

    steps = [
        ("身の安全を確保する", "まず自分と周囲の人の安全を確認してください。交通事故・火事・自然災害などの危険がある場合は、安全な場所へ速やかに移動してください。他の人の救助が必要な場合も、まず自身の安全を確保した上で行なってください。", "最優先"),
        ("緊急機関への通報", "負傷者・病人がいる場合は119番（救急・消防）へ、盗難・事故・暴力の場合は110番（警察）へ通報してください。日本語が不得意の場合は「English, please.」と伝えることで英語対応可能です。", "必要な場合"),
        ("添乗員への連絡", "できるだけ早く担当添乗員に電話・LINEで連絡してください。状況・場所・怪我の情報を伝えてください。添乗員は状況に応じて救急・警察・保険会社へのサポートを行います。", "必須"),
        ("弊社緊急連絡先への連絡", "添乗員と連絡がとれない場合は弊社緊急連絡先（会社ページ記載）にご連絡ください。旅行傷害保険範囲内で必要なサポートを行います。", ""),
        ("状況・証拠の記録", "事故・盗難・怪我などの場合は、現場の写真・動画を撮影。警察の受理番号（受理証明書）を必ず受け取ってください。保険請求の際の手続きに必要です。事故相手の一覧・連絡先を記録しておくと便利です。", ""),
        ("帰国後の保険手続き", "帰国後は速やかに旅行傷害保険の保険会社に連絡し、申請手続きを行ってください。必要書類（診断書・警察証明書・領収書など）は旅行中から準備しておくとスムーズです。", "旅行後"),
    ]
    for i, (title, desc, tag) in enumerate(steps):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([title, desc, tag], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "top" if col == 2 else "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 50
        r += 1

    section_title(ws, r, 1, 3, "  ■ その他の緊急連絡先（救急・警察など）"); r += 1
    header_row(ws, r, [("機関名", 24), ("電話番号", 46), ("メモ・備考", 30)], bg=C_BLUE)
    r += 1

    others = [
        ("救急・消防", "119", "日本全国共通・無料"),
        ("警察", "110", "日本全国共通・無料"),
        ("海外旅行保険", "0120-258-365", "全損・クレイム保険会社"),
    ]
    for i, (name, phone, note) in enumerate(others):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([name, phone, note], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 22
        r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 13: 会社情報・SNS
# ============================================================
def build_company(wb):
    ws = wb.create_sheet("⑬会社情報・SNS")
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 30

    r = sheet_title(ws, "⑬  会社情報・SNS・グッズ", "company_information.htmlに表示する会社情報・SNSリンク・グッズ情報を設定してください")
    notice_row(ws, r, "  ★ グッズ写真はadmin.htmlの会社情報タブからアップロードしてください。", 3)
    r += 1

    section_title(ws, r, 1, 3, "  ■ 会社基本情報"); r += 1
    input_row(ws, r, "会社名", "MOTO TOURS JAPAN", ""); r += 1
    input_row(ws, r, "会社住所", "〒145-0062 東京都大田区北千束一丁目5-七 2F", ""); r += 1
    input_row(ws, r, "電話番号", "050-1742-3855", ""); r += 1
    input_row(ws, r, "メールアドレス", "inquiry@mototoursjapan.com", ""); r += 1
    input_row(ws, r, "営業時間", "平日 10:00〜18:00", ""); r += 1

    section_title(ws, r, 1, 3, "  ■ SNS リンク（公式アカウント）"); r += 1
    header_row(ws, r, [("SNS名", 22), ("URL（公式アカウント）", 50), ("表示ラベル", 30)], bg=C_BLUE)
    r += 1

    sns_list = [
        ("Instagram", "https://www.instagram.com/mototoursjapan/", "@mototoursjapan"),
        ("X（旧Twitter）", "https://twitter.com/mototoursjapan", "@mototoursjapan"),
        ("YouTube", "https://www.youtube.com/@mototoursjapan", "MOTO TOURS JAPAN"),
        ("LINE公式", "https://lin.ee/xxxxx", "@638nrfza"),
    ]
    for i, (name, url, label) in enumerate(sns_list):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([name, url, label], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 22
        r += 1

    section_title(ws, r, 1, 3, "  ■ オリジナルグッズ（ショッピング情報）"); r += 1
    header_row(ws, r, [("グッズ名", 22), ("説明文", 50), ("価格・購入方法など", 30)], bg=C_BLUE)
    r += 1

    goods = [
        ("オリジナルTシャツ", "MOTO TOURS JAPANロゴ入りTシャツ。カラー：ブラック・ホワイト", "¥3,500〜 / ツアー当日または公式サイトから購入"),
        ("ステッカーセット", "バイクに貼れる防水ステッカー5枚セット", "¥800 / 当日販売"),
        ("キャップ", "ロゴ刺繍入りメッシュキャップ", "¥4,200 / 公式サイト"),
    ]
    for i, (name, desc, price) in enumerate(goods):
        bg = C_GRAY if i % 2 == 0 else C_WHITE
        for col, val in enumerate([name, desc, price], 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = fnt(10)
            c.fill = fill(C_YELLOW)
            c.alignment = aln("left", "center", wrap=True)
            c.border = border_all()
        ws.row_dimensions[r].height = 26
        r += 1

    ws.freeze_panes = "A4"

# ============================================================
# SHEET 0: 使い方ガイド
# ============================================================
def build_guide_sheet(wb):
    ws = wb.create_sheet("【使い方ガイド】", 0)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 60
    ws.column_dimensions["C"].width = 36

    ws.merge_cells("A1:C1")
    c = ws["A1"]
    c.value = "旅のしおり 編集シート  -  使い方ガイド"
    c.font = fnt(16, bold=True, color="FFFFFF")
    c.fill = fill(C_NAVY)
    c.alignment = aln("center")
    ws.row_dimensions[1].height = 42

    ws.merge_cells("A2:C2")
    c2 = ws["A2"]
    c2.value = "MOTO TOURS JAPAN  |  内部管理資料  ©2026"
    c2.font = fnt(10, italic=True, color="FFFFFF")
    c2.fill = fill(C_BLUE)
    c2.alignment = aln("center")
    ws.row_dimensions[2].height = 20

    guide_data = [
        ("", "", ""),
        ("★ このファイルの使い方", "", ""),
        ("手順①", "黄色のセルを編集する", "各シートの黄色セルがすべて入力欄です。白・グレーは変更不要です。"),
        ("手順②", "このExcelを担当者に共有する", "ツアー担当者がこのシートに情報を入力します。"),
        ("手順③", "admin.htmlで内容を貼り付け・入力する", "各タブに対応した管理画面で入力・保存してください。"),
        ("手順④", "「保存する」をクリック", "admin.htmlの保存ボタンを押すと旅のしおりに反映されます。"),
        ("", "", ""),
        ("★ シート構成", "", ""),
        ("①基本情報",        "ツアー名・お客様名・日程",               "index.html トップページに表示"),
        ("②集合・解散",      "集合場所・解散場所・シャトル情報",       "index.html 集合情報セクション"),
        ("③添乗員情報",      "担当者氏名・連絡先・ご挨拶文",           "index.html 添乗員紹介"),
        ("④含む・含まない", "ツアーに含まれるもの・含まれないもの",   "index.html インクルード表"),
        ("⑤Day1行程",       "Day1のスケジュール一覧",                  "itinerary_day1.html"),
        ("⑥Day2行程",       "Day2のスケジュール一覧",                  "itinerary_day2.html"),
        ("⑦Day3行程",       "Day3のスケジュール一覧",                  "itinerary_day2.html（Day3も同ページ）"),
        ("⑧ハイライト",     "ツアーの見どころカード",                  "route.html ハイライトセクション"),
        ("⑨宿泊施設",       "ホテル名・住所・チェックイン情報",        "route.html 宿泊情報セクション"),
        ("⑩持ち物リスト",   "必須・推奨持ち物チェックリスト",          "caution.html 持ち物タブ"),
        ("⑪Travel Tips",    "アコーディオン式Tips",                    "caution.html Travel Tipsタブ"),
        ("⑫緊急連絡先",     "緊急対応手順・連絡先",                    "caution.html 緊急時セクション"),
        ("⑬会社情報・SNS",  "会社情報・SNSリンク・グッズ",             "company_information.html"),
        ("", "", ""),
        ("★ 注意事項", "", ""),
        ("画像について",     "写真・画像はExcelでは管理しません。",     "admin.htmlの各タブからアップロードしてください。"),
        ("地図URLについて",  "GoogleマップのiframeのsrcURLを使用。",    "Googleマップ→共有→「地図を埋め込む」→URLをコピー"),
        ("保存について",     "入力後は上書き保存（Ctrl+S）してください。", "admin.htmlでの反映後に旅のしおりを確認してください。"),
    ]

    for i, (col1, col2, col3) in enumerate(guide_data, 3):
        ws.row_dimensions[i].height = 22
        for col, val in enumerate([col1, col2, col3], 1):
            c = ws.cell(row=i, column=col, value=val)
            if col1.startswith("★"):
                c.font = fnt(11, bold=True, color=C_NAVY if col == 1 else "333333")
                c.fill = fill("E3F2FD")
                c.alignment = aln("left", "center")
                if col == 1:
                    ws.row_dimensions[i].height = 26
            elif col1 in ("", ) and col2 == "":
                c.fill = fill(C_WHITE)
            elif col == 1:
                c.font = fnt(10, bold=True, color=C_NAVY)
                c.fill = fill(C_GRAY)
                c.alignment = aln("right", "center")
                c.border = border_all()
            else:
                c.font = fnt(10)
                c.fill = fill(C_WHITE)
                c.alignment = aln("left", "center", wrap=True)
                c.border = border_all()

    ws.freeze_panes = "A3"


# ============================================================
# MAIN
# ============================================================
wb = openpyxl.Workbook()
wb.remove(wb.active)

build_guide_sheet(wb)
build_basic(wb)
build_meeting(wb)
build_guide(wb)
build_includes(wb)

day1_items = [
    {"time":"10:00","title":"バイカーズパラダイス南箱根","place":"集合","desc":"ブリーフィング・レクチャー・装備確認・バイクレンタル・保険手続きを行います。","badge":"集合","badgeType":"red","isHighlight":False},
    {"time":"11:30","title":"木負 大村屋","place":"伊豆半島・富士山","desc":"昔ながらの木造建物で大村屋の雰囲気が、老舗の技とともに迎えてくれるお店","badge":"観光","badgeType":"","isHighlight":False},
    {"time":"13:00","title":"ランチタイム シオン","place":"富士チン","desc":"伊豆の四季を感じながら心地よい空気と癒しの時間を味わえる、人気の海鮮料理店","badge":"観光","badgeType":"blue","isHighlight":True},
    {"time":"14:00","title":"伊豆ループウェイ","place":"後楽園大学","desc":"壮大な自然景色を空から楽しみながら、ここならではのダイナミックな眺色を満喫","badge":"観光","badgeType":"gold","isHighlight":True},
    {"time":"15:40","title":"富士山スカイライン","place":"静岡県スカイパーク","desc":"壮大な自然景色を空から楽しみながら、ここならではのダイナミックな眺色を満喫","badge":"走行","badgeType":"blue","isHighlight":True},
    {"time":"17:00","title":"ホテルニューアカオ","place":"静岡県熱海市熱海1993-250","desc":"熱海の美しい海岸線と華やかなリゾート感を味わえる、心地よくくつろげるリゾートホテル","badge":"宿泊","badgeType":"green","isHighlight":True},
]
build_day(wb, 1, "2026年4月10日（金）", "伊豆の絶景を駆け抜ける旅", day1_items)

day2_items = [
    {"time":"9:00","title":"ホテルニューアカオ","place":"静岡県熱海市熱海1993-250","desc":"熱海の美しい海岸線と華やかなリゾート感を味わえる、心地よくくつろげるリゾートホテル。","badge":"集合","badgeType":"blue","isHighlight":False},
    {"time":"10:00","title":"伊豆スカイライン","place":"熱海峠方面","desc":"富士山や駿河湾を眺めながら爽快な大空を楽しめる、伊豆随一の絶景ルート","badge":"走行","badgeType":"","isHighlight":True},
    {"time":"10:35","title":"十三峠休憩","place":"駐車","desc":"伊豆スカイラインの開始地点付近、景色を眺めながら休憩できる絶景スポット","badge":"休憩","badgeType":"","isHighlight":False},
    {"time":"12:00","title":"わなかいとところ","place":"静岡県伊豆市韮317","desc":"丁寧に仕上げた肴とともに料理を楽しんで、和の味わいを満喫できる人気のお店","badge":"ランチ","badgeType":"blue","isHighlight":True},
    {"time":"13:40","title":"わさび屋 峰の家","place":"峰の家 リゾート","desc":"伊豆の特産物であるわさびを使ったわさびづくし料理で、幸の思い出としてを喜ぶ人気","badge":"アクティビティ","badgeType":"blue","isHighlight":False},
    {"time":"15:15","title":"波伝説ループ道","place":"静岡県西伊豆スカイライン沿道","desc":"絶景標高を気にしながら伊豆の景色を楽しめながら、伊豆ならではの一帯的なループ道","badge":"ライディング","badgeType":"gold","isHighlight":True},
    {"time":"16:30","title":"ホテルニュー銀水","place":"静岡県西伊豆町堂ヶ島2977-1","desc":"伊豆の美しい海岸を眺めながら、穏やかと上質な温泉でゆったりくつろげる人気の宿","badge":"宿泊","badgeType":"green","isHighlight":True},
]
build_day(wb, 2, "2026年4月11日（土）", "伊豆スカイライン・堂ヶ島ループなどライディングを満喫", day2_items)

day3_items = [
    {"time":"8:30","title":"ホテルニュー銀水","place":"静岡県西伊豆町堂ヶ島2977-1","desc":"フロント7Fに集合","badge":"集合","badgeType":"blue","isHighlight":False},
    {"time":"9:35","title":"絶景高台コーヒーの会","place":"静岡県西伊豆町堂ヶ島色浜3609-1","desc":"ここならではの穏やかな空気と日差しを楽しみながら、伊豆らしい自然豊かなスポット","badge":"休憩","badgeType":"","isHighlight":False},
    {"time":"10:10","title":"西伊豆スカイライン","place":"","desc":"伊豆の山々と駿河湾の景色を眺めながら、爽快な大空を楽しめる絶景ルート","badge":"走行","badgeType":"","isHighlight":True},
    {"time":"10:40","title":"達磨山レストハウス","place":"静岡県伊豆市笹原","desc":"伊豆の自然景色が広がりながら、富士山のような仔羊のパノラマ景色を楽しめる人気の景観スポット","badge":"休憩","badgeType":"blue","isHighlight":True},
    {"time":"12:10","title":"浜辺の食堂 潮天 みなとや","place":"静岡県沼津市本字田100-1","desc":"新鮮な海の幸を目前に味わえる、沼津ならではの海辺に佇むお食事処","badge":"昼食","badgeType":"","isHighlight":True},
    {"time":"14:40","title":"グラスカイウォーク","place":"静岡県三島市広小路313","desc":"かんざんじ湖周辺の上から、浜松・伊豆エリアの麓の田園風景を眺められる魅惑的な場所","badge":"観光","badgeType":"blue","isHighlight":False},
    {"time":"17:00","title":"ツアー終了・解散","place":"バイカーズパラダイス南箱根","desc":"楽しいコーヒーによるご観光の後、解散となります。また次回のご参加を心からお待ちしております。","badge":"解散","badgeType":"red","isHighlight":True},
]
build_day(wb, 3, "2026年4月12日（日）", "西伊豆スカイラインを駆け抜け、駿河湾の絶景でフィナーレ", day3_items)

build_highlights(wb)
build_hotels(wb)
build_checklist(wb)
build_tips(wb)
build_emergency(wb)
build_company(wb)

wb.save(OUT)
print(f"Saved: {OUT}")
