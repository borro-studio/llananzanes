// Exporta la home entera a un PDF de una sola hoja (texto vectorial): node pdf.js <salida.pdf> [ancho]
const p=require('puppeteer-core');
(async()=>{
 const out=process.argv[2], W=+(process.argv[3]||1440);
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
 const pg=await b.newPage(); await pg.setViewport({width:W,height:900});
 await pg.emulateMediaType('screen');
 await pg.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
 await pg.goto('http://localhost:4320/?flat',{waitUntil:'networkidle0'});
 // fuentes estáticas (pesos fijos) para que el PDF lleve fuentes reales y el texto sea editable en Illustrator
 const fs=require('fs'), FD=require('os').homedir()+'/Downloads/llananzanes/export/fuentes/';
 const face=(fam,file,w,st)=>`@font-face{font-family:"${fam}";src:url(data:font/ttf;base64,${fs.readFileSync(FD+file).toString('base64')}) format("truetype");font-weight:${w};font-style:${st};}`;
 await pg.addStyleTag({content:[
   face('CG Static','CormorantGaramond-Medium.ttf',500,'normal'),face('CG Static','CormorantGaramond-SemiBold.ttf',600,'normal'),face('CG Static','CormorantGaramond-MediumItalic.ttf',500,'italic'),
   face('SG Static','SchibstedGrotesk-Regular.ttf',400,'normal'),face('SG Static','SchibstedGrotesk-Medium.ttf',500,'normal'),face('SG Static','SchibstedGrotesk-SemiBold.ttf',600,'normal'),
   ':root{--f-display:"CG Static",serif;--f-text:"SG Static",sans-serif}'].join('\n')});
 // modo 'ai': sin kerning ni interletraje, para que Illustrator importe cada línea como un bloque de texto
 if(process.argv[4]==='ai') await pg.addStyleTag({content:'*{font-kerning:none!important;letter-spacing:0!important;font-variant-ligatures:none!important;font-feature-settings:"kern" 0,"liga" 0,"clig" 0!important;text-rendering:optimizeSpeed!important}'});
 // cargar todas las imágenes diferidas
 await pg.evaluate(async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');
   await Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r}))); await document.fonts.ready;});
 const H=await pg.evaluate(()=>document.documentElement.scrollHeight);
 // la altura en impresión puede diferir unos px de la de pantalla: subir hasta que quepa en una hoja
 let extra=0, pages=2;
 while(pages>1 && extra<400){
   const buf=await pg.pdf({width:W+'px',height:(H+extra)+'px',printBackground:true,margin:{top:0,right:0,bottom:0,left:0}});
   pages=(Buffer.from(buf).toString('latin1').match(/\/Type\s*\/Page[^s]/g)||[]).length;
   if(pages<=1){require('fs').writeFileSync(out,buf);break;} extra+=4;
 }
 console.log('extra px',extra,'pages',pages);
 if(process.argv[4]!=='ai') await pg.screenshot({path:out.replace(/\.pdf$/,'.jpg'),fullPage:true,type:'jpeg',quality:70});
 console.log(W,H); await b.close();
})();
