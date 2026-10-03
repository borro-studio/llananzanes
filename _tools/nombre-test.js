// Pantalla de entrada con nombre: saludo correcto, audios sincronizados, vídeo de portada y texto de saludo
const p=require('puppeteer-core');
(async()=>{
 const out=process.argv[2], U=process.env.URL||'http://localhost:4320/';
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy=document-user-activation-required','--mute-audio']});
 const casos=[['movil','Beñat',{width:390,height:844,isMobile:true,hasTouch:true}],['escritorio','ioana',{width:1440,height:900}],['escritorio','Zuriñe',{width:1440,height:900}],['movil','',{width:390,height:844,isMobile:true,hasTouch:true}]];
 for(const [dev,nombre,vp] of casos){
  const pg=await b.newPage(); await pg.setViewport(vp); const errs=[]; pg.on('pageerror',e=>errs.push(String(e))); pg.on('requestfailed',r=>errs.push('FALLO '+r.url().split('/').slice(-2).join('/')));
  await pg.evaluateOnNewDocument(()=>{const O=window.Audio;window.__a=[];window.Audio=function(s){const a=new O(s);window.__a.push(a);return a}});
  await pg.goto(U,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1000));
  if(nombre){ await pg.type('.intro__input',nombre,{delay:40}); await new Promise(r=>setTimeout(r,500)); }
  if(out&&nombre==='Beñat') await pg.screenshot({path:`${out}/n-intro-movil.jpg`,type:'jpeg',quality:80});
  if(out&&nombre==='ioana') await pg.screenshot({path:`${out}/n-intro-escritorio.jpg`,type:'jpeg',quality:80});
  if(nombre) await pg.keyboard.press('Enter'); else await pg.tap('.intro__enter');
  await new Promise(r=>setTimeout(r,4200));
  const st=await pg.evaluate(()=>({hola:document.querySelector('.hero__hello').textContent, holaVisible:document.querySelector('.hero__hello').classList.contains('is-on'), video:(()=>{const v=document.querySelector('.hero__video');return (v.currentSrc||v.src).split('/').pop()+(v.paused?' PARADO':' en marcha')+' t='+v.currentTime.toFixed(1)+(v.classList.contains('is-on')?' visible':' oculto')})(), audio:window.__a.filter(a=>!a.paused||a.currentTime>0).map(a=>a.src.split('/').slice(-1)[0]+(a.paused?(a.ended?' terminado':' PARADO'):' sonando')+' t='+a.currentTime.toFixed(1)).join(' | ')}));
  if(out&&nombre==='Beñat') await pg.screenshot({path:`${out}/n-dentro-movil.jpg`,type:'jpeg',quality:80});
  if(out&&nombre==='ioana') await pg.screenshot({path:`${out}/n-dentro-escritorio.jpg`,type:'jpeg',quality:80});
  console.log(`[${dev}] nombre="${nombre}"`,JSON.stringify(st),errs.length?errs:'sin errores'); await pg.close();
 }
 await b.close();
})();
