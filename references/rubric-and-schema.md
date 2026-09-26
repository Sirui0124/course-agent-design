# 评价与输出协议

## 六级标准的含义

采用修订布鲁姆认知过程分类；教学设计依据可参见[CMU教学中心](https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html)。本协议将六类操作化用于领域内任务，不把它们当作固定学生能力、自然等距分数或必然逐级发展的阶段。

| 级别 | 评价任务 | 应出现的证据 |
|---|---|---|
| L1 记忆 | 识别、回忆领域对象和规则 | 关键术语、符号、必要条件准确 |
| L2 理解 | 用自己的表述解释、比较、举例 | 意义和关系正确，能区别易混概念 |
| L3 应用 | 在条件给定的常规问题中执行方法 | 方法适用，关键步骤与结果正确 |
| L4 分析 | 在变式问题中分解结构、条件和依赖 | 指出影响结论的结构或错误原因，有推理证据 |
| L5 评价 | 根据明确准则审查方法、结论或解答 | 给出准则、证据、局限和有依据的判断 |
| L6 创造 | 在开放约束下形成方案、模型、实例族或作品 | 有非照抄的方案构造、方法整合及验证；不要求科研原创 |

每项标准用“动作＋领域对象＋质量条件”写成一句可判断的话。完整六项并不意味着每个学生每级各答一题，或完成L6自动证明所有基础已稳固。难算的题未必高认知；按模板代公式通常仍是L3；照抄“设计”代码也未必L6。

诊断时将任务要求、学生独立表现、辅助程度分别记录。只能看到AI答案、学生说“懂了”、重复对话、QA3/QA Pro类型，均不足以直接判定等级。信息不足返回U（unknown）。充分证据显示未达到L1可记L0。某次任务的高等级表现不等于全领域稳定掌握；稳定达标需要预先约定的多样化评价证据，本技能不擅自规定统一正确率阈值。

## 初始级别与目标级别

示例默认initial_basis.type=planning_assumption。L0表示暂按没有本领域可用基础设计教学；L1表示暂按能识记核心术语设计。二者均不是测量结果；单凭先修课程不能升级。用户已有诊断时使用diagnostic_evidence并记录匿名证据。学生评估未知用U，课程规划仍可另填有明示依据的L0/L1假设。

target_level为L3、L4、L5或L6单值，是当前课程准备让学生独立完成的主要目标任务类型。target_basis说明具体课程任务为何支持该目标，并标注AI建议或教师原定。用户手动修改目标时type使用user_configuration，保留修改依据，不冒充教师原定。完整rubric仍含L1–L6；高于目标的条目用于扩展，不列入本学期必达要求。用户希望目标低于L3时保留原意并说明与本表默认协议不同，不伪造更高课程要求。

## JSON结构

一个文件对应一门课程；所有字段不含学生身份。示例遵循：

```json
{
  "schema_version":"course-agent-design-v1",
  "course":"课程名称",
  "scope":"学段、学期与内容边界",
  "source_facts":[{"id":"S1","url":"https://example.edu.cn/syllabus","title":"大纲原名","institution":"学校","teacher":null,"hours":40,"version":null,"accessed_at":"YYYY-MM-DD","verification":"official_body_read"}],
  "interpretation_note":"领域、标准及等级的证据性质",
  "domains":[{
    "id":"course-01",
    "name":"知识领域标签",
    "definition":"核心问题；纳入内容；相邻边界",
    "rubric":[{"level":"L1","standard":"该级可观察标准"},{"level":"L2","standard":"该级可观察标准"},{"level":"L3","standard":"该级可观察标准"},{"level":"L4","standard":"该级可观察标准"},{"level":"L5","standard":"该级可观察标准"},{"level":"L6","standard":"该级可观察标准"}],
    "initial_level":"L0",
    "target_level":"L4",
    "initial_basis":{"type":"planning_assumption","note":"未有诊断；暂按无领域基础设计"},
    "target_basis":{"type":"ai_design_suggestion","note":"目标任务及理由"},
    "source_mapping":[{"source_id":"S1","section":"章节或页码","coverage":"required"}]
  }],
  "uncertainties":[]
}
```

rubric数组恰好六项，按L1到L6排序。initial_level允许L0–L6；target_level默认限定L3–L6。coverage取required/optional/purpose；purpose不等于有独立课时。扩展内容与综合多来源模板必须在scope和interpretation_note披露。

表格只投影name、definition、rubric、initial_level、target_level。rubric单元格使用真实JSON数组，不是伪JSON、单引号字典或“见另页”。来源和理由放表外或JSON元数据，不省略证据，也不扩成八九列表。
