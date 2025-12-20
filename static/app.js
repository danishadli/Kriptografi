function encryptText(){
 fetch("/text/encrypt",{method:"POST",headers:{'Content-Type':'application/json'},
 body:JSON.stringify({text:text.value,key:key.value})})
 .then(r=>r.json()).then(d=>textResult.textContent=d.result)
}

function decryptText(){
 fetch("/text/decrypt",{method:"POST",headers:{'Content-Type':'application/json'},
 body:JSON.stringify({text:text.value,key:key.value})})
 .then(r=>r.json()).then(d=>textResult.textContent=d.result)
}

function analyze(){
 fetch(`/analysis/${preset.value}`).then(r=>r.json()).then(d=>{
  let h="<tr><th>Metric</th><th>Value</th></tr>";
  for(let k in d) h+=`<tr><td>${k}</td><td>${d[k]}</td></tr>`;
  analysisTable.innerHTML=h;
 })
 fetch(`/sbox/${preset.value}`).then(r=>r.json()).then(drawSbox)
}

function drawSbox(data){
 let h="<tr><th></th>"+[...Array(16).keys()].map(i=>`<th>${i}</th>`).join("")+"</tr>";
 data.forEach((r,i)=>{
  h+=`<tr><th>${i}</th>`+r.map(v=>`<td>${v}</td>`).join("")+"</tr>";
 })
 sboxTable.innerHTML=h;
}

function exportExcel(){
 window.location=`/export/${preset.value}`
}
