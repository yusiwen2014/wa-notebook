"""
WA错题本 - Mock AI 分析器 v0.0.3
支持问题分类：CE / RE / WA / TLE / MLE
其中 RE 分为除以0、越界访问；WA 分为思路错误、代码错误
"""

ERROR_CATEGORIES = {
    # ====== 编译错误 ======
    "CE": {
        "name": "CE 编译错误",
        "severity": "low",
        "summaries": [
            "代码无法通过编译，存在语法或类型错误",
            "编译器报告了语法错误，需要检查代码结构",
        ],
        "details": [
            "常见的编译错误包括：缺少分号、括号不匹配、变量未声明、类型不匹配。",
            "请仔细阅读编译器输出的错误信息，通常会指出具体的行号和错误类型。",
        ],
        "suggestions": "根据编译器报错定位到具体行，优先检查语法和拼写错误。",
        "error_points": [
            "编译器报错行号及具体错误信息",
            "头文件/命名空间是否缺失",
            "括号、引号、分号是否成对匹配",
            "变量是否在使用前声明",
        ],
        "hints": [
            "编译器报错提示在哪一行？",
            "是否缺少头文件或 using namespace std;？",
            "所有的括号、引号是否成对出现？",
        ],
    },

    # ====== 运行错误 ======
    "RE_div0": {
        "name": "RE 除以零",
        "severity": "low",
        "summaries": [
            "程序运行中出现除以零错误",
            "分母可能为 0，导致运行时错误",
        ],
        "details": [
            "除法、取模运算前必须判断分母是否为 0。",
            "特别注意输入数据可能导致分母为 0 的边界情况。",
        ],
        "suggestions": "在执行除法或取模前，增加对分母是否为 0 的判断。",
        "error_points": [
            "所有涉及除法/取模的位置",
            "分母为 0 的边界输入",
            "整数除法与浮点除法混淆",
            "中间结果是否可能为 0",
        ],
        "hints": [
            "你的代码中哪些位置进行了除法或取模？",
            "分母有没有可能是 0？",
            "如果输入全为 0，你的程序会怎样？",
        ],
    },
    "RE_oob": {
        "name": "RE 越界访问",
        "severity": "low",
        "summaries": [
            "数组或容器访问越界，导致运行时错误",
            "访问了非法内存地址",
        ],
        "details": [
            "检查所有数组下标访问是否在有效范围内。",
            "注意 i=0、i=n-1、i=n 等临界位置。",
        ],
        "suggestions": "养成习惯：每次写循环前先明确 [l, r] 的开闭区间含义。",
        "error_points": [
            "数组/vector 下标访问范围",
            "循环边界是否越界",
            "数组大小是否足够",
            "递归栈是否过深",
        ],
        "hints": [
            "你的循环是从 0 开始还是从 1 开始？",
            "当 n=1 时，你的代码会访问到 arr[-1] 或 arr[n] 吗？",
            "数组开得足够大吗？",
        ],
    },

    # ====== 答案错误 ======
    "WA_logic": {
        "name": "WA 思路错误",
        "severity": "high",
        "summaries": [
            "算法思路与题目要求不符",
            "核心逻辑存在缺陷，当前解法无法覆盖所有情况",
        ],
        "details": [
            "仔细对比你的算法和题目要求，找出遗漏的条件。",
            "尝试手动模拟几个边界样例，看是否与预期一致。",
        ],
        "suggestions": "建议回到题目描述，逐条核对每个约束条件是否都被正确处理。",
        "error_points": [
            "题意理解是否完整",
            "算法选择是否正确",
            "状态定义/转移是否遗漏",
            "边界条件是否全部覆盖",
        ],
        "hints": [
            "这道题的核心要求是什么？",
            "有没有哪个条件你觉得比较特殊？",
            "如果输入是最小/最大值，你的代码还能正确运行吗？",
        ],
    },
    "WA_code": {
        "name": "WA 代码错误",
        "severity": "low",
        "summaries": [
            "算法思路正确，但代码实现细节有误",
            "拼写、运算符、边界等小错误导致答案错误",
        ],
        "details": [
            "常见原因：== 写成 =、变量名写错、循环边界错误、复制粘贴未修改。",
            "思路没问题的情况下，建议逐行检查代码。",
        ],
        "suggestions": "写完后通读一遍代码，重点关注运算符和变量名。",
        "error_points": [
            "== 与 = 是否混用",
            "变量名/数组名是否一致",
            "循环边界是否有 ±1 偏差",
            "输入输出格式是否匹配",
        ],
        "hints": [
            "所有赋值语句里的 == 都检查过了吗？",
            "复制粘贴过来的代码块里，变量名都改过来了吗？",
            "循环边界有没有 ±1 的错误？",
        ],
    },

    # ====== 时间超限 ======
    "TLE": {
        "name": "TLE 时间超限",
        "severity": "high",
        "summaries": [
            "时间复杂度过高，无法在规定时间内完成",
            "算法效率不足或存在冗余计算",
        ],
        "details": [
            "一般 O(n²) 在 n≤10⁵ 时会 TLE。",
            "检查是否有不必要的重复计算，考虑记忆化或预处理。",
        ],
        "suggestions": "先估算数据规模，再选择合适的算法复杂度级别。",
        "error_points": [
            "时间复杂度与数据规模匹配度",
            "是否存在重复计算",
            "是否可以预处理/前缀和优化",
            "输入输出是否使用快速 IO",
        ],
        "hints": [
            "题目中 n 和 m 的最大值分别是多少？",
            "你的算法在最坏情况下要执行多少次基本操作？",
            "有没有重复计算的子问题？",
        ],
    },

    # ====== 内存超限 ======
    "MLE": {
        "name": "MLE 内存超限",
        "severity": "high",
        "summaries": [
            "申请的内存超过题目限制",
            "数据结构选择不当导致空间浪费",
        ],
        "details": [
            "注意题目给出的内存限制（通常 256MB 或 512MB）。",
            "大数组尽量开在全局而非函数内部。",
        ],
        "suggestions": "估算一下你的数据结构大概占用多少内存。",
        "error_points": [
            "数组/数据结构大小估算",
            "内存限制是否清楚",
            "是否可以滚动数组优化",
            "递归栈深度是否过大",
        ],
        "hints": [
            "题目内存限制是多少 MB？",
            "数组是在 main 函数里面开的还是全局的？",
            "有没有可以不用存下来的数据？",
        ],
    },
}


