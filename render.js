// Render deterministik: tiap frame digambar pada waktu t = f/30 (tidak bergantung kecepatan perangkat)
const {chromium}=require("playwright");const fs=require("fs");
(async()=>{fs.mkdirSync("frames",{recursive:true});
const b=await chromium.launch(),p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto("file://"+process.cwd()+"/index.html?render=1");const c=p.locator("canvas");
for(let f=0;f<900;f++){await p.evaluate(t=>window.seek(t),f/30);
await c.screenshot({path:`frames/${String(f).padStart(4,"0")}.jpg`,type:"jpeg",quality:95})}
await b.close()})();
