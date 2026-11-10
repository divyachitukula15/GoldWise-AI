from goldwise.database import get_latest_rates, get_snapshots, update_snapshot

def detect_changes():
    latest = get_latest_rates()
    previous = get_snapshots()

    if not latest:
        return None, None
    if not previous:
        return latest, None

    changes = []
    for metal, current in latest.items():
        old_rate = previous.get(metal)
        if old_rate is None or current["rate"] != old_rate:
            old_value = float(old_rate) if old_rate is not None else None
            new_value = float(current["rate"])
            percentage = (
                round((new_value - old_value) / old_value * 100, 2)
                if old_value not in (None, 0) else None
            )
            changes.append({
                "metal": metal,
                "old_rate": old_value,
                "new_rate": new_value,
                "difference": (
                    round(new_value - old_value, 2)
                    if old_value is not None else None
                ),
                "percentage": percentage,
                "date": str(current["date"]),
            })

    return latest, changes

__all__ = ["detect_changes", "update_snapshot"]
