# 复习模板与 Dataview 联动

> 供 knowledge-review-spaced 生成复习清单和统计报告时参考，按对应模板执行。**算法口径以 [review-algorithm.md](review-algorithm.md) 为唯一权威**，本文件只负责字段、模板与查询，二者字段一一对应。

---

## Frontmatter 扩展字段

在笔记的 Frontmatter 中添加以下字段，用于间隔复习跟踪：

```yaml
---
title: 笔记标题
category: 分类
tags: [标签1, 标签2]
difficulty: ⭐⭐⭐
# 复习跟踪字段
review_status: new          # new / learning / reviewing / mastered
review_count: 0             # 连续通过次数（q≥3 累加，q≤2 归零）
streak: 0                   # 连续高质量(q≥4)次数，驱动 reviewing→mastered
last_review: 2026-08-01     # 上次复习日期 YYYY-MM-DD
next_review: 2026-08-02     # 下次复习日期 YYYY-MM-DD
ease_factor: 2.5            # 难度系数 EF，范围 1.3-3.0，默认 2.5，按难度初始化
interval: 1                 # 当前间隔（天）
---
```

**字段说明**：
| 字段 | 类型 | 说明 | 可选值 |
|------|------|------|--------|
| review_status | string | 复习状态 | new（新笔记）、learning（学习中）、reviewing（复习中）、mastered（已掌握） |
| review_count | number | 连续通过次数 | 整数，从 0 开始，q≤2 归零 |
| streak | number | 连续高质量次数 | 整数，用于状态升级判定，q≤2 清零 |
| last_review | date | 上次复习日期 | YYYY-MM-DD |
| next_review | date | 下次复习日期 | YYYY-MM-DD |
| ease_factor | number | 难度系数 EF | 1.3–3.0，默认 2.5 |
| interval | number | 当前间隔（天） | 正整数 |

**难度 → 初始 EF**（详见 review-algorithm.md 第三节）：⭐=2.7 / ⭐⭐=2.6 / ⭐⭐⭐=2.5（默认）/ ⭐⭐⭐⭐=2.3 / ⭐⭐⭐⭐⭐=2.1。

**状态流转**（与算法文件一致）：
- new → learning：完成第一次评分后
- learning → reviewing：连续 2 次 q≥3
- reviewing → mastered：连续 3 次 q≥4
- 回退：mastered→reviewing、reviewing→learning（出现一次 q≤2，streak 清零、review_count 归零、间隔重置为 1 天）

---

## 今日复习清单模板

````markdown
## 📅 今日复习清单（2026-08-31）

**今日需复习**：N 篇
**已完成**：M 篇
**完成率**：XX%

### 🔴 逾期复习（应在今天之前复习）
| 笔记 | 分类 | 难度 | 逾期天数 | 上次复习 | 状态 |
|------|------|------|---------|---------|------|
| [[笔记1]] | 分类 | ⭐⭐⭐ | 3天 | 2026-08-25 | learning |
| ... | ... | ... | ... | ... | ... |

### 🟡 今日到期
| 笔记 | 分类 | 难度 | 连续通过 | 上次复习 | 状态 |
|------|------|------|---------|---------|------|
| [[笔记2]] | 分类 | ⭐⭐ | 2次 | 2026-08-28 | reviewing |
| ... | ... | ... | ... | ... | ... |

### 🟢 新笔记建议复习（今天新学的）
| 笔记 | 分类 | 难度 | 学习时间 | 状态 |
|------|------|------|---------|------|
| [[笔记3]] | 分类 | ⭐⭐⭐⭐ | 今天 | new |
| ... | ... | ... | ... | ... |

### 复习记录怎么写
复习每篇笔记后记录：笔记链接 + 复习时间 + 复习质量 q（1-5，✅🟡❌ 按 5/3/1 换算）；随后更新 Frontmatter——review_count 按规则增减、last_review=今天、next_review 按 SM-2 计算、ease_factor 微调、review_status 按状态机更新。
````

---

## 复习统计报告模板

````markdown
## 📊 复习统计报告

**统计周期**：2026-08-01 至 2026-08-31
**生成时间**：2026-08-31

### 总体统计
| 指标 | 数值 |
|------|------|
| 知识库总笔记数 | N |
| 已纳入复习计划 | N（XX%） |
| 本月复习总次数 | N |
| 本月完成复习 | N 篇次 |
| 平均复习质量 | X.X / 5 |
| 掌握率（mastered 占比） | XX% |

