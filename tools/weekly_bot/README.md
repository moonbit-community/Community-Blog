# MoonBit 周报仓库收集器 

自动搜索、分类 MoonBit 相关仓库，使用 DeepSeek-V3 AI 智能分类，并通过 Cursor Agent 生成高质量周报条目。

## 特性 

- 🚀 **一键流程**: 分类完成后按回车自动进入 Review 和生成写作指引
- 🤖 **AI 分类**: 使用 DeepSeek-V3 智能分类 project/package
- 📥 **重量级抓取**: 获取 README 全文、moon.mod.json、代码片段
- 👤 **智能作者识别**: 自动提取用户昵称，处理组织/Fork 仓库
- 🎯 **交互式 Review**: CLI 友好的交互界面，快速标注和分类
- 📊 **分区 Review**: 组织仓库/分类存疑/抓取失败分别展示
- 📝 **写作指引**: 自动生成包含完整数据的写作指引文档
- ✍️ **Cursor Agent 集成**: 利用超长上下文，生成高质量条目
- 💰 **成本优化**: 批量处理，约¥0.5/100 仓库
- 🧹 **简洁输出**: 去除冗余信息，流程清晰明了
- 🔧 **格式自动修复**: 自动更新历史周报 embed 格式，确保格式一致性
- 📋 **增强验证**: postcheck.py 自动检查所有格式问题
- 🎯 **智能周数描述**: 根据日期跨度自动生成"单周/双周/三周"描述
- 🚫 **锚点标记优化**: 明确禁止空文档添加锚点标记

## 使用

### 1. 环境准备

```bash
# 激活conda环境
conda activate samupy

# 确保依赖已安装
pip install -r requirements.txt
```

### 2. 配置 API Keys

环境变量已永久配置（在~/.zshrc 中）：
```bash
export GITHUB_TOKEN='ghp_...'
export SILICONFLOW_API_KEY='sk-...'
```

验证配置：
```bash
python config.py
```

### 3. 一键运行

```bash
# 启动自动化流程（推荐）
python bot.py 2025-10-08

# 后续交互：
# 1. AI分类完成 → 按回车进入Review
# 2. 标注贡献者、快速分类 → Review完成
# 3. 按回车生成写作指引
# 4. ✅ 自动化完成！

# 或交互式输入日期
python bot.py
```

## 输出

生成 `output/repos_weeklyN_YYYY-MM-DD.md`，包含三个分区：

### 📦 Package
- 带作者昵称（如：`[username 昵称](url)`）
- README 前 500 字符
- 完整元数据

### 🚀 Project  
- 同 Package 格式
- 区分应用/游戏/工具

### ⚠️ Review（分三类）
- **作者存疑**: 组织仓库、Fork 仓库
- **分类存疑**: AI 置信度低、特征不明
- **抓取失败**: 网络超时、文件过大

## 完整工作流程

### 一键启动（bot.py）
```bash
python bot.py 2025-10-08
```

**自动执行：**
1. 🔍 搜索仓库 (GraphQL: moonbit + language:moonbit)
2. 📥 重量级抓取 (README 2000 字 + moon.mod.json + .mbt 代码)
3. 👤 作者识别 (个人→提取昵称，组织/Fork→Review)
4. 🤖 AI 分类 (DeepSeek-V3 单仓库并发分类)
5. 💾 生成文件：
   - `output/repos_weeklyN_YYYY-MM-DD.md` (分类结果)
   - `output/repos_weeklyN_YYYY-MM-DD_full_data.json` (完整数据)

**交互流程：**

#### Step 1: AI 分类完成
```
⚠️ 发现 10 个待Review仓库
👉 按回车进入交互式Review，或Ctrl+C退出
```
→ **按回车** 自动启动 `review.py`

#### Step 2: 交互式 Review（3-5 分钟）
```
🏢 组织/Fork仓库：
  - 自动提取贡献者（如 Yoorkin）
  - 选择贡献者 (1/2/0)
  - 快速分类 (1=Package/2=Project/3=跳过)

🤔 其他Review仓库：
  - 快捷键分类 (1/2/3)
  
📊 Review汇总 → 确认保存 (y/n)
```
→ **按回车** 自动启动 `generate_writing_guide.py`

#### Step 3: 生成写作指引（1 秒，内置 Writer Contract）
```
✅ 写作指引已生成
📄 output/writing_guide_weekly15_2025-10-14.md
```
→ ✅ **自动化完成！**

**写作指引包含：**
- 完整 README（1000 字）
- 代码片段（500 字）
- 结构化提示词
- 模板要求 + Writer Contract（只覆盖锚点、禁止重复模板、固定路径）
- 智能周数描述生成（单周/双周/三周）
- 格式对比示例（正确/错误格式）
- 空文档处理说明（禁止锚点标记）

### Step 4: Cursor Agent 生成条目（30 秒，一句指令）
在 Cursor 里发送：
```
@output/writing_guide_weekly15_2025-10-14.md

按照文档要求生成周报条目
```

Agent 自动：
- 创建 `trees/weekly/weekly15/` 目录
- 生成 `packages.md` 和 `projects.md`（含 frontmatter）
- 生成主文档 `weekly15.md`（含智能周数描述）
- 生成 `official.md` 和 `community.md`（空模板，无锚点标记）
- 更新 `index.md`（使用正确的 `[+]` 格式）
- 自动更新上一周 embed 格式（`[+]` → `[+-]`）
> 若文件已存在，请覆盖锚点内内容，不要在文件尾部再次粘贴整段模板。

