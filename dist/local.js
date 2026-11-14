'use strict';
(()=>{
 const form=document.querySelector('#form-local');if(!form)return;
 const input=document.querySelector('#local-termo'),scope=document.querySelector('#local-escopo');
 const status=document.querySelector('#local-status'),area=document.querySelector('#local-results');
 const results=document.querySelector('#local-itens'),more=document.querySelector('#local-mais');
 const repeatBox=document.querySelector('#local-repeticoes'),submit=document.querySelector('#local-enviar');
 const source='https://www.camara.rio/atividade-parlamentar/processo-legislativo';
 const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const link=(url,label,cls='')=>`<a class="${cls}" href="${escape(url)}" target="_blank" rel="noopener">${label}</a>`;
 const brDate=s=>s?s.split('-').reverse().join('/'):'Data não informada';
 const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/\bav\.?(?=\s)/g,'avenida').replace(/\best\.(?=\s)/g,'estrada').replace(/\btrav\.(?=\s)/g,'travessa').replace(/\br\.(?=\s)/g,'rua');
 const stop=new Set(['a','o','as','os','de','da','do','das','dos','e','em','no','na','nos','nas','bairro','bairros']);
 const roads=new Set(['rua','avenida','estrada','travessa']);
 const groupNames=new Map(DATA.grupos.map(g=>[g.id,g.nome]));
 let manifestPromise=null,sequence=0,currentIds=[],limit=20;
 const bucketCache=new Map(),pageCache=new Map();
 async function json(url){const r=await fetch(url);if(!r.ok)throw new Error('Falha ao carregar dados');return r.json()}
 function manifest(){
  if(!manifestPromise)manifestPromise=json('busca/manifesto.json').then(m=>({...m,pedidoSet:new Set(m.pedidos),rank:new Map(m.ordem.map((id,i)=>[id,i]))})).catch(e=>{manifestPromise=null;throw e});
  return manifestPromise;
 }
 function cached(cache,key,url){
  if(!cache.has(key))cache.set(key,json(url).catch(e=>{cache.delete(key);throw e}));
  return cache.get(key);
 }
 async function getRows(ids,m){
  const pages=[...new Set(ids.map(id=>Math.floor(id/m.por_pagina)))];let cursor=0;
  await Promise.all(Array.from({length:Math.min(4,pages.length)},async()=>{
   while(cursor<pages.length){const page=pages[cursor++];await cached(pageCache,page,'busca/registros/'+page+'.json')}
  }));
  return Promise.all(ids.map(async id=>(await pageCache.get(Math.floor(id/m.por_pagina)))[id%m.por_pagina]));
 }
 function queryTerms(text){
  const seq=normalize(text).match(/[a-z0-9]+/g)||[];
  const terms=seq.filter(w=>!stop.has(w));
  if(roads.has(seq[0])&&seq[1])terms.push(seq[0]+'_'+seq[1]);
  const significant=seq.filter(w=>!stop.has(w)&&!roads.has(w));
  const namedRoad=roads.has(seq[0])&&seq.length===2&&seq[1].length===1;
  if(!significant.some(w=>w.length>=3)&&!namedRoad)return [];
  return [...new Set(terms)].map(w=>({word:w,prefix:(w===seq.at(-1)&&w.length>=3)||(seq.length===2&&w===seq.join('_')&&seq[1].length>=3)}));
 }
 async function lookup(term){
  const bucket=await cached(bucketCache,term.word[0],'busca/indice/'+term.word[0]+'.json');
  if(!term.prefix)return new Set(bucket[term.word]||[]);
  if(bucket[term.word])return new Set(bucket[term.word]);
  const ids=new Set();
  for(const [word,values]of Object.entries(bucket))if(word.startsWith(term.word))for(const id of values)ids.add(id);
  return ids;
 }
 function recordHTML(r){
  const profileButtons=r.pessoas.map(id=>{const p=DATA.pessoas.find(p=>p.id===id);return p?`<button class="local-person" data-local-person="${escape(id)}">Ver perfil de ${escape(p.nome)} →</button>`:''}).join('');
  return `<article class="local-record cat-${r.grupo}"><div class="local-record-meta"><span>${escape(groupNames.get(r.grupo)||'Outro registro')}</span>${r.data?link(r.fonte,'Publicado em '+brDate(r.data)):'<span>Data de publicação não disponível no índice</span>'}</div><h4>${link(r.fonte,`${escape(r.tipo)} ${escape(r.numero)} ↗`)}</h4><p class="local-ementa">${escape(r.ementa||"Resumo não informado no índice oficial")}</p><p class="local-author"><strong>Quem apresentou:</strong> ${escape(r.autores_fonte)}</p>${profileButtons}<p class="source-note">${link(r.fonte,'Ler o documento oficial completo ↗')}</p></article>`;
 }
 async function showRows(m,token){
  const rows=await getRows(currentIds.slice(0,limit),m);if(token!==sequence)return;
  results.innerHTML=rows.map(recordHTML).join('');more.hidden=currentIds.length<=limit;
 }
 function showRepetitions(m,ids){
  const matches=new Set(ids),serviceNames=new Map(m.servicos.map(s=>[s.id,s.nome]));
  const groups=m.repeticoes.filter(g=>g.registros.some(id=>matches.has(id))).sort((a,b)=>(a.rua+' '+a.bairro).localeCompare(b.rua+' '+b.bairro,'pt-BR'));
  if(!groups.length){repeatBox.innerHTML='<p class="unavailable">Nenhum cruzamento com segurança suficiente foi identificado para esta busca. Isso não significa que não existam pedidos repetidos.</p>';return}
  repeatBox.innerHTML='<p class="source-note">As contagens são do grupo completo da rua e do bairro, inclusive outros números ou trechos, e não apenas dos resultados filtrados.</p>'+groups.map(g=>`<details class="repeat-group" data-repeat="${g.id}"><summary><span>${escape(serviceNames.get(g.servico))}<small>${escape(g.rua)} · ${escape(g.bairro)}</small></span>${link(source,`${g.registros.length} ↗`,'repeat-count')}</summary><div class="repeat-body"><p class="source-note">Datas de publicação: ${g.datas_fontes.map(d=>link(d.fonte,brDate(d.data))).join(' · ')}.</p><p class="source-note">Documentos distintos; uma autoria conjunta conta como um único registro.</p><div class="repeat-documents">Abra para carregar os documentos.</div></div></details>`).join('');
  repeatBox.querySelectorAll('.repeat-count').forEach(a=>a.onclick=e=>e.stopPropagation());
  repeatBox.querySelectorAll('.repeat-group').forEach(details=>{
   const g=groups.find(g=>g.id===Number(details.dataset.repeat));let loaded=false;
   details.addEventListener('toggle',async()=>{
    if(!details.open||loaded)return;loaded=true;
    const body=details.querySelector('.repeat-documents');body.textContent='Carregando os documentos…';
    try{const rows=await getRows(g.registros,m);body.innerHTML=rows.map(recordHTML).join('')}
    catch(e){loaded=false;body.textContent='Não foi possível carregar agora. Feche e abra este grupo para tentar novamente.'}
   });
  });
 }
 form.addEventListener('submit',async e=>{
  e.preventDefault();const text=input.value.trim(),terms=queryTerms(text);const token=++sequence;
  if(!terms.length){status.textContent='Digite o nome de um bairro ou uma rua, como Tijuca ou Rua Conde de Bonfim.';area.hidden=true;submit.disabled=false;return}
  status.textContent='Buscando nos resumos oficiais…';area.hidden=true;submit.disabled=true;more.hidden=true;
  try{
   const m=await manifest(),sets=await Promise.all(terms.map(lookup));if(token!==sequence)return;
   sets.sort((a,b)=>a.size-b.size);
   currentIds=[...sets[0]].filter(id=>sets.every(set=>set.has(id))&&(scope.value==='todos'||m.pedidoSet.has(id))).sort((a,b)=>m.rank.get(a)-m.rank.get(b));
   limit=20;await showRows(m,token);if(token!==sequence)return;
   document.querySelector('#local-contagem').innerHTML=link(source,`${currentIds.length} ${currentIds.length===1?'registro encontrado':'registros encontrados'} ↗`)+`<span class="source-note"> · Busca por “${escape(text)}”. Datas mais recentes primeiro; registros sem data ficam ao final.</span>`;
   if(!currentIds.length)results.innerHTML='<p class="unavailable">Nenhum resumo com essas palavras foi encontrado neste filtro. Tente um trecho do nome, outra grafia ou “Todos os tipos de registro”. Isso não prova que não existam pedidos para o local.</p>';
   showRepetitions(m,currentIds);area.hidden=false;
   status.textContent='Busca concluída. Os autores e as fontes estão em cada registro. Os agrupamentos abaixo não informam se o serviço foi realizado.';
   const url=new URL(location.href);url.searchParams.set('local',text);url.searchParams.set('escopo',scope.value);url.hash='busca-local';history.replaceState(null,'',url);
  }catch(error){if(token===sequence)status.textContent='Não foi possível carregar os dados agora. Tente a busca novamente.'}
  finally{if(token===sequence)submit.disabled=false}
 });
 more.onclick=async()=>{more.disabled=true;const token=sequence;limit+=20;try{await showRows(await manifest(),token)}catch(e){status.textContent='Não foi possível carregar mais registros. Tente novamente.'}finally{more.disabled=false}};
 document.querySelectorAll('[data-local-query]').forEach(b=>b.onclick=()=>{input.value=b.dataset.localQuery;form.requestSubmit()});
 scope.onchange=()=>{if(input.value.trim())form.requestSubmit()};
 area.addEventListener('click',e=>{const b=e.target.closest('[data-local-person]');if(b)openPerson(b.dataset.localPerson)});
 const params=new URLSearchParams(location.search);
 if(params.has('local')){input.value=params.get('local');scope.value=params.get('escopo')==='todos'?'todos':'pedidos';form.requestSubmit()}
})();
