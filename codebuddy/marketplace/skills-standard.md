# Skills（技能）标准

## 目录结构

**位置**：插件根目录的 `skills/` 目录

```
skills/
├── skill-name/
│   ├── SKILL.md          # 必需：技能主文件
│   ├── reference.md      # 可选：参考文档
│   └── scripts/          # 可选：辅助脚本
└── another-skill/
    └── SKILL.md
```

## SKILL.md 格式

### Frontmatter 配置（必需）

```markdown
---
name: 技能名称（可选，默认使用目录名）
description: 技能描述
allowed-tools: Read,Write,Bash（允许使用的工具列表，逗号分隔）
---

技能的指令内容
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| name | string | 否 | 技能名称，默认使用目录名 |
| description | string | 是 | 技能描述 |
| allowed-tools | string | 否 | 允许使用的工具列表，逗号分隔 |

## 特性

- 技能可以包含辅助文件和脚本
- 技能的 `baseDirectory` 指向技能目录，可访问同目录下的资源文件

## 示例

```markdown
---
name: pdf-processor
description: 处理 PDF 文档，提取文本和元数据
allowed-tools: Read,Write,Bash
---

# PDF 处理技能

本技能用于处理 PDF 文档...
```
