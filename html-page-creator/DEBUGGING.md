# 调试指南

> 本文档描述 html-page-creator Skill 常见问题的排查和解决方法。

## 常见问题排查

### 1. 页面渲染异常（白屏/样式错乱）

**症状**：打开HTML文件后页面空白或样式完全错乱。

**排查步骤**：
1. 检查HTML结构是否完整
   ```html
   <!DOCTYPE html>
   <html lang="zh-CN" data-theme="dark">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>页面标题</title>
     <!-- <style> 标签 -->
   </head>
   <body>
     <!-- 页面内容 -->
     <!-- <script> 标签 -->
   </body>
   </html>
   ```

2. 检查CSS是否正确闭合
   - 所有 `{` 都有对应的 `}`
   - 所有属性都以 `;` 结尾
   - 没有语法错误

3. 检查浏览器控制台
   - 按 F12 打开开发者工具
   - 查看 Console 面板是否有错误
   - 查看 Elements 面板检查DOM结构

**常见原因**：
- 复制模板时遗漏了 `</style>` 或 `</script>` 标签
- 修改CSS时破坏了语法结构
- 删除了必需的CSS变量定义

---

### 2. 主题切换不生效

**症状**：点击主题切换按钮，页面颜色没有变化。

**排查步骤**：
1. 检查主题切换按钮是否存在
   ```html
   <button class="theme-toggle" id="themeToggle" aria-label="切换主题"></button>
   ```

2. 检查JavaScript代码是否完整
   ```javascript
   const themeToggle = document.getElementById('themeToggle');
   const savedTheme = localStorage.getItem('theme') || 'dark';
   document.documentElement.setAttribute('data-theme', savedTheme);
   themeToggle.addEventListener('click', () => {
     const current = document.documentElement.getAttribute('data-theme');
     const next = current === 'dark' ? 'light' : 'dark';
     document.documentElement.setAttribute('data-theme', next);
     localStorage.setItem('theme', next);
   });
   ```

3. 检查CSS变量是否定义了浅色主题
   ```css
   [data-theme="light"] {
     --bg: #faf6f0;
     --text: #2a2218;
     /* ... 其他变量 */
   }
   ```

4. 检查浏览器控制台是否有JavaScript错误

**常见原因**：
- 按钮ID不匹配（`themeToggle` vs `theme-toggle`）
- JavaScript代码被意外删除
- 浅色主题CSS变量未定义
- localStorage被禁用（隐私模式）

---

### 3. 滚动入场动画不生效

**症状**：滚动页面时，元素没有淡入上移动画。

**排查步骤**：
1. 检查元素是否有 `.reveal` 类
   ```html
   <div class="card reveal">...</div>
   ```

2. 检查CSS是否定义了 `.reveal` 和 `.reveal.visible`
   ```css
   .reveal {
     opacity: 0;
     transform: translateY(30px);
     transition: opacity .7s var(--ease), transform .7s var(--ease);
   }
   .reveal.visible {
     opacity: 1;
     transform: translateY(0);
   }
   ```

3. 检查IntersectionObserver代码是否完整
   ```javascript
   const revealElements = document.querySelectorAll('.reveal');
   const revealObserver = new IntersectionObserver((entries) => {
     entries.forEach(entry => {
       if (entry.isIntersecting) {
         entry.target.classList.add('visible');
         revealObserver.unobserve(entry.target);
       }
     });
   }, {threshold: 0.1, rootMargin: '0px 0px -50px 0px'});
   revealElements.forEach(el => revealObserver.observe(el));
   ```

4. 检查系统是否开启了"减少动画"
   - Windows：设置 > 辅助功能 > 视觉效果 > 动画效果
   - macOS：系统设置 > 辅助功能 > 显示 > 减少动态效果

**常见原因**：
- 元素缺少 `.reveal` 类
- CSS被意外删除或覆盖
- IntersectionObserver代码不完整
- 系统开启了 `prefers-reduced-motion`（正常行为，动画会被禁用）

---

### 4. 玻璃效果不显示（卡片不透明）

**症状**：卡片背景是纯色，没有模糊透明效果。

**排查步骤**：
1. 检查卡片是否使用了正确的CSS
   ```css
   .card {
     background: var(--bg-glass);
     backdrop-filter: var(--glass);
     border: 1px solid var(--line);
   }
   ```

2. 检查CSS变量是否定义
   ```css
   :root {
     --bg-glass: rgba(30,24,18,.62);
     --glass: blur(24px) saturate(160%);
   }
   ```

