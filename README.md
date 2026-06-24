<!-- PROJECT LOGO -->
<div align="center">

<img src="https://raw.githubusercontent.com/your-username/wa-notebook/main/.github/logo.png" alt="WA错题本" width="120" height="120" style="border-radius: 20px;">

# WA错题本

### 面向 OI / ACM 竞赛选手的智能错题管理平台

*让每一次 WA 都有价值*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square&logo=mit)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/your-username/wa-notebook?style=flat-square&logo=github)](https://github.com/your-username/wa-notebook/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/your-username/wa-notebook?style=flat-square&logo=github)](https://github.com/your-username/wa-notebook/network/members)
[![TRAE AI 大赛](https://img.shields.io/badge/TRAE%20AI-%E5%88%9B%E9%80%A0%E5%8A%9B%E5%A4%A7%E8%B5%9B-9cf?style=flat-square)](https://www.trae.cn/ai-creativity)

*🎯 参赛赛道：学习工作 / 造个新解法 | TRAE AI 创造力大赛 2026*

</div>

---

## 📖 项目简介

WA错题本是一个**智能错题管理平台**，专为 OI / ACM 竞赛选手设计。

每次 WA（Wrong Answer）后不再盲目翻题解——只需粘贴提交链接，AI 自动抓取代码和题目，分析错误根因，识别知识盲区，用**引导式教学**帮你建立真正的 Debug 能力。

> *"真正的成长不是在 AC 之后庆祝，而是在 WA 之后反思。"*

---

## ✨ 核心特性

### 🤖 AI 智能分析

- 自动抓取 Codeforces / 洛谷提交页面的代码和题目信息
- 基于 12 类常见竞赛错误进行智能分类
- 区分「低级错误」（当场指出）与「深层问题」（渐进引导）

### 📋 系统化错题管理

- 按平台、难度、错误类型多维度归档
- 支持错题列表筛选与详情查看
- 记录分析历史，随时回溯，永不过期

### 🧭 引导式教学（Socratic Method）

- 不直接给答案，像真正的教练一样分层递进提问
- 引导你自己找到问题所在
- 锻炼 Debug 能力，而不是养成"看答案"的依赖

### 📈 数据驱动的成长追踪

- 错误类型分布统计
- 个人错误画像分析
- 阶段性总结，精准定位薄弱环节

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Linux / Windows / macOS

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/wa-notebook.git
cd wa-notebook

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate        # Linux/macOS
# 或: venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python run.py
```

### 使用方式

1. 服务启动后，浏览器打开 **http://localhost:8000**
2. 粘贴你的 WA 提交链接
3. 选择对应的 OJ 平台
4. 点击「开始分析」，等待 AI 诊断结果

> 📖 完整的 API 文档可在 **http://localhost:8000/docs** 查看（Swagger UI）

---

## 🛠️ 技术栈

| 层级 | 技术选型 |
|------|----------|
| **后端框架** | FastAPI + Uvicorn |
| **数据库** | SQLite + SQLAlchemy (异步) |
| **HTTP 客户端** | aiohttp + BeautifulSoup4 |
| **数据校验** | Pydantic v2 |
| **前端** | 原生 HTML/CSS/JS + Chart.js |
| **AI（规划中）** | DeepSeek / OpenAI API (v0.1.0+) |

<details>
<summary><b>完整的依赖清单（点击展开）</b></summary>

```
fastapi==0.110.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.28
aiosqlite==0.19.0
aiohttp==3.9.5
beautifulsoup4==4.12.3
lxml==5.1.0
pydantic==2.6.4
pydantic-settings==2.1.0
jinja2==3.1.3
python-multipart==0.0.9
pytest==8.1.1
pytest-asyncio==0.23.6
httpx==0.27.0
```

</details>

---

## 📂 项目结构

```
wa-notebook/
├── app/
│   ├── api/              # API 路由层
│   │   ├── submission.py # 提交与错题接口
│   │   └── stats.py     # 统计接口
│   ├── models/          # 数据模型
│   │   ├── database.py  # 数据库引擎
│   │   ├── submission.py# 提交记录
│   │   └── mistake.py   # 错题分析
│   ├── schemas/         # Pydantic 数据校验
│   ├── services/        # 核心业务逻辑
│   │   ├── scraper.py   # OJ 爬虫服务
│   │   ├── analyzer.py  # AI 分析服务
│   │   └── stats.py    # 统计分析
│   ├── utils/           # 工具函数
│   └── main.py         # FastAPI 入口
├── static/             # 前端静态资源
├── data/               # SQLite 数据库
├── tests/             # 测试代码
├── requirements.txt   # 依赖清单
└── run.py             # 启动脚本
```

---

## 🎯 错误分类体系

v0.0.1 支持识别以下 **12 类**常见竞赛错误：

| 类别 | 名称 | 严重程度 | 说明 |
|------|------|----------|------|
| `logic_error` | 逻辑错误 | 🔴 高 | 算法思路与题目要求不符 |
| `boundary` | 边界条件 | 🟡 低 | 数组越界、极端情况未处理 |
| `overflow` | 整数溢出 | 🟡 低 | int 范围不足，应使用 long long |
| `uninitialized` | 未初始化 | 🟡 低 | 变量未赋初值导致不确定行为 |
| `complexity` | 复杂度超限 | 🔴 高 | O(n²) 导致 TLE |
| `precision` | 精度问题 | 🟡 低 | 浮点数比较未用 eps |
| `io_format` | 输入输出格式 | 🟡 低 | 多组数据未循环读取 |
| `memory` | 内存超限 | 🔴 高 | 申请空间超过限制 |
| `typo` | 拼写笔误 | 🟡 低 | 复制粘贴后变量名忘改 |
| `modular` | 取模错误 | 🟡 低 | 负数取模或取模时机错误 |
| `graph` | 图论细节 | 🔴 高 | 无向图忘双向加边 |
| `dp` | DP 状态/转移 | 🔴 高 | 状态定义不完整 |

---

## 📊 版本路线图

| 版本 | 目标 | 状态 |
|------|------|------|
| **v0.0.1** | MVP —— Mock AI 分析，可跑通全流程 | 🚧 开发中 |
| **v0.1.0** | 接入真实 LLM API（DeepSeek/OpenAI） | 📋 规划 |
| **v0.2.0** | 用户系统 + 数据隔离 | 📋 规划 |
| **v0.3.0** | 周/月自动总结报告 | 📋 规划 |
| **v0.5.x** | Desktop 桌面客户端 | 📋 规划 |
| **v1.0.0** | 完整版发布 + AtCoder 支持 | 📋 规划 |

---

## 🖼️ 截图预览

> *截图待补充（建议启动项目后截图替换）*

<!--
### 提交分析界面
![Submit](.github/screenshots/submit.png)

### 错题列表
![List](.github/screenshots/list.png)

### 统计面板
![Stats](.github/screenshots/stats.png)
-->

<details>
<summary><b>预览占位（上线前请替换为真实截图，点击展开）</b></summary>

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│              📸 截图区域 - 请替换为真实截图               │
│                                                          │
│     建议截取:                                            │
│     1. 首页/提交页面                                      │
│     2. 错题列表页面                                       │
│     3. 统计概览页面                                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

</details>

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/your-username/wa-notebook.git

# 3. 创建功能分支
git checkout -b feature/your-feature-name

# 4. 开发并测试
# ... 你的代码 ...

# 5. 提交（请使用清晰的 commit message）
git commit -m "feat: add xxx feature"

# 6. 推送并创建 PR
git push origin feature/your-feature-name
```

### 开发规范

- Python 代码遵循 PEP 8
- 新功能请附带测试用例
- API 改动请更新对应的文档注释

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源，你可以自由使用、修改和分发，但请保留原作者署名。

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) — 现代化的 Python Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) — 强大的 ORM 库
- [TRAE](https://www.trae.cn/) — AI 创造力大赛主办方
- 所有参与测试和反馈的 OIer 们

---

## 📬 联系方式

- **GitHub Issues**: [报告 Bug / 提出建议](https://github.com/your-username/wa-notebook/issues)
- **大赛讨论帖**: [TRAE 论坛](https://forum.trae.cn/t/topic/22548)

---

<div align="center">

*如果这个项目对你有帮助，请点个 ⭐ 支持一下！*

</div>
