'use strict';
(()=>{
 const format=n=>new Intl.NumberFormat('pt-BR').format(n);
 const source='https://www.camara.rio/atividade-parlamentar/processo-legislativo';
 const glyphs={melhorias:'<path d="m3 11 9-8 9 8M6 9v12h12V9M10 21v-7h4v7"/>',cobrancas:'<path d="M4 4h16v12H9l-5 5V4Z"/><path d="M8 8h8M8 12h5"/>',homenagens:'<circle cx="12" cy="8" r="5"/><path d="m8 12-2 10 6-3 6 3-2-10"/>',leis:'<path d="M6 3h9l4 4v14H6V3ZM14 3v5h5M9 12h7M9 16h7"/>',outros:'<circle cx="5" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="19" cy="12" r="1.2"/>'};
 const icon=g=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${glyphs[g]}</svg>`;
 const totals=DATA.classificacao.por_grupo;
 document.querySelector('#hero-total').textContent=format(DATA.classificacao.total_documentos)+' ↗';
 const stats=[['melhorias',totals.melhorias,'pedidos de melhoria'],['homenagens',totals.homenagens,'homenagens'],['leis',totals.leis,'outras propostas de lei'],['outros',DATA.pessoas.length,'vereadores na consulta']];
 document.querySelector('#hero-stats').innerHTML=stats.map(([g,n,label])=>`<a href="${g==='outros'?esc(DATA.cadastro_fonte):source}" target="_blank" rel="noopener" class="radar-stat cat-${g}"><strong>${format(n)}</strong><span>${label} ↗</span></a>`).join('');
 document.querySelector('#group-bar').innerHTML=DATA.grupos.map(g=>`<a class="cat-${g.id}" href="${source}" target="_blank" rel="noopener" style="flex:${totals[g.id]}" aria-label="${esc(g.nome)}: ${totals[g.id]} registros, fonte oficial"></a>`).join('');
 document.querySelector('#global-groups').innerHTML=DATA.grupos.map(g=>`<article class="global-category cat-${g.id}"><div class="category-top"><span class="category-icon">${icon(g.id)}</span>${official(source,format(totals[g.id])+' ↗','category-number')}<h3>${esc(g.nome)}</h3></div><p>${esc(g.descricao)}</p><button data-global-group="${g.id}">Ler os registros →</button></article>`).join('');
 const dialog=document.querySelector('#grupo-dialog');let groupFocus=null,currentGroup=null,allIds=[],visibleIds=[],shown=15,serial=0,groupIndex=null;
 const buckets=new Map(),pages=new Map();
 async function fetchJSON(url){const r=await fetch(url);if(!r.ok)throw new Error('Dados indisponíveis');return r.json()}
 function cache(map,key,url){if(!map.has(key))map.set(key,fetchJSON(url).catch(e=>{map.delete(key);throw e}));return map.get(key)}
 async function records(ids){
  const pending=[...new Set(ids.map(id=>Math.floor(id/250)))];let cursor=0;
  await Promise.all(Array.from({length:Math.min(4,pending.length)},async()=>{while(cursor<pending.length){const page=pending[cursor++];await cache(pages,page,'busca/registros/'+page+'.json')}}));
  return Promise.all(ids.map(async id=>(await pages.get(Math.floor(id/250)))[id%250]));
 }
 function item(r){return `<article class="local-record cat-${r.grupo}"><div class="local-record-meta"><span>${esc(r.tipo)}</span>${r.data?official(r.fonte,date(r.data)):'<span>Data não disponível no índice</span>'}</div><h3>${official(r.fonte,esc(r.tipo)+' '+esc(r.numero)+' ↗')}</h3><p class="local-ementa">${esc(r.ementa||"Resumo não informado no índice oficial")}</p><p class="local-author"><strong>Autoria na fonte:</strong> ${esc(r.autores_fonte)}</p><p>${official(r.fonte,'Abrir na Câmara ↗','ext-link')}</p></article>`}
 async function draw(token){
  const rows=await records(visibleIds.slice(0,shown));if(token!==serial)return;
  document.querySelector('#grupo-dialog-lista').innerHTML=rows.map(item).join('')||'<p class="unavailable">Nenhum registro encontrado para esta busca neste grupo.</p>';
  document.querySelector('#grupo-dialog-mais').hidden=visibleIds.length<=shown;
 }
 async function openGroup(id){
  const g=DATA.grupos.find(g=>g.id===id);if(!g)return;const token=++serial;currentGroup=g;groupFocus=document.activeElement;
  dialog.className='cat-'+id;
  document.querySelector('#grupo-dialog-title').textContent=g.nome;
  document.querySelector('#grupo-dialog-info').innerHTML=`${official(source,format(totals[id])+' registros ↗')} · ${esc(DATA.classificacao.periodo)}. ${esc(g.descricao)}<br><small>Agrupamento automático deste site. O tipo oficial e a autoria aparecem em cada item.</small>`;
  document.querySelector('#grupo-dialog-busca').value='';document.querySelector('#grupo-dialog-lista').textContent='Carregando registros…';document.querySelector('#grupo-dialog-mais').hidden=true;
  dialog.showModal();document.body.classList.add('modal-open');
  try{if(!groupIndex)groupIndex=await fetchJSON('grupos-indice.json');if(token!==serial)return;allIds=groupIndex[id];visibleIds=allIds;shown=15;await draw(token)}
  catch(e){if(token===serial)document.querySelector('#grupo-dialog-lista').textContent='Não foi possível carregar a lista. Feche e abra o grupo para tentar novamente.'}
 }
 document.querySelector('#global-groups').onclick=e=>{const b=e.target.closest('[data-global-group]');if(b)openGroup(b.dataset.globalGroup)};
 document.querySelector('#grupo-fechar').onclick=()=>dialog.close();
 dialog.addEventListener('close',()=>{serial++;document.body.classList.remove('modal-open');if(groupFocus instanceof HTMLElement)groupFocus.focus()});
 let timer;
 document.querySelector('#grupo-dialog-busca').oninput=e=>{
  const query=e.target.value;clearTimeout(timer);timer=setTimeout(async()=>{
   const token=++serial;document.querySelector('#grupo-dialog-lista').textContent='Buscando…';
   try{
    const words=[...new Set(norm(query).match(/[a-z0-9]+/g)||[])].filter(w=>!['a','o','as','os','de','da','do','das','dos','e','em','no','na'].includes(w));
    if(words.length){
     const sets=await Promise.all(words.map(async w=>{const index=await cache(buckets,w[0],'busca/indice/'+w[0]+'.json');return new Set(index[w]||[])}));
     if(token!==serial)return;visibleIds=allIds.filter(id=>sets.every(s=>s.has(id)));
    }else visibleIds=allIds;
    shown=15;await draw(token);
   }catch(e){if(token===serial)document.querySelector('#grupo-dialog-lista').textContent='Não foi possível carregar a busca agora.'}
  },250);
 };
 document.querySelector('#grupo-dialog-mais').onclick=async e=>{e.target.disabled=true;try{shown+=20;await draw(serial)}finally{e.target.disabled=false}};
 fetchJSON('bussola-resumo.json').then(data=>{
  const names=new Map(data.servicos.map(s=>[s.id,s.nome]));
  document.querySelector('#repeat-overview').innerHTML=data.repeticoes.map(g=>`<article class="street-example"><div class="street-count">${official(source,format(g.registros.length))}<small>REGISTROS</small></div><div><h3>${esc(g.rua)}</h3><p>${esc(g.bairro)}</p></div><div class="street-service">${esc(names.get(g.servico))}</div><p class="street-dates">Publicações de ${official(g.datas_fontes[0].fonte,date(g.datas[0]))} a ${official(g.datas_fontes.at(-1).fonte,date(g.datas.at(-1)))}.</p><button data-street="${esc(g.rua)} ${esc(g.bairro)}">Ver pedidos e datas →</button></article>`).join('');
  document.querySelector('#repeat-overview').onclick=e=>{const b=e.target.closest('[data-street]');if(!b)return;document.querySelector('#local-termo').value=b.dataset.street;document.querySelector('#local-escopo').value='pedidos';document.querySelector('#form-local').requestSubmit();document.querySelector('#busca-local').scrollIntoView({behavior:'smooth'})};
 }).catch(()=>{document.querySelector('#repeat-overview').innerHTML='<p class="source-note">Os cruzamentos estão disponíveis pela busca de bairro ou rua.</p>'});
})();
