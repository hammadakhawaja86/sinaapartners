/* Contrast audit for the Sinaa Partners site.
 *
 *   npm i playwright && node site/scripts/contrast-audit.mjs
 *
 * Loads every page, walks every element that owns a text node, resolves the
 * nearest opaque ancestor background, and asserts WCAG 2.1 AA — 4.5:1, or
 * 3:1 for large text (>=24px, or >=18.66px at weight 700+).
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pages=fs.readdirSync(dir).filter(f=>f.endsWith('.html'));
const exe = process.env.CHROMIUM_PATH; // optional: point at a preinstalled build
const b=await chromium.launch(exe ? {executablePath: exe} : {});
const c=await b.newContext({viewport:{width:1280,height:900}});
const p=await c.newPage();
let fails=[];
for (const f of pages) {
  await p.goto('file://'+dir+'/'+f);
  await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(n=>n.classList.add('is-in')));
  const res = await p.evaluate(() => {
    const L=h=>{const [r,g,bb]=h;const f=c=>{c/=255;return c<=0.04045?c/12.92:((c+0.055)/1.055)**2.4};
      return 0.2126*f(r)+0.7152*f(g)+0.0722*f(bb)};
    const parse=s=>{const m=s.match(/[\d.]+/g); return m?m.map(Number):null};
    const bgOf=el=>{let n=el;while(n&&n!==document.documentElement){const cs=getComputedStyle(n);
      const c=parse(cs.backgroundColor); if(c&&(c[3]===undefined||c[3]>0.95)) return c; n=n.parentElement;}
      return [255,255,255];};
    const out=[];
    document.querySelectorAll('body *').forEach(el=>{
      const txt=Array.from(el.childNodes).filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join('');
      if(!txt) return;
      const cs=getComputedStyle(el);
      if(cs.visibility==='hidden'||cs.display==='none'||Number(cs.opacity)<0.99) return;
      const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
      const fg=parse(cs.color), bg=bgOf(el);
      if(!fg) return;
      const l1=L(fg), l2=L(bg);
      const ratio=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
      const size=parseFloat(cs.fontSize), w=parseInt(cs.fontWeight)||400;
      const large = size>=24 || (size>=18.66 && w>=700);
      const need = large?3:4.5;
      if (ratio < need) out.push({tag:el.tagName, cls:el.className&&el.className.toString().slice(0,40), txt:txt.slice(0,50), ratio:+ratio.toFixed(2), need, size, fg:cs.color, bg:`rgb(${bg.slice(0,3)})`});
    });
    return out;
  });
  if(res.length) fails.push({page:f, res});
}
await b.close();
if(!fails.length) console.log('PASS — no text below WCAG AA on any page');
else { console.log(JSON.stringify(fails,null,1)); process.exitCode = 1; }
