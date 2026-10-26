# 使用示例

## 示例 1：把求职冲刺看板改成学习看板

**输入**：用户有一个 `项目进程设计.html`（35 周求职冲刺，带 WebGL 八芒星），要改成 29 周 RAG+Agent 学习看板。

**步骤**：
1. `Copy-Item` 复制为 `学习作战看板.html`
2. Grep 定位 `const START=new Date(2026,8,28)`
3. 替换为 `new Date(2026,9,12)`
4. 替换 PHASES 7 个阶段名
5. 用 Python 脚本生成新 BASE_PLAN（29 周，每天 8h，周日 4h）
6. 替换 renderRhythm() 为 SVG 折线图
7. 换 localStorage key `focus35-*` → `ragstudy-*`
8. 加 800ms setTimeout 兜底

**输出**：`学习作战看板.html`，WebGL 背景/动画完整保留，数据全换。

## 示例 2：修复 CDN 白屏

**输入**：用户反馈"打开网页全黑"。

**步骤**：
1. 检查是否加了 CSS `!important`（如果有，删掉）
2. 在主 `</script>` 前加：
```js
setTimeout(function(){
  document.querySelectorAll('.rv,.rv-nl,.wk-in').forEach(e=>e.classList.add('in'));
},800);
```
3. 用户刷新即可看到内容

## 示例 3：柱状图改折线图

**输入**：原 renderBars() 画柱状图，要改成玻璃风折线图。

**步骤**：按 `references/03` 的模板替换整个 renderRhythm 函数，不动其他 render 函数。
