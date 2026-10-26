# Changelog

## v2.1.0 (2026-10-15)

- 补全六套美学主题（prism/corridor/threads/waves/fibers/acid），右上角色板切换
- 补全大卡片 3D tilt（鼠标跟随 perspective 900px rotateY/rotateX）+ 小卡片微抬升
- 补全入场 3D 翻入（perspective 900px rotateX 5deg）
- 补全顶部栏（brand logo + 项目名 + 主题色板）
- 补全 hero 总进度条
- 统计卡从 4 个写死 0 改为 3 个真实计算（连续打卡天数/累计投入小时/任务 x/y）
- 补全阶段进度条（7 列，当前阶段高亮）
- 补全周切换器（折线图右上角 ‹ › 翻页看历史）
- 补全 N 周全景网格（每周一个方块，点击跳周，已完成填充色）
- 补全底部 fixed 总进度条
- 补全落后提示条（dev-strip：计划 x 项/实际 y 项/落后 z 项，落后时才显示）
- 补全周视图（点"查看详情"进入：7 天任务展开 + 本周统计 + 复盘笔记自动保存）
- 铁律新增：动态模块同步入场（不手动 add("in")）+ 禁止 backdrop-filter 避免 GPU 卡顿
- references/01 新增"动态模块入场规范"章节

## v2.0.0 (2026-10-15)

- 重写为"从零生成"方法论（不再是改造已有 HTML）
- templates/dashboard-skeleton.html 改为完整可运行模板（CSS 极光+玻璃拟态+SVG折线图+三态打卡+localStorage）
- references/02 改为"数据层生成规范"（CFG/BASE_PLAN JSON 结构）
- SKILL.md 改为五步生成流程：收集需求→复制模板→填占位符→验证→交付
- 所有设计固化在模板，Agent 只填数据

## v1.0.0 (2026-10-15)

- 初始版本（改造已有 HTML 方法论，已废弃）
