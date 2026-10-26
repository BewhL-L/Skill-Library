# 快速开始

5 分钟把旧看板改成你的。

## 1. 复制原文件

```powershell
Copy-Item "项目进程设计.html" "我的看板.html"
```

## 2. 定位数据位置

```powershell
Grep -n "const START|const END|const PHASES|const BASE_PLAN|todayPos|<h1>|pl-node" "我的看板.html"
```

## 3. 替换数据

按 `references/02-数据驱动替换清单.md` 的表格，写 Python 脚本替换：
- START/END 日期
- PHASES 阶段名
- BASE_PLAN 任务数组
- todayPos 硬编码
- localStorage key

## 4. 替换折线图

按 `references/03-SVG玻璃风图表规范.md`，替换 `renderRhythm()` 函数。

## 5. 加兜底

在主 `</script>` 前加 800ms setTimeout 兜底（见 `references/04`）。

## 6. 验证

```powershell
# JS 语法
python -c "import re,io; s=io.open('我的看板.html',encoding='utf-8').read(); b=max(re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>',s,re.S),key=len); io.open('_m.js','w',encoding='utf-8').write(b)"
node --check _m.js
```

浏览器打开 `我的看板.html`，Ctrl+Shift+R 强制刷新。
