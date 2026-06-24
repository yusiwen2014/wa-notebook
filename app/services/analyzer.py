ERROR_CATEGORIES = {
    "logic_error": {
        "name": "逻辑错误",
        "severity": "high",
        "keywords": ["逻辑", "思路", "算法", "方向"],
        "summaries": [
            "算法思路与题目要求不符，建议重新审题",
            "核心逻辑存在缺陷，当前解法无法覆盖所有情况",
            "贪心/DP 状态转移方程可能有误",
        ],
        "details": [
            "仔细对比你的算法和题目要求，找出遗漏的条件。",
            "尝试手动模拟几个边界样例，看是否与预期一致。",
            "考虑是否有反例可以推翻当前的思路。",
        ],
        "suggestions": "建议回到题目描述，逐条核对每个约束条件是否都被正确处理了。",
        "hints": [
            "这道题的核心要求是什么？你的代码主要实现了哪部分？",
            "有没有哪个条件你觉得比较特殊？它是怎么处理的？",
            "如果输入是最小/最大值，你的代码还能正确运行吗？",
            "试着画一个简单的例子，一步步跟踪代码执行过程。",
        ],
    },
    "boundary": {
        "name": "边界条件",
        "severity": "low",
        "keywords": ["边界", "越界", "范围", "首尾", "空"],
        "summaries": [
            "数组访问越界，未处理空数据或极端边界情况",
            "循环边界条件设置不当，导致少处理或多处理元素",
        ],
        "details": [
            "检查所有数组/容器的下标访问，确保不会超出有效范围。",
            "特别注意 i=0、i=n-1、i=n 这些临界位置的处理。",
            "空数组、单元素数组等特殊情况是否被覆盖？",
        ],
        "suggestions": "养成习惯：每次写循环前先明确 [l, r] 的开闭区间含义。",
        "hints": [
            "你的循环是从 0 开始还是从 1 开始？到 n 还是到 n-1 结束？",
            "当 n=1 时，你的代码会怎么执行？会有问题吗？",
            "有没有可能访问到 arr[-1] 或 arr[n] 这种非法下标？",
        ],
    },
    "overflow": {
        "name": "整数溢出",
        "severity": "low",
        "keywords": ["溢出", "int", "long long", "范围", "1e9", "1e18", "2^31"],
        "summaries": [
            "数据类型范围不足，中间运算结果溢出",
            "应使用 long long (int64) 但使用了 int (int32)",
        ],
        "details": [
            "int 范围约 ±2.1×10⁹，long long 范围约 ±9.2×10¹⁸",
            "即使最终结果在范围内，中间乘法也可能溢出",
            "特别注意累加/累乘操作的数据类型",
        ],
        "suggestions": "竞赛中默认使用 long long，除非确定数据范围很小。",
        "hints": [
            "题目给定的数据最大值是多少？int 能存下吗？",
            "你的代码中有乘法或累加操作吗？中间结果会不会超 int？",
            "把变量类型改成 long long 后再试试？",
        ],
    },
    "uninitialized": {
        "name": "变量未初始化",
        "severity": "low",
        "keywords": ["未初始化", "垃圾值", "随机值", "初始值"],
        "summaries": [
            "局部变量声明后未赋初值就读取，导致不确定行为",
            "数组/容器未清空就被复用",
        ],
        "details": [
            "C++ 中局部变量不会自动初始化为 0",
            "vector resize 后新元素的值是不确定的",
            "多次测试用例之间记得重置全局变量",
        ],
        "suggestions": "声明变量时顺手赋初值，这是好习惯。",
        "hints": [
            "你声明的每个变量都有明确的初始值吗？",
            "如果这段代码跑第二遍，全局变量的值还是正确的吗？",
            "编译器开了 -Wall 警告了吗？看看有没有 uninitialized 警告。",
        ],
    },
    "complexity": {
        "name": "复杂度超限",
        "severity": "high",
        "keywords": ["超时", "TLE", "复杂度", "O(", "n²", "n³"],
        "summaries": [
            "时间复杂度过高，无法在规定时间内完成",
            "嵌套循环过多或算法选择不当",
        ],
        "details": [
            "一般 O(n²) 在 n≤10⁵ 时会 TLE",
            "检查是否有不必要的重复计算",
            "考虑是否可以使用更优的算法或数据结构",
        ],
        "suggestions": "先估算数据规模，再选择合适的算法复杂度级别。",
        "hints": [
            "题目中 n 和 m 的最大值分别是多少？",
            "你的算法在最坏情况下要执行多少次基本操作？",
            "有没有重复计算的子问题？能否用记忆化或预处理优化？",
        ],
    },
    "precision": {
        "name": "精度问题",
        "severity": "low",
        "keywords": ["精度", "浮点", "double", "eps", "误差"],
        "summaries": [
            "浮点数比较未使用 eps 容差，导致判断错误",
            "输出格式中小数位数不足",
        ],
        "details": [
            "浮点数不能直接用 == 比较，应使用 abs(a-b) < eps",
            "注意 double 精度约 15-16 位有效数字",
            "输出时注意四舍五入 vs 直接截断的区别",
        ],
        "suggestions": "浮点运算统一使用 double + eps 比较。",
        "hints": [
            "你的代码中有浮点数相等判断吗？用了 eps 吗？",
            "输出要求保留几位小数？printf 格式对吗？",
            "是否存在大数减小数导致精度丢失的情况？",
        ],
    },
    "io_format": {
        "name": "输入输出格式",
        "severity": "low",
        "keywords": ["输入", "输出", "格式", "scanf", "cin", "换行", "空格"],
        "summaries": [
            "读入/输出格式与题目要求不一致",
            "多组数据未正确处理，缺少循环读取",
        ],
        "details": [
            "检查是否有 T 组测试数据但只读了 1 组",
            "注意每行末尾的换行符和多余的空格",
            "输入数据间可能是空格也可能是换行分隔",
        ],
        "suggestions": "仔细阅读题目的「输入格式」和「输出格式」说明。",
        "hints": [
            "题目说有几组测试数据？你的代码循环了几次？",
            "样例输入和你的读入方式完全匹配吗？",
            "输出的每一行末尾有多余的空格吗？（PE 错误常见原因）",
        ],
    },
    "memory": {
        "name": "内存超限",
        "severity": "high",
        "keywords": ["内存", "MLE", "空间", "数组太大", "vector"],
        "summaries": [
            "申请的内存超过题目限制",
            "数据结构选择不当导致空间浪费",
        ],
        "details": [
            "注意题目给出的内存限制（通常 256MB 或 512MB）",
            "大数组尽量开在全局而非函数内部（栈空间有限）",
            "避免存储冗余数据，按需计算",
        ],
        "suggestions": "估算一下你的数据结构大概占用多少内存。",
        "hints": [
            "题目内存限制是多少 MB？你的数组大小 × 元素大小 = ？",
            "数组是在 main 函数里面开的还是全局的？",
            "有没有可以不用存下来、边算边丢掉的数据？",
        ],
    },
    "typo": {
        "name": "拼写/笔误",
        "severity": "low",
        "keywords": ["拼写", "笔误", "打错", "手滑", "复制粘贴"],
        "summaries": [
            "变量名拼错、运算符写反等低级失误",
            "复制粘贴后忘记修改变量名",
        ],
        "details": [
            "常见的：把 == 写成 =，把 i 写成 j，把 < 写成 <=",
            "复制一段代码后，内部的变量索引忘记更新",
        ],
        "suggestions": "这类错误最难发现，建议写完后通读一遍代码。",
        "hints": [
            "所有赋值语句里的 == 都检查过了吗？没有写成 = ？",
            "复制粘贴过来的代码块里，变量名都改过来了吗？",
            "把代码大声读一遍，有时候能发现眼睛忽略的错误。",
        ],
    },
    "modular": {
        "name": "取模错误",
        "severity": "low",
        "keywords": ["模", "%", "MOD", "取余", "负数"],
        "summaries": [
            "取模操作时机不对或遗漏",
            "负数取模结果不符合预期（C++ 中负 % 正 = 负）",
        ],
        "details": [
            "每一步运算后都要取模，不能只在最后取",
            "C++ 中负数取模结果是负数，需要 (x % MOD + MOD) % MOD",
            "减法后也要取模防止出现负数",
        ],
        "suggestions": "涉及取模的题目，封装一个安全的 add/mul 函数。",
        "hints": [
            "你的代码中有减法吗？减完之后取模了吗？结果可能是负数吗？",
            "每一步乘法和加法之后都有 % MOD 吗？",
            "写一个 (a+b)%MOD 的安全加法函数来替代直接运算？",
        ],
    },
    "graph": {
        "name": "图论细节",
        "severity": "high",
        "keywords": ["图", "树", "DFS", "BFS", "连通", "环", "最短路"],
        "summaries": [
            "图的遍历漏节点或多走节点",
            "建图方式与题目给出的形式不匹配",
        ],
        "details": [
            "无向图要双向加边！这是最常见的图论错误",
            "注意 1-indexed 和 0-indexed 的转换",
            "DFS/BFS 访问标记要在入队/入栈时就设置，不是出的时候",
        ],
        "suggestions": "图论题目先确认：有向/无向？1-index/0-index？多重边/自环？",
        "hints": [
            "这道题的图是有向的还是无向的？加了几条边？",
            "点的编号是从 0 开始还是从 1 开始？你的数组够大吗？",
            "vis 标记是在进 DFS 之前设的还是之后设的？",
        ],
    },
    "dp": {
        "name": "DP 状态/转移错误",
        "severity": "high",
        "keywords": ["DP", "动态规划", "状态", "转移", "最优子结构"],
        "summaries": [
            "DP 状态定义不完整或有重叠",
            "状态转移方程遗漏情况或转移顺序错误",
            "初始化边界值设置不当",
        ],
        "details": [
            "先想清楚「状态表示什么」，再写转移方程",
            "检查 DP 数组的维度是否包含了所有必要的决策因素",
            "边界情况（如空串、长度为1）的手动初始化不要漏",
        ],
        "suggestions": "DP 题目一定要先在纸上画出状态转移表格。",
        "hints": [
            "你的 DP 状态数组 dp[i][j] 具体代表什么含义？",
            "从状态 A 转移到状态 B，有哪些可能的决策？都列出来了吗？",
            "最小的子问题（如 i=0 或 i=1）的值是多少？初始化对吗？",
        ],
    },
}


