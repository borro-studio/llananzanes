const p=require('puppeteer-core');(async()=>{const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});const pg=await b.newPage();
await pg.setViewport({width:390,height:844,deviceScaleFactor:2,isMobile:true,hasTouch:true});
await pg.goto('http://localhost:4320/',{waitUntil:'networkidle0'});await new Promise(r=>setTimeout(r,3000));
const r=await pg.evaluate(()=>{const q=s=>document.querySelector(s);const cs=e=>getComputedStyle(e);const R=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]};
const sp=q('.hero h1 .line > span'),ln=q('.hero h1 .line'),h=q('.hero h1'),inner=q('.hero__inner'),side=q('.hero__side');
return {inner:R(inner),innerCols:cs(inner).gridTemplateColumns,innerDisp:cs(inner).display,h1:R(h),h1color:cs(h).color,h1op:cs(h).opacity,line:R(ln),lineOv:cs(ln).overflow,span:R(sp),spanTr:cs(sp).transform,spanAnim:cs(sp).animationName,side:R(side),sideCol:cs(side).gridColumn,h1Col:cs(h).gridColumn+' / '+cs(h).gridRow,h1pos:cs(h).position+' z'+cs(h).zIndex, media:document.querySelector('.hero__media')&&cs(document.querySelector('.hero__media')).zIndex+' '+cs(document.querySelector('.hero__media')).position, innerPos:cs(inner).position+' z'+cs(inner).zIndex}});
console.log(JSON.stringify(r,null,1));await b.close()})()
