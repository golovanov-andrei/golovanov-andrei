from datetime import date, timedelta
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location(
    "activity", Path(__file__).resolve().parents[1] / "scripts/update_activity.py")
activity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activity)


class ActivityTests(unittest.TestCase):
    def test_counts_come_from_tooltips_not_colour_levels(self):
        html = '''
        <td id="a" data-date="2026-10-14" data-level="0"></td>
        <td id="b" data-date="2026-10-15" data-level="4"></td>
        <tool-tip for="a">No contributions on October 14th.</tool-tip>
        <tool-tip for="b">1,234 contributions on October 15th.</tool-tip>
        '''
        self.assertEqual(activity.parse_calendar(html), {
            date(2026, 10, 14): 0, date(2026, 10, 15): 1234})

    def test_missing_data_is_not_silently_reported_as_zero(self):
        end = date(2026, 1, 10)
        calendar = {end - timedelta(days=i): 0 for i in range(31)}
        self.assertEqual(len(activity.select_days(calendar, end)), 31)
        del calendar[date(2025, 12, 31)]
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            activity.select_days(calendar, end)

    def test_graph_retains_dates_counts_and_accessible_description(self):
        end = date(2026, 10, 15)
        calendar = {end - timedelta(days=i): int(i == 0) * 6 for i in range(31)}
        svg = activity.render_svg("golovanov-andrei", activity.select_days(calendar, end))
        root = ET.fromstring(svg)
        ns = {"s": "http://www.w3.org/2000/svg"}
        circles = root.findall(".//s:circle", ns)
        self.assertEqual(len(circles), 31)
        self.assertEqual(circles[-1].find("s:title", ns).text,
                         "2026-10-15: 6 contributions")
        self.assertIn("6 public contributions across 1 active days", root.find("s:desc", ns).text)


if __name__ == "__main__":
    unittest.main()
