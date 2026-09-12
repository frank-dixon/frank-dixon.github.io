#!/usr/bin/env python3
"""Fetch frank-dixon contribution calendar and write a teal cream heatmap SVG."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

LOGIN = "frank-dixon"
OUT = Path(__file__).resolve().parents[1] / "assets" / "github-contributions.svg"

# Site palette: cream → teal greens
LEVEL_COLORS = {
    "NONE": "#E8E0D2",
    "FIRST_QUARTILE": "#A8D4D6",
    "SECOND_QUARTILE": "#4FAEB3",
    "THIRD_QUARTILE": "#0B8A8F",
    "FOURTH_QUARTILE": "#087075",
}

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          firstDay
          contributionDays {
            contributionCount
            contributionLevel
            date
            weekday
          }
        }
      }
    }
  }
}
"""


def fetch_calendar(token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "frank-dixon-contributions-heatmap",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GraphQL HTTP {exc.code}: {body}") from exc

    if payload.get("errors"):
        raise SystemExit(f"GraphQL errors: {payload['errors']}")

    user = (payload.get("data") or {}).get("user")
    if not user:
        raise SystemExit("No user data returned for frank-dixon")

    return user["contributionsCollection"]["contributionCalendar"]


def month_labels(weeks: list[dict], cell: int, gap: int, left: int) -> list[str]:
    labels: list[str] = []
    seen: set[str] = set()
    for wi, week in enumerate(weeks):
        days = week["contributionDays"]
        if not days:
            continue
        first = days[0]["date"]
        dt = datetime.strptime(first, "%Y-%m-%d")
        key = f"{dt.year}-{dt.month:02d}"
        if key in seen:
            continue
        # Prefer labeling near start of month (day <= 7) or first week overall
        if dt.day > 7 and wi != 0:
            continue
        seen.add(key)
        x = left + wi * (cell + gap)
        labels.append(
            f'<text x="{x}" y="12" class="month">{dt.strftime("%b")}</text>'
        )
    return labels


def render_svg(calendar: dict) -> str:
    weeks = calendar["weeks"]
    total = calendar["totalContributions"]
    cell = 11
    gap = 3
    left = 28
    top = 22
    rows = 7
    width = left + len(weeks) * (cell + gap) - gap + 8
    height = top + rows * (cell + gap) - gap + 36

    rects: list[str] = []
    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            # GitHub weekday: 0=Sunday … 6=Saturday
            y = top + day["weekday"] * (cell + gap)
            x = left + wi * (cell + gap)
            fill = LEVEL_COLORS.get(day["contributionLevel"], LEVEL_COLORS["NONE"])
            count = day["contributionCount"]
            date = day["date"]
            title = f"{count} contribution{'s' if count != 1 else ''} on {date}"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" ry="2" '
                f'fill="{fill}" data-date="{date}" data-count="{count}">'
                f"<title>{title}</title></rect>"
            )

    dow = [
        ('M', 1),
        ('W', 3),
        ('F', 5),
    ]
    dow_labels = []
    for label, row in dow:
        y = top + row * (cell + gap) + cell - 2
        dow_labels.append(f'<text x="0" y="{y}" class="dow">{label}</text>')

    legend_y = top + rows * (cell + gap) + 14
    legend_x = left
    legend_cells = "".join(
        f'<rect x="{legend_x + i * (cell + gap)}" y="{legend_y}" width="{cell}" height="{cell}" '
        f'rx="2" ry="2" fill="{color}"/>'
        for i, color in enumerate(
            [
                LEVEL_COLORS["NONE"],
                LEVEL_COLORS["FIRST_QUARTILE"],
                LEVEL_COLORS["SECOND_QUARTILE"],
                LEVEL_COLORS["THIRD_QUARTILE"],
                LEVEL_COLORS["FOURTH_QUARTILE"],
            ]
        )
    )
    legend_w = 5 * (cell + gap) - gap
    legend = (
        f'<text x="{legend_x - 4}" y="{legend_y + cell - 2}" class="legend" text-anchor="end">Less</text>'
        f"{legend_cells}"
        f'<text x="{legend_x + legend_w + 8}" y="{legend_y + cell - 2}" class="legend">More</text>'
    )

    total_label = (
        f'<text x="{width - 8}" y="{legend_y + cell - 2}" class="total" text-anchor="end">'
        f"{total:,} contributions in the last year</text>"
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub contribution activity for {LOGIN}">
  <title>GitHub contribution activity for {LOGIN}</title>
  <desc>{total:,} contributions in the last year</desc>
  <style>
    text {{ font-family: "Source Sans 3", system-ui, sans-serif; fill: #6A635B; }}
    .month {{ font-size: 11px; font-weight: 600; }}
    .dow {{ font-size: 10px; font-weight: 600; }}
    .legend, .total {{ font-size: 11px; }}
    .total {{ fill: #3F3A35; font-weight: 600; }}
  </style>
  <rect width="100%" height="100%" fill="#F3EEE4"/>
  {''.join(month_labels(weeks, cell, gap, left))}
  {''.join(dow_labels)}
  {''.join(rects)}
  {legend}
  {total_label}
</svg>
"""


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("GITHUB_TOKEN (or GH_TOKEN) is required", file=sys.stderr)
        return 1

    calendar = fetch_calendar(token)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    svg = render_svg(calendar)
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT} ({calendar['totalContributions']} contributions, {len(calendar['weeks'])} weeks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
