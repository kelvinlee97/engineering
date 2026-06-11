---
description: 加载 tcase-codegen skill，生成通用自动化测试用例代码
allowed-tools: Read,Write,Bash,Search
---

根据用户提供的 uuid / text_case / node / standard 生成任意仓库的自动化测试用例代码。

## 强制执行流程

skill 每次请求都**必须显式加载**并**精读SKILL.md**，不可跳过任何一步：

### 步骤1: 加载 `tcase-codegen` skill（每次请求必须重新执行）
- **【强制】调用 `use_skill: tcase-codegen`，不得因"已加载"而跳过**
- **【强制】必须重新执行 `env_prepare.py` 脚本获取 user_id、user_repo、user_branch，禁止复用对话历史中已有的环境信息**
- 参数组装与校验，自动识别操作模式（uuid / text_case / node / standard）
- 调用 TCase MCP 工具获取用例相关信息
- 根据 MCP 返回的 order 模板 + 项目搜索生成完整代码
- 文件写入 + 验证
- **本步骤完成的标志**：生成完整可执行的测试代码文件

### 步骤2: tcase_uuid 校验与补全（每次生成完成后必须重新执行）
- 对所有生成的测试函数检查 `tcase_uuid` 字段
- 若已有 `tcase_uuid`，**禁止修改**，直接跳过
- 若缺少 `tcase_uuid`：**必须**复用 `design_case_uuid`；若也没有则调用脚本批量生成
- **本步骤完成的标志**：所有 `tcase_uuid` 均通过 RFC4122 格式校验
