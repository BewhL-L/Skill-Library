# SVG 玻璃风图表规范

## 核心原则

- **不拉伸**：不用 `preserveAspectRatio="none"`，用 `height:auto` 保持比例
- **居中**：`max-width:560px; margin:0 auto`
- **克制**：网格线只画 2/4/6/8h 四条，不喧宾夺主
- **平滑**：catmull-rom 转 cubic bezier，不要硬折线

## 折线图模板

```js
function renderRhythm(){
  const planH = wk.days.map(d=>d.reduce((a,tt)=>a+tt[1],0));  // 计划学时
  const doneH = wk.days.map((_,di)=>dayStat(wi,di).doneH);    // 实际学时
  const maxH = 9;  // 固定上限，刻度对齐
  const W=600,H=210,padL=28,padR=16,padT=20,padB=26;
  const iw=W-padL-padR, ih=H-padT-padB;
  const X=i=>padL+(iw*i/6);
  const Y=h=>padT+ih-(h/maxH)*ih;

  // catmull-rom -> bezier 平滑曲线
  function smooth(pts){
    if(pts.length<3) return "M"+pts.map(p=>p[0].toFixed(1)+","+p[1].toFixed(1)).join(" L");
    let d="M"+pts[0][0].toFixed(1)+","+pts[0][1].toFixed(1);
    for(let i=0;i<pts.length-1;i++){
      const p0=pts[i-1]||pts[i], p1=pts[i], p2=pts[i+1], p3=pts[i+2]||p2;
      const c1x=p1[0]+(p2[0]-p0[0])/6, c1y=p1[1]+(p2[1]-p0[1])/6;
      const c2x=p2[0]-(p3[0]-p1[0])/6, c2y=p2[1]-(p3[1]-p1[1])/6;
      d+=" C"+c1x.toFixed(1)+","+c1y.toFixed(1)+" "+c2x.toFixed(1)+","+c2y.toFixed(1)+" "+p2[0].toFixed(1)+","+p2[1].toFixed(1);
    }
    return d;
  }

  const planPts=planH.map((h,i)=>[X(i),Y(h)]);
  const donePts=doneH.map((h,i)=>[X(i),Y(h)]);
  const planPath=smooth(planPts);
  const donePath=smooth(donePts);
  const baseY=padT+ih;
  const areaPath=donePath+" L"+X(6).toFixed(1)+","+baseY+" L"+X(0).toFixed(1)+","+baseY+" Z";

  let svg='<svg viewBox="0 0 '+W+' '+H+'" style="display:block;margin:4px auto 0;width:100%;height:auto;overflow:visible">';
  svg+='<defs>'
    +'<linearGradient id="rgFill" x1="0" y1="0" x2="0" y2="1">'
    +'<stop offset="0%" stop-color="#e06391" stop-opacity="0.28"/>'
    +'<stop offset="60%" stop-color="#e06391" stop-opacity="0.08"/>'
    +'<stop offset="100%" stop-color="#e06391" stop-opacity="0"/></linearGradient>'
    +'<filter id="rgGlow" x="-20%" y="-40%" width="140%" height="180%">'
    +'<feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    +'</defs>';

  // 网格线 2/4/6/8h
  [2,4,6,8].forEach(h=>{
    const gy=Y(h);
    svg+='<line x1="'+padL+'" y1="'+gy+'" x2="'+(W-padR)+'" y2="'+gy+'" stroke="rgba(255,255,255,.06)"/>';
    svg+='<text x="'+(padL-5)+'" y="'+(gy+3)+'" text-anchor="end" fill="rgba(255,255,255,.32)" font-size="9">'+h+'h</text>';
  });

  svg+='<path d="'+areaPath+'" fill="url(#rgFill)"/>';           // 渐变面积
  svg+='<path d="'+planPath+'" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="1.2" stroke-dasharray="3 4" stroke-linecap="round"/>';  // 计划虚线
  svg+='<path d="'+donePath+'" fill="none" stroke="#e06391" stroke-width="2.2" stroke-linecap="round" filter="url(#rgGlow)"/>';  // 实际发光线

  // 点：今天大粉点，其他小白点
  for(let i=0;i<7;i++){
    const isT=i===tp.di, cx=X(i), cy=Y(doneH[i]);
    if(isT){
      svg+='<circle cx="'+cx+'" cy="'+cy+'" r="9" fill="#e06391" opacity="0.18"/>';
      svg+='<circle cx="'+cx+'" cy="'+cy+'" r="5" fill="#e06391" stroke="#fff" stroke-width="2"/>';
    } else {
      svg+='<circle cx="'+cx+'" cy="'+cy+'" r="3.5" fill="rgba(255,255,255,.85)"/>';
    }
    svg+='<text x="'+cx+'" y="'+(cy-11)+'" text-anchor="middle" fill="rgba(255,255,255,.6)" font-size="11" font-weight="700">'+doneH[i]+'</text>';
    svg+='<text x="'+cx+'" y="'+(H-6)+'" text-anchor="middle" fill="rgba(255,255,255,.4)" font-size="10">'+DOW[i]+'</text>';
  }
  svg+='</svg>';
  box.innerHTML=svg;
}
```

## 参数速查

| 参数 | 值 | 原因 |
|------|-----|------|
| 实际线宽 | 2.2px | 清晰不细 |
| 计划线宽 | 1.2px 虚线 | 退到背景 |
| 发光 stdDeviation | 2.5 | 不糊，精确光晕 |
| 渐变三层 | 28%/8%/0% | 柔和消退 |
| 今天点 | r=9 光晕 + r=5 实心 | 焦点 |
| 其他点 | r=3.5 | 克制 |
| 网格线 | rgba(255,255,255,.06) | 几乎不可见 |
| Y轴上限 | 9h（8h 顶+余量） | 刻度对齐 |
