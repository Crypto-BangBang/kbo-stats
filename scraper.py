import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.kbo.or.kr"
}

def _get(url, **kwargs):
    return requests.get(url, headers=HEADERS, timeout=10, **kwargs)

def _post(url, data):
    return requests.post(url, headers=HEADERS, data=data, timeout=10)

def _extract_id(tag, param):
    if not tag: return ""
    href = tag.get("href", "")
    m = re.search(rf'{param}=([^&"\']+)', href)
    return m.group(1) if m else ""

# ── 날짜별 경기 일정 ─────────────────────────────────────────────
def get_games_by_date(date_str):
    """date_str: 'YYYYMMDD'"""
    try:
        ym  = date_str[:6]
        day = date_str[6:8]
        res = _post("https://www.kbo.or.kr/pub/schedule/scheduleList.do",
                    {"date": ym, "stadiumCode": "", "teamCode": ""})
        soup = BeautifulSoup(res.text, "lxml")
        games = []
        current_day = ""
        for row in soup.select("table tbody tr"):
            cols = row.select("td")
            if not cols: continue
            texts = [c.get_text(strip=True) for c in cols]
            if len(texts) < 4: continue

            day_cell = cols[0].get_text(strip=True)
            if re.match(r'\d{2}', day_cell):
                current_day = day_cell

            if current_day != day:
                continue

            link = row.select_one("a[href*='gameCode']")
            game_code = _extract_id(link, "gameCode") if link else ""

            games.append({
                "time":      texts[1] if len(texts) > 1 else texts[0],
                "away":      texts[2] if len(texts) > 2 else "",
                "score":     texts[3] if len(texts) > 3 else "vs",
                "home":      texts[4] if len(texts) > 4 else "",
                "stadium":   texts[5] if len(texts) > 5 else "",
                "status":    texts[6] if len(texts) > 6 else "",
                "game_code": game_code,
            })
        return games
    except Exception:
        return []

def get_today_games():
    return get_games_by_date(datetime.now().strftime("%Y%m%d"))

# ── 경기 상세 (박스스코어 + 타자/투수 기록) ────────────────────
def get_game_detail(game_code):
    try:
        res  = _get(f"https://www.kbo.or.kr/game/gameScore.do?gameCode={game_code}")
        soup = BeautifulSoup(res.text, "lxml")

        result = {
            "game_code":     game_code,
            "date":          game_code[:8] if len(game_code) >= 8 else "",
            "away_team":     "",
            "home_team":     "",
            "box":           [],   # 이닝별 점수
            "away_batting":  [],
            "home_batting":  [],
            "away_pitching": [],
            "home_pitching": [],
        }

        # 팀명
        team_els = soup.select(".tbl_score .team_name, .team_name, h4.team")
        if len(team_els) >= 2:
            result["away_team"] = team_els[0].get_text(strip=True)
            result["home_team"] = team_els[1].get_text(strip=True)

        # 박스스코어 (이닝별)
        box_table = soup.select_one("table.tbl_score") or soup.select_one(".score_board table")
        if box_table:
            for row in box_table.select("tr"):
                cells = [c.get_text(strip=True) for c in row.select("th, td")]
                if cells:
                    result["box"].append(cells)

        # 타자 기록 (원정/홈 두 테이블)
        bat_tables = soup.select("table.tbl_batter") or soup.select("table.tData01")
        for i, tbl in enumerate(bat_tables[:2]):
            rows = []
            for row in tbl.select("tbody tr"):
                cols = row.select("td")
                texts = [c.get_text(strip=True) for c in cols]
                if len(texts) < 5: continue
                link = row.select_one("a[href*='playerId']")
                pid  = _extract_id(link, "playerId")
                rows.append({
                    "player_id": pid,
                    "name": texts[0], "pos": texts[1],
                    "ab":   texts[2], "r":   texts[3],
                    "h":    texts[4], "rbi": texts[5] if len(texts) > 5 else "-",
                    "bb":   texts[6] if len(texts) > 6 else "-",
                    "so":   texts[7] if len(texts) > 7 else "-",
                    "avg":  texts[8] if len(texts) > 8 else "-",
                })
            if i == 0: result["away_batting"] = rows
            else:      result["home_batting"] = rows

        # 투수 기록
        pit_tables = soup.select("table.tbl_pitcher")
        for i, tbl in enumerate(pit_tables[:2]):
            rows = []
            for row in tbl.select("tbody tr"):
                cols = row.select("td")
                texts = [c.get_text(strip=True) for c in cols]
                if len(texts) < 5: continue
                link = row.select_one("a[href*='playerId']")
                pid  = _extract_id(link, "playerId")
                rows.append({
                    "player_id": pid,
                    "name": texts[0],
                    "ip":   texts[1], "h":   texts[2],
                    "r":    texts[3], "er":  texts[4],
                    "bb":   texts[5] if len(texts) > 5 else "-",
                    "so":   texts[6] if len(texts) > 6 else "-",
                    "era":  texts[7] if len(texts) > 7 else "-",
                    "result": texts[8] if len(texts) > 8 else "",
                })
            if i == 0: result["away_pitching"] = rows
            else:      result["home_pitching"] = rows

        return result
    except Exception:
        return {}

