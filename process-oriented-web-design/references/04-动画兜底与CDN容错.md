# 动画兜底与 CDN 容错

## 为什么不能加 CSS `!important`

原文件的入场动画机制：
```css
.js .rv{opacity:0;transform:translateY(20px)}
.js .rv.in{opacity:1;transform:none;transition:opacity .8s var(--ease),transform .8s var(--ease)}
```
GSAP/IntersectionObserver 在元素进入视口时加 `.in` 类，触发过渡动画。

**错误做法**：
```css
.js .rv{opacity:1!important;transform:none!important;transition:none!important}
```
这会：
- 永久禁用入场动画（用户要的就是这个动画）
- 破坏 GSAP 的时间线编排
- 导致所有元素瞬间出现，没有层次感

## 正确做法：JS setTimeout 智能兜底

```js
/* 放在主 </script> 前 */
setTimeout(function(){
  document.querySelectorAll('.rv,.rv-nl,.wk-in,.wk-head.rv-nl').forEach(function(e){
    e.classList.add('in');
  });
},800);
```

工作原理：
- GSAP 正常加载（用户浏览器有加速器）→ 它会在 800ms 前加 `.in`，动画正常播放
- GSAP CDN 失败/慢 → 800ms 后兜底加 `.in`，内容显示（无动画但可见）
- 不破坏任何 CSS，不影响用户浏览器里的动画

## CDN 依赖

典型依赖：
```html
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js"}}</script>
```

- jsdelivr 在国内可能慢/失败
- 用户有加速器时正常
- headless Chrome 截图时 CDN 不加载，所以：
  - 截图看不到 WebGL 背景（正常）
  - GSAP 不跑，`.rv` 元素初始 opacity:0（靠兜底显示）
  - **不要因此"修复"CDN 或改动画逻辑**

## 验证方法

不要用 headless 截图判断"3D 效果是否正常"——headless 本来就不加载 CDN。让用户在自己浏览器里 `Ctrl+Shift+R` 强制刷新看。

验证 JS 语法：
```powershell
python -c "import re,io; s=io.open('文件.html',encoding='utf-8').read(); b=max(re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>',s,re.S),key=len); io.open('_m.js','w',encoding='utf-8').write(b)"
node --check _m.js
```

## localStorage 进度隔离

换数据时必须换 key：
```python
s = s.replace('"focus35-v1"', '"ragstudy-v1"')
s = s.replace('"focus35-notes"', '"ragstudy-notes"')
s = s.replace('"focus35-links"', '"ragstudy-links"')
```
否则用户在旧数据上的打卡记录会残留，导致进度错乱。
