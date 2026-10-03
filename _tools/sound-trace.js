const p=require('puppeteer-core');
(async()=>{
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy=document-user-activation-required','--mute-audio']});
 const pg=await b.newPage(); await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true});
 pg.on('console',m=>console.log('  >',m.text().slice(0,400)));
 await pg.evaluateOnNewDocument(()=>{const O=window.Audio;window.__a=[];window.Audio=function(s){const a=new O(s);const n=s.split('/').pop();const pl=a.play.bind(a),pa=a.pause.bind(a);
   a.play=()=>{console.log('play',n,'t='+a.currentTime.toFixed(2),(new Error().stack.split('\n')[2]||'').trim());return pl()};
   a.pause=()=>{console.log('pause',n,'t='+a.currentTime.toFixed(2),(new Error().stack.split('\n')[2]||'').trim());return pa()};
   window.__a.push(a);return a};
   document.addEventListener('visibilitychange',()=>console.log('visibility',document.visibilityState));
   ['pointerdown','pointerup','mousedown','touchend','click'].forEach(e=>addEventListener(e,()=>console.log('evento',e),true));});
 await pg.goto(process.env.URL||'http://localhost:4320/',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,1500));
 await pg.touchscreen.tap(200,300); await new Promise(r=>setTimeout(r,3500));
 console.log(JSON.stringify(await pg.evaluate(()=>window.__a.map(a=>({paused:a.paused,t:+a.currentTime.toFixed(2)})))));
 await b.close();
})();
