// Aviso de nieve: no sale durante la presentación; sale al acabar la locución o al bajar; no vuelve tras cerrarlo
const p=require('puppeteer-core');
const W=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const U=process.env.URL||'http://localhost:4320/', out=process.argv[2];
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--mute-audio','--autoplay-policy=no-user-gesture-required']});
 const vis=pg=>pg.evaluate(()=>{const s=document.querySelector('.snowcard');return !s.hidden&&s.classList.contains('is-on')});
 for (const [dev,vp] of [['escritorio',{width:1440,height:900}],['movil',{width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:2}]]){
  // 1) con sonido: espera a la locución
  let pg=await b.newPage(); await pg.setViewport(vp); const errs=[]; pg.on('pageerror',e=>errs.push(String(e)));
  await pg.goto(U,{waitUntil:'networkidle0'}); await pg.click('.intro__enter');
  await W(8000); const a8=await vis(pg);
  let t=8; while(!(await vis(pg)) && t<40){ await W(1000); t++; }
  const loc=await pg.evaluate(()=>[...document.querySelectorAll('audio')].length);
  if(out) { await W(1200); await pg.screenshot({path:`${out}-${dev}.jpg`,type:'jpeg',quality:80}); }
  await pg.click('.snowcard__x'); await W(900); const cerrado=!(await vis(pg));
  await pg.reload({waitUntil:'networkidle0'}); await pg.click('.intro__mute'); await W(3000);
  await pg.evaluate(()=>scrollTo(0,innerHeight)); await W(1500); const tras=await vis(pg);
  await pg.close();
  // 2) sin sonido + bajar (sesión nueva)
  const ctx=await b.createBrowserContext(); pg=await ctx.newPage(); await pg.setViewport(vp);
  await pg.goto(U,{waitUntil:'networkidle0'}); await pg.click('.intro__mute'); await W(3000); const a3=await vis(pg);
  await pg.evaluate(()=>scrollTo(0,innerHeight)); await W(1500); const bajar=await vis(pg);
  await ctx.close();
  console.log(`[${dev}] con sonido: oculto a los 8 s ${!a8}, sale hacia el s ${t} · cerrado ${cerrado} · no vuelve tras recargar ${!tras} | sin sonido: oculto a los 3 s ${!a3}, sale al bajar ${bajar}`, errs.length?errs:'sin errores');
 }
 await b.close();
})();
