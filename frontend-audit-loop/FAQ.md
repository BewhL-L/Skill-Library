# 常见问题

### Q: 小屏截图元素被裁出右边缘，是真溢出吗？
A: 多数是 headless 视口钳制伪影（请求 390 实际按 492 布局）。用 iframe 法探针读 `scrollWidth/clientWidth` 裁定，勿凭截图下结论。见 verification-toolkit §1。

### Q: 探针输出一直是空？
A: 截图/导出发生在页面定时器（如 setTimeout 3000）触发前。改用 `--virtual-time-budget=8000 --dump-dom` 读 DOM 文本。

### Q: jsdom 焦点恢复断言失败，是产品 bug 吗？
A: 先排除伪影：jsdom 点击不聚焦，activeElement 停在 body。断言前显式 `.focus()`；仍失败才是真问题。

### Q: 手动切主题后部分颜色不对？
A: 典型的主题块令牌泄漏——媒体查询块声明了某令牌而 `[data-theme]` 手动块漏声明。跑 verification-toolkit §3 的 diff，要求为空。

### Q: 勾选框对勾在 Firefox 不显示？
A: `input::after` 伪元素在表单控件上不被 Firefox 支持。改用背景图 data-URI 勾号（CSS 变量分主题换色）。

### Q: 修一处坏一处，怎么破？
A: 违反回归纪律。每轮修复后必须全量重跑断言 + 关键区段读回确认（编辑工具可能吞相邻行）。

### Q: 什么时候该停，不再继续打磨？
A: 出现第一个零发现轮即收敛。新想法记入待办，不进本轮——每轮额外改动本身都是回归风险。

### Q: 什么时候值得组团队而不是单干？
A: 改动面 ≥3 个维度或需要对立评审视角。单干时省去全部编排开销。见 team-orchestration.md。
