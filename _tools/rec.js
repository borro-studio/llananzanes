// Vídeo de recorrido: node rec.js <ancho> <alto> <dpr> <dirFrames> [pxPorFrame]
const p=require('puppeteer-core');
(async()=>{
 const [,,w,h,dpr,dir,spd]=process.argv; const mobile=+w<700;
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
 const pg=await b.newPage();
 await pg.setViewport({width:+w,height:+h,deviceScaleFactor:+dpr,isMobile:mobile,hasTouch:mobile});
 await pg.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
 await pg.goto('http://localhost:4320/',{waitUntil:'networkidle0'});
 await pg.evaluate(()=>document.documentElement.style.scrollBehavior='auto');
 let n=0; const shot=async()=>pg.screenshot({path:`${dir}/f${String(n++).padStart(5,'0')}.jpg`,type:'jpeg',quality:82});
 const t0=Date.now(); while(Date.now()-t0<2600){await shot();}
 const H=await pg.evaluate(()=>document.documentElement.scrollHeight-innerHeight);
 let y=0; const V=+spd||14;
 while(y<H){
   const v=Math.min(1,(y+1)/300,(H-y+1)/300)*V+2;
   y=Math.min(H,y+v); await pg.evaluate(y=>scrollTo(0,y),y);
   await new Promise(r=>setTimeout(r,16)); await shot();
 }
 for(let i=0;i<40;i++) await shot();
 console.log(n,H); await b.close();
})();
