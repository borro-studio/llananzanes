// Tarjeta de temporada de nieve: aparece tras entrar, se cierra y no vuelve en la misma visita
const p=require('puppeteer-core');
(async()=>{
 const U=process.env.URL||'http://localhost:4320/', out=process.argv[2];
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--mute-audio']});
 for (const [dev,vp] of [['escritorio',{width:1440,height:900}],['movil',{width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:2}]]){
  const pg=await b.newPage(); await pg.setViewport(vp); const errs=[]; pg.on('pageerror',e=>errs.push(String(e)));
  await pg.goto(U,{waitUntil:'networkidle0'});
  const antes=await pg.evaluate(()=>document.querySelector('.snowcard').hidden);
  await pg.click('.intro__mute'); await new Promise(r=>setTimeout(r,6500));
  const visible=await pg.evaluate(()=>{const s=document.querySelector('.snowcard');return !s.hidden&&s.classList.contains('is-on')});
  if(out) await pg.screenshot({path:`${out}-${dev}.jpg`,type:'jpeg',quality:80});
  await pg.click('.snowcard__x'); await new Promise(r=>setTimeout(r,900));
  const cerrada=await pg.evaluate(()=>document.querySelector('.snowcard').hidden);
  await pg.reload({waitUntil:'networkidle0'}); await pg.click('.intro__mute'); await new Promise(r=>setTimeout(r,6500));
  const tras=await pg.evaluate(()=>document.querySelector('.snowcard').hidden);
  console.log(`[${dev}] oculta antes de entrar: ${antes} · visible a los 6 s: ${visible} · cerrada: ${cerrada} · oculta tras recargar: ${tras}`, errs.length?errs:'sin errores');
  await pg.close();
 }
 await b.close();
})();
