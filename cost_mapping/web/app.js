'use strict';
const form=document.querySelector('#calculator');
const status=document.querySelector('#status');
const metrics=document.querySelector('#metrics');
const breakdown=document.querySelector('#breakdown');
let latest=null;
let lastPayload=null;
const money=value=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(value);
function element(tag,text){const item=document.createElement(tag);if(text!==undefined)item.textContent=text;return item;}
function payload(){
  const gig={},assumptions={};
  for(const [key,value] of new FormData(form)){
    if(['cost_per_mile','target_hourly'].includes(key))assumptions[key]=Number(value);
    else gig[key]=key==='name'?value:Number(value);
  }
  return {gig,assumptions};
}
async function calculate(value){
  const response=await fetch('/api/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(value)});
  const data=await response.json();if(!response.ok)throw new Error(data.error||'Calculation failed');return data;
}
function show(data){
  metrics.replaceChildren();breakdown.replaceChildren();
  for(const [label,value] of [['After trip expenses',data.net_earnings],['Effective hourly',data.effective_hourly],['Trip cash cost',data.cash_cost],['Minimum target payout',data.minimum_payout]]){
    const box=element('div');box.className='metric';box.append(element('span',label),element('strong',money(value)));metrics.append(box);
  }
  breakdown.append(element('p',`${data.total_minutes.toFixed(1)} minutes total · ${data.miles.toFixed(1)} miles`),
    element('p',`${money(data.payout)} payout − ${money(data.cash_cost)} trip expenses = ${money(data.net_earnings)} before tax.`),
    element('p',`Vehicle operating cost: ${money(data.vehicle_cost)}. Time target: ${money(data.target_time_value)}.`));
  status.textContent=data.meets_target?`${data.name} meets your target by ${money(data.surplus)}.`:`${data.name} falls short of your target by ${money(-data.surplus)}.`;
}
form.addEventListener('submit',async event=>{
  event.preventDefault();const button=form.querySelector('button');button.disabled=true;status.textContent='Calculating…';
  try{const input=payload();latest=await calculate(input);lastPayload=input;show(latest);}
  catch(error){status.textContent=error.message;}
  finally{button.disabled=false;}
});

const compared=[];
function table(headers,rows){
  const item=element('table');const head=element('thead');const top=element('tr');
  headers.forEach(value=>top.append(element('th',value)));head.append(top);item.append(head);
  const body=element('tbody');for(const values of rows){const row=element('tr');values.forEach(value=>row.append(element('td',value)));body.append(row);}item.append(body);return item;
}
document.querySelector('#scenarios').addEventListener('click',async()=>{
  try{
    if(!lastPayload)throw new Error('Calculate a trip first.');
    const response=await fetch('/api/scenarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(lastPayload)});
    const data=await response.json();if(!response.ok)throw new Error(data.error||'Scenario calculation failed');
    document.querySelector('#scenario-results').replaceChildren(element('h3','Driving uncertainty: ±20%'),table(['Cost factor','Driving time factor','Hourly earnings'],data.map(row=>[`${row.cost_factor}×`,`${row.driving_time_factor}×`,money(row.effective_hourly)])));
  }catch(error){status.textContent=error.message;}
});
function showComparison(){
  const sorted=[...compared].sort((a,b)=>b.effective_hourly-a.effective_hourly);
  document.querySelector('#comparison-table').replaceChildren(table(['Trip','Net earnings','Hourly','Meets target'],sorted.map(row=>[row.name,money(row.net_earnings),money(row.effective_hourly),row.meets_target?'Yes':'No'])));
}
document.querySelector('#remember').addEventListener('click',()=>{
  if(!latest){status.textContent='Calculate a trip first.';return;}
  if(compared.length>=50){status.textContent='Compare up to 50 trips. Clear the list to start again.';return;}
  compared.push({...latest});showComparison();status.textContent='Trip added to comparison.';
});
document.querySelector('#clear-comparison').addEventListener('click',()=>{compared.length=0;showComparison();});

document.querySelector('#download').addEventListener('click',()=>{
  if(!latest){status.textContent='Calculate a trip first.';return;}
  const report={schema_version:1,inputs:lastPayload,result:latest,comparison:compared};
  const url=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)],{type:'application/json'}));
  const link=element('a');link.href=url;link.download='trip-report.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
document.querySelector('#save-inputs').addEventListener('click',()=>{
  try{localStorage.setItem('cost-mapping-assumptions-v1',JSON.stringify(payload().assumptions));status.textContent='Assumptions saved in this browser.';}
  catch(error){status.textContent=error.message;}
});
document.querySelector('#forget-inputs').addEventListener('click',()=>{
  try{localStorage.removeItem('cost-mapping-assumptions-v1');status.textContent='Saved assumptions removed.';}
  catch(error){status.textContent=error.message;}
});
try{
  const saved=JSON.parse(localStorage.getItem('cost-mapping-assumptions-v1')||'null');
  if(saved)for(const key of ['cost_per_mile','target_hourly'])if(Number.isFinite(saved[key])&&saved[key]>=0)form.elements[key].value=saved[key];
}catch{status.textContent='Saved assumptions could not be read; defaults are shown.';}
