const p=require('puppeteer-core');
(async()=>{const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--mute-audio','--autoplay-policy=no-user-gesture-required']});
for(const u of ['/','/casa-i.html','/casa-iii','/experiencias/esqui-y-nieve.html','/no-existe']){
 const pg=await b.newPage(); await pg.setViewport({width:1440,height:900}); const bad=[];
 pg.on('response',x=>{if(x.status()>=400&&!x.url().endsWith('/no-existe'))bad.push(x.status()+' '+x.url().replace('http://localhost:4399',''))});
 pg.on('pageerror',e=>bad.push('JS '+e.message));
 const res=await pg.goto('http://localhost:4399'+u,{waitUntil:'networkidle0'});
 if(u==='/'){await pg.click('.intro__enter'); await new Promise(r=>setTimeout(r,4000));}
 const info=await pg.evaluate(()=>({t:document.title.slice(0,40),css:getComputedStyle(document.body).fontFamily.slice(0,20),vid:document.querySelector('video')?.currentSrc?.replace(location.origin,'')||'-',imgs:[...document.images].filter(i=>i.complete&&!i.naturalWidth&&i.loading!=='lazy').length}));
 console.log(res.status(),u,JSON.stringify(info),bad.length?bad:'sin fallos'); await pg.close();}
await b.close();})();
