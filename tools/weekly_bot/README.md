# MoonBit 周报仓库收集器 

自动搜索、分类MoonBit相关仓库，使用DeepSeek-V3 AI智能分类，并通过Cursor Agent生成高质量周报条目。

## 特性 

- 🚀 **一键流程**: 分类完成后按回车自动进入Review和生成写作指引
- 🤖 **AI分类**: 使用DeepSeek-V3智能分类project/package
- 📥 **重量级抓取**: 获取README全文、moon.mod.json、代码片段
- 👤 **智能作者识别**: 自动提取用户昵称，处理组织/Fork仓库
- 🎯 **交互式Review**: CLI友好的交互界面，快速标注和分类
- 📊 **分区Review**: 组织仓库/分类存疑/抓取失败分别展示
- 📝 **写作指引**: 自动生成包含完整数据的写作指引文档
- ✍️ **Cursor Agent集成**: 利用超长上下文，生成高质量条目
- 💰 **成本优化**: 批量处理，约¥0.5/100仓库
- 🧹 **简洁输出**: 去除冗余信息，流程清晰明了
- 🔧 **格式自动修复**: 自动更新历史周报embed格式，确保格式一致性
- 📋 **增强验证**: postcheck.py自动检查所有格式问题
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

### 2. 配置API Keys

环境变量已永久配置（在~/.zshrc中）：
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
- README前500字符
- 完整元数据

### 🚀 Project  
- 同Package格式
- 区分应用/游戏/工具

### ⚠️ Review（分三类）
- **作者存疑**: 组织仓库、Fork仓库
- **分类存疑**: AI置信度低、特征不明
- **抓取失败**: 网络超时、文件过大

## 完整工作流程

### 一键启动（bot.py）
```bash
python bot.py 2025-10-08
```

**自动执行：**
1. 🔍 搜索仓库 (GraphQL: moonbit + language:moonbit)
2. 📥 重量级抓取 (README 2000字 + moon.mod.json + .mbt代码)
3. 👤 作者识别 (个人→提取昵称，组织/Fork→Review)
4. 🤖 AI分类 (DeepSeek-V3单仓库并发分类)
5. 💾 生成文件：
   - `output/repos_weeklyN_YYYY-MM-DD.md` (分类结果)
   - `output/repos_weeklyN_YYYY-MM-DD_full_data.json` (完整数据)

**交互流程：**

#### Step 1: AI分类完成
```
⚠️ 发现 10 个待Review仓库
👉 按回车进入交互式Review，或Ctrl+C退出
```
→ **按回车** 自动启动 `review.py`

#### Step 2: 交互式Review（3-5分钟）
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

#### Step 3: 生成写作指引（1秒，内置 Writer Contract）
```
✅ 写作指引已生成
📄 output/writing_guide_weekly15_2025-10-14.md
```
→ ✅ **自动化完成！**

**写作指引包含：**
- 完整README（1000字）
- 代码片段（500字）
- 结构化提示词
- 模板要求 + Writer Contract（只覆盖锚点、禁止重复模板、固定路径）
- 智能周数描述生成（单周/双周/三周）
- 格式对比示例（正确/错误格式）
- 空文档处理说明（禁止锚点标记）

### Step 4: Cursor Agent生成条目（30秒，一句指令）
在Cursor里发送：
```
@output/writing_guide_weekly15_2025-10-14.md

按照文档要求生成周报条目
```

Agent自动：
- 创建 `trees/weekly/weekly15/` 目录
- 生成 `packages.md` 和 `projects.md`（含frontmatter）
- 生成主文档 `weekly15.md`（含智能周数描述）
- 生成 `official.md` 和 `community.md`（空模板，无锚点标记）
- 更新 `index.md`（使用正确的 `[+]` 格式）
- 自动更新上一周embed格式（`[+]` → `[+-]`）
> 若文件已存在，请覆盖锚点内内容，不要在文件尾部再次粘贴整段模板。

