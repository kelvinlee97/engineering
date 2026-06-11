# ai-workflow

基于 CodeBuddy 平台的 AI 驱动测试用例生成与管理工作流，集成 TestBuddy 脑图可视化和 TCase 自动化测试代码生成能力。

## 项目概述

ai-workflow 提供从需求分析到测试用例设计、再到自动化代码生成的全流程 AI 辅助工作流。项目包含五个核心技能包：

- **testbuddy-skill**：文本测试用例生成，支持脑图可视化管理（调度入口）
- **tcase-casegen-workflow**：TCase 用例生成 spec 工作流，提供完整的5阶段测试用例生成流程（testbuddy-skill 自动检测并调用）
- **tcase-codegen**：自动化测试代码生成，对接 TCase MCP 服务
- **yottadb-function-testing**：YottaDB 数据库专项功能测试代码生成
- **alb-autotest-codegen**：ALB 负载均衡系统自动化测试代码生成

## 目录结构

```
ai-workflow/
├── README.md
└── .codebuddy/
    ├── .mcp.json                          # MCP 服务器配置
    ├── agents/                            # 子代理定义
    │   ├── tcase-testcase-generator.md     # TCase 通用测试用例生成器（用例描述→代码→写入文件）
    │   ├── yottadb-testcase-generator.md  # YottaDB 测试生成器（串联多技能包）
    │   └── alb-testcase-generator.md      # ALB 测试生成器（串联多技能包）
    ├── commands/                           # 快捷命令
    │   ├── tb_open.md                     # 打开 TestBuddy 平台
    │   ├── alb_codegen_cmd.md             # ALB 自动化测试代码生成命令
    │   └── yottadb_codegen_cmd.md         # YottaDB 测试代码生成命令
    ├── rules/                             # 工作流规则
    │   └── TCase用例生成工作流.md           # Spec 工作流（5阶段全流程）
    └── skills/
        ├── testbuddy-skill/               # ★ 核心：文本测试用例生成
        │   ├── SKILL.md                   # 技能包定义（意图识别+调度）
        │   ├── generators/                # 生成器模块
        │   │   ├── case-generator.md      # 测试用例生成
        │   │   ├── deduplicator.md        # 节点去重
        │   │   ├── feature-generator.md   # 功能模块生成
        │   │   ├── framework-generator.md # 测试框架生成
        │   │   ├── issue-analyst.md       # 需求分析
        │   │   ├── scene-generator.md     # 测试场景生成
        │   │   └── tpoint-generator.md    # 测试点生成
        │   ├── scripts/                   # Python 脚本
        │   │   ├── load_session.py        # 加载会话参数
        │   │   ├── select_rule.py         # 规则路由
        │   │   ├── select_workflow.py     # 工作流路由
        │   │   ├── validate_nodes.py      # 节点格式校验
        │   │   ├── write_node_from_file.py# 从文件写入节点
        │   │   └── write_nodes.py         # 节点增删改操作
        │   ├── tools/                     # 工具能力定义
        │   │   ├── add_nodes.md           # 添加脑图节点
        │   │   ├── delete_nodes.md        # 删除脑图节点
        │   │   ├── get_descendants.md     # 获取子节点树
        │   │   ├── load_session.md        # 加载会话
        │   │   ├── rag_search.md          # 知识库检索
        │   │   ├── search_nodes.md        # 搜索节点
        │   │   ├── select_rule.md         # 选择规则
        │   │   ├── select_workflow.md     # 选择工作流
        │   │   └── update_nodes.md        # 更新节点
        │   └── workflows/                 # 工作流定义
        │       ├── case-generation.md     # 用例生成工作流
        │       ├── feature-generation.md  # 模块生成工作流
        │       ├── framework-generation.md# 框架生成工作流
        │       └── testpoint-generation.md# 测试点生成工作流
        ├── tcase-codegen/                 # TCase 自动化代码生成
        │   ├── SKILL.md                   # 技能包定义（uuid/text/node/standard模式）
        │   ├── references/                # 阶段参考文档
        │   │   ├── phase1_env_prepare.md  # 环境准备
        │   │   ├── phase2_params.md       # 参数组装
        │   │   ├── phase3_result.md       # 结果处理
        │   │   ├── phase4_batch.md        # 批量处理
        │   │   └── phase5_upload.md       # 上传到 TCase
        │   └── scripts/                   # Python 脚本
        │       ├── env_prepare.py         # 环境准备脚本
        │       ├── pre_tool_debug.py      # 工具调试前置脚本
        │       ├── task_upload_hook.py    # 任务上传 hook
        │       ├── tcase_upload_hook.py   # TCase 上传 hook
        │       └── upload_to_tcase.py     # 上传脚本
        ├── tcase-casegen-workflow/         # TCase 用例生成 spec 工作流（新增）
        │   └── SKILL.md                   # 技能包定义（5阶段 spec 工作流）
        ├── alb-autotest-codegen/          # ALB 自动化测试代码生成
        │   ├── SKILL.md                   # 技能包定义
        │   ├── references/                # 参考文档
        │   │   ├── code-templates.md      # 代码模板
        │   │   ├── coding-standards.md    # 编码标准
        │   │   ├── example-complete.md    # 完整示例
        │   │   ├── source-discovery.md    # 源码发现
        │   │   └── test-standards.md      # 测试标准
        │   └── scripts/                   # Shell 脚本
        │       └── fetch_source.sh        # 获取源码脚本
        └── yottadb-function-testing/      # YottaDB 专项测试
            ├── SKILL.md                   # 技能包定义
            └── references/                # 参考文档
                ├── api-reference.md       # API 参考
                ├── best-practices.md      # 最佳实践
                ├── code-discovery.md      # 代码发现
                ├── code-templates.md      # 代码模板
                └── module-architecture.md # 模块架构
```

