import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import PDFDocument from 'pdfkit';
import SVGtoPDF from 'svg-to-pdfkit';
import sharp from 'sharp';
import { Document, Packer, Paragraph, TextRun, AlignmentType } from 'docx';

const dir = path.dirname(fileURLToPath(import.meta.url));
const xml = s => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const W=1400,H=1140;
const layers=[
 {id:'presentation',name:'Presentation layer',x:40,y:115,w:1320,h:190,color:'#2563eb',fill:'#eff6ff'},
 {id:'business',name:'Application / business layer',x:40,y:360,w:1320,h:205,color:'#15803d',fill:'#f0fdf4'},
 {id:'infrastructure',name:'Infrastructure / data layer',x:40,y:675,w:1320,h:210,color:'#b45309',fill:'#fffbeb'}
];
const components=[
 {id:'ui',name:'User Interface',layer:'presentation',x:450,y:170,w:500,h:105,lines:['Touchscreen: Espresso / Americano / Latte','Small / Large; show order and payment status']},
 {id:'order',name:'Order Manager',layer:'business',x:450,y:420,w:500,h:105,lines:['Validate selection; calculate amount; coordinate checkout','Request payment; print receipt after approval']},
 {id:'payment',name:'Payment Service',layer:'infrastructure',x:95,y:730,w:350,h:105,lines:['Credit-card authorization via terminal SDK','Return result and transaction reference']},
 {id:'menu',name:'Menu Repository',layer:'infrastructure',x:525,y:730,w:350,h:105,lines:['Store coffee types, sizes, and prices','Read menu and prices via database queries']},
 {id:'receipt',name:'Receipt Printer',layer:'infrastructure',x:955,y:730,w:350,h:105,lines:['Format order details; report print status','USB/serial hardware driver']}
];
const interfaces=[
 {id:'order_api',name:'Order Interface',consumer:'ui',provider:'order',cx:700,cy:332,req:[[700,275],[700,318]],prov:[[700,345],[700,420]],label:[730,325],detail:'Local API: getMenu(), submitOrder(), getStatus()'},
 {id:'payment_api',name:'Payment Interface',consumer:'order',provider:'payment',cx:270,cy:615,req:[[475,525],[475,582],[270,582],[270,601]],prov:[[270,628],[270,730]],label:[85,638],detail:'Local API: processPayment() / terminal SDK'},
 {id:'menu_api',name:'Menu Interface',consumer:'order',provider:'menu',cx:700,cy:615,req:[[700,525],[700,601]],prov:[[700,628],[700,730]],label:[515,638],detail:'Repository API: getMenu(), getPrice() / SQL'},
 {id:'receipt_api',name:'Receipt Interface',consumer:'order',provider:'receipt',cx:1130,cy:615,req:[[925,525],[925,582],[1130,582],[1130,601]],prov:[[1130,628],[1130,730]],label:[945,638],detail:'Local API: printReceipt(), getPrinterStatus()'}
];
for(const f of interfaces.slice(1)) {
 f.label=[f.cx+25,610];
 f.details=f.id==='payment_api'?['processPayment()','Local API / terminal SDK']:f.id==='menu_api'?['getMenu(), getPrice()','Repository API / SQL']:['printReceipt(), getPrinterStatus()','Local API / USB/serial driver'];
}
function text(x,y,value,size=15,bold=false,color='#1e293b',anchor='start'){
 return `<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-size="${size}" font-weight="${bold?'bold':'normal'}" fill="${color}" text-anchor="${anchor}">${xml(value)}</text>`;
}
const line=points=>`<polyline points="${points.map(p=>p.join(',')).join(' ')}" fill="none" stroke="#334155" stroke-width="2"/>`;
let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="white"/>`;
svg+=text(40,48,'Self-Service Coffee Kiosk System',30,true)+text(40,80,'Lab 3 - UML Component Diagram | Sujay Hegde | PES1UG24CS478 | Layered Architecture',17);
for(const l of layers)svg+=`<rect x="${l.x}" y="${l.y}" width="${l.w}" height="${l.h}" fill="${l.fill}" stroke="${l.color}" stroke-width="2"/>`+text(l.x+20,l.id==='infrastructure'?l.y+l.h-15:l.y+30,l.name,18,true,l.color);
for(const c of components){
 const l=layers.find(l=>l.id===c.layer);
 svg+=`<rect x="${c.x}" y="${c.y}" width="${c.w}" height="${c.h}" fill="white" stroke="${l.color}" stroke-width="2"/>`;
 svg+=text(c.x+c.w/2,c.y+23,'«component»',14,false,'#475569','middle')+text(c.x+c.w/2,c.y+47,c.name,20,true,'#1e293b','middle');
 c.lines.forEach((s,i)=>svg+=text(c.x+c.w/2,c.y+72+i*19,s,13,false,'#475569','middle'));
}
for(const f of interfaces){
 // Consumer stem ends at the top of a downward-opening socket.
 // Provider stem meets the bottom of the hollow lollipop.
 svg+=line(f.req)+line(f.prov);
 svg+=`<path d="M ${f.cx-14},${f.cy} A 14,14 0 0 1 ${f.cx+14},${f.cy}" fill="none" stroke="#334155" stroke-width="2"/>`;
 svg+=`<circle cx="${f.cx}" cy="${f.cy+3}" r="9" fill="white" stroke="#334155" stroke-width="2"/>`;
 svg+=text(f.label[0],f.label[1],f.name,15,true);
 (f.details||[f.detail]).forEach((s,i)=>svg+=text(f.label[0],f.label[1]+21+i*16,s,f.details?11:12));
}
svg+=text(40,925,'Notation: hollow ball = provided interface; semicircle = required interface; solid stems = assembly connection.',15);
svg+=text(40,951,'Requests go from consumer (socket) to provider (ball); results return through the same interface.',15);
svg+=text(40,985,'Checkout flow',18,true);
svg+=text(40,1012,'1. Read menu and prices   2. Select coffee and size   3. Authorize credit card   4. Print receipt after approval',16);
svg+=text(40,1041,'Declined payment: show failure. Printer failure after payment: retry printing without charging again.',15);
svg+=text(40,1082,'Logical layers within one kiosk application. External payment authorization may require network access.',14,false,'#475569');
svg+='</svg>';
fs.writeFileSync(path.join(dir,'Architecture_Diagram.svg'),svg);
await sharp(Buffer.from(svg)).resize(W*2,H*2).png().toFile(path.join(dir,'Architecture_Diagram.png'));

async function pdf(file,options,build){
 const doc=new PDFDocument({...options,info:{Title:path.basename(file,'.pdf'),Author:'Sujay Hegde | PES1UG24CS478'}});
 const out=fs.createWriteStream(file); const done=new Promise((resolve,reject)=>{out.on('finish',resolve);out.on('error',reject);doc.on('error',reject);});
 doc.pipe(out);build(doc);doc.end();await done;
}
await pdf(path.join(dir,'Architecture_Diagram.pdf'),{size:[W,H],margin:0},doc=>SVGtoPDF(doc,svg,0,0,{width:W,height:H,assumePt:true}));

// Editable draw.io uses the same coordinates and paths as the exports.
const cell=(id,value,style,x,y,w,h)=>`<mxCell id="${id}" value="${xml(value)}" style="${xml(style)}" vertex="1" parent="1"><mxGeometry x="${x}" y="${y}" width="${w}" height="${h}" as="geometry"/></mxCell>`;
const label=(id,x,y,w,h,value,size=15,bold=false)=>cell(id,value,`text;html=0;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize=${size};fontStyle=${bold?1:0};`,x,y,w,h);
let cells='<mxCell id="0"/><mxCell id="1" parent="0"/>';
cells+=label('title',40,20,1250,40,'Self-Service Coffee Kiosk System',30,true)+label('subtitle',40,60,1250,30,'Lab 3 - UML Component Diagram | Sujay Hegde | PES1UG24CS478 | Layered Architecture',17);
for(const l of layers){
 cells+=cell(l.id,'',`fillColor=${l.fill};strokeColor=${l.color};strokeWidth=2;`,l.x,l.y,l.w,l.h);
 cells+=label(l.id+'_label',l.x+20,l.id==='infrastructure'?l.y+l.h-42:l.y+8,450,35,l.name,18,true);
}
for(const c of components){
 const color=layers.find(l=>l.id===c.layer).color;
 cells+=cell(c.id,`«component»\n${c.name}\n${c.lines.join('\n')}`,`html=0;whiteSpace=wrap;fontSize=14;fillColor=#ffffff;strokeColor=${color};strokeWidth=2;`,c.x,c.y,c.w,c.h);
}
function edge(id,points,component,role,interfaceId){
 const first=points[0],last=points.at(-1),middle=points.slice(1,-1);
 const c=components.find(c=>c.id===component), p=role==='required'?first:last;
 const rx=(p[0]-c.x)/c.w,ry=(p[1]-c.y)/c.h;
 const attrs=role==='required'?`source="${component}" target="${interfaceId}_socket"`:`source="${interfaceId}_ball" target="${component}"`;
 const anchors=role==='required'?`exitX=${rx};exitY=${ry};entryX=0.5;entryY=0;`:`exitX=0.5;exitY=1;entryX=${rx};entryY=${ry};`;
 return `<mxCell id="${id}" value="" style="${anchors}exitPerimeter=0;entryPerimeter=0;endArrow=none;startArrow=none;strokeWidth=2;strokeColor=#334155;" edge="1" parent="1" ${attrs}><mxGeometry relative="1" as="geometry"><mxPoint x="${first[0]}" y="${first[1]}" as="sourcePoint"/><mxPoint x="${last[0]}" y="${last[1]}" as="targetPoint"/>${middle.length?'<Array as="points">'+middle.map(p=>`<mxPoint x="${p[0]}" y="${p[1]}"/>`).join('')+'</Array>':''}</mxGeometry></mxCell>`;
}
for(const f of interfaces){
 cells+=edge(f.id+'_requires',f.req,f.consumer,'required',f.id)+edge(f.id+'_provides',f.prov,f.provider,'provided',f.id);
 cells+=cell(f.id+'_socket','', 'shape=mxgraph.basic.arc;startAngle=0.75;endAngle=0.25;fillColor=none;strokeColor=#334155;strokeWidth=2;',f.cx-14,f.cy-14,28,28);
 cells+=cell(f.id+'_ball','', 'ellipse;fillColor=#ffffff;strokeColor=#334155;strokeWidth=2;aspect=fixed;',f.cx-9,f.cy-6,18,18);
 cells+=label(f.id+'_name',f.label[0],f.label[1]-17,f.details?210:600,22,f.name,15,true);
 (f.details||[f.detail]).forEach((s,i)=>cells+=label(f.id+'_details_'+i,f.label[0],f.label[1]+6+i*16,f.details?210:600,20,s,f.details?11:12));
}
for(const [i,y,s] of [[0,905,'Notation: hollow ball = provided interface; semicircle = required interface; solid stems = assembly connection.'],[1,936,'Requests go from consumer (socket) to provider (ball); results return through the same interface.'],[2,971,'Checkout: read menu -> select coffee and size -> authorize credit card -> print receipt after approval.'],[3,1011,'Printer failure after payment: retry printing without charging again.'],[4,1062,'Logical layers within one kiosk application. External payment authorization may require network access.']])cells+=label('note_'+i,40,y,1300,35,s,15);
fs.writeFileSync(path.join(dir,'Architecture_Diagram.drawio'),`<mxfile host="app.diagrams.net"><diagram id="coffee-kiosk" name="Coffee Kiosk Components"><mxGraphModel grid="1" page="1" pageWidth="${W}" pageHeight="${H}"><root>${cells}</root></mxGraphModel></diagram></mxfile>`);