3. 检查浏览器是否支持 `backdrop-filter`
   - Chrome 76+ ✅
   - Edge 79+ ✅
   - Firefox 103+ ✅（默认开启）
   - Safari 9+ ✅（需 `-webkit-backdrop-filter`）

4. 检查卡片后面是否有内容可以模糊
   - backdrop-filter需要卡片后面有内容（背景图、其他元素）才能看到效果
   - 如果卡片后面是纯色背景，模糊效果不明显

**常见原因**：
- 使用了硬编码的 `background: #xxx` 而非 `var(--bg-glass)`
- `backdrop-filter` 属性被删除
- 浏览器版本过低不支持
- 卡片后面没有可模糊的内容

---

### 5. 响应式布局异常（移动端错乱）

**症状**：在手机或小窗口下，布局错乱、内容溢出、卡片不换行。

**排查步骤**：
1. 检查viewport meta标签
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```

2. 检查媒体查询是否存在
   ```css
   @media (max-width: 768px) {
     .nav-links { display: none; }
     .card-grid { grid-template-columns: 1fr; }
     /* ... */
   }
   ```

3. 检查是否有固定宽度导致溢出
   - 搜索 `width: xxxpx` 固定值
   - 改用 `max-width` 或百分比

4. 使用浏览器开发者工具的设备模拟功能测试
   - 按 F12 > 点击设备图标
   - 选择不同设备尺寸测试

**常见原因**：
- 缺少viewport meta标签
- 媒体查询被删除或断点不正确
- 元素使用了固定宽度（如 `width: 1200px`）
- 网格布局没有设置 `auto-fit` 或响应式列数

---

### 6. 控制台JavaScript错误

**症状**：浏览器控制台显示红色错误信息。

**排查步骤**：
1. 读取错误信息，定位问题代码
2. 检查变量名是否正确（大小写敏感）
3. 检查DOM元素ID是否匹配
4. 检查函数是否在使用前定义
5. 检查是否有语法错误（括号、分号）

**常见错误及解决**：

| 错误信息 | 原因 | 解决 |
|---------|------|------|
| `Cannot read property 'addEventListener' of null` | 元素ID不存在 | 检查HTML中是否有对应ID的元素 |
| `Uncaught ReferenceError: xxx is not defined` | 变量/函数未定义 | 检查变量名拼写和定义位置 |
| `Uncaught SyntaxError` | 语法错误 | 检查括号、分号、引号是否匹配 |
| `Failed to read 'localStorage'` | 隐私模式禁用 | 添加try-catch容错 |

---

## 性能问题排查

### 页面卡顿/滚动不流畅

**排查步骤**：
1. 检查backdrop-filter数量
   - 建议页面中玻璃卡片≤20个
   - 大量使用时降低 `blur(24px)` 到 `blur(16px)`

2. 检查动画数量
   - 不要给所有元素都添加 `.reveal` 入场动画
   - 只给关键模块添加

3. 检查图片大小
   - 背景图片建议≤500KB
   - 使用WebP格式
   - 避免使用超大分辨率图片

4. 使用浏览器Performance面板分析
   - 按 F12 > Performance > 录制
   - 查看FPS和耗时任务

### 页面加载慢

**排查步骤**：
1. 检查HTML文件大小（建议≤100KB）
2. 检查是否有外部资源引用（应全部内联）
3. 检查CSS是否有大量未使用的样式
4. 检查JavaScript是否有冗余代码

---

## 设计一致性问题

### 颜色不统一

**症状**：页面中出现多种不同的橙色/蓝色，不是设计系统定义的颜色。

**排查**：
- 搜索CSS中的硬编码颜色值（如 `#ff9a2e`、`rgb(...)`）
- 替换为CSS变量（如 `var(--accent)`）

### 间距不统一

**症状**：各模块间距大小不一，没有规律。

**排查**：
- 检查 `padding`、`margin`、`gap` 值
- 确保都是8px的倍数（8, 16, 24, 32, 48, 64, 80）

---

## 获取帮助

如果以上方法无法解决问题：
1. 查看 [FAQ.md](FAQ.md) 常见问题
2. 查看 [USE-CASES.md](USE-CASES.md) 使用案例
3. 参考 [SUPPORT.md](SUPPORT.md) 获取支持

---

**版本**：v1.0.0
**最后更新**：2026-09-13
