<!-- ============== HERO BANNER ============== -->

<div align="center">

<img src="https://img.shields.io/badge/Version-v0.0.3-a855f7?style=flat-square&logo=github" alt="Version"/>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/AI-Multi--Model-00e5ff?style=flat-square&logo=openai&logoColor=white" alt="AI"/>
<img src="https://img.shields.io/badge/Storage-Local%20Only-10b981?style=flat-square&logo=lock&logoColor=white" alt="Local"/>
<img src="https://img.shields.io/badge/License-MIT-ec4899?style=flat-square" alt="License"/>
<img src="https://img.shields.io/badge/TRAE-AI%20%E5%88%9B%E9%80%A0%E5%8A%9B%E5%A4%A7%E8%B5%9B-9cf?style=flat-square" alt="TRAE"/>

<br/><br/>

# WA · 错题本

### <span style="color:#a855f7;">**让每一次 WA 都有价值**</span>

**面向 OI / ACM 竞赛选手的 AI 智能错题分析与学习画像平台**

> *真正的成长，不是在 AC 之后庆祝，而是在 WA 之后反思。*

<br/>

[🚀 快速开始](#-快速开始) · [✨ 核心特性](#-核心特性) · [🧠 AI 模型广场](#-ai-模型广场) · [🛠️ 技术栈](#️-技术栈) · [📂 项目结构](#-项目结构) · [🗺️ 路线图](#️-路线图)

</div>

---

## 📖 项目简介

**WA 错题本** 是一款面向信息学竞赛（OI / ACM）选手的智能化错题分析与学习助手。

> 传统错题本依赖选手**手动复制**题目、整理错误原因，费时费力且容易遗漏规律。WA 错题本首创性地将 **「OI / ACM 提交记录」** 与 **「AI 智能画像」** 结合，自动化完成错题归档、归因分析与个性化复习推荐。

粘贴一条 WA 提交链接，AI 自动：
- 抓取 **Codeforces / 洛谷** 提交页面的代码与题目信息
- 基于 **12 类** 常见竞赛错误进行智能分类
- 生成**结构化错题总结**，识别错误模式与知识盲区
- 跨题目分析，绘制**个人错误画像**，告诉你要重点突破什么

**v0.0.3 已完成：** 真实多模型 AI 接入（百度文心 / DuckDuckGo），数据本地存储，引导式教学。

---

## ✨ 核心特性

<table>
<tr>
<td width="50%" valign="top">

### 🤖 AI 智能分析
- 自动抓取 Codeforces / 洛谷的提交记录
- 基于 **12 类** 常见竞赛错误进行智能分类
- 区分「低级错误」当场指出 vs「深层问题」渐进引导
- 支持**多模型聚合** + **Auto 自动降级**

</td>
<td width="50%" valign="top">

### 📋 系统化错题管理
- 按**平台 / 难度 / 错误类型**多维度归档
- 支持错题列表筛选与详情查看
- 记录分析历史，随时回溯
- 关键状态标签：**WA / TLE / RE / AC** 一目了然

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧭 引导式教学
- 不直接给答案，像真正的教练一样**分层递进提问**
- 引导你自己找到问题所在
- 锻炼 Debug 能力，告别"看答案"依赖

</td>
<td width="50%" valign="top">

### 📈 数据驱动的成长追踪
- 错误类型分布统计
- 个人错误画像分析
- 阶段性总结，精准定位薄弱算法领域
- 所有数据 **100% 本地存储**，保护隐私

</td>
</tr>
</table>

---

## 🧠 AI 模型广场

> 灵感来自 **OpenCode** 风格的模型管理界面。

| 厂家 | 模型 | 提供方 |
|------|------|--------|
| 🟦 **百度** · `baidu-2api` | ERNIE-4.0 / ERNIE-Speed / ERNIE-Lite | 反代（免费） |
| 🟧 **DuckDuckGo** · `DDG2API` | GPT-4o mini / Claude 3 Haiku / Llama 3.3 70B | 反代（免费） |
| 🟪 **自定义** · OpenAI 兼容 | DeepSeek-V3 / 自有 API | 用户自配 |
| 🟩 **Auto** · 自动降级 | 依次探测可用模型 | 内置 |

**多源 AI 聚合 + Auto 模式**：当某一个服务不可用时，自动尝试下一个，确保你始终能获得 AI 辅助。

所有反代均通过 `third_party/baidu-2api` 和 `third_party/DDG2API` **本地部署**，无需 API Key，开箱即用。

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 运行 `DDG2API`（DuckDuckGo 反代） |
| 操作系统 | macOS / Windows / Linux | 跨平台支持 |

### 一键启动（推荐） ⭐

```bash
git clone https://github.com/yusiwen2014/wa-notebook.git
cd wa-notebook
python start_all.py
```

`start_all.py` 会自动：
1. 检测虚拟环境
2. 启动 `baidu-2api`（端口 8000）
3. 启动 `DDG2API`（端口 3000）
4. 启动 WA 错题本主服务（端口 **8083**）

启动完成后浏览器打开 👉 **http://localhost:8083**

### 手动启动

```bash
# 1️⃣ 克隆 & 进入项目
git clone https://github.com/yusiwen2014/wa-notebook.git
cd wa-notebook

# 2️⃣ 创建虚拟环境
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# 3️⃣ 安装依赖
pip install -r requirements.txt

# 4️⃣ 启动后端
python run.py
```

### 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 🌐 主服务 | `http://localhost:8083` | WA 错题本主界面 |
| 💚 健康检查 | `http://localhost:8083/health` | 后端存活探测 |
| 🟦 baidu-2api | `http://localhost:8000` | 百度文心反代 |
| 🟧 DDG2API | `http://localhost:3000` | DuckDuckGo AI 反代 |

### API 端点

```http
GET  /health                         # 健康检查
GET  /api/ai/models                  # 列出所有可用模型
POST /api/ai/chat/completions        # 发起对话（支持流式 stream=true）
```

---

## 🛠️ 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| **后端框架** | **Flask 3.0** + flask-cors | 轻量、稳定、易部署 |
| **数据存储** | **SQLite** | 本地文件，零配置 |
| **AI 反代** | `baidu-2api` · `DDG2API` | 百度文心 + DuckDuckGo 免费 AI |
| **HTTP 客户端** | `requests` | 简洁的同步请求库 |
| **前端** | 原生 HTML / CSS / JS | Gemini 风格 · 暗 / 亮主题 |
| **跨平台启动** | `start_all.py` | 一键拉起三个服务 |

### 完整依赖

```text
flask==3.0.3
flask-cors==4.0.0
requests==2.32.3
```

### 配置说明

通过**环境变量**添加自定义模型：

```bash
export CUSTOM_MODELS="deepseek-chat,DeepSeek-V3;gpt-4o,GPT-4o"
```

格式：`model_id,显示名;model_id,显示名`

---

## 📂 项目结构

```text
wa-notebook/
├── app/
│   ├── __init__.py              # Flask 应用工厂
│   ├── config.py                # 全局配置（端口 8083 / 平台支持）
│   ├── api/
│   │   └── ai.py                # AI 对话与模型列表接口
│   └── services/
│       └── ai_service.py        # 核心：百度 / DDG / 测试 / 自定义 模型调度
├── third_party/
│   ├── baidu-2api/              # 百度文心反代（端口 8000）
│   └── DDG2API/                 # DuckDuckGo AI 反代（端口 3000）
├── static/                      # 前端静态资源（HTML / CSS / JS）
├── tests/                       # 测试用例
├── data/                        # SQLite 数据库（运行时自动创建）
├── venv/                        # 虚拟环境（已配置 .gitignore）
├── requirements.txt             # Python 依赖
├── run.py                       # 单服务启动入口
└── start_all.py                 # ⭐ 一键启动三件套
```

---

## 🎯 12 类错误分类体系

| 类别 | 名称 | 严重程度 | 说明 |
|------|------|----------|------|
| `logic_error` | 逻辑错误 | 🔴 高 | 算法思路与题目要求不符 |
| `boundary` | 边界条件 | 🟡 低 | 数组越界、极端情况未处理 |
| `overflow` | 整数溢出 | 🟡 低 | `int` 范围不足，应使用 `long long` |
| `uninitialized` | 未初始化 | 🟡 低 | 变量未赋初值导致不确定行为 |
| `complexity` | 复杂度超限 | 🔴 高 | O(n²) 导致 TLE |
| `precision` | 精度问题 | 🟡 低 | 浮点数比较未用 `eps` |
| `io_format` | 输入输出格式 | 🟡 低 | 多组数据未循环读取 |
| `memory` | 内存超限 | 🔴 高 | 申请空间超过限制 |
| `typo` | 拼写笔误 | 🟡 低 | 复制粘贴后变量名忘改 |
| `modular` | 取模错误 | 🟡 低 | 负数取模或取模时机错误 |
| `graph` | 图论细节 | 🔴 高 | 无向图忘双向加边 |
| `dp` | DP 状态 / 转移 | 🔴 高 | 状态定义不完整 |

---

## 🗺️ 路线图

| 版本 | 目标 | 状态 |
|------|------|------|
| **v0.0.1** | MVP —— 基础架构 + 错题流 | ✅ 完成 |
| **v0.0.2** | 接入 baidu-2api / DDG2API 反代 | ✅ 完成 |
| **v0.0.3** | 错误点 AI 自动生成 + 状态格式化 | ✅ 当前版本 |
| **v0.1.0** | 模型广场 UI + Auto 自动降级 | 🚧 进行中 |
| **v0.2.0** | 用户系统 + 数据隔离 | 📋 规划 |
| **v0.3.0** | 周 / 月自动总结报告 | 📋 规划 |
| **v0.5.x** | Desktop 桌面客户端（Electron / Tauri） | 📋 规划 |
| **v1.0.0** | 完整版 + AtCoder / LeetCode 支持 | 📋 规划 |

---

## 🖼️ 界面预览

> *启动项目后访问 `http://localhost:8083` 查看完整界面*
>
> 主要亮点：
> - **Gemini 风格** 圆角卡片 + 柔和阴影
> - **暗 / 亮主题** 一键切换，自动记忆
> - **OpenCode 风格** 模型管理
> - **粒子背景** + 鼠标光斑追随
> - **渐变文字** + 滚动 Reveal 动画

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/<your-name>/wa-notebook.git

# 3. 创建功能分支
git checkout -b feature/your-feature

# 4. 开发并测试
python run.py

# 5. 提交（请使用 Conventional Commits）
git commit -m "feat: add xxx feature"

# 6. 推送并创建 PR
git push origin feature/your-feature
```

### 开发规范

- Python 代码遵循 **PEP 8**
- 保持 **本地优先** 原则：用户数据不离开本机
- 新功能请附带测试用例（`tests/` 目录）
- API 改动请同步更新 `app/api/` 注释

---

## 🙏 致谢

| 项目 | 说明 |
|------|------|
| [baidu-2api](https://github.com/dijiaozhibei-top/baidu-2api) | 百度文心一言反代 |
| [DDG2API](https://github.com/meethuhu/DDG2API) | DuckDuckGo AI 反代 |
| [lbbniu/ai-proxy](https://github.com/lbbniu/ai-proxy) | 多厂商 AI 代理参考 |
| [1234567Yang/cf-proxy-ex](https://github.com/1234567Yang/cf-proxy-ex) | CF 反代参考 |
| [TRAE](https://www.trae.cn/) | AI 创造力大赛主办方 |

特别感谢所有参与测试和反馈的 **OIer** 们 ❤️

---

## 📬 联系方式

- 🐛 **GitHub Issues**: [报告 Bug / 提出建议](https://github.com/yusiwen2014/wa-notebook/issues)
- 💬 **大赛讨论帖**: [TRAE 论坛](https://forum.trae.cn/t/topic/22548)
- 🏆 **参赛赛道**: 学习工作 / 造个新解法

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源 —— 你可以自由使用、修改和分发，但请保留原作者署名。

---

<div align="center">

### ⭐ 如果这个项目对你有帮助，请点个 Star 支持一下！

<sub>🤖 Built with AI · 🎨 Designed in Gemini × OpenCode style</sub>

</div>
