// Comprueba que el audio se reproduce de verdad (currentTime avanza), no solo el estado del botón
const p=require('puppeteer-core');
const run=async(policy,label,mobile)=>{
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy='+policy,'--mute-audio']});
 const pg=await b.newPage(); await pg.setViewport(mobile?{width:390,height:844,isMobile:true,hasTouch:true}:{width:1440,height:900});
 const logs=[]; pg.on('pageerror',e=>logs.push('ERR '+e)); pg.on('console',m=>{if(m.type()==='error')logs.push('console '+m.text())}); pg.on('requestfailed',r=>logs.push('FAIL '+r.url())); pg.on('response',r=>{if(/audio\//.test(r.url()))logs.push(r.status()+' '+r.url().split('/').pop())});
 await pg.evaluateOnNewDocument(()=>{const O=window.Audio;window.__a=[];window.Audio=function(s){const a=new O(s);window.__a.push(a);return a}});
 await pg.goto(process.env.URL||'http://localhost:4320/',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1500));
 const st=()=>pg.evaluate(()=>window.__a.map(a=>({f:a.src.split('/').pop().split('?')[0],paused:a.paused,t:+a.currentTime.toFixed(2),vol:+a.volume.toFixed(2),ready:a.readyState,err:a.error&&a.error.code,dur:a.duration})));
 const o={alCargar:await st()};
 if(mobile) await pg.touchscreen.tap(200,300); else await pg.mouse.click(400,400);
 await new Promise(r=>setTimeout(r,3000)); o.tras3s=await st();
 console.log(label,JSON.stringify(o,null,0)); console.log('  ',logs.join(' | ')); await b.close();
};
(async()=>{await run('document-user-activation-required','MOVIL bloqueado',true);await run('document-user-activation-required','ESCRITORIO bloqueado',false);await run('no-user-gesture-required','ESCRITORIO permitido',false);})();
