---
description: 加载 tcase-codegen 和 alb-autotest-codegen 两个 skill，生成 ALB 测试用例代码
allowed-tools: Read,Write,Bash,Search
---

根据用户提供的 uuid / 文本描述 / node 生成 ALB 测试用例代码。

## 强制执行流程

两个 skill 每次请求都**必须按顺序显式加载**并**精读SKILL.md**，缺一不可，不可跳过任何一步：

### 步骤1: 加载 `tcase-codegen` skill（每次请求必须重新执行）
- **【强制】必须重新执行 `env_prepare.py` 脚本获取 user_id、user_repo、user_branch，禁止复用对话历史中已有的环境信息**
- 参数组装与校验
- 调用 TCase MCP 工具获取用例相关信息
- **本步骤完成的标志**：MCP 返回 code 字段

### 步骤2: 加载 `alb-autotest-codegen` skill（每次请求必须重新执行）
- **必须在步骤1完成后立即加载，禁止自行搜索代码**
- **强制**按照该`alb-autotest-codegen`的`SKILL.md`定义的完整工作流（读取 API 文档 → 判定接口类型 → 读取目标文件已有用例提取编码风格 → 按规范生成测试代码 → 验证和完善代码
- 消除所有 TODO 占位符
- **本步骤完成的标志**：生成完整可执行的测试代码文件

### 步骤3: tcase_uuid 校验与补全
- 对所有生成的测试函数检查 `tcase_uuid` 字段
- 若已有 `tcase_uuid`，**禁止修改**，直接跳过
- 若缺少 `tcase_uuid`：**必须**复用 `design_case_uuid`；若也没有则调用脚本批量生成
- **本步骤完成的标志**：所有 `tcase_uuid` 均通过 RFC4122 格式校验