import json
import os
from bs4 import BeautifulSoup

# pip install beautifulsoup4

SKILL_POSITIONS = {"QB", "RB", "WR", "TE"}
POS_DICT = {"QB": 0, "RB": 1, "WR": 2, "TE": 3}

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def parse_file(filepath, team_keys):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    table = soup.find('table')
    if not table:
        print(f"  No table found in {filepath}")
        return []

    entries = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if not cells or len(cells) < 54:
            continue

        data = [td.get_text(strip=True) for td in cells]

        # Column layout (0-indexed, data rows have no Rk column):
        # [0]     Player
        # [1-5]   Summary cols (pass Yds/TD, rush Yds, FantPt, rec Yds) — skipped
        # [6]     Day — skipped
        # [7]     G#  — skipped
        # [8]     Week
        # [9]     Date (YYYY-MM-DD)
        # [10]    Age (YY-DDD)
        # [11]    Team
        # [12]    Home/away indicator — skipped
        # [13]    Opp
        # [14]    Result (e.g. "L, 20-27")
        # [15-33] Passing stats (19 values)
        # [34-39] Rushing stats (6 values)
        # [40-48] Receiving stats (9 values)
        # [49]    FantPt standard — skipped
        # [50]    PPR
        # [51]    DKPt — skipped
        # [52]    FDPt — skipped
        # [53]    Pos.

        pos_str = data[53][:2]
        if pos_str not in SKILL_POSITIONS:
            continue

        player_name = data[0]
        week        = data[8]
        date_str    = data[9]
        full_age    = data[10]
        team_name   = data[11]
        opp_name    = data[13]
        result      = data[14]

        year = date_str[:4]

        # Age: "27-242" -> years + days/365.25
        try:
            dash = full_age.index('-')
            age = float(full_age[:dash]) + float(full_age[dash + 1:]) / 365.25
        except (ValueError, IndexError):
            continue

        # Score: "L, 20-27" or "W, 27-20 (OT)"
        try:
            score_part = result.split(', ', 1)[1].replace(' (OT)', '')
            t_score, o_score = score_part.split('-')
            team_score = float(t_score)
            opp_score  = float(o_score)
        except (IndexError, ValueError):
            continue

        try:
            team_id = team_keys[team_name]
            opp_id  = team_keys[opp_name]
        except KeyError:
            print(f"  Unknown team code in row: {team_name} / {opp_name}")
            continue

        passing   = [safe_float(data[i]) for i in range(15, 34)]  # 19 values
        rushing   = [safe_float(data[i]) for i in range(34, 40)]  #  6 values
        receiving = [safe_float(data[i]) for i in range(40, 49)]  #  9 values
        ppr       = safe_float(data[50])
        pos_enc   = POS_DICT[pos_str]

        row_data = (
            [week, age, team_id, opp_id, team_score, opp_score]
            + passing + rushing + receiving
            + [ppr, pos_enc]
        )

        entries.append((player_name, year, week, row_data))

    return entries

def main():
    base       = os.path.dirname(os.path.abspath(__file__))
    raw_dir    = os.path.join(base, 'data', 'raw')
    player_dir = os.path.join(base, 'data', 'players')

    os.makedirs(raw_dir,    exist_ok=True)
    os.makedirs(player_dir, exist_ok=True)

    with open(os.path.join(base, 'teams.json')) as f:
        team_keys = json.load(f)

    raw_files = [f for f in os.listdir(raw_dir) if f.endswith(('.xls', '.xlsx'))]
    if not raw_files:
        print('No .xls/.xlsx files found in data/raw/')
        return

    for filename in raw_files:
        print(f'Processing {filename}...')
        entries = parse_file(os.path.join(raw_dir, filename), team_keys)
        print(f'  {len(entries)} player-game rows written')

        for player_name, year, week, row_data in entries:
            pdir = os.path.join(player_dir, player_name)
            os.makedirs(pdir, exist_ok=True)
            with open(os.path.join(pdir, f'{year}_{week}.csv'), 'w') as f:
                f.write(', '.join(str(x) for x in row_data))

main()
