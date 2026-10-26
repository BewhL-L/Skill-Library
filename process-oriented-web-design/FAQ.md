# FAQ

## 为什么不能直接在原文件上改？

原文件是你的视觉资产。直接改容易误删 three.js/GSAP 初始化代码。复制副本改，原件保留回滚能力。

## 为什么打开网页全黑？

GSAP CDN 没加载。不要加 CSS `!important`，用 800ms setTimeout 兜底（见 references/04）。用户有加速器时 CDN 正常加载。

## 为什么折线图拉伸变形？

用了 `preserveAspectRatio="none"`。删掉，改用 `height:auto`。

## headless 截图为什么看不到 3D 背景？

headless Chrome 不加载 CDN（three.js/GSAP）。这是正常的，用户浏览器里有加速器就能看到。不要因此"修复"。

## 换了数据后旧打卡记录还在？

localStorage key 没换。把 `focus35-*` 改成 `ragstudy-*` 或你的项目名。

## 文字发虚怎么办？

加 `-moz-osx-font-smoothing:grayscale` 和 `text-rendering:optimizeLegibility`（见 references/05）。Windows 缩放用 100% 或 150%。