## 核心技能包

### 1. testbuddy-skill — 文本测试用例生成

轻量级意图识别与工作流调度器，根据用户输入的关键词自动选择对应的生成工作流。调度时优先检测 `tcase-casegen-workflow` 技能包是否存在，若存在则直接使用其 spec 工作流；否则回退到 `select_workflow` 流程。

#### 能力矩阵

| 生成目标 | 触发关键词 | 输入节点类型 | 输出节点类型 |
|---------|-----------|-------------|-------------|
| 测试框架 | `framework` / `框架` | STORY / BUG | FEATURE / SCENE / TEST_POINT |
| 测试模块 | `feature` / `模块` | STORY / BUG | FEATURE |
| 测试场景 | `scene` / `场景` | FEATURE / STORY / BUG | SCENE |
| 测试点 | `tpoint` / `testpoint` / `测试点` | FEATURE / SCENE / STORY / BUG | TEST_POINT |
| 测试用例 | `case` / `用例` | STORY / BUG / FEATURE / TEST_POINT / SCENE | CASE |

#### 节点类型层级

```
STORY / BUG（需求 / 缺陷）
  └── FEATURE（功能模块, ##）
       └── SCENE（测试场景, ###）
            └── TEST_POINT（测试点, ####）
                 └── CASE（测试用例, #####）
```

#### 生成器模块

| 生成器 | 功能 | 输出 |
|-------|------|------|
| `issue-analyst` | 需求分析，提取关键点与待澄清问题 | 需求分析文档 |
| `framework-generator` | 生成完整测试框架（多层级树形结构） | JSON 树形结构 |
| `feature-generator` | 生成功能模块节点 | JSON 数组 |
| `scene-generator` | 生成测试场景节点 | JSON 数组 |
| `tpoint-generator` | 生成测试点节点 | JSON 数组 |
| `case-generator` | 生成测试用例（含步骤和预期结果） | JSON 数组 |
| `deduplicator` | 对生成的节点进行去重 | 去重后的节点列表 |

### 2. tcase-casegen-workflow — TCase 用例生成 Spec 工作流

独立的 spec 工作流技能包，提供完整的 5 阶段测试用例生成流程。当 `testbuddy-skill` 检测到此技能包存在时自动使用，无需手动调用 `select_workflow`。

#### 工作流阶段

| 阶段 | 内容 | 输出 | 用户确认 |
|------|------|------|---------|
| 阶段1：查询需求 | 整理用户当前需求详情 | — | 自动进入下一阶段 |
| 阶段2：需求分析 | 提取关键点，查询知识库补充信息 | `/tmp/test_analysis.md` | 需要确认 |
| 阶段3：测试点设计 | 识别模块和测试点（正常/异常/专项） | `/tmp/test_design.md` | 需要确认 |
| 阶段4：用例生成 | 基于测试点生成详细用例（含步骤和预期） | `/tmp/test_cases.md` | 需要确认 |
| 阶段5：同步到脑图 | 校验 → 解析引用 → 写入 → 渲染 | 脑图节点可视化 | — |

#### 核心特性

- **强制用户确认门禁**：阶段2→3、3→4、4→5 的过渡必须经过用户明确批准，不可跳过
- **与 testbuddy-skill 能力矩阵集成**：阶段2对应需求分析、阶段3对应测试点生成、阶段4对应用例生成
- **使用工具能力**：`load_session`、`add_nodes`（阶段5同步到脑图时）
- **支持节点类型**：STORY、BUG、FEATURE、SCENE、TEST_POINT、CASE（共6种）

### 3. tcase-codegen — 自动化测试代码生成

调用 TCase MCP 工具生成自动化测试代码，支持四种输入模式：

