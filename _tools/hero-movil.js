// Captura la portada en un móvil (DPR 3) con el vídeo en marcha, para juzgar la nitidez
const p=require('puppeteer-core');(async()=>{const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--mute-audio']});const pg=await b.newPage();
await pg.setViewport({width:390,height:844,deviceScaleFactor:3,isMobile:true,hasTouch:true});
await pg.goto(process.env.URL||'http://localhost:4320/',{waitUntil:'networkidle0'});await pg.type('.intro__input','Beñat');await pg.keyboard.press('Enter');
for(const [t,n] of [[8,'1'],[5,'2']]){await new Promise(r=>setTimeout(r,t*1000));await pg.screenshot({path:process.argv[2]+'/hm'+n+'.jpg',type:'jpeg',quality:85});}
console.log(await pg.evaluate(()=>{const v=document.querySelector('.hero__video');return v.currentSrc.split('/').pop()+' '+v.videoWidth+'x'+v.videoHeight+' t='+v.currentTime.toFixed(1)}));await b.close()})()
