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
