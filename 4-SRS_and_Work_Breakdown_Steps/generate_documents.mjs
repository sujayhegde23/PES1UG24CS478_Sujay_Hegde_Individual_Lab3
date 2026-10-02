import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const dir=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(path.join(dir,'../2-Architectural_Diagram/package.json'));
const PDFDocument=require('pdfkit');
const plain=s=>s.replace(/\[([^\]]+)\]\([^)]+\)/g,'$1').replaceAll('**','').replaceAll('`','');
function render(doc, source) {
 const lines=source.split('\n');const x=doc.page.margins.left;
 const width=doc.page.width-x-doc.page.margins.right;
 const limit=()=>doc.page.height-doc.page.margins.bottom;
 const ensure=h=>{if(doc.y+h>limit())doc.addPage();};
 let code=false;
 for(let i=0;i<lines.length;i++){
  const row=lines[i];
  if(row.startsWith('```')){code=!code;doc.moveDown(0.3);continue;}
  if(!row.trim()){doc.moveDown(0.35);continue;}
  if(row.startsWith('|')&&!code){
   const table=[];
   while(i<lines.length&&lines[i].startsWith('|')){
    const text=lines[i++];
    if(!/^\|[\s|:-]+\|$/.test(text))table.push(text.split('|').slice(1,-1).map(s=>plain(s.trim())));
   }i--;
   const cols=table[0].length;const colWidth=width/cols;const fontSize=cols>=6?8:9;
   const drawRow=(values,header)=>{
    doc.font(header?'Helvetica-Bold':'Helvetica').fontSize(fontSize);
    const height=Math.max(...values.map(s=>doc.heightOfString(s,{width:colWidth-12,lineGap:2})))+14;
    if(doc.y+height>limit()){
     doc.addPage();if(!header)drawRow(table[0],true);
    }
    const top=doc.y;
    for(let j=0;j<cols;j++){
     doc.rect(x+j*colWidth,top,colWidth,height).fillAndStroke(header?'#e2e8f0':'#ffffff','#cbd5e1');
     doc.fillColor('#0f172a').font(header?'Helvetica-Bold':'Helvetica').fontSize(fontSize)
       .text(values[j]||'',x+j*colWidth+6,top+7,{width:colWidth-12,lineGap:2});
    }
    doc.x=x;doc.y=top+height;
   };
   table.forEach((r,j)=>drawRow(r,j===0));doc.moveDown(0.5);continue;
  }
  const heading=row.match(/^(#{1,3}) (.*)/);
  const size=heading?[18,13,11][heading[1].length-1]:code?9:10;
  doc.font(heading?'Helvetica-Bold':code?'Courier':'Helvetica').fontSize(size);
  const value=plain(heading?heading[2]:row);
  ensure(doc.heightOfString(value,{width,lineGap:2})+(heading?30:8));
  doc.fillColor('#0f172a').text(value,x,doc.y,{width,lineGap:2}).moveDown(heading?0.5:0.2);
 }
}
async function exportPdf(file,sources,landscape=false){
 const doc=new PDFDocument({size:'A4',layout:landscape?'landscape':'portrait',margin:40,bufferPages:true,
  info:{Title:path.basename(file,'.pdf'),Author:'Sujay Hegde | PES1UG24CS478'}});
 const stream=fs.createWriteStream(file);const done=new Promise((resolve,reject)=>{stream.on('finish',resolve);stream.on('error',reject);doc.on('error',reject);});doc.pipe(stream);
 sources.forEach((s,i)=>{if(i)doc.addPage();render(doc,fs.readFileSync(s,'utf8'));});
 const pages=doc.bufferedPageRange();for(let i=0;i<pages.count;i++){
  doc.switchToPage(i);doc.font('Helvetica').fontSize(8).fillColor('#64748b').text(`Sujay Hegde | PES1UG24CS478 - Page ${i+1} of ${pages.count}`,40,doc.page.height-25,{lineBreak:false});
 }
 doc.end();await done;console.log(path.basename(file)+': '+pages.count+' pages');
}
const srs=path.join(dir,'SRS_Document.md'),wbs=path.join(dir,'Work_Breakdown_Structure.md');
await exportPdf(path.join(dir,'SRS_Document.pdf'),[srs]);
await exportPdf(path.join(dir,'Work_Breakdown_Structure.pdf'),[wbs]);
await exportPdf(path.join(dir,'SRS_and_Work_Breakdown_Steps.pdf'),[srs,wbs]);
await exportPdf(path.join(dir,'../1-RE/RTM_Table.pdf'),[path.join(dir,'../1-RE/RTM_Table.md')],true);
