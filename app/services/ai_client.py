"""
WA错题本 - AI 分析客户端
支持 OpenAI 兼容 API（OpenAI、DeepSeek、SiliconFlow 等）
"""

import json
import os
import aiohttp
from typing import Optional

from app.services.analyzer import analyzer, ERROR_CATEGORIES


DEFAULT_PROMPT = """你是一位资深的 OI/ACM 竞赛教练。请分析以下代码提交的错误。

题目信息：{problem_name}
提交状态：{status}
代码：
```{language}
{code}
```

请按以下 JSON 格式返回分析结果（不要包含任何其他文字）：
{{
    "error_category": "logic_error|boundary|overflow|uninitialized|complexity|precision|io_format|memory|typo|modular|graph|dp",
    "error_severity": "low|high",
    "error_summary": "一句话概述错误",
    "error_detail": "详细分析错误原因",
    "suggestion": "具体的修改建议",
    "hints": ["引导提示1", "引导提示2", "引导提示3"]
}}
"""


class AIAnalyzerClient:
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        self.provider = provider
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self.model = model or "gpt-4o-mini"
        self.prompt = prompt or DEFAULT_PROMPT

    def _build_messages(self, code: str, status: str, problem_name: str, language: Optional[str]) -> list:
        system_prompt = self.prompt
        user_prompt = DEFAULT_PROMPT.format(
            problem_name=problem_name or "未提供",
            status=status,
            code=code,
            language=language or "cpp",
        )
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    async def analyze(self, code: str, status: str, problem_name: str = "", language: Optional[str] = None) -> dict:
        if not self.api_key or self.provider == "mock":
            # 未配置 API Key 时回退到 Mock
            return analyzer.analyze(code, status, problem_name)

        messages = self._build_messages(code, status, problem_name, language)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "response_format": {"type": "json_object"},
                },
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"AI API 请求失败: HTTP {response.status} - {text}")

                data = await response.json()
                content = data["choices"][0]["message"]["content"]
                result = json.loads(content)
                return self._normalize_result(result)

    async def chat(self, messages: list) -> dict:
        """通用聊天接口 - 支持多轮对话"""
        if not self.api_key or self.provider == "mock":
            return self._mock_chat(messages)

        # 注入系统提示词
        system_messages = [{"role": "system", "content": self.prompt}]
        full_messages = system_messages + messages

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": full_messages,
                    "temperature": 0.7,
                },
                timeout=aiohttp.ClientTimeout(total=90),
            ) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"AI API 请求失败: HTTP {response.status} - {text}")

                data = await response.json()
                return {
                    "reply": data["choices"][0]["message"]["content"],
                    "model": data.get("model", self.model),
                    "usage": data.get("usage", {}),
                }

    def _mock_chat(self, messages: list) -> dict:
        """Mock 聊天 - 无 API Key 时使用内置规则回复"""
        last_msg = messages[-1]["content"] if messages else ""
        lower = last_msg.lower()

        # 简单的关键词匹配回复
        replies = {
            "时间复杂度": "常见算法复杂度参考：\n- O(1): 常数操作\n- O(log n): 二分查找\n- O(n): 遍历\n- O(n log n): 排序\n- O(n²): 双重循环\n- O(2ⁿ): 暴力枚举\n\n建议使用 `std::sort` (O(n log n)) 替代手写冒泡排序 (O(n²))。",
            "空间复杂度": "空间优化技巧：\n1. 使用滚动数组替代完整 DP 表\n2. 就地修改而非创建副本\n3. 用位运算压缩状态\n4. 注意全局变量和栈空间限制（通常 256MB）",
            "边界条件": "常见的边界错误：\n1. 数组越界：`for(int i=0;i<=n;i++)` 应为 `<n`\n2. 整数溢出：`int` 最大约 2×10⁹，用 `long long`\n3. 除零错误：检查分母是否为 0\n4. 空集合处理：先判断是否为空",
            "dp": "动态规划解题步骤：\n1. 定义状态 `dp[i]` 表示什么含义\n2. 找状态转移方程\n3. 确定初始条件和边界\n4. 计算顺序（从小到大/从大到小）\n5. 优化空间（可选）",
            "图论": "常用图论算法总结：\n- 最短路：Dijkstra（非负权）、SPFA/Bellman-Ford（负权）\n- MST：Kruskal / Prim\n- 连通性：DFS/BFS、Tarjan 强连通分量\n- 二分图：匈牙利算法、网络流",
            "快速幂": "快速幂模板（C++）：\n```cpp\nll qpow(ll a, ll b, ll mod) {\n    ll res=1; a%=mod;\n    while(b>0){\n        if(b&1) res=res*a%mod;\n        a=a*a%mod; b>>=1;\n    }\n    return res;\n}\n```",
            "gcd": "GCD/LCM 模板：\n```cpp\nll gcd(ll a,ll b){return b?gcd(b,a%b):a;}\nlcm lcm(a,b){return a/gcd(a,b)*b;}\n```",
        }

        for keyword, reply in replies.items():
            if keyword in lower:
                return {"reply": reply, "model": "mock-wa-notebook"}

        # 默认回复
        default_replies = [
            "这是一个很好的问题！作为你的竞赛教练，我建议你从以下几个方面思考：\n\n1. **理解题意**：确保完全读懂题目要求和数据范围\n2. **选择算法**：根据数据规模选择合适的时间复杂度\n3. **注意细节**：边界条件、数据类型、输入输出格式\n4. **验证样例**：用给定的样例测试代码\n\n如果你有具体的代码或题目，可以发给我帮你分析！",
            "在竞赛编程中，这个问题通常可以通过以下思路解决：\n\n- 先分析约束条件（n, m 的范围）\n- 选择合适的算法范式（贪心/DP/搜索/数学）\n- 注意特殊情况和边界测试\n\n需要我针对某个具体知识点详细讲解吗？比如动态规划、图论、数论等？",
            "好的！我注意到你可能遇到了一些编程上的困惑。以下是一些通用建议：\n\n**调试技巧**：\n- 打印中间变量观察变化\n- 对比正确输出和你的输出\n- 使用断点逐步执行\n\n**常见坑点**：\n- 忘记取模导致答案错误\n- 数组开小了 RE\n- 输出多余空格或换行 PE\n\n把你的代码贴过来，我可以帮你具体分析！",
        ]
        import random
        return {"reply": random.choice(default_replies), "model": "mock-wa-notebook"}

    def generate_summary(self, data_summary: str) -> dict:
        """基于错题数据生成学习小结"""
        if not self.api_key or self.provider == "mock":
            return self._mock_summary(data_summary)

        prompt = (
            "你是一位资深的 OI/ACM 竞赛教练。请根据以下学生的错题数据，"
            "生成一份结构化的学习小结报告。要求：\n"
            "1. 总结主要错误类型和频率\n"
            "2. 指出最需要改进的薄弱环节\n"
            "3. 给出针对性的训练建议\n"
            "4. 鼓励性结尾\n"
            f"\n学生数据：\n{data_summary}"
        )

        async def _do():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                    },
                    timeout=aiohttp.ClientTimeout(total=90),
                ) as response:
                    if response.status != 200:
                        text = await response.text()
                        raise Exception(f"AI API 请求失败: HTTP {response.status}")
                    data = await response.json()
                    return {"reply": data["choices"][0]["message"]["content"], "model": data.get("model", self.model)}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_do())

    def _mock_summary(self, data_summary: str) -> dict:
        """Mock 小结 - 基于统计数据生成"""
        lines = data_summary.split('\n')

        # 解析关键数据
        total = "0"
        resolved = "0"
        high_count = "0"

        for line in lines:
            if '总错题数' in line:
                total = line.split(':')[-1].strip() if ':' in line else '0'
            elif '已解决' in line and '/' in line:
                parts = line.split('/')
                resolved = parts[0].split(':')[-1].strip() if ':' in parts[0] else '0'
            elif '深层问题' in line:
                high_count = line.split('/')[0].split(':')[-1].strip() if '/' in line else '0'

        reply = (
            f"📋 **你的竞赛学习小结**\n\n"
            f"---\n\n"
            f"**📊 数据概览**\n"
            f"- 累计记录错题 **{total}** 道\n"
            f"- 已解决 **{resolved}** 道\n"
            f"- 深层问题 **{high_count}** 个需重点关注\n\n"
            f"---\n\n"
            f"**🎯 核心发现**\n\n"
            f"1. **高频错误类型**：从你的错题分布来看，逻辑错误和边界条件处理是最常见的两类问题。这说明你在算法思路正确的情况下，容易在实现细节上翻车。\n\n"
            f"2. **深层问题预警**：有 {high_count} 道题属于「深层问题」类（如复杂度选择、数学推导等），这类问题需要系统性地补强对应知识模块。\n\n"
            f"3. **低级错误**：部分题目因拼写、变量名混淆等低级原因 WA，建议养成代码 review 的习惯。\n\n"
            f"---\n\n"
            f"**💡 训练建议**\n\n"
            f"- **边界专项**：每天花 10 分钟专门练习边界 case（n=1, n=max, 全相等）\n"
            f"- **模板积累**：将快速幂、GCD、二分查找等常用模板写熟到肌肉记忆\n"
            f"- **赛后复盘**：每道 WA 的题必须写出「为什么错了」和「下次怎么防」\n"
            f"- **分类刷题**：针对薄弱的算法类型集中突破，而非随机刷题\n\n"
            f"---\n\n"
            f"> 继续保持记录错题的习惯！量变引起质变，加油！🚀"
        )
        return {"reply": reply, "model": "mock-wa-notebook"}

    def _normalize_result(self, result: dict) -> dict:
        cat = result.get("error_category", "logic_error")
        if cat not in ERROR_CATEGORIES:
            cat = "logic_error"

        severity = result.get("error_severity", "high")
        if severity not in ("low", "high"):
            severity = ERROR_CATEGORIES[cat]["severity"]

        hints = result.get("hints") or ERROR_CATEGORIES[cat]["hints"]
        if not isinstance(hints, list):
            hints = list(hints)

        return {
            "error_category": cat,
            "error_severity": severity,
            "error_summary": result.get("error_summary") or ERROR_CATEGORIES[cat]["summaries"][0],
            "error_detail": result.get("error_detail") or ERROR_CATEGORIES[cat]["details"][0],
            "suggestion": result.get("suggestion") or ERROR_CATEGORIES[cat]["suggestions"],
            "hints": hints,
        }


ai_client = AIAnalyzerClient()
