# QUICKSTART · 5 分钟上手

## 1. 复制模板

```powershell
Copy-Item "<skill目录>\templates\schedule-template.html" .\我的排期表.html
```

## 2. 替换 10 个占位符

打开 `我的排期表.html`，全局搜索 `{{`，依次替换：

| 占位符 | 改成什么 |
|--------|---------|
| `{{TITLE}}` | 浏览器标签页标题 |
| `{{DESCRIPTION}}` | SEO 描述 |
| `{{HERO_TITLE_HTML}}` | 大标题，可用 `<span class="hl">` 做渐变高亮 |
| `{{HERO_SUBTITLE}}` | 一段说明 |
| `{{CHIPS_HTML}}` | 5 个 `<div class="chip">...</div>` |
| `{{START_JS}}` | `new Date(2026,9,16)`（月份从 0 开始） |
| `{{STAGES_JSON}}` | 阶段数组，见下 |
| `{{STORAGE_KEY}}` | 项目英文短名，如 `ragstudy-v1` |
| `{{THEME_KEY}}` | 项目英文短名 + theme，如 `ragstudy-theme-v1` |
| `{{FOOTER_TEXT}}` | 页脚一句原则文案 |

## 3. stages 数组最小示例

```js
const stages = [
  {
    name: "阶段一 · 入门", badge: "W1–W2",
    goal: "跑通环境",
    weeks: [
      { title: "环境准备", tag: "setup",
        tasks: ["装 Node 20（2h）", "git init（0.5h）"],
        deliver: "环境可跑" },
      { title: "第一个 demo", tag: "code",
        tasks: ["写 Hello World（1h）"],
        deliver: "能跑" }
    ]
  }
];
```

## 4. 打开验证

- [ ] 浏览器打开无白屏
- [ ] 深浅色切换按钮可用
- [ ] 勾选任务后进度条变化
- [ ] 刷新后勾选状态还在
- [ ] 右侧周导航点击能跳转
