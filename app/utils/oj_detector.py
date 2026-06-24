import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ParsedSubmission:
    platform: str
    submission_id: str
    contest_id: str | None = None
    problem_index: str | None = None


def detect_platform(url: str) -> str | None:
    domain = urlparse(url).netloc.lower()
    if "luogu" in domain:
        return "luogu"
    elif "codeforces" in domain:
        return "codeforces"
    elif "atcoder" in domain:
        return "atcoder"
    return None


def parse_submission_url(url: str, platform: str) -> ParsedSubmission:
    if platform == "luogu":
        match = re.search(r'/record/(\d+)', url)
        if match:
            return ParsedSubmission(platform="luogu", submission_id=match.group(1))
    elif platform == "codeforces":
        match = re.search(r'/contest/(\d+)/submission/(\d+)', url)
        if match:
            return ParsedSubmission(
                platform="codeforces",
                contest_id=match.group(1),
                submission_id=match.group(2),
            )
    raise ValueError(f"无法解析 URL: {url}")


def build_api_url(parsed: ParsedSubmission) -> str:
    if parsed.platform == "luogu":
        return f"https://www.luogu.com.cn/record/{parsed.submission_id}"
    elif parsed.platform == "codeforces":
        return f"https://codeforces.com/contest/{parsed.contest_id}/submission/{parsed.submission_id}"
    raise ValueError(f"不支持的平台: {parsed.platform}")
