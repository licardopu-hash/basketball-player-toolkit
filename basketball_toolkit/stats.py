"""Descriptive basketball statistics. No proprietary ratings or ranking models."""
from collections import defaultdict

COUNTS = ("minutes", "points", "fgm", "fga", "tpm", "tpa", "ftm", "fta",
          "rebounds", "assists", "steals", "blocks", "turnovers")

def _number(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a non-negative number")
    try:
        n = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a non-negative number") from None
    if not (0 <= n < float("inf")):
        raise ValueError(f"{name} must be a finite non-negative number")
    return n

def _pct(made, attempts):
    return round(100 * made / attempts, 2) if attempts else None

def summarize_player(games):
    """Aggregate a player's games; percentages are weighted by attempts."""
    totals = {key: 0.0 for key in COUNTS}
    count = 0
    for row in games:
        count += 1
        parsed = {key: _number(row.get(key, 0), key) for key in COUNTS}
        for made, attempted in (("fgm", "fga"), ("tpm", "tpa"), ("ftm", "fta")):
            if parsed[made] > parsed[attempted]:
                raise ValueError(f"{made} cannot exceed {attempted}")
        if parsed["tpm"] > parsed["fgm"] or parsed["tpa"] > parsed["fga"]:
            raise ValueError("3-point totals cannot exceed field-goal totals")
        for key in COUNTS:
            totals[key] += parsed[key]
    result = {"games": count, "totals": {k: round(v, 2) for k,v in totals.items()}}
    result["per_game"] = {k: round(v / count, 2) if count else None for k,v in totals.items()}
    result["fg_pct"] = _pct(totals["fgm"], totals["fga"])
    result["three_pt_pct"] = _pct(totals["tpm"], totals["tpa"])
    result["ft_pct"] = _pct(totals["ftm"], totals["fta"])
    result["ts_pct"] = _pct(totals["points"], 2*(totals["fga"] + 0.44*totals["fta"]))
    return result

def summarize_games(rows):
    """Group game records by player_id; returns a dictionary of summaries."""
    grouped = defaultdict(list)
    for row in rows:
        player_id = str(row.get("player_id", "")).strip()
        if not player_id:
            raise ValueError("Every row requires a non-empty player_id")
        grouped[player_id].append(row)
    return {player_id: summarize_player(games) for player_id, games in sorted(grouped.items())}
