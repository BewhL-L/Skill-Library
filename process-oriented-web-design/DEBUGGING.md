# 调试指南

## 白屏/全黑

1. 检查是否加了 CSS `.rv{opacity:1!important}` —— 删掉
2. 检查 800ms setTimeout 兜底是否加了
3. 检查浏览器控制台是否有 CDN 加载错误（jsdelivr）

## 图表拉伸变形

检查 SVG 是否有 `preserveAspectRatio="none"` —— 删掉。

## JS 报错

```powershell
python -c "import re,io; s=io.open('文件.html',encoding='utf-8').read(); b=max(re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>',s,re.S),key=len); io.open('_m.js','w',encoding='utf-8').write(b)"
node --check _m.js
```

## 替换 MISS

先 `Grep` 原文件实际文字，不要凭记忆写匹配串。