### Step 5: 发布前自检（postcheck）
```bash
python tools/weekly_bot/postcheck.py trees/weekly/weekly15
```
**增强检查项：**
- 重复frontmatter/模板
- 条目空行、结尾换行
- 主文档与子文档路径
- 索引embed格式（当前周报使用 `[+]`，历史周报使用 `[+-]`）
- 子文档标题格式（必须包含"本周"字样）
- 主文档embed格式（禁止使用 `[+-]`）
- 锚点标记检查（禁止在空文档中添加）

### Step 6: 发布准备（5-10分钟）
1. 填写 `official.md` 和 `community.md`（空模板已自动生成）
2. 检查主文档周数描述是否正确
3. Git提交发布

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
- **100个仓库**: 约¥0.5
- **实时统计**: 运行结束显示精确成本

## 时间估算

| 步骤 | 时间 | 说明 |
|------|------|------|
| Step 1: bot.py | 2-3分钟 | 全自动 |
| Step 2: review.py | 2-5分钟 | 交互式CLI，增强贡献者输入 |
| Step 3: 生成指引 | 5秒 | 全自动，智能周数描述+格式修复 |
| Step 4: AI生成条目 | 30秒 | Cursor Agent自动，格式优化 |
| Step 5: 发布前验证 | 5秒 | postcheck.py自动检查 |
| Step 6: 发布准备 | 5-10分钟 | 填充内容 |
| **总计** | **10-19分钟** | 对比以前1-2小时，质量更高 |

## 技术细节

### AI分类逻辑
1. moon.mod.json name字段（组织名→package）
2. 代码结构（lib/目录→package，main.mbt→project）
3. README描述（library/framework→package，game/app→project）
4. 源码内容（函数定义→package，业务逻辑→project）

### 作者格式
- `[username 昵称](url)` - 个人仓库有昵称
- `[username](url)` - 个人仓库无昵称
- 组织/Fork → 不显示作者，进Review区

### 错误处理
- GraphQL超时 → 标记Review（抓取失败）
- 文件过大 → 标记Review（抓取失败）
- AI分类失败 → 标记Review（分类存疑）

### v3.3 优化细节

#### 格式自动修复
- **自动更新历史embed格式**: 生成新周报时，自动将上一周的 `[+]` 改为 `[+-]`
- **智能周数描述**: 根据日期跨度自动生成"为单周周报"、"为双周周报"等描述
- **格式验证增强**: postcheck.py检查embed格式、标题格式、锚点标记等

#### 贡献者输入优化
- **多步确认机制**: 支持粘贴后确认、重新输入、跳过等操作
- **自动补全**: 支持 `@username`、URL、`[name](url)` 等多种格式
- **错误恢复**: 输入错误时可重新输入，不会直接跳过

#### 指令优化
- **格式对比示例**: 提供正确/错误格式的对比，减少Agent误解
- **空文档处理**: 明确说明空文档不要添加锚点标记
- **验证清单**: 详细的输出验证清单，确保质量

## 历史版本

归档在 `archive/` 目录：
- `v1_url_collector.py` - v1.0（仅URL收集）

## 更新日志

### v3.3 (2025-01-XX)
- ✨ 自动更新历史周报embed格式（`[+]` → `[+-]`）
- ✨ 智能周数描述生成（单周/双周/三周）
- ✨ 增强postcheck.py验证（格式检查、标题检查、锚点检查）
- ✨ 优化贡献者输入体验（多步确认、自动补全、错误恢复）
- ✨ 强化Agent指令（格式对比示例、空文档处理说明）
- 🐛 修复embed格式空格问题
- 🐛 修复锚点标记误生成问题
- 🐛 修复子文档标题格式问题

### v3.2 (2025-01-XX)
- ✨ 一键流程自动化
- ✨ 交互式Review界面
- ✨ Cursor Agent集成
- ✨ 简洁输出优化