def _detect_from_status(status: str, code: str) -> str:
    """根据判题状态进行初步分类"""
    s = status.upper().strip()

    if s == "CE" or s == "COMPILATION ERROR":
        return "CE"
    if s == "RE" or s == "RUNTIME ERROR":
        # 判断是除以0还是越界
        if any(kw in code.lower() for kw in ["/", "%", "div", "/="]):
            return "RE_div0"
        return "RE_oob"
    if s == "TLE" or s == "TIME LIMIT EXCEEDED":
        return "TLE"
    if s == "MLE" or s == "MEMORY LIMIT EXCEEDED":
        return "MLE"

    # WA 需要进一步判断是思路还是代码
    return None


def _detect_wa_subtype(code: str, problem_name: str) -> str:
    """判断 WA 是思路错误还是代码错误"""
    combined = (code + " " + problem_name).lower()

    # 思路错误关键词：算法方向、复杂结构
    logic_keywords = [
        "dp[", "dp(", "状态", "转移", "记忆化", "贪心", "dfs", "bfs",
        "最短路", "最小生成树", "图论", "树形", "二分", "网络流",
        "算法", "思路", "逻辑错误",
    ]

    # 代码错误关键词：细节、拼写、边界、类型
    code_keywords = [
        "==", "=", "++", "--", "[", "]", "for", "while", "if",
        "int", "long long", "scanf", "cin", "cout", "printf",
    ]

    logic_score = sum(1 for kw in logic_keywords if kw in combined)
    code_score = sum(1 for kw in code_keywords if kw in combined)

    # 简单启发：只要出现算法关键词就视为思路错误，否则代码错误
    if logic_score >= 1:
        return "WA_logic"
    return "WA_code"


class MockAnalyzer:
    def analyze(self, code: str, status: str, problem_name: str = "") -> dict:
        category = _detect_from_status(status, code)
        if category is None:
            category = _detect_wa_subtype(code, problem_name)
        return self._build_result(category)

    def _build_result(self, category):
        import random
        cat_info = ERROR_CATEGORIES[category]
        summary_idx = random.randint(0, len(cat_info["summaries"]) - 1)
        detail_idx = random.randint(0, len(cat_info["details"]) - 1)

        return {
            "error_category": category,
            "error_severity": cat_info["severity"],
            "error_summary": cat_info["summaries"][summary_idx],
            "error_detail": cat_info["details"][detail_idx],
            "suggestion": cat_info["suggestions"],
            "error_points": cat_info["error_points"],
            "hints": cat_info["hints"],
        }

    def get_next_hint(self, hints: list, current_index: int) -> tuple:
        if not hints:
            return ("暂无可用的提示", current_index)
        if current_index >= len(hints):
            return ("💡 你已经掌握了所有引导步骤，现在尝试独立修复这道题吧！", current_index)
        return (hints[current_index], current_index + 1)


analyzer = MockAnalyzer()