### Step 5: 发布前自检（postcheck）
```bash
python tools/weekly_bot/postcheck.py trees/weekly/weekly15
```
**增强检查项：**
- 重复 frontmatter/模板
- 条目空行、结尾换行
- 主文档与子文档路径
- 索引 embed 格式（当前周报使用 `[+]`，历史周报使用 `[+-]`）
- 子文档标题格式（必须包含"本周"字样）
- 主文档 embed 格式（禁止使用 `[+-]`）
- 锚点标记检查（禁止在空文档中添加）

### Step 6: 发布准备（5-10 分钟）
1. 填写 `official.md` 和 `community.md`（空模板已自动生成）
2. 检查主文档周数描述是否正确
3. Git 提交发布

## 文件结构

```
tools/weekly_bot/
├── bot.py                    # Step 1: 自动分类
├── review.py                 # Step 2: 交互式Review（增强贡献者输入）✨
├── generate_writing_guide.py # Step 3: 生成写作指引（智能周数描述+格式修复）✨
├── postcheck.py              # Step 5: 发布前验证（增强格式检查）✨
├── config.py                 # 配置管理
├── fetcher.py                # GraphQL数据抓取
├── classifier.py             # AI分类（DeepSeek-V3）
├── formatter.py              # 输出格式化
├── requirements.txt          # 依赖
├── README.md                 # 本文档
├── output/                   # 输出目录
│   ├── repos_weekly15_2025-10-14.md         # 分类结果
│   ├── repos_weekly15_2025-10-14_full_data.json  # 完整数据
│   ├── writing_guide_instructions_weekly15_2025-10-14.md  # 指令文档
│   └── writing_guide_data_weekly15_2025-10-14.json        # 数据文档
└── archive/                  # 历史版本
    └── v1_url_collector.py
```

## 成本估算

- **模型**: DeepSeek-V3
- **价格**: 输入¥0.001/1K, 输出¥0.002/1K
- **100 个仓库**: 约¥0.5
- **实时统计**: 运行结束显示精确成本

## 时间估算

| 步骤 | 时间 | 说明 |
|------|------|------|
| Step 1: bot.py | 2-3 分钟 | 全自动 |
| Step 2: review.py | 2-5 分钟 | 交互式 CLI，增强贡献者输入 |
| Step 3: 生成指引 | 5 秒 | 全自动，智能周数描述 + 格式修复 |
| Step 4: AI 生成条目 | 30 秒 | Cursor Agent 自动，格式优化 |
| Step 5: 发布前验证 | 5 秒 | postcheck.py 自动检查 |
| Step 6: 发布准备 | 5-10 分钟 | 填充内容 |
| **总计** | **10-19 分钟** | 对比以前 1-2 小时，质量更高 |

## 技术细节

### AI 分类逻辑
1. moon.mod.json name 字段（组织名→package）
2. 代码结构（lib/目录→package，main.mbt→project）
3. README 描述（library/framework→package，game/app→project）
4. 源码内容（函数定义→package，业务逻辑→project）

### 作者格式
- `[username 昵称](url)` - 个人仓库有昵称
- `[username](url)` - 个人仓库无昵称
- 组织/Fork → 不显示作者，进 Review 区

### 错误处理
- GraphQL 超时 → 标记 Review（抓取失败）
- 文件过大 → 标记 Review（抓取失败）
- AI 分类失败 → 标记 Review（分类存疑）

### v3.3 优化细节

#### 格式自动修复
- **自动更新历史 embed 格式**: 生成新周报时，自动将上一周的 `[+]` 改为 `[+-]`
- **智能周数描述**: 根据日期跨度自动生成"为单周周报"、"为双周周报"等描述
- **格式验证增强**: postcheck.py 检查 embed 格式、标题格式、锚点标记等

#### 贡献者输入优化
- **多步确认机制**: 支持粘贴后确认、重新输入、跳过等操作
- **自动补全**: 支持 `@username`、URL、`[name](url)` 等多种格式
- **错误恢复**: 输入错误时可重新输入，不会直接跳过

#### 指令优化
- **格式对比示例**: 提供正确/错误格式的对比，减少 Agent 误解
- **空文档处理**: 明确说明空文档不要添加锚点标记
- **验证清单**: 详细的输出验证清单，确保质量

## 历史版本

归档在 `archive/` 目录：
- `v1_url_collector.py` - v1.0（仅 URL 收集）

## 更新日志

### v3.3 (2025-01-XX)
- ✨ 自动更新历史周报 embed 格式（`[+]` → `[+-]`）
- ✨ 智能周数描述生成（单周/双周/三周）
- ✨ 增强 postcheck.py 验证（格式检查、标题检查、锚点检查）
- ✨ 优化贡献者输入体验（多步确认、自动补全、错误恢复）
- ✨ 强化 Agent 指令（格式对比示例、空文档处理说明）
- 🐛 修复 embed 格式空格问题
- 🐛 修复锚点标记误生成问题
- 🐛 修复子文档标题格式问题

### v3.2 (2025-01-XX)
- ✨ 一键流程自动化
- ✨ 交互式 Review 界面
- ✨ Cursor Agent 集成
- ✨ 简洁输出优化
