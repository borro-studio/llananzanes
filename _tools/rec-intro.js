// Vídeo con pantalla de entrada: node rec-intro.js <ancho> <alto> <dpr> <dirFrames> <pxPorFrame>
// Imprime el fotograma del clic en "Entrar" para sincronizar el audio al montar.
const p=require('puppeteer-core'), fs=require('fs');
(async()=>{
 const [,,w,h,dpr,dir,spd]=process.argv; const mobile=+w<700, FPS=30;
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--mute-audio']});
 const pg=await b.newPage();
 await pg.setViewport({width:+w,height:+h,deviceScaleFactor:+dpr,isMobile:mobile,hasTouch:mobile});
 await pg.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
 await pg.goto('http://localhost:4320/',{waitUntil:'networkidle0'});
 await pg.evaluate(()=>document.documentElement.style.scrollBehavior='auto');
 let n=0; const name=i=>`${dir}/f${String(i).padStart(5,'0')}.jpg`;
 const shot=async()=>{await pg.screenshot({path:name(n),type:'jpeg',quality:82}); n++;};
 // tramo en tiempo real: se duplican fotogramas para que dure lo que duró de verdad
 const realtime=async(sec)=>{const t0=Date.now(), n0=n; while(Date.now()-t0<sec*1000){await shot(); const want=n0+Math.round((Date.now()-t0)/1000*FPS); while(n<want){fs.copyFileSync(name(n-1),name(n)); n++;}}};
 await realtime(2.5);
 const clickFrame=n;
 const btn=await pg.$('.intro__enter'); const bb=await btn.boundingBox();
 if(mobile) await pg.touchscreen.tap(bb.x+bb.width/2,bb.y+bb.height/2); else await pg.mouse.click(bb.x+bb.width/2,bb.y+bb.height/2);
 await realtime(4);
 const H=await pg.evaluate(()=>document.documentElement.scrollHeight-innerHeight);
 let y=0; const V=+spd;
 while(y<H){const v=Math.min(1,(y+1)/300,(H-y+1)/300)*V+2; y=Math.min(H,y+v); await pg.evaluate(y=>scrollTo(0,y),y); await new Promise(r=>setTimeout(r,16)); await shot();}
 for(let i=0;i<45;i++){fs.copyFileSync(name(n-1),name(n)); n++;}
 console.log(JSON.stringify({frames:n,clickFrame,clickMs:Math.round(clickFrame/FPS*1000)})); await b.close();
})();
