const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:2000,height:720}});
for(const n of ['scene-navy','scene-cream']){await p.goto('file://'+__dirname+'/'+n+'.svg');await p.screenshot({path:__dirname+'/'+n+'.png'});}
await b.close();})();