const justification=[
 ['Architecture selection','We chose Layered Architecture for the Self-Service Coffee Kiosk System. Presentation contains User Interface; application/business contains Order Manager; infrastructure/data contains Payment Service, Receipt Printer, and Menu Repository. These are logical layers in one kiosk application.'],
 ['Reason 1: Separation of concerns','The touchscreen offers Espresso, Americano, and Latte in Small or Large sizes. Keeping display logic separate from order validation and pricing allows screen changes without changing the checkout rules. UI requires Order Interface instead of accessing storage or drivers directly.'],
 ['Reason 2: Replaceable adapters','Payment Service encapsulates credit-card authorization, Receipt Printer encapsulates the printer driver, and Menu Repository encapsulates menu/price storage. Their explicit contracts let a device or storage adapter change while Order Manager keeps its workflow.'],
 ['Security advantage','A card-terminal SDK captures and authorizes card data. Payment Interface returns the outcome and transaction reference to Order Manager; raw card data is excluded from storage and receipts. This limits exposure, although logical layering alone does not provide process isolation or establish payment compliance.'],
 ['Performance benefit','Local API calls and cached menu prices avoid remote round trips during selection and total calculation. Payment authorization may still need a network call. The design aims to keep the touch interface responsive; measured latency depends on implementation and testing.'],
 ['Interfaces and interaction','The diagram shows five components and four ball/socket assemblies: Order, Payment, Receipt, and Menu. Order Manager validates the selection, reads pricing, requests payment, and prints only after approval. A print retry must not charge the customer again.']
];
await pdf(path.join(dir,'Architecture_Justification_Document.pdf'),{size:'A4',margin:48},doc=>{
 doc.font('Helvetica-Bold').fontSize(17).text('Lab 3: Architecture Justification');
 doc.font('Helvetica').fontSize(10).text('Sujay Hegde | PES1UG24CS478 | PES University').moveDown(0.8);
 for(const [h,s] of justification){doc.font('Helvetica-Bold').fontSize(11).text(h);doc.moveDown(0.2);doc.font('Helvetica').fontSize(10.5).text(s,{lineGap:2}).moveDown(0.65);}
});
const children=[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:'Lab 3: Architecture Justification',bold:true,size:32})]}),new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:200},children:[new TextRun({text:'Sujay Hegde | PES1UG24CS478 | PES University',size:20})]})];
for(const [h,s] of justification){children.push(new Paragraph({spacing:{before:130,after:50},children:[new TextRun({text:h,bold:true,size:22})]}),new Paragraph({spacing:{after:90,line:260},children:[new TextRun({text:s,size:21})]}));}
const word=new Document({styles:{default:{document:{run:{font:'Arial',size:21}}}},sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:800,bottom:800,left:850,right:850}}},children}]});
fs.writeFileSync(path.join(dir,'Architecture_Justification_Document.docx'),await Packer.toBuffer(word));

await pdf(path.join(dir,'Architecture_Specification.pdf'),{size:'A4',margin:45},doc=>{
 const source=fs.readFileSync(path.join(dir,'Architecture_Specification.md'),'utf8').replace(/^\uFEFF/,'');
 for(const row of source.split('\n')){
  if(!row.trim()){doc.moveDown(0.3);continue;}
  if(/^\|[\s|:-]+\|$/.test(row))continue;
  const heading=row.match(/^(#{1,3}) (.*)/);
  const value=(heading?heading[2]:row).replaceAll('**','').replace(/^\|\s*/,'').replace(/\s*\|$/,'').replaceAll(' | ','  /  ');
  doc.font(heading?'Helvetica-Bold':'Helvetica').fontSize(heading?(heading[1].length===1?17:12):10);
  doc.text(value,{lineGap:2}).moveDown(heading?0.4:0.15);
 }
});
console.log('Generated diagram (draw.io/SVG/PNG/PDF), justification (DOCX/PDF), and specification PDF.');
