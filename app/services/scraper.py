import asyncio
import re
from bs4 import BeautifulSoup
import aiohttp
from app.utils.oj_detector import parse_submission_url, build_api_url
from app.models.submission import Platform, Status


class OJScraper:
    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
            timeout = aiohttp.ClientTimeout(total=15)
            self.session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def scrape_submission(self, url: str, platform_str: str) -> dict:
        platform = Platform(platform_str)
        parsed = parse_submission_url(url, platform.value)
        target_url = build_api_url(parsed)

        session = await self._get_session()

        async with session.get(target_url) as response:
            if response.status != 200:
                raise Exception(f"请求失败: HTTP {response.status}")
            html = await response.text()

        if platform == Platform.LUOGU:
            return self._parse_luogu(html, parsed)
        elif platform == Platform.CODEFORCES:
            return self._parse_codeforces(html, parsed)

        raise ValueError(f"不支持的平台: {platform}")

    def _parse_luogu(self, html: str, parsed) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        result = {
            "platform": "luogu",
            "problem_id": "",
            "problem_name": "",
            "problem_url": "",
            "difficulty": None,
            "code": "",
            "language": None,
            "status": "WA",
            "failed_test_case": None,
        }

        title_elem = soup.select_one("h1") or soup.select_one(".lfe-h1-title")
        if title_elem:
            result["problem_name"] = title_elem.get_text(strip=True)

        code_elem = soup.select_one("pre code") or soup.select_one(".code")
        if code_elem:
            result["code"] = code_elem.get_text()

        status_text = soup.get_text()
        if "Wrong Answer" in status_text or "答案错误" in status_text:
            result["status"] = "WA"
        elif "Accepted" in status_text or "通过" in status_text:
            result["status"] = "AC"
        elif "Time Limit" in status_text or "超时" in status_text:
            result["status"] = "TLE"
        elif "Runtime Error" in status_text or "运行错误" in status_text:
            result["status"] = "RE"

        return result

    def _parse_codeforces(self, html: str, parsed) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        result = {
            "platform": "codeforces",
            "problem_id": f"{parsed.contest_id}" if parsed.contest_id else "",
            "problem_name": "",
            "problem_url": "",
            "difficulty": None,
            "code": "",
            "language": None,
            "status": "WA",
            "failed_test_case": None,
        }

        problem_elem = soup.select_one(".problem-statement .title") \
                       or soup.select_one("a[href*='problem']")
        if problem_elem:
            result["problem_name"] = problem_elem.get_text(strip=True)

        program_elem = soup.select_one("#program-source-text")
        if program_elem:
            result["code"] = program_elem.get_text()
        else:
            code_elem = soup.select_one("pre")
            if code_elem:
                result["code"] = code_elem.get_text()

        lang_elem = soup.select_one(".program-language")
        if lang_elem:
            result["language"] = lang_elem.get_text(strip=True)

        if soup.select_one(".verdict-wa") or soup.select_one(".verdict-rejected"):
            result["status"] = "WA"
        elif soup.select_one(".verdict-accepted"):
            result["status"] = "AC"

        tc_elem = soup.select_one(".stateFAILED .test-case-number")
        if tc_elem:
            try:
                result["failed_test_case"] = int(tc_elem.get_text().strip())
            except ValueError:
                pass

        return result


scraper = OJScraper()
