// Tras recargar la misma pestaña, la locución debe volver a sonar; y el rótulo debe verse mientras esté parado
const p=require('puppeteer-core');
(async()=>{
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy=document-user-activation-required','--mute-audio']});
 for(const mobile of [true,false]){
  const pg=await b.newPage(); await pg.setViewport(mobile?{width:390,height:844,isMobile:true,hasTouch:true}:{width:1440,height:900});
  await pg.evaluateOnNewDocument(()=>{const O=window.Audio;window.__a=[];window.Audio=function(s){const a=new O(s);window.__a.push(a);return a}});
  const st=()=>pg.evaluate(()=>({btn:document.querySelector('.sound').innerText.trim(),a:window.__a.map(a=>a.src.split('/').pop()+(a.paused?' PARADO':' sonando')+' t='+a.currentTime.toFixed(1)).join(', ')}));
  const tap=()=>mobile?pg.touchscreen.tap(200,300):pg.mouse.click(400,400);
  await pg.goto(process.env.URL||'http://localhost:4320/',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1200));
  const o={antes:await st()};
  if(mobile&&process.argv[2]) await pg.screenshot({path:process.argv[2]+'/snd2.jpg',type:'jpeg',quality:80});
  await tap(); await new Promise(r=>setTimeout(r,2500)); o.trasToque=await st();
  await pg.reload({waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1200)); await tap(); await new Promise(r=>setTimeout(r,2500)); o.trasRecargarYToque=await st();
  console.log(mobile?'MOVIL':'ESCRITORIO',JSON.stringify(o)); await pg.close();
 }
 await b.close();
})();