| 模式 | op_type | 输入说明 |
|------|---------|---------|
| UUID 模式 | `uuid` | 通过测试用例 UUID 生成代码 |
| 文本用例模式 | `text_case` | 通过测试用例描述文本生成代码 |
| 节点模式 | `node` | 通过脑图节点 UID 批量生成代码 |
| 标准模式 | `standard` | 基于 RFC 文档引用生成代码 |

完整流程：环境准备 → 参数组装 → MCP 调用 → 批量处理 → 上传到 TCase 系统。

### 4. yottadb-function-testing — YottaDB 专项测试

针对 YottaDB 分布式数据库的专业测试代码生成器，覆盖 TSDB、MEMDB、Control Plane、Data Plane、FasterKV、BDB、Marvel 等模块。提供完整的 API 参考、代码模板和最佳实践文档。

### 5. alb-autotest-codegen — ALB 自动化测试

针对 ALB（Application Load Balancer）负载均衡系统的专业自动化测试代码生成器。支持通过关键词（ALB）自动拉取对应源码，严格遵循 DB 校验、接口联动、数据清理、LD 配置校验等测试规范。

主要特性：
- 自动识别产品线并拉取源码（`git clone`）
- 按接口类型（create/update/delete/get）选择对应测试策略
- 完整的测试流程覆盖：资源获取 → 参数构造 → 请求下发 → DB 校验 → 接口查询校验 → LD 配置校验 → fixture teardown 清理
- 使用 pytest 框架（不使用 allure），提供完整的代码模板和编码标准

## Spec 工作流

Spec 工作流是推荐的完整测试设计流程，现已独立为 `tcase-casegen-workflow` 技能包（`.codebuddy/skills/tcase-casegen-workflow/SKILL.md`），当 `testbuddy-skill` 检测到该技能包存在时自动使用。原有规则定义（`.codebuddy/rules/TCase用例生成工作流.md`）作为备用路径保留。

```
查询需求 → 需求分析 → 测试点设计 → 用例生成 → 同步到脑图
```

### 阶段说明

| 阶段 | 内容 | 输出 | 用户确认 |
|------|------|------|---------|
| 阶段1：查询需求 | 整理用户当前需求详情 | — | 自动进入下一阶段 |
| 阶段2：需求分析 | 提取关键点，查询知识库补充信息 | `/tmp/test_analysis.md` | 需要确认 |
| 阶段3：测试点设计 | 识别模块和测试点（正常/异常/专项） | `/tmp/test_design.md` | 需要确认 |
| 阶段4：用例生成 | 基于测试点生成详细用例（含步骤和预期） | `/tmp/test_cases.md` | 需要确认 |
| 阶段5：同步到脑图 | 校验 → 解析引用 → 写入 → 渲染 | 脑图节点可视化 | — |

### 阶段5 同步流程

1. 加载会话参数（`load_session.py`）
2. 更新模块 PARENT_UID 为最新 `design_uid`
3. 校验节点格式（`validate_nodes.py`）
4. 解析 PARENT_UID 中文引用为真实 UID
5. 清理旧 update 文件
6. 添加节点到脑图（`write_node_from_file.py`）
7. 调用 MCP `show_node` 渲染到画布
8. 清理临时文件

## 工具能力

### 脑图操作工具

| 工具 | 功能 | 实现方式 |
|-----|------|---------|
| `load_session` | 加载会话参数（design_uid、token 等） | Python 脚本读取 session.json |
| `add_nodes` | 添加节点到脑图 | 校验 → 写入 → MCP 渲染 |
| `update_nodes` | 更新脑图节点 | 校验 → 更新 → MCP 渲染 |
| `delete_nodes` | 删除脑图节点 | 定位 → 删除 → 渲染 |
| `search_nodes` | 搜索脑图节点 | 读取 JSON 文件递归匹配 |
| `get_descendants` | 获取子节点树 | 读取 JSON 文件递归遍历 |

### 调度工具

| 工具 | 功能 | 实现方式 |
|-----|------|---------|
| `select_workflow` | 根据关键词选择工作流 | 优先检测 tcase-casegen-workflow 技能包，回退匹配自定义规则，再回退默认映射 |
| `select_rule` | 根据关键词选择规则 | 优先匹配自定义规则，回退默认映射 |
| `rag_search` | 知识库检索 | 双策略：MCP retrieve_knowledge + RAG_search |

## 子代理

| 代理 | 职责 |
|------|------|
| `tcase-testcase-generator` | 将 MCP 返回的用例描述生成完整测试代码并写入文件，写入后强制 Read 验证 |
| `yottadb-testcase-generator` | 串联 tcase-codegen 和 yottadb-function-testing，完成 UUID → 环境准备 → MCP 获取 → 代码生成 → 上传全流程 |
| `alb-testcase-generator` | 串联 tcase-codegen 和 alb-autotest-codegen，完成 UUID → 环境准备 → MCP 获取 → 源码拉取 → 代码生成 → 上传全流程 |

