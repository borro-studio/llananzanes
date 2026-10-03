// Repite la entrada en móvil y registra quién llama a pause() en los audios
const p=require('puppeteer-core');
(async()=>{
 const U=process.env.URL||'http://localhost:4320/', N=+(process.argv[2]||8);
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--autoplay-policy=document-user-activation-required','--mute-audio']});
 let malos=0;
 for(let i=0;i<N;i++){
  const pg=await b.newPage(); await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true}); const log=[];
  pg.on('console',m=>{const t=m.text(); if(/^(PAUSE|VIS|EVT)/.test(t)) log.push(t)});
  await pg.evaluateOnNewDocument(()=>{const t0=performance.now(),T=()=>((performance.now()-t0)/1000).toFixed(2);const O=window.Audio;window.__a=[];window.Audio=function(s){const a=new O(s);const n=s.split('/').pop();const pa=a.pause.bind(a);
    a.pause=()=>{console.log('PAUSE',T(),n,'t='+a.currentTime.toFixed(2),(new Error().stack.split('\n').slice(2,4).join(' <- ')).replace(/https?:\/\/[^ ]*\//g,''));return pa()};
    a.addEventListener('pause',()=>console.log('EVT pause',T(),n,'t='+a.currentTime.toFixed(2),'ended='+a.ended));
    window.__a.push(a);return a};
    document.addEventListener('visibilitychange',()=>console.log('VIS',T(),document.visibilityState));});
  await pg.goto(U,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,800));
  if(i%2===0){ await pg.type('.intro__input','Beñat',{delay:40}); await new Promise(r=>setTimeout(r,400)); await pg.keyboard.press('Enter'); } else await pg.tap('.intro__enter');
  await new Promise(r=>setTimeout(r,4200));
  const st=await pg.evaluate(()=>window.__a.filter(a=>!/saludos/.test(a.src)).map(a=>a.src.split('/').pop()+(a.paused?' PARADO':' ok')+' '+a.currentTime.toFixed(1)).join(', '));
  const malo=/PARADO/.test(st); if(malo) malos++;
  console.log(`#${i} ${i%2===0?'teclado':'toque'}: ${st}`); if(malo||i<2) log.forEach(l=>console.log('     ',l));
  await pg.close();
 }
 console.log('pasadas con audio parado:',malos,'de',N); await b.close();
})();
