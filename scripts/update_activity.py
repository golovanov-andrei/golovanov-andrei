"""Render a 31-day graph from GitHub's public contribution calendar."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.dates = {}
        self.counts = {}
        self.target = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("data-date") and attrs.get("id"):
            self.dates[attrs["id"]] = date.fromisoformat(attrs["data-date"])
        if tag == "tool-tip":
            self.target = attrs.get("for")
            self.text = []

    def handle_data(self, data):
        if self.target:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.target:
            text = " ".join("".join(self.text).split())
            match = re.match(r"(No|[\d,]+) contributions?\b", text)
            if match:
                value = 0 if match[1] == "No" else int(match[1].replace(",", ""))
                self.counts[self.target] = value
            self.target = None
            self.text = []

    def contributions(self):
        return {day: self.counts[key] for key, day in self.dates.items()
                if key in self.counts}


def parse_calendar(html: str) -> dict[date, int]:
    parser = CalendarParser()
    parser.feed(html)
    return parser.contributions()


def fetch_calendar(username: str, year: int) -> dict[date, int]:
    url = (f"https://github.com/users/{username}/contributions"
           f"?from={year}-01-01&to={year}-12-31")
    request = Request(url, headers={
        "User-Agent": "github-profile-activity/1.0",
        "Accept": "text/html", "Accept-Language": "en-US",
    })
    for attempt in range(3):
        try:
            with urlopen(request, timeout=25) as response:
                return parse_calendar(response.read().decode("utf-8"))
        except OSError:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    raise RuntimeError("Calendar download failed")


def select_days(calendar: dict[date, int], end: date) -> list[tuple[date, int]]:
    days = [end - timedelta(days=i) for i in range(30, -1, -1)]
    missing = [day.isoformat() for day in days if day not in calendar]
    if missing:
        raise ValueError("Incomplete GitHub calendar; keeping the previous graph: "
                         + ", ".join(missing))
    if any(not isinstance(calendar[day], int) or calendar[day] < 0 for day in days):
        raise ValueError("Contribution counts must be non-negative integers")
    return [(day, calendar[day]) for day in days]


def render_svg(username: str, days: list[tuple[date, int]]) -> str:
    if len(days) != 31:
        raise ValueError("Expected 31 days")
    counts = [count for _, count in days]
    maximum = max(3, ((max(counts) + 2) // 3) * 3)
    x0, x1, y0, y1 = 58, 952, 104, 242
    points = [(x0 + i * (x1 - x0) / 30,
               y1 - count * (y1 - y0) / maximum) for i, count in enumerate(counts)]
    line = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    area = f"{x0},{y1} {line} {x1},{y1}"
    total = sum(counts)
    active = sum(count > 0 for count in counts)
    start, end = days[0][0].isoformat(), days[-1][0].isoformat()
    title = escape(f"{username}: GitHub contributions, {start} — {end}")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="310" '
        'viewBox="0 0 1000 310" role="img" aria-labelledby="title desc">',
        f'<title id="title">{title}</title>',
        f'<desc id="desc">{total} public contributions across {active} active days. '
        'Source: GitHub public contribution calendar.</desc>',
        '<defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1">'
        '<stop stop-color="#2dd4bf" stop-opacity=".35"/>'
        '<stop offset="1" stop-color="#2dd4bf" stop-opacity=".02"/>'
        '</linearGradient></defs>',
        '<rect width="1000" height="310" rx="18" fill="#0d1726"/>',
        '<g font-family="Segoe UI,Arial,sans-serif">',
        '<text x="32" y="42" font-size="23" font-weight="700" fill="#f8fafc">'
        'GitHub · активность</text>',
        f'<text x="32" y="68" font-size="13" fill="#94a3b8">{start} — {end}</text>',
        f'<text x="952" y="42" text-anchor="end" font-size="15" '
        f'font-weight="600" fill="#5eead4">{total} contributions · {active} active days</text>',
    ]
    for step in range(4):
        value = maximum * step // 3
        y = y1 - (y1 - y0) * step / 3
        parts.append(f'<path d="M{x0} {y}H{x1}" stroke="#243447" stroke-width="1"/>')
        parts.append(f'<text x="42" y="{y + 4}" text-anchor="end" '
                     f'font-size="12" fill="#94a3b8">{value}</text>')
    parts.append(f'<polygon points="{area}" fill="url(#area)"/>')
    parts.append(f'<polyline points="{line}" fill="none" stroke="#2dd4bf" '
                 'stroke-width="2.5" stroke-linejoin="round"/>')
    for (day, count), (x, y) in zip(days, points):
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#5eead4">'
                     f'<title>{day.isoformat()}: {count} contributions</title></circle>')
    for i in (0, 5, 10, 15, 20, 25, 30):
        label = days[i][0].strftime("%d.%m")
        parts.append(f'<text x="{points[i][0]:.2f}" y="268" text-anchor="middle" '
                     f'font-size="12" fill="#94a3b8">{label}</text>')
    parts.append('<text x="32" y="294" font-size="11" fill="#64748b">'
                 'Source: GitHub public contribution calendar · Updated daily</text>')
    parts.append('</g></svg>')
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="golovanov-andrei")
    parser.add_argument("--output", type=Path, default=Path("assets/activity.svg"))
    parser.add_argument("--end-date", type=date.fromisoformat,
                        default=datetime.now(timezone.utc).date())
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", args.username):
        parser.error("Invalid GitHub username")
    start = args.end_date - timedelta(days=30)
    calendar = {}
    for year in sorted({start.year, args.end_date.year}):
        calendar.update(fetch_calendar(args.username, year))
    days = select_days(calendar, args.end_date)
    result = render_svg(args.username, days)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(f"Saved {args.output}: {sum(count for _, count in days)} contributions")


if __name__ == "__main__":
    main()