## 安装配置

### 1. 部署技能包

将项目复制到 CodeBuddy 的 `.codebuddy/` 目录下：

```bash
cp -r .codebuddy/ <your-project>/.codebuddy/
```

### 2. MCP 服务器配置

项目预配置了 TCase MCP 服务（`.codebuddy/.mcp.json`），如需添加 TestBuddy MCP 服务：

```json
{
  "mcpServers": {
    "testbuddy_tools": {
      "url": "http://testbuddy.woa.com/api/tb/v1/cb-plugin/sse",
      "headers": {
        "x-testbuddy-origin": "cb-plugin"
      },
      "timeout": 100000,
      "transportType": "streamable-http"
    }
  }
}
```

### 3. 验证安装

```bash
python3 .codebuddy/skills/testbuddy-skill/scripts/load_session.py
```

## 使用指南

### Spec 工作流（推荐）

适用于从零开始设计测试用例的完整场景：

```
用户：请帮我分析这个需求并生成测试用例：[需求描述]
AI：输出需求分析 → 等待确认 → 测试点设计 → 等待确认 → 用例生成 → 等待确认 → 同步到脑图
```

每个阶段都支持用户反馈修订，确认后自动进入下一阶段。

### TestBuddy Skill（灵活调度）

适用于已有部分测试设计、需要补充特定层级的场景：

```
用户：为这个需求生成测试框架
用户：根据这个模块生成测试点
用户：根据这些测试点生成测试用例
```

### 常用命令

```bash
# 打开 TestBuddy 平台
# 使用 .codebuddy/commands/tb_open.md 命令

# 加载会话参数
python3 .codebuddy/skills/testbuddy-skill/scripts/load_session.py

# 校验节点格式
python3 .codebuddy/skills/testbuddy-skill/scripts/validate_nodes.py <file_path>

# 添加节点到脑图
python3 .codebuddy/skills/testbuddy-skill/scripts/write_node_from_file.py add <design_uid> <file_path>
```

## 技术架构

```
┌─────────────────────────────────────────────────────┐
│                   CodeBuddy 平台                      │
├──────────┬──────────┬──────────┬────────────────────┤
│  Rules   │ Commands │  Agents  │      Skills        │
│ Spec工作流│ tb_open  │ tcase    │ testbuddy-skill    │
│          │          │ yottadb  │ tcase-casegen-wf   │
│          │          │ alb      │ tcase-codegen      │
│          │          │          │ yottadb-testing    │
│          │          │          │ alb-autotest       │
├──────────┴──────────┴──────────┴────────────────────┤
│                   调度层                              │
│     select_workflow.py  /  select_rule.py            │
├─────────────────────────────────────────────────────┤
│                  脚本执行层                            │
│  load_session / validate_nodes / write_nodes         │
├──────────────┬──────────────────────────────────────┤
│   MCP 服务层  │                                      │
│  TCase MCP   │  TestBuddy MCP (show_node 等)         │
├──────────────┴──────────────────────────────────────┤
│                  数据存储层                            │
│  .testbuddy/assets/{design_uid}.json                 │
│  .testbuddy/assets/{design_uid}-update.json          │
│  .testbuddy/env/session.json                         │
└─────────────────────────────────────────────────────┘
```

## 数据格式

### 支持的输入格式

脚本统一支持三种输入格式，解析后转为 JSON 操作：

- **Structured Markdown**（推荐）：`##` ~ `#####` 四级标题映射节点类型
- **JSON**：标准 JSON 数组
- **YAML**：标准 YAML 格式

### Markdown 层级映射

| Markdown 标题 | 节点类型 |
|--------------|---------|
| `##` | FEATURE |
| `###` | SCENE |
| `####` | TEST_POINT |
| `#####` | CASE |

### CASE 节点 instance 字段

```json
{
  "preconditions": "前置条件",
  "priority": "P0",
  "steps": [
    { "action": "操作描述", "expected": "预期结果" }
  ]
}
```

## 注意事项

- Markdown 文件中禁止使用 `---` 分割线（干扰脚本解析）
- 脚本只解析 4 级标题（`##` ~ `#####`），不支持 `######` 及更深层级
- PARENT_UID 必须与对应标题前缀完全一致，同步前需解析中文引用为真实 UID
- 所有脑图写入操作后必须调用 MCP `show_node` 渲染，否则节点不可见
- 添加节点前必须通过 `validate_nodes.py` 格式校验

## 联系方式

- **项目维护者**：seagullliu
- **TestBuddy 平台**：http://testbuddy.woa.com
