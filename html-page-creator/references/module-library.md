# 模块库参考

## 目录
1. [导航栏模块](#导航栏模块)
2. [Hero区域模块](#hero区域模块)
3. [统计卡片模块](#统计卡片模块)
4. [功能卡片网格模块](#功能卡片网格模块)
5. [时间线模块](#时间线模块)
6. [进度条模块](#进度条模块)
7. [表格模块](#表格模块)
8. [代码块模块](#代码块模块)
9. [引用/提示框模块](#引用提示框模块)
10. [标签/徽章模块](#标签徽章模块)
11. [按钮模块](#按钮模块)
12. [表单模块](#表单模块)
13. [页脚模块](#页脚模块)

---

## 导航栏模块

### 基础导航栏
```html
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-logo">
      <div class="logo-icon">AI</div>
      <span>网站名称</span>
    </div>
    <div class="nav-links">
      <a href="#section1">导航1</a>
      <a href="#section2">导航2</a>
      <a href="#section3">导航3</a>
    </div>
    <div class="nav-actions">
      <button class="theme-toggle" id="themeToggle" aria-label="切换主题"></button>
    </div>
  </div>
</nav>
```

### 带字体大小调节的导航栏
```html
<div class="nav-actions">
  <div class="font-size-control">
    <button class="font-btn" data-size="small">A-</button>
    <button class="font-btn" data-size="medium">A</button>
    <button class="font-btn" data-size="large">A+</button>
  </div>
  <button class="theme-toggle" id="themeToggle"></button>
</div>
```

---

## Hero区域模块

### 基础Hero
```html
<section class="hero" id="hero">
  <div class="hero-content">
    <h1>主标题第一行<br><span class="highlight">高亮文字</span></h1>
    <p class="subtitle">副标题描述文字</p>
    <div class="hero-stats">
      <!-- 统计卡片 -->
    </div>
  </div>
</section>
```

### 带背景图的Hero
```html
<section class="hero hero-with-bg" style="background-image:url('背景图.jpg');background-size:cover;background-position:center;">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <!-- 内容 -->
  </div>
</section>
```
```css
.hero-overlay{
  position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(16,13,10,.7),rgba(16,13,10,.9));
}
```

---

## 统计卡片模块

### 四列统计卡片
```html
<div class="hero-stats">
  <div class="stat-card">
    <span class="num">6</span>
    <span class="label">个月完整周期</span>
  </div>
  <div class="stat-card">
    <span class="num">4</span>
    <span class="label">阶段里程碑</span>
  </div>
  <div class="stat-card">
    <span class="num">3</span>
    <span class="label">高质量项目</span>
  </div>
  <div class="stat-card">
    <span class="num">9</span>
    <span class="label">核心能力章节</span>
  </div>
</div>
```

### 带图标的统计卡片
```html
<div class="stat-card">
  <div class="stat-icon">✅</div>
  <span class="num">0/46</span>
  <span class="label">已完成任务</span>
</div>
```

---

## 功能卡片网格模块

### 基础卡片网格
```html
<div class="card-grid">
  <div class="card reveal">
    <div class="card-icon">🚀</div>
    <h3>卡片标题</h3>
    <p>卡片描述文字，说明这个卡片的核心内容和价值。</p>
  </div>
  <div class="card reveal">
    <div class="card-icon">💡</div>
    <h3>卡片标题</h3>
    <p>卡片描述文字</p>
  </div>
  <div class="card reveal">
    <div class="card-icon">🎯</div>
    <h3>卡片标题</h3>
    <p>卡片描述文字</p>
  </div>
</div>
```

### 带优先级标签的卡片
```html
<div class="card priority-card">
  <div class="priority-badge p0">P0</div>
  <div class="card-icon">🔥</div>
  <h3>高优先级任务</h3>
  <p>必须完成的核心任务</p>
</div>
```
```css
.priority-badge{
  display:inline-block;padding:4px 10px;border-radius:6px;
  font-size:12px;font-weight:700;margin-bottom:12px;
}
.priority-badge.p0{background:rgba(255,80,80,.2);color:#ff5050}
.priority-badge.p1{background:rgba(255,154,46,.2);color:#ff9a2e}
.priority-badge.p2{background:rgba(79,196,180,.2);color:#4fc4b4}
```

---

## 时间线模块

```html
<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <div class="timeline-date">第1个月</div>
      <h4>阶段标题</h4>
      <p>阶段描述内容</p>
    </div>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <div class="timeline-date">第2个月</div>
      <h4>阶段标题</h4>
      <p>阶段描述内容</p>
    </div>
  </div>
</div>
```
```css
.timeline{position:relative;padding-left:32px}
.timeline::before{
  content:'';position:absolute;left:8px;top:0;bottom:0;
  width:2px;background:var(--line);
}
.timeline-item{position:relative;margin-bottom:32px}
.timeline-dot{
  position:absolute;left:-28px;top:4px;
  width:14px;height:14px;border-radius:50%;
  background:var(--accent);border:3px solid var(--bg);
}
.timeline-date{font-size:13px;color:var(--accent);font-weight:600;margin-bottom:4px}
```

---

## 进度条模块

### 基础进度条
```html
<div class="progress-bar">
  <div class="progress-label">
    <span>任务名称</span>
    <span>75%</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" style="width:75%"></div>
  </div>
</div>
```
```css
.progress-bar{margin-bottom:16px}
.progress-label{display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px}
.progress-track{
  height:8px;background:var(--line);border-radius:4px;overflow:hidden;
}
.progress-fill{
  height:100%;background:linear-gradient(90deg,var(--accent),var(--accent-third));
  border-radius:4px;transition:width .6s var(--ease);
}
```

### 环形进度
```html
<div class="circle-progress">
  <svg viewBox="0 0 100 100">
    <circle class="circle-bg" cx="50" cy="50" r="40"></circle>
    <circle class="circle-fill" cx="50" cy="50" r="40" style="stroke-dashoffset:100"></circle>
  </svg>
  <div class="circle-text">75%</div>
</div>
```

---

## 表格模块

```html
<div class="table-container">
  <table class="data-table">
    <thead>
      <tr>
        <th>列标题1</th>
        <th>列标题2</th>
        <th>列标题3</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>数据1</td>
        <td>数据2</td>
        <td>数据3</td>
      </tr>
      <tr>
        <td>数据4</td>
        <td>数据5</td>
        <td>数据6</td>
      </tr>
    </tbody>
  </table>
</div>
```
```css
.table-container{overflow-x:auto;border-radius:var(--radius-md)}
.data-table{width:100%;border-collapse:collapse}
.data-table th{
  background:var(--bg-secondary);padding:14px 16px;text-align:left;
  font-weight:600;font-size:14px;border-bottom:2px solid var(--line);
}
.data-table td{
  padding:12px 16px;border-bottom:1px solid var(--line);font-size:14px;
}
.data-table tr:hover{background:var(--bg-glass)}
```

---

## 代码块模块

```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">JavaScript</span>
    <button class="copy-btn">复制</button>
  </div>
  <pre><code>const hello = "Hello, World!";
console.log(hello);</code></pre>
</div>
```
```css
.code-block{
  background:#1a1a2e;border-radius:var(--radius-md);overflow:hidden;
  border:1px solid rgba(255,255,255,.1);
}
.code-header{
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 16px;background:rgba(255,255,255,.05);
  border-bottom:1px solid rgba(255,255,255,.1);
}
.code-lang{font-size:13px;color:#888;font-family:monospace}
.copy-btn{
  background:rgba(255,255,255,.1);border:none;color:#ccc;
  padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px;
}
.code-block pre{padding:16px;overflow-x:auto}
.code-block code{font-family:"Fira Code",monospace;font-size:14px;color:#e0e0e0}
```

---

## 引用/提示框模块

### 信息提示
```html
<div class="alert alert-info">
  <span class="alert-icon">💡</span>
  <div class="alert-content">
    <strong>提示</strong>
    <p>这是一条信息提示内容。</p>
  </div>
</div>
```

### 警告提示
```html
<div class="alert alert-warning">
  <span class="alert-icon">⚠️</span>
  <div class="alert-content">
    <strong>注意</strong>
    <p>这是一条警告提示内容。</p>
  </div>
</div>
```

```css
.alert{
  display:flex;gap:12px;padding:16px 20px;border-radius:var(--radius-md);
  margin-bottom:16px;border-left:4px solid;
}
.alert-info{background:rgba(79,196,180,.1);border-color:#4fc4b4}
.alert-warning{background:rgba(255,154,46,.1);border-color:#ff9a2e}
.alert-error{background:rgba(255,80,80,.1);border-color:#ff5050}
.alert-success{background:rgba(79,196,180,.1);border-color:#4fc4b4}
.alert-icon{font-size:20px;flex-shrink:0}
.alert-content strong{display:block;margin-bottom:4px}
.alert-content p{font-size:14px;color:var(--text-secondary);margin:0}
```

---

## 标签/徽章模块

```html
<span class="badge badge-primary">主要</span>
<span class="badge badge-success">完成</span>
<span class="badge badge-warning">进行中</span>
<span class="badge badge-danger">紧急</span>
```
```css
.badge{
  display:inline-block;padding:4px 10px;border-radius:6px;
  font-size:12px;font-weight:600;
}
.badge-primary{background:rgba(255,154,46,.2);color:var(--accent)}
.badge-success{background:rgba(79,196,180,.2);color:var(--accent-secondary)}
.badge-warning{background:rgba(230,180,92,.2);color:#e6b45c}
.badge-danger{background:rgba(232,121,160,.2);color:var(--accent-fourth)}
```

---

## 按钮模块

### 主要按钮
```html
<button class="btn btn-primary">主要按钮</button>
<button class="btn btn-secondary">次要按钮</button>
<button class="btn btn-ghost">幽灵按钮</button>
```
```css
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  padding:12px 24px;border-radius:var(--radius-sm);font-size:15px;
  font-weight:600;border:none;cursor:pointer;transition:all .25s var(--ease);
}
.btn-primary{background:var(--accent);color:#fff}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(255,154,46,.3)}
.btn-secondary{background:var(--bg-glass);color:var(--text);border:1px solid var(--line)}
.btn-ghost{background:transparent;color:var(--text-secondary)}
.btn-ghost:hover{color:var(--text);background:var(--line)}
```

---

## 表单模块

```html
<div class="form-group">
  <label class="form-label">输入框标签</label>
  <input type="text" class="form-input" placeholder="请输入...">
</div>
<div class="form-group">
  <label class="form-label">下拉选择</label>
  <select class="form-select">
    <option>选项1</option>
    <option>选项2</option>
  </select>
</div>
<div class="form-group">
  <label class="form-label">文本域</label>
  <textarea class="form-textarea" rows="4" placeholder="请输入..."></textarea>
</div>
```
```css
.form-group{margin-bottom:20px}
.form-label{display:block;font-size:14px;font-weight:600;margin-bottom:8px}
.form-input,.form-select,.form-textarea{
  width:100%;padding:12px 16px;border-radius:var(--radius-sm);
  background:var(--bg-glass);border:1px solid var(--line);color:var(--text);
  font-size:14px;transition:border-color .25s;
}
.form-input:focus,.form-select:focus,.form-textarea:focus{
  outline:none;border-color:var(--accent);
}
```

---

## 页脚模块

```html
<footer class="footer">
  <div class="footer-content">
    <div class="footer-logo">网站名称</div>
    <div class="footer-links">
      <a href="#about">关于</a>
      <a href="#contact">联系</a>
      <a href="#privacy">隐私</a>
    </div>
    <p class="footer-copyright">© 2024 网站名称. All rights reserved.</p>
  </div>
</footer>
```
```css
.footer{
  padding:48px 32px;border-top:1px solid var(--line);
  color:var(--text-secondary);font-size:14px;text-align:center;
}
.footer-links{display:flex;justify-content:center;gap:24px;margin:16px 0}
.footer-links a{color:var(--text-secondary);transition:color .25s}
.footer-links a:hover{color:var(--accent)}
```

---

## 进阶效果模块

### 3D Tilt卡片
```html
<div class="tilt-card">
  <div class="tilt-shine"></div>
  <!-- 卡片内容 -->
</div>
```
```css
.tilt-card{
  transform-style:preserve-3d;perspective:1000px;
  transition:transform .3s var(--ease);
}
.tilt-shine{
  position:absolute;inset:0;border-radius:inherit;
  background:radial-gradient(circle at var(--mouse-x,50%) var(--mouse-y,50%),
    rgba(255,255,255,.1),transparent 60%);
  pointer-events:none;opacity:0;transition:opacity .3s;
}
.tilt-card:hover .tilt-shine{opacity:1}
```

### 点击波纹
```javascript
document.addEventListener('click', (e) => {
  const ripple = document.createElement('div');
  ripple.className = 'click-ripple';
  ripple.style.left = e.clientX + 'px';
  ripple.style.top = e.clientY + 'px';
  document.body.appendChild(ripple);
  setTimeout(() => ripple.remove(), 800);
});
```
```css
.click-ripple{
  position:fixed;width:20px;height:20px;border-radius:50%;
  background:rgba(255,154,46,.4);pointer-events:none;z-index:9999;
  transform:translate(-50%,-50%);animation:rippleExpand .8s ease-out forwards;
}
@keyframes rippleExpand{
  to{width:200px;height:200px;opacity:0}
}
```

### 数字计数动画
```javascript
function animateCountUp(el, target, duration = 1500) {
  const start = 0;
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(start + (target - start) * easeProgress);
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
```
