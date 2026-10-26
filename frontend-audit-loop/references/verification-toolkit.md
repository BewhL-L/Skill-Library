# 验证工具箱：探针 / 断言 / 截图模板

原则：**能断言的不靠截图，能读 DOM 的不靠读图**。以下模板均为可直接落地的最小实现（Edge/Chrome headless + Node jsdom）。

## 1. 文档级溢出探针（iframe 真实视口法）

headless 浏览器有最小视口钳制（常见 492px），请求 390 会按 492 布局再缩放出"伪裁切"。用 iframe 在任意大外窗内构造真实小视口：

```html
<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="margin:0">
<iframe id="f" style="width:390px;height:900px;border:0"></iframe>
<div id="out"></div>
<script>
const f=document.getElementById('f');
f.src=encodeURI('file:///绝对路径/目标页.html');
f.onload=()=>setTimeout(()=>{
  try{
    const doc=f.contentDocument, de=doc.documentElement, bad=[];
    doc.querySelectorAll('*').forEach(el=>{
      const r=el.getBoundingClientRect();
      if(r.width>0 && r.right > de.clientWidth+1){
        let cn=el.className; if(cn && cn.baseVal!==undefined) cn=cn.baseVal; /* SVG 陷阱 */
        bad.push(el.tagName+'.'+(cn||'')+' right='+Math.round(r.right));
      }
    });
    document.getElementById('out').textContent=
      'ICW='+de.clientWidth+' ISW='+de.scrollWidth+' BAD='+bad.length+' :: '+bad.slice(0,10).join(' | ');
  }catch(e){document.getElementById('out').textContent='ERR '+e.message;}
}, 3000);
</script></body></html>
```

运行与取数：

```bash
msedge --headless=old --disable-gpu --no-sandbox --allow-file-access-from-files \
  --window-size=492,900 --virtual-time-budget=8000 \
  --dump-dom "file:///…/probe.html" | grep -o 'ICW=[^<]*'
```

判定：`ISW === ICW` → 文档级零溢出；BAD>0 时逐个归因（横滑容器内 / fixed 装饰层 = 合法越界）。

要点：
- `--allow-file-access-from-files` 必须，否则 file:// iframe 同源被禁读不到 contentDocument
- `--virtual-time-budget` 必须，否则截图/导出发生在 3 秒定时器前，输出恒空
- 读探针结果用 `--dump-dom`，**不要用截图读文本**（时机不稳）

## 2. 双主题截图（含手动主题注入）

headless 无法模拟 `prefers-color-scheme`，用包装页在加载后手动置主题：

```html
<iframe id="f" style="width:492px;height:1100px;border:0"></iframe>
<script>
f.onload=()=>setTimeout(()=>{
  f.contentDocument.documentElement.setAttribute('data-theme','light');
},300);
</script>
```

截图矩阵建议：`1440/1200/1024/492 × 深/浅`，重点看跨列空洞、白压白、玻璃换肤。

## 3. 主题块令牌泄漏 diff（shell 一行）

```bash
F=目标页.html
extract(){ sed -n "$2" "$F" | grep -o -- '--[a-z0-9-]*:' | sort -u; }
diff <(extract '/@media (prefers-color-scheme: light){/,/^}/p') \
     <(extract '/:root\[data-theme="dark"\]{/,/^}/p')
```

输出非空即泄漏——媒体查询块声明了、手动块漏声明的令牌，会在"系统主题 × 手动主题"交叉组合下串色。手动深/浅两块分别与媒体块 diff，要求为空。

## 4. jsdom 交互冒烟（断言模板要点）

环境：Node + jsdom（`NODE_PATH` 指向既有 node_modules；`JSDOM.fromFile` 配 `url:'http://localhost/'` 启用 localStorage，`runScripts:'dangerously'`）。

骨架：

```js
const dom = await JSDOM.fromFile(page, {url:'http://localhost/', runScripts:'dangerously', pretendToBeVisual:true});
window.confirm = () => true;                 // 危险操作放行
await new Promise(r=>setTimeout(r,300));     // 等 init
// 断言 T(name, cond) 计数输出；checkbox 用 box.focus(); box.click();
```

必测清单：渲染数量 / 今日定位 / 写操作→持久化→刷新 / 重刷不重放动画（重刷产物无 `.rv`）/ 焦点恢复 / 危险操作拦截 / 主题切换与 meta 同步 / 日期越界 clamp。

已知伪影（勿当 bug 修）：
- jsdom 点击不聚焦 → activeElement 停在 body，焦点断言需先显式 `.focus()`
- jsdom 无 `matchMedia` → 页面代码须有 `window.matchMedia &&` 守卫，否则脚本报错
- `window.scrollTo` "Not implemented" 警告可忽略
- file:// 直载 localStorage 抛 SecurityError → 一律用 `url:'http://localhost/'`

## 5. headless 命令速查

```bash
# 截图（注意视口钳制，读图只看布局不看像素级测量）
msedge --headless=old --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1440,1000 --user-data-dir=<临时目录> \
  --screenshot=out.png "file:///目标页.html"

# 读 DOM 文本（配合页面内探针/定时器）
… --virtual-time-budget=8000 --dump-dom "URL" | grep -o '标记[^<]*'
```

- `--headless=old` 优先：new headless 曾出现不出图问题
- 每次 run 用独立 `--user-data-dir`，避免缓存串味
- 中文/空格路径用 URL 编码（encodeURI 或手写 %XX）