### 复习状态分布
| 状态 | 笔记数 | 占比 |
|------|--------|------|
| new（新笔记） | N | XX% |
| learning（学习中） | N | XX% |
| reviewing（复习中） | N | XX% |
| mastered（已掌握） | N | XX% |

### 按分类统计
| 分类 | 总笔记 | 已复习 | 掌握 | 掌握率 |
|------|--------|--------|------|--------|
| Java | N | N | N | XX% |
| 前端 | N | N | N | XX% |
| ... | ... | ... | ... | ... |

### 按难度统计
| 难度 | 总笔记 | 平均连续通过 | 平均质量 | 掌握率 |
|------|--------|------------|---------|--------|
| ⭐ 入门 | N | X.X | X.X | XX% |
| ⭐⭐ 进阶 | N | X.X | X.X | XX% |
| ... | ... | ... | ... | ... |

### 薄弱环节（复习质量 q<3 的笔记）
| 笔记 | 分类 | 难度 | 连续通过 | 平均质量 | 建议 |
|------|------|------|---------|---------|------|
| [[笔记]] | 分类 | ⭐⭐⭐ | 0 | 2.3 | 重新学习，用 tech-concept-deep-dive 深化 |
| ... | ... | ... | ... | ... | ... |

### 下月建议
1. 优先复习薄弱环节的 N 篇笔记
2. 新学习的笔记及时纳入复习计划
3. 已 mastered 的笔记降低复习频率（间隔由 EF 自动拉长）
4. 建议每周复习 X-X 篇，保持节奏
````

---

## 与 Obsidian Dataview 联动

### 查询1：今日待复习笔记

```dataview
TABLE category, difficulty, review_status, last_review, next_review
FROM "知识库"
WHERE next_review <= date(today) AND review_status != "mastered"
SORT next_review ASC
```

### 查询2：逾期未复习笔记

```dataview
TABLE category, difficulty, review_status, last_review, next_review, (date(today) - next_review).days AS 逾期天数
FROM "知识库"
WHERE next_review < date(today) AND review_status != "mastered"
SORT 逾期天数 DESC
```

### 查询3：复习状态分布

```dataview
TABLE length(rows) AS 笔记数
FROM "知识库"
WHERE review_status
GROUP BY review_status
```

### 查询4：按分类统计掌握率

```dataview
TABLE 
  length(rows) AS 总笔记,
  length(rows.filter(r => r.review_status = "mastered")) AS 已掌握,
  round(length(rows.filter(r => r.review_status = "mastered")) / length(rows) * 100, 1) + "%" AS 掌握率
FROM "知识库"
WHERE category
GROUP BY category
```

### 查询5：本周复习记录

```dataview
TABLE category, difficulty, review_status, review_count, last_review
FROM "知识库"
WHERE last_review >= date(today) - dur(7 days)
SORT last_review DESC
```

### 查询6：薄弱笔记（连续通过次数低、仍未掌握）

```dataview
TABLE category, difficulty, review_count, review_status
FROM "知识库"
WHERE review_status != "mastered" AND review_count <= 2
SORT review_count ASC, difficulty DESC
LIMIT 20
```

---

## 复习质量评分标准（与算法文件完全一致）

| 评分 q | 含义 | 表现 | EF 调整 | 间隔/次数动作 |
|--------|------|------|---------|--------------|
| 5 | 完全记住 | 能准确复述全部要点、能迁移应用 | +0.10（上限 3.0） | 通过，按主公式拉长间隔 |
| 4 | 基本记住 | 能复述大部分，少量遗忘 | +0.05 | 通过，按主公式拉长间隔 |
| 3 | 有点印象 | 记得大概，细节遗忘较多 | 不变 | 通过但不算高质量，间隔照常推进 |
| 2 | 比较模糊 | 只有模糊印象，需要重学 | −0.15（下限 1.3） | review_count 归零、间隔重置 1 天、状态回退 |
| 1 | 完全忘了 | 没有任何印象，等于新学 | −0.30（下限 1.3） | review_count 归零、间隔重置 1 天、回退到 learning |

> 间隔主公式：第 1 次通过=1 天、第 2 次=6 天、第 n≥3 次=round(上次间隔 × EF)；完整推导与示例见 [review-algorithm.md](review-algorithm.md)。
