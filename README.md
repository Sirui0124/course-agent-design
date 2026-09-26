# 课程agent设计和解读

将公开课程大纲转为课程Agent可用的五列表格：**知识领域｜定义｜L1–L6评估标准（JSON数组）｜初始级别｜目标级别**。

本技能设置为 **manual**，仅显式调用 `$course-agent-design` 时使用。通常每课10–20个领域，允许更少或更多；不按公式、例题凑数。

## 安装与使用

将本仓库下载或克隆到 Codex 的 `skills/course-agent-design/` 目录，确保该目录下直接包含 `SKILL.md`。已存在同名技能时先保留自己的修改，不要直接覆盖。重新打开任务后显式调用：

> 请使用 $course-agent-design 解读这份课程大纲，输出知识领域、定义、六级评价标准JSON数组、初始级别和目标级别五列表格，保留来源及假设依据。

`agents/openai.yaml` 中的 `allow_implicit_invocation: false` 控制手动调用。技能不包含模型API、账号Token或联网服务；由调用它的Agent读取用户提供的大纲或官方公开来源。

## 示例和数据约定

`references/examples/` 包含数学建模12、线性代数10、概率统计12、高数上12个领域，共46领域、276条标准的JSON和Markdown。数学建模12类为已选课程设计目录；其余三门是公开课程大纲解读示例。文件记录原始来源，领域归并、标准与级别均为AI设计建议，不能声称为教师原定标准。

初始级别可用L0/L1待测假设；没有学生证据时不能判定真实L0，实际评估未知用U。目标为L3–L6单值。每行仍保留完整六级标准，高于目标的条目只供扩展。L0是本技能扩展，不属于布鲁姆六级。没有学生成绩或原始对话数据。

校验及渲染只需要Python 3：

```bash
python3 scripts/validate_render.py references/examples/mathematical-modeling.json --markdown model-table.md
```

校验器检查六级完整性、来源引用、重复ID与级别范围，不证明教学效度。详见 [SKILL.md](SKILL.md) 和 [评价与输出协议](references/rubric-and-schema.md)。
