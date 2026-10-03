const p=require('puppeteer-core');
const run=async(policy,label)=>{
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy='+policy,'--mute-audio']});
 const pg=await b.newPage(); await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true});
 const errs=[]; pg.on('pageerror',e=>errs.push(String(e))); pg.on('requestfailed',r=>errs.push('FAIL '+r.url()));
 await pg.goto('http://localhost:4320/',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1500));
 const st=()=>pg.evaluate(()=>({on:document.querySelector('.sound').classList.contains('is-on'),label:document.querySelector('.sound').getAttribute('aria-label'),voz:sessionStorage.getItem('mll-voz'),pref:localStorage.getItem('mll-sonido')}));
 const o={alCargar:await st()};
 await pg.touchscreen.tap(200,300); await new Promise(r=>setTimeout(r,1200)); o.trasPrimerToque=await st();
 if(process.argv[2]&&label==='bloqueado') await pg.screenshot({path:process.argv[2]+'/snd.jpg',type:'jpeg',quality:80});
 await pg.tap('.sound'); await new Promise(r=>setTimeout(r,800)); o.trasPulsarBoton=await st();
 await pg.reload({waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1200)); await pg.touchscreen.tap(200,300); await new Promise(r=>setTimeout(r,800)); o.trasRecargarYTocar=await st();
 console.log(label,JSON.stringify(o),errs.length?errs:'sin errores'); await b.close();
};
(async()=>{await run('document-user-activation-required','bloqueado');await run('no-user-gesture-required','permitido');})();
