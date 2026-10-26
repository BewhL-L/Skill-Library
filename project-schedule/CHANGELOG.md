# CHANGELOG

## v1.0.1 (2026-10-16)

- 修复：模板 hero-meta 替换后残留 4 个原 chip 和一个多余 `</div>`（正则非贪婪匹配 bug）
- 修复：footer 项目特定文案（"关闭参考自己重写一遍..."）改为 `{{FOOTER_TEXT}}` 占位符
- 补充：SKILL.md 占位符清单加 FOOTER_TEXT，CHIPS_HTML 给具体示例
- 验证：全文件 grep 确认无项目特定内容残留

## v1.0.0 (2026-10-16)

- 首发版本
- 从「29 周 AI 全栈项目学习排期表」实战模板提炼
- 固化暖色玻璃拟态设计系统（橙/青/紫/粉四 accent）
- 支持深色/浅色双主题
- 支持 checkbox 进度持久化（localStorage）
- 支持右侧周导航、今日高亮、滚动入场动画
- 提供 `templates/schedule-template.html` 完整模板（10 个占位符）
- 提供 `references/design-system.md` 设计规范
