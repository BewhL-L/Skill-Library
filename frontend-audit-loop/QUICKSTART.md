# 快速上手

## 触发方式

对 Agent 说：

- 「对 35周冲刺打卡.html 做多轮全面自检，直到没有优化空间」
- 「网页改完了，做一次体检：布局/配色/交互/性能都要查，发现问题直接修」
- 「交付前做一轮防回归验收」

## 最小执行路径（约 5 分钟出第一轮结论）

1. **静态扫描**（1 分钟）：grep 十六进制色与散落 rgba → 记录待收敛项；grep `will-change`、`transition:all`、`@keyframes` → 核对动画属性白名单
2. **截图走查**（2 分钟）：headless 截 `1440 / 492 × 深/浅` 四张，看跨列空洞、白压白、玻璃换肤
3. **溢出探针**（1 分钟）：用 [references/verification-toolkit.md](references/verification-toolkit.md) §1 的 iframe 探针跑最窄视口，确认 `ISW === ICW`
4. **交互冒烟**（1 分钟）：跑 §4 的 jsdom 模板，核心链路断言
5. 汇总「通过项 / 已修复项」，修复后**重跑 1–4**，零发现即收敛

## 深入使用

- 完整五维清单 → [references/audit-rounds.md](references/audit-rounds.md)
- 团队编排（改动面大时）→ [references/team-orchestration.md](references/team-orchestration.md)
- 工具坑点（headless 钳制、jsdom 伪影）→ [references/verification-toolkit.md](references/verification-toolkit.md)

## 判定收敛

某一轮五个维度**全部零发现**，且上一轮修复的回归断言全绿 → 输出终轮结论并附依据（回归证据 + 探针数值）。不再继续"感觉还能更好"的打磨。
