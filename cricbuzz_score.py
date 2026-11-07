"""
playwright_Automation_cricbuzz_score.py

Finds a completed match from Cricbuzz's Recent Matches page, opens its
scorecard, extracts the innings scores and result from rendered page text,
and saves score.png.

Install:
    python -m pip install playwright
    python -m playwright install chromium

Run headed:
    python playwright_Automation_cricbuzz_score.py

Run headless:
    python playwright_Automation_cricbuzz_score.py --headless

Optional:
    python playwright_Automation_cricbuzz_score.py --recent-url "https://www.cricbuzz.com/cricket-match/live-scores/recent-matches"
"""

import argparse
import re
import sys
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

HOME_URL = "https://www.cricbuzz.com/"
RECENT_URL = "https://www.cricbuzz.com/cricket-match/live-scores/recent-matches"
SCREENSHOT = "score.png"
TIMEOUT_MS = 45_000

# Score formats: IND 287-4 (45.2), IND 287/4 (45.2 Ov), 287-4 (45.2 Ov)
SCORE_RE = re.compile(
    r"(?<!\d)([A-Z][A-Z0-9]{1,8})\s+(\d{1,3})\s*[-/]\s*(\d{1,2})"
    r"\s*\(\s*(\d{1,2}(?:\.\d)?)\s*(?:Ov|Overs)?\s*\)",
    re.IGNORECASE,
)
RESULT_RE = re.compile(
    r"([A-Z][A-Za-z .&'-]+?)\s+won\s+by\s+"
    r"(\d+\s+(?:runs?|wickets?|wkts?))",
    re.IGNORECASE,
)


def normalize(value):
    return re.sub(r"\s+", " ", value).strip()


def find_completed_match_link(page):
    """
    Inspect links in the recent-matches page. Choose the first visible
    match link whose surrounding card text contains a completed result.
    """
    links = page.locator("a[href]")
    count = links.count()

    for index in range(count):
        link = links.nth(index)
        try:
            if not link.is_visible():
                continue

            href = link.get_attribute("href") or ""
            if not any(part in href for part in (
                "live-cricket-scorecard",
                "live-cricket-scores/",
            )):
                continue

            # Match cards normally contain score and result text in a nearby
            # parent container. Inspect a few ancestors without assuming CSS classes.
            card_text = link.evaluate(
                """el => {
                    let node = el;
                    for (let i = 0; i < 5 && node; i++, node = node.parentElement) {
                        const t = (node.innerText || "").trim();
                        if (t.length > 20 && t.length < 1200 &&
                            /won by|match drawn|match tied|abandoned/i.test(t)) {
                            return t;
                        }
                    }
                    return (el.innerText || "").trim();
                }"""
            )
            if re.search(r"won by|match drawn|match tied|abandoned", card_text, re.I):
                return urljoin(RECENT_URL, href), normalize(card_text)
        except Exception:
            continue

    return None, None


def extract_score_lines(text):
    """Extract team abbreviation, runs, wickets and overs from page text."""
    matches = SCORE_RE.findall(text.upper())
    return [
        (team, runs, wickets, overs)
        for team, runs, wickets, overs in matches
    ]


def extract_result(text):
    match = RESULT_RE.search(text)
    if match:
        winner = normalize(match.group(1))
        margin = normalize(match.group(2))
        margin = re.sub(r"\bwkts?\b", "wickets", margin, flags=re.I)
        return f"{winner} won by {margin}"

    for phrase in ("Match drawn", "Match tied", "Match abandoned"):
        if re.search(re.escape(phrase), text, re.I):
            return phrase
    return None


def format_output(page, page_text):
    scores = extract_score_lines(page_text)
    if not scores:
        raise ValueError(
            "No team score pattern was found on the scorecard. "
            "Cricbuzz may have changed its page layout."
        )

    # Scorecards list innings in order; the final innings score is normally last.
    team, runs, wickets, overs = scores[-1]
    title = normalize(page.title())

    # Prefer team abbreviations found in the scorecard title; otherwise use
    # the final innings' team code and a neutral opponent label.
    title_match = re.search(
        r"([A-Z0-9]{2,8})\s+vs\.?\s+([A-Z0-9]{2,8})",
        title,
        re.I,
    )
    if title_match:
        team_a, team_b = title_match.group(1).upper(), title_match.group(2).upper()
    else:
        team_a, team_b = "MATCH", team

    result = extract_result(page_text)
    if not result:
        raise ValueError(
            "The page did not contain a completed-match result. "
            "The selected match may not be completed."
        )

    score_line = f"{team} {runs}/{wickets} ({overs} Ov)"
    status_line = f"{team_a} vs {team_b} - {result}"
    return score_line, status_line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--recent-url", default=RECENT_URL)
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})

        try:
            print("Opening Cricbuzz...")
            page.goto(HOME_URL, wait_until="domcontentloaded", timeout=60_000)

            print("Opening recent matches...")
            page.goto(args.recent_url, wait_until="domcontentloaded", timeout=60_000)

            # Wait for completed-result text to be rendered on the recent page.
            page.wait_for_function(
                """() => /won by|match drawn|match tied|abandoned/i.test(
                    document.body?.innerText || ""
                )""",
                timeout=TIMEOUT_MS,
            )

            match_url, card_text = find_completed_match_link(page)
            if not match_url:
                # Diagnostic fallback: recent-match page may expose results
                # as text but not a scorecard anchor detectable by this version.
                raise ValueError(
                    "A completed result was visible, but no scorecard link "
                    "could be identified on the recent-matches page."
                )

            print("Opening a completed match scorecard...")
            page.goto(match_url, wait_until="domcontentloaded", timeout=60_000)

            # Wait until one innings score is visible in the rendered DOM.
            page.wait_for_function(
                """() => /\\b[A-Z0-9]{2,8}\\s+\\d{1,3}\\s*[-/]\\s*\\d{1,2}\\s*\\(\\s*\\d{1,2}(?:\\.\\d)?\\s*(?:Ov|Overs)?\\s*\\)/i.test(
                    document.body?.innerText || ""
                )""",
                timeout=TIMEOUT_MS,
            )

            page_text = page.locator("body").inner_text(timeout=15_000)
            score_line, status_line = format_output(page, page_text)

            print()
            print(score_line)
            print(status_line)
            print()

            page.screenshot(path=SCREENSHOT, full_page=True)
            print(f"saved {SCREENSHOT}")
            return 0

        except PlaywrightTimeoutError:
            print("Timed out waiting for Cricbuzz match content.")
            print("Current URL:", page.url)
            try:
                print("Page title:", page.title())
                print("Page text preview:")
                print(page.locator("body").inner_text(timeout=5_000)[:1500])
            except Exception:
                print("Could not retrieve diagnostic page text.")
            page.screenshot(path=SCREENSHOT, full_page=True)
            print(f"saved {SCREENSHOT} (diagnostic screenshot)")
            return 1

        except Exception as exc:
            print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
            try:
                print("Current URL:", page.url)
                print("Page title:", page.title())
                print("Page text preview:")
                print(page.locator("body").inner_text(timeout=5_000)[:1500])
                page.screenshot(path=SCREENSHOT, full_page=True)
                print(f"saved {SCREENSHOT} (diagnostic screenshot)")
            except Exception:
                pass
            return 1

        finally:
            browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
