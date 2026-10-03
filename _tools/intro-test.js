// Pantalla de entrada: se ve al cargar, "Entrar" arranca el sonido y descubre la web
const p=require('puppeteer-core');
(async()=>{
 const out=process.argv[2], U=process.env.URL||'http://localhost:4320/';
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy=document-user-activation-required','--mute-audio']});
 for(const [name,vp] of [['movil',{width:390,height:844,isMobile:true,hasTouch:true}],['escritorio',{width:1440,height:900}]]){
  const pg=await b.newPage(); await pg.setViewport(vp); const errs=[]; pg.on('pageerror',e=>errs.push(String(e)));
  await pg.evaluateOnNewDocument(()=>{const O=window.Audio;window.__a=[];window.Audio=function(s){const a=new O(s);window.__a.push(a);return a}});
  const st=()=>pg.evaluate(()=>({intro:!!document.querySelector('.intro')&&getComputedStyle(document.querySelector('.intro')).visibility,entered:document.documentElement.classList.contains('entered'),scrollLock:getComputedStyle(document.body).overflow,sonido:document.querySelector('.sound').classList.contains('is-on'),audio:window.__a.map(a=>a.src.split('/').pop()+(a.paused?' PARADO':' sonando')+' t='+a.currentTime.toFixed(1)).join(', ')}));
  await pg.goto(U,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1200));
  const o={alCargar:await st()};
  if(out) await pg.screenshot({path:`${out}/intro-${name}.jpg`,type:'jpeg',quality:80});
  if(vp.isMobile) await pg.tap('.intro__enter'); else await pg.click('.intro__enter');
  await new Promise(r=>setTimeout(r,2600)); o.trasEntrar=await st();
  if(out) await pg.screenshot({path:`${out}/intro-${name}-dentro.jpg`,type:'jpeg',quality:80});
  await pg.reload({waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1000)); o.trasRecargar=(await st()).intro;
  if(vp.isMobile) await pg.tap('.intro__mute'); else await pg.click('.intro__mute'); await new Promise(r=>setTimeout(r,1800)); o.sinSonido=await st();
  await pg.goto(U+(U.includes('?')?'&':'?')+'nointro',{waitUntil:'networkidle0'}); o.nointro=(await st()).entered;
  console.log(name,JSON.stringify(o,null,0),errs.length?errs:'sin errores'); await pg.close();
 }
 await b.close();
})();
