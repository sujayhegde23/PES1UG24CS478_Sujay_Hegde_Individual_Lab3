import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const dir=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(path.join(dir,'../2-Architectural_Diagram/package.json'));
const PDFDocument=require('pdfkit');
const evidence=JSON.parse(fs.readFileSync(path.join(dir,'jira/Evidence_Provenance.json'),'utf8'));
const notes={
 Bug_Tracker:'The backlog shows four defects BB-1 through BB-4, all in To Do with Medium priority. The detail view records the missing 15-day SSL expiry alert. These are lab defect records, not evidence of a tested implementation.',
 Kanban:'The captures show the initial board, seven requirements, six epics, implementation work items, and FR-001 details. Visible work remains in To Do. An expanded list supports the hierarchy shown; task names alone do not establish that all subtasks are complete.',
 Scrum:'The source report describes a one-week sprint with FR-001, FR-002, FR-004, and NFR-001 totaling 26 planned story points. Captures show setup, a To Do board, scope changes, and a burndown view. They do not demonstrate a completed sprint or completion of the planned work.'
};
for(const group of ['Kanban','Scrum','Bug_Tracker']){
 const entries=evidence.filter(x=>x.group===group);
 const doc=new PDFDocument({size:'A4',margin:40,info:{Title:'Lab 2 - '+group,Author:'Sujay Hegde | PES1UG24CS478'}});
 const stream=fs.createWriteStream(path.join(dir,'jira',group+'_Evidence_Report.pdf'));
 const done=new Promise((resolve,reject)=>{stream.on('finish',resolve);stream.on('error',reject);doc.on('error',reject);});doc.pipe(stream);
 doc.font('Helvetica-Bold').fontSize(19).text('Lab 2: '+group.replaceAll('_',' ')+' Evidence');
 doc.moveDown().font('Helvetica').fontSize(11).text('Sujay Hegde | PES1UG24CS478 | BPS #47');
 doc.moveDown().text('Domain & SSL Certificate Expiry Alert System');
 doc.moveDown().text(notes[group],{lineGap:3});
 doc.moveDown().fontSize(9).text('Source supplied by the student: '+entries[0].source);
 doc.moveDown().text('Screenshots were extracted from the source PDF at their original pixel dimensions. This report updates student metadata and uses captions limited to the captured evidence. The original report is retained under source_reports/.');
 for(const [i,x] of entries.entries()){
  doc.addPage();doc.font('Helvetica-Bold').fontSize(14).text(`${i+1}. ${x.caption}`);
  doc.moveDown().font('Helvetica').fontSize(10).text('Sujay Hegde | PES1UG24CS478 | BPS #47');
  doc.moveDown().fontSize(9).text(`Source page ${x.page}; extracted screenshot ${x.file} (${x.width} x ${x.height} pixels).`);
  doc.image(path.join(dir,'jira',x.file),40,150,{fit:[515,530],align:'center',valign:'top'});
 }
 doc.end();await done;
}
// The original Lab 1 markdown is retained alongside a readable one-page export.
const spec=fs.readFileSync(path.join(dir,'../1-RE/UseCaseSpecification.md'),'utf8').replace(/^\uFEFF/,'');
const doc=new PDFDocument({size:'A4',margin:45,info:{Title:'UC-005 Acknowledge Expiry Alert',Author:'Sujay Hegde | PES1UG24CS478'}});
const stream=fs.createWriteStream(path.join(dir,'../1-RE/UseCaseSpecification.pdf'));
const done=new Promise((resolve,reject)=>{stream.on('finish',resolve);stream.on('error',reject);doc.on('error',reject);});doc.pipe(stream);
for(const row of spec.split('\n')){
 if(!row.trim()){doc.moveDown(0.2);continue;}
 const heading=row.match(/^(#{1,2}) (.*)/);
 doc.font(heading?'Helvetica-Bold':'Helvetica').fontSize(heading?(heading[1].length===1?16:11):10);
 doc.text((heading?heading[2]:row).replaceAll('**',''),{lineGap:2}).moveDown(0.12);
}
doc.end();await done;
console.log('Generated three Jira evidence reports and the one-page use-case specification.');
