'use strict';
const DATA=JSON.parse(document.querySelector('#dados').textContent);
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const official=(url,label,cls='')=>`<a class="${cls}" href="${esc(url)}" target="_blank" rel="noopener">${label}</a>`;
const date=s=>s.split('-').reverse().join('/');
const projectSource='https://www.camara.rio/atividade-parlamentar/processo-legislativo';
const voteSource='https://aplicnt.camara.rj.gov.br/APL/Legislativos/discvot.nsf/anoint?OpenForm&Count=1000';
const people=DATA.pessoas.slice().sort((a,b)=>a.nome.localeCompare(b.nome,'pt-BR'));
const months=DATA.frequencia;
const available=months.filter(m=>m.registros.length);
const defaultMonth=(available.filter(m=>m.mes<new Date(DATA.coletado_em).getMonth()+1).at(-1)||available.at(-1)||months.at(-1));
const proposalsCache=new Map();
const proposalCount=id=>Object.values(DATA.propostas_resumo[id]).reduce((a,b)=>a+b,0);
const votesById=new Map(people.map(p=>[p.id,DATA.votacoes.flatMap(x=>x.votos.filter(v=>v.pessoa===p.id).map(v=>({...x,voto:v.voto}))) ]));
const findPresence=(p,m=defaultMonth)=>m.registros.find(r=>r.pessoa===p.id);
$('#roster-count').innerHTML=`${people.length} vereadores ↗`;
const parties=[...new Set(people.map(p=>p.partido).filter(Boolean))].sort();
parties.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;$('#partido').append(o)});
function render(){
 const query=norm($('#busca').value.trim()),party=$('#partido').value;
 const found=people.filter(p=>norm(p.nome).includes(query)&&(!party||p.partido===party));
 $('#resultados').textContent=found.length===people.length?'Todos os nomes':`${found.length} ${found.length===1?'nome':'nomes'}`;
 $('#vazio').hidden=!!found.length;
 $('#lista').innerHTML=found.map(p=>{
  const f=findPresence(p),counts=DATA.propostas_resumo[p.id],vs=votesById.get(p.id),yes=vs.filter(v=>v.voto==='Sim').length,no=vs.filter(v=>v.voto==='Não').length;
  const faltas=f?`<div class="badge-faltas">${official(defaultMonth.fonte,`<strong>${f.faltas}</strong><span>faltas registradas</span>`)}${official(defaultMonth.fonte,`<strong>${f.abonadas}</strong><span>faltas abonadas</span>`)}${official(defaultMonth.fonte,`<strong>${f.total}</strong><span>após abonos</span>`)}</div>`:'<p class="missing">Sem registro neste mês</p>';
  return `<article class="person radar-badge"><div class="person-head"><span class="badge-slot" aria-hidden="true"></span><div class="badge-identity"><img class="avatar" src="${esc(p.foto)}" alt="" loading="eager" decoding="async" width="84" height="84"><div><button class="name-button" data-person="${p.id}">${esc(p.nome)}</button><span class="party">${esc(p.partido)}</span></div></div></div><div class="badge-body"><div><p class="badge-eyebrow">FALTAS · ${esc(defaultMonth.rotulo.toUpperCase())}</p>${faltas}<p class="badge-small">Valores da tabela oficial. Não equivalem a percentual de presença.</p></div><div><p class="badge-eyebrow">O QUE APRESENTOU · DESDE 2025</p><div class="badge-bar" aria-hidden="true">${DATA.grupos.map(g=>`<i class="cat-${g.id}" style="flex:${Math.max(counts[g.id],1)}"></i>`).join('')}</div><div class="badge-groups">${DATA.grupos.map(g=>`<div class="badge-group cat-${g.id}"><span class="group-dot" aria-hidden="true"></span><button data-person="${p.id}" data-group="${g.id}">${esc(g.nome)}</button>${official(projectSource,`${counts[g.id]} ↗`,'badge-group-count')}</div>`).join('')}</div></div><div><p class="badge-eyebrow">VOTOS IDENTIFICADOS · ${esc(DATA.periodo_votos.toUpperCase())}</p><div class="badge-votes">${official(vs.find(v=>v.voto==='Sim')?.fonte||voteSource,`<strong>${yes}</strong><span>votos sim ↗</span>`,'vote-yes')}${official(vs.find(v=>v.voto==='Não')?.fonte||voteSource,`<strong>${no}</strong><span>votos não ↗</span>`,'vote-no')}</div><p class="badge-small">Somente o período consultado, não o mandato completo.</p></div><button class="open-profile" data-person="${p.id}" aria-label="Ver dados de ${esc(p.nome)}">Abrir ficha e registros →</button><div class="badge-source">${official(p.fonte,'Ficha oficial na Câmara ↗')}</div></div></article>`;
 }).join('');
}
$('#busca').addEventListener('input',render);$('#partido').addEventListener('change',render);
$('#limpar').onclick=()=>{$('#busca').value='';$('#partido').value='';render();$('#busca').focus()};
$('#lista').addEventListener('click',e=>{const b=e.target.closest('[data-person]');if(b)openPerson(b.dataset.person,b.dataset.group||null)});
let activePerson=null,returnFocus=null,loadSequence=0;
function openPerson(id,initialGroup=null){
 const p=people.find(x=>x.id===id);if(!p)return;
 returnFocus=document.activeElement;activePerson=p;
 $('#perfil-conteudo').innerHTML=`<div class="profile-heading"><img class="avatar" src="${esc(p.foto)}" alt="" width="70" height="70"><div><h2 id="perfil-nome">${esc(p.nome)}</h2><p>${esc(p.partido)} · Rio de Janeiro</p></div></div><div class="profile-links">${official(p.fonte,'Perfil na Câmara ↗')}${p.email?`<a href="mailto:${esc(p.email)}">E-mail do gabinete ↗</a>`:''}</div><p class="note">Os períodos abaixo são diferentes. Leia a data antes de comparar informações.</p><section class="profile-section"><h3>Faltas nas sessões</h3><p>O total desconta as faltas justificadas e aceitas pela Câmara.</p><label for="mes-perfil" class="sr-only">Escolher mês das faltas</label><select class="month-select" id="mes-perfil">${months.slice().reverse().map(m=>`<option value="${m.mes}" ${m.mes===defaultMonth.mes?'selected':''}>${esc(m.rotulo)}${m.registros.length?'':' · sem tabela publicada'}</option>`).join('')}</select><div id="presenca-perfil"></div></section><section class="profile-section" id="propostas-secao"><h3>O que apresentou</h3><p>Propostas e ofícios de 2025 e 2026. Inclui autoria e coautoria identificada.</p><p class="note">O agrupamento é deste site e segue a mesma regra para todos. Cada registro entra em um só grupo. <a href="#regra-classificacao" id="ir-regra">Leia a regra completa →</a></p><div id="grupos-perfil" aria-live="polite"><p>Carregando os registros deste vereador…</p></div></section><section class="profile-section"><h3>Como votou</h3><p>Consulta de ${esc(DATA.periodo_votos)}. Veja os votos nominais identificados.</p><p class="note">Um “sim” ou “não” pode se referir a uma proposta, emenda ou outra decisão da sessão. Abra o registro para conferir o que foi votado.</p><div id="votos-perfil"></div></section><p class="source-note">Dados consultados em ${date(DATA.coletado_em.slice(0,10))}. Não encontrar um registro não significa que a pessoa faltou ou não trabalhou.</p>`;
 $('#mes-perfil').addEventListener('change',()=>renderPresence(Number($('#mes-perfil').value)));
 $('#ir-regra').onclick=e=>{e.preventDefault();returnFocus=null;closeProfile();document.querySelector('#regra-classificacao').open=true;document.querySelector('#regra-classificacao').scrollIntoView({behavior:'smooth'})};
 renderPresence(defaultMonth.mes);loadProposals(p.id).then(()=>{if(initialGroup&&activePerson?.id===p.id){const target=$('#grupo-'+initialGroup);if(target){target.open=true;target.scrollIntoView({block:'start'})}}});renderVotes();
 if(!$('#perfil').open){$('#perfil').showModal();document.body.classList.add('modal-open')}
 $('#perfil').scrollTop=0;
 history.replaceState(null,'','#vereador-'+id);
}
function renderPresence(month){
 const m=months.find(x=>x.mes===month),r=findPresence(activePerson,m);
 if(!r){$('#presenca-perfil').innerHTML=`<p class="unavailable">${m.registros.length?'O nome deste vereador não foi identificado na tabela deste mês.':'A Câmara informa que não há dados atualizados para este mês.'} ${official(m.fonte,'Conferir na fonte ↗')}</p>`;return}
 $('#presenca-perfil').innerHTML=`<div class="stat-grid">${official(m.fonte,`<strong>${r.faltas} ↗</strong><span>Faltas registradas</span>`)}${official(m.fonte,`<strong>${r.abonadas} ↗</strong><span>Faltas abonadas</span>`)}${official(m.fonte,`<strong>${r.total} ↗</strong><span>Total após abonos</span>`)}</div><p class="source-note">${m.atualizado_fonte?'Tabela atualizada pela Câmara em '+esc(m.atualizado_fonte)+'. ':''}Pode mudar com novos abonos. ${official(m.fonte,'Abrir tabela oficial ↗')}</p>${m.observacoes?`<details><summary>Observações da Câmara para este mês</summary><p>${esc(m.observacoes)}</p></details>`:''}`;
}
async function loadProposals(id){
 const sequence=++loadSequence;
 try{
  if(!proposalsCache.has(id)){
   const response=await fetch('propostas/'+encodeURIComponent(id)+'.json');
   if(!response.ok)throw new Error('HTTP '+response.status);
   proposalsCache.set(id,await response.json());
  }
  if(sequence!==loadSequence||activePerson.id!==id)return;
  const rows=proposalsCache.get(id);
  const container=$('#grupos-perfil');
  container.innerHTML=DATA.grupos.map(g=>`<details class="proposal-group cat-${g.id}" id="grupo-${g.id}"><summary><span>${esc(g.nome)}</span>${official(projectSource,`${DATA.propostas_resumo[id][g.id]} ↗`,'group-count')}</summary><p class="group-description">${esc(g.descricao)}</p><div class="group-body"></div></details>`).join('')+`<p class="source-note"><a href="propostas/${encodeURIComponent(id)}.json" download>Baixar os registros deste vereador (JSON)</a></p>`;
  container.querySelectorAll('.group-count').forEach(a=>a.onclick=e=>e.stopPropagation());
  DATA.grupos.forEach(g=>{
   const details=$('#grupo-'+g.id),items=rows.filter(r=>r.grupo===g.id);
   let limit=10,query='',ready=false;
   const body=details.querySelector('.group-body');
   function draw(){
    const found=items.filter(r=>norm(r.ementa+' '+r.tipo+' '+r.numero).includes(norm(query)));
    body.querySelector('ul').innerHTML=found.slice(0,limit).map(proposalHTML).join('')||'<li>Nenhum registro encontrado neste grupo para a busca.</li>';
    body.querySelector('button').hidden=found.length<=limit;
   }
   details.addEventListener('toggle',()=>{
    if(!details.open||ready)return;ready=true;
    if(!items.length){body.innerHTML='<p class="unavailable">Nenhum registro deste grupo foi identificado para este nome no período consultado.</p>';return}
    body.innerHTML=`<label for="buscar-${g.id}" class="sr-only">Buscar em ${esc(g.nome)}</label><input type="search" id="buscar-${g.id}" class="list-search" placeholder="Buscar um assunto neste grupo"><ul class="proposal-list"></ul><button class="load-more">Ver mais registros deste grupo</button>`;
    body.querySelector('input').oninput=e=>{query=e.target.value;limit=10;draw()};
    body.querySelector('button').onclick=()=>{limit+=20;draw()};draw();
   });
  });
 }catch(error){
  if(sequence!==loadSequence)return;
  $('#grupos-perfil').innerHTML='<p class="unavailable">Não foi possível carregar a lista agora. Tente novamente ou consulte a fonte oficial.</p><button class="load-more" id="tentar-propostas">Tentar novamente</button>';
  $('#tentar-propostas').onclick=()=>loadProposals(id);
 }
}
function proposalHTML(p){
 let stamp='';
 if(p.publicacao_fonte){const m=p.publicacao_fonte.match(/^(\d{2})\/(\d{2})\/(\d{4})/);if(m)stamp=`<small>Publicado em ${m[2]}/${m[1]}/${m[3]}</small>`}
 return `<li>${official(p.fonte,`${esc(p.tipo)} ${esc(p.numero)} ↗<br>${esc(p.ementa||"Resumo não informado no índice oficial")}`)}<small>Autoria na fonte: ${esc(p.autores_fonte)}</small>${stamp}<details class="classification-reason"><summary>Por que está neste grupo?</summary><p>${esc(p.motivo_grupo)}</p><p>Regra aplicada pelo site ao tipo e à ementa oficiais. Não é uma classificação publicada pela Câmara.</p></details></li>`;
}
function renderVotes(){
 const votes=votesById.get(activePerson.id);
 $('#votos-perfil').innerHTML=votes.length?votes.map(v=>`<div class="vote-item"><div><p>${esc(v.titulo)}</p><small>Sessão de ${date(v.data)}</small><details><summary>Ler o registro desta votação</summary><p>${v.contexto_fonte?official(v.fonte,esc(v.contexto_fonte))+'</p><p>':''}${official(v.fonte,esc(v.trecho))}</p></details></div>${official(v.fonte,`${esc(v.voto)} ↗`,'vote-link')}</div>`).join(''):`<p class="unavailable">Nenhum voto nominal deste nome foi identificado no período consultado. Isso não informa se o vereador estava presente ou ausente. ${official(voteSource,'Consultar registros oficiais ↗')}</p>`;
}
function closeProfile(){ $('#perfil').close(); }
$('#fechar').onclick=closeProfile;
$('#perfil').addEventListener('close',()=>{document.body.classList.remove('modal-open');history.replaceState(null,'','#inicio');if(returnFocus instanceof HTMLElement)returnFocus.focus()});
$('#perfil').addEventListener('click',e=>{if(e.target===$('#perfil')){const r=$('#perfil').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeProfile()}});
$('#metodologia').innerHTML=`<p>Cadastro e faltas consultados em ${date(DATA.coletado_em.slice(0,10))}. Propostas e ofícios: ${esc(DATA.classificacao.periodo)}. Votos: ${esc(DATA.periodo_votos)}.</p><p>${DATA.votacoes_pendencias.length?'Há registro nominal que não pôde ser extraído com segurança. Nem todos os votos do período aparecem.':'Os votos são extraídos das listas nominais identificadas no período.'}</p><p>Foram consultados os tipos oficiais abaixo. As contagens incluem registros com autoria de outros vereadores e do Executivo; cada perfil mostra somente os vinculados ao seu nome.</p><ul>${DATA.classificacao.tipos.map(t=>`<li>${official(t.paginas[0],esc(t.tipo)+' ↗')}</li>`).join('')}</ul><p>Todos os registros coletados receberam um grupo; cada perfil carrega sua lista completa. Registros sem nome vinculado a um vereador atual não são atribuídos a ele.</p>`;

render();
if(/^#vereador-\d+$/.test(location.hash))openPerson(location.hash.replace('#vereador-',''));
