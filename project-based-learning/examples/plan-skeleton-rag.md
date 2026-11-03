# 示例骨架：RAG 知识库问答（节选）

> 输入："做一个 RAG 知识库问答系统练手，Python + FastAPI + LangChain + Chroma，4 周，要和 Obsidian 知识库联动。"
> 下面是 8 部分**各取一段**，用于标定颗粒度。真实方案每人每项目都不同。

## 一、项目概述（节选）

**项目名称**：Obsidian 知识库 RAG 问答助手
**类型**：AI RAG 应用 ｜ **难度**：⭐⭐⭐ ｜ **周期**：4 周
**最终产物**：可本地运行的 Web 问答服务，支持对 200+ 篇笔记的检索问答，回答附引用来源
**学习目标**：掌握文档切分策略、向量检索与重排、引用溯源、流式输出

## 二、需求文档（节选）

| 模块 | 功能点 | 优先级 | 验收口径 |
|---|---|---|---|
| 摄入 | 目录扫描 + 增量更新 | P0 | 新增 1 篇笔记后 10s 内可被检索到 |
| 检索 | 向量 + BM25 混合召回 | P0 | Top5 命中率 ≥ 80%（20 条标注问题） |
| 问答 | 流式回答 + 引用来源 | P0 | 首 token < 2s，引用可点开到具体笔记段落 |

## 三、技术选型（节选）

| 层 | 选择 | 为什么不选替代 |
|---|---|---|
| 向量库 | Chroma（本地持久化） | Milvus 功能更强但需独立服务，4 周项目里运维成本 > 收益 |
| 检索 | BM25 + 向量 + RRF 融合 | 纯向量对专有名词不敏感（如 `wait_for_db`）；纯 BM25 抓不住同义表述 |
| 编排 | 原生 LCEL，不上 LangGraph | 单轮问答无多分支，图编排只会增加调试面 |

## 四、架构设计（节选）

```
app/
├── ingest/      # 扫描、切分、写入（幂等：按文件 hash 去重）
├── retrieve/    # 向量检索 + BM25 + RRF 融合 + 重排
├── chat/        # 流式问答、引用拼装
└── api/         # /ingest /query /health
```

## 五、分步实现（节选阶段 2）

**阶段 2：检索可用（第 2 周）**

| 项 | 内容 |
|---|---|
| 目标 | 给定问题，返回 Top5 相关片段 |
| 步骤 | ① 建 512/64 切分器 → ② 批量向量化写入 → ③ BM25 索引 → ④ RRF 融合 → ⑤ 评测脚本 |
| 关键点 | 切分要按标题层级优先，硬切会把一个概念切成两半 |
| 知识库 | [[文档切分]]、[[向量检索]]、[[RRF 融合排序]] |
| 阶段产物 | `python -m app.retrieve.eval` 输出 Top5 命中率 |
| 阶段验收 | `python -m app.retrieve.eval --topk 5` → `hit_rate=0.82` |

## 六、验收标准（节选）

```bash
# 功能
curl -s localhost:8000/health | jq -e '.status=="ok"'
curl -s -X POST localhost:8000/query -d '{"q":"RRF 是什么"}' | jq -e '.citations|length>0'

# 性能
python -m app.retrieve.eval --topk 5     # hit_rate ≥ 0.80
# 首 token 延迟：ttft < 2s（脚本取 SSE 首帧时间戳）
```

## 七、扩展方向（节选）

1. **加入重排**：Cross-Encoder 对 Top20 重排，预期命中率 +5~8pp，前置条件：已有一批标注问题；
2. **多模态**：图片笔记走 OCR 后入同一索引，前置条件：切分器支持图文混排。

## 八、学习资源（节选）

- Chroma 官方文档「Collections & Persistence」
- LangChain 官方文档「Retrievers → EnsembleRetriever」
- 论文：Reciprocal Rank Fusion（Cormack et al., 2009）
