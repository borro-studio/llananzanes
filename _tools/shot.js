// Capturas de la vista previa: node shot.js <url> <ancho> <alto> <prefijo> <selector@offset|y>...
const p=require('puppeteer-core');
(async()=>{
 const [,,url,w,h,out,...ys]=process.argv;
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
 const pg=await b.newPage(); await pg.setViewport({width:+w,height:+h});
 await pg.goto(url,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,2500));
 let i=0;
 for(const y of ys){
   await pg.evaluate(y=>{const [sel,f]=y.split('@'); const e=isNaN(sel)?document.querySelector(sel):null; const top=e?e.getBoundingClientRect().top+scrollY+(+f||0):+sel; document.documentElement.style.scrollBehavior='auto'; scrollTo(0,top)},y);
   await new Promise(r=>setTimeout(r,2200));
   await pg.screenshot({path:`${out}-${String(i++).padStart(2,'0')}.jpg`,type:'jpeg',quality:70});
 }
 await b.close();
})();