# ── 선수 상세 ────────────────────────────────────────────────────
def get_player_detail(player_id):
    try:
        res  = _get(f"https://www.kbo.or.kr/player/playerDetail.do?playerId={player_id}")
        soup = BeautifulSoup(res.text, "lxml")

        result = {
            "player_id":   player_id,
            "name":        "",
            "team":        "",
            "position":    "",
            "birth":       "",
            "debut":       "",
            "avatar":      "",
            "season_stats": [],   # 시즌별 기록
            "game_log":    [],    # 최근 경기 기록
            "stat_headers": [],
        }

        # 선수 기본 정보
        name_el = soup.select_one(".player_name, h3.name, .name_wrap h4")
        if name_el: result["name"] = name_el.get_text(strip=True)

        img_el = soup.select_one(".player_img img, .photo img")
        if img_el: result["avatar"] = img_el.get("src", "")

        info_els = soup.select(".player_info li, .info_list li")
        for li in info_els:
            text = li.get_text(strip=True)
            if "팀" in text or "소속" in text:
                result["team"] = re.sub(r'팀|소속|[:：]', '', text).strip()
            elif "포지션" in text or "위치" in text:
                result["position"] = re.sub(r'포지션|위치|[:：]', '', text).strip()
            elif "생년월일" in text or "출생" in text:
                result["birth"] = re.sub(r'생년월일|출생|[:：]', '', text).strip()

        # 시즌 기록 테이블
        tables = soup.select("table")
        for tbl in tables:
            thead = tbl.select_one("thead")
            if not thead: continue
            headers = [th.get_text(strip=True) for th in thead.select("th")]
            rows = []
            for row in tbl.select("tbody tr"):
                cols = [c.get_text(strip=True) for c in row.select("td")]
                if cols and len(cols) >= 3:
                    rows.append(cols)
            if rows:
                result["stat_headers"]  = headers
                result["season_stats"]  = rows[:10]
                break

        # 최근 경기 기록 (두 번째 테이블 이후)
        for tbl in tables[1:]:
            rows = []
            thead = tbl.select_one("thead")
            headers = [th.get_text(strip=True) for th in thead.select("th")] if thead else []
            for row in tbl.select("tbody tr"):
                cols = [c.get_text(strip=True) for c in row.select("td")]
                link = row.select_one("a[href*='gameCode']")
                gc   = _extract_id(link, "gameCode")
                if cols and len(cols) >= 3:
                    rows.append({"cells": cols, "game_code": gc})
            if rows:
                result["game_log"]         = rows[:15]
                result["game_log_headers"] = headers
                break

        return result
    except Exception:
        return {}

# ── 타자 기록 ────────────────────────────────────────────────────
def get_batting_stats():
    try:
        data = {
            "gyear": str(datetime.now().year),
            "stype": "R", "orderby": "HRA", "orderbytype": "DESC",
            "searchtype": "A", "startrow": "1", "pageno": "1"
        }
        res  = _post("https://www.kbo.or.kr/pub/records/battingRecordList.do", data)
        soup = BeautifulSoup(res.text, "lxml")
        rows = soup.select("table.tData01 tbody tr") or soup.select("table tbody tr")
        stats = []
        for row in rows[:30]:
            cols = [c.get_text(strip=True) for c in row.select("td")]
            if len(cols) < 10: continue
            link = row.select_one("a[href*='playerId']")
            pid  = _extract_id(link, "playerId")
            stats.append({
                "player_id": pid,
                "rank": cols[0], "name": cols[1], "team": cols[2],
                "games": cols[3], "ab": cols[4], "hits": cols[5],
                "hr": cols[6], "rbi": cols[7], "avg": cols[8],
                "obp": cols[9]  if len(cols) > 9  else "-",
                "slg": cols[10] if len(cols) > 10 else "-",
                "ops": cols[11] if len(cols) > 11 else "-",
            })
        return stats
    except Exception:
        return []

# ── 투수 기록 ────────────────────────────────────────────────────
def get_pitching_stats():
    try:
        data = {
            "gyear": str(datetime.now().year),
            "stype": "R", "orderby": "ERA", "orderbytype": "ASC",
            "searchtype": "A", "startrow": "1", "pageno": "1"
        }
        res  = _post("https://www.kbo.or.kr/pub/records/pitchingRecordList.do", data)
        soup = BeautifulSoup(res.text, "lxml")
        rows = soup.select("table.tData01 tbody tr") or soup.select("table tbody tr")
        stats = []
        for row in rows[:30]:
            cols = [c.get_text(strip=True) for c in row.select("td")]
            if len(cols) < 10: continue
            link = row.select_one("a[href*='playerId']")
            pid  = _extract_id(link, "playerId")
            stats.append({
                "player_id": pid,
                "rank": cols[0], "name": cols[1], "team": cols[2],
                "games": cols[3], "wins": cols[4], "losses": cols[5],
                "saves": cols[6], "ip": cols[7], "era": cols[8],
                "so":   cols[9]  if len(cols) > 9  else "-",
                "whip": cols[10] if len(cols) > 10 else "-",
            })
        return stats
    except Exception:
        return []

# ── 팀 순위 ──────────────────────────────────────────────────────
def get_team_rankings():
    try:
        data = {"gyear": str(datetime.now().year), "stype": "R"}
        res  = _post("https://www.kbo.or.kr/pub/records/teamRecordList.do", data)
        soup = BeautifulSoup(res.text, "lxml")
        rows = soup.select("table.tData01 tbody tr") or soup.select("table tbody tr")
        teams = []
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.select("td")]
            if len(cols) < 6: continue
            teams.append({
                "rank": cols[0], "team": cols[1], "games": cols[2],
                "wins": cols[3], "losses": cols[4], "draws": cols[5],
                "pct":  cols[6] if len(cols) > 6 else "-",
                "gb":   cols[7] if len(cols) > 7 else "-",
            })
        return teams
    except Exception:
        return []