class MockAnalyzer:
    def analyze(self, code: str, status: str, problem_name: str = "") -> dict:
        code_lower = code.lower()
        combined = code_lower + " " + status.lower() + " " + problem_name.lower()

        if any(kw in combined for kw in ["dfs", "bfs", "邻接", "adj", "graph"]):
            if "addedge" in code_lower or ("<<" in code_lower and ">>" not in code_lower[:50]):
                return self._build_result("graph")

        if any(kw in combined for kw in ["dp[", "dp(", "memo", "记忆化", "状态转移"]):
            return self._build_result("dp")

        if "%" in code and ("mod" in code_lower or "1000000007" in code or "998244353" in code):
            return self._build_result("modular")

        if status.upper() in ("TLE", "TIME LIMIT"):
            return self._build_result("complexity")

        # 边界条件优先于溢出：访问 a[i]/a[n] 且循环边界异常
        if any(kw in code_lower for kw in ["[n]", "[m]", ".size()", ".length", "vector<", "["]):
            if "for" in code_lower and ("i <=" in code_lower or "i >= " in code_lower or "a[n]" in code_lower):
                return self._build_result("boundary")

        if ("int " in code_lower and "long long" not in code_lower) or \
           ("1e9" in code or "1e18" in code or "2e9" in code):
            if "int " in code_lower[:500]:
                return self._build_result("overflow")

        if any(kw in combined for kw in ["vector", "数组", "memset"]):
            if "resize" in code_lower or "push_back" in code_lower:
                return self._build_result("uninitialized")

        if any(kw in code_lower for kw in ["cin", "scanf", "cout", "printf", "while"]):
            return self._build_result("io_format")

        return self._build_result("logic_error")

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
            "hints": cat_info["hints"],
        }

    def get_next_hint(self, hints: list, current_index: int) -> tuple[str, int]:
        if not hints:
            return ("暂无可用的提示", current_index)

        if current_index >= len(hints):
            return ("💡 你已经掌握了所有引导步骤，现在尝试独立修复这道题吧！", current_index)

        return (hints[current_index], current_index + 1)


analyzer = MockAnalyzer()
