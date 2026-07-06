# WA 错题本 · 用户数据目录

本目录集中存放 WA 错题本的所有用户数据，方便备份、迁移、查看。

## 文件说明

| 文件 | 作用 |
|---|---|
| `conversations.json` | 所有历史对话（含每道题的 platform / id / code / link） |
| `profile.json` | 用户偏好：用户名、主题、活动对话 ID |
| `settings.json` | 应用设置（流式响应、Enter 发送、代码高亮等） |
| `custom_models.json` | 用户在「模型广场」里自建的模型 |
| `problems/<id>.md` | 导出的每道错题：标题 / 题目信息 / 用户代码 / 完整对话 |
| `backups/*.bak` | 每次覆盖写入前自动备份的旧版本（按时间戳命名） |

## 在哪里

- 本仓库：`wa-notebook/userdata/`
- Docker / 部署时建议挂载到独立卷，例如 `-v $(pwd)/userdata:/app/userdata`

## 怎么用

在 WA 错题本 → **设置 → 数据** 标签页可：

- **同步**：把当前浏览器 localStorage 里的数据写到这里
- **恢复**：从这里把数据写回浏览器
- **导出所有错题为 Markdown**：每个对话生成一个 `problems/<id>.md`
- **查看已导出文件**：右下角显示当前文件数与目录

## 隐私

- 所有数据**只在你的电脑**上，不会上传到任何云端
- 迁移到另一台机器：把这个目录整个复制即可
