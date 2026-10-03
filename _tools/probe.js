const p=require('puppeteer-core');(async()=>{const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});const pg=await b.newPage();
await pg.setViewport({width:390,height:844,deviceScaleFactor:2,isMobile:true,hasTouch:true});
await pg.goto('http://localhost:4320/',{waitUntil:'networkidle0'});await new Promise(r=>setTimeout(r,3000));
const out=process.argv[2];
await pg.screenshot({path:out+'/mh.jpg',type:'jpeg',quality:75});
const r=await pg.evaluate(()=>{const h=document.querySelector('.hero h1'),i=document.querySelector('.hero__inner'),hero=document.querySelector('.hero');const b=h.getBoundingClientRect(),hb=hero.getBoundingClientRect(),ib=i.getBoundingClientRect();return {h1:[b.top,b.bottom,b.height],hero:[hb.top,hb.bottom],inner:[ib.top,ib.bottom],fs:getComputedStyle(h).fontSize,vh:innerHeight}});
console.log(JSON.stringify(r));
await pg.click('.nav__burger');await new Promise(r=>setTimeout(r,1200));await pg.screenshot({path:out+'/mm.jpg',type:'jpeg',quality:75});
await b.close()})()
