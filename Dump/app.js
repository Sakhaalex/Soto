const { useState, useEffect, useRef } = React;

const STORAGE_KEY = 'soto_data_v1';

// Utilities
function uid(prefix, n) {
  return `${prefix}${String(n).padStart(3,'0')}`;
}

function download(filename, text) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv' }));
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function quoteCsv(s){
  if(s == null) return '';
  const needs = /[",\n]/.test(s);
  return needs ? '"'+String(s).replace(/"/g,'""')+'"' : String(s);
}

function parseCSV(text){
  // simple CSV parser supporting quoted fields
  const rows = [];
  const re = /(?:\s*\n|^)(?:"((?:[^"]|"")*)"|([^",\n]*))(?:,|\n|$)/g;
  let row=[];
  let m;
  let idx=0;
  while(idx<text.length){
    re.lastIndex=idx;
    m=re.exec(text);
    if(!m) break;
    const val = m[1]!==undefined ? m[1].replace(/""/g,'"') : m[2];
    row.push(val);
    idx=re.lastIndex;
    const ch = text[idx-1];
    if(ch==='\n' || idx>=text.length){
      rows.push(row);
      row=[];
    }
  }
  // fallback: simple split if parser failed
  if(rows.length===0){
    const lines = text.split(/\r?\n/).filter(Boolean);
    for(const line of lines){
      const parts = line.split(',');
      rows.push(parts.map(p=>p.trim().replace(/^"|"$/g,'')));
    }
  }
  return rows;
}

function csvToNodes(csvText){
  const rows = parseCSV(csvText);
  if(rows.length<1) return [];
  const headers = rows[0].map(h=>h.trim());
  const nodes = [];
  for(let i=1;i<rows.length;i++){
    const r = rows[i];
    if(r.length===0) continue;
    const obj = {};
    for(let j=0;j<headers.length;j++){
      obj[headers[j]] = r[j]||'';
    }
    nodes.push(obj);
  }
  return nodes;
}

function normalizeNode(n){
  const out = Object.assign({}, n);
  if(out.TYPE) out.TYPE = String(out.TYPE).toUpperCase();
  if(out.STATUS_TAG) out.STATUS_TAG = String(out.STATUS_TAG).toUpperCase();
  if(!out.STATUS_TAG) out.STATUS_TAG = 'PENDING';
  return out;
}

function getNextIdFor(existingNodes, type){
  const prefix = type==='COURSE' ? 'CRS' : type==='UNIT' ? 'UNT' : type==='CO' ? 'CO' : type==='LAB' ? 'LAB' : type==='TUT' ? 'TUT' : type.slice(0,3).toUpperCase();
  let max = 0;
  for(const n of existingNodes){
    if(n.ID && n.ID.startsWith(prefix)){
      const num = parseInt(n.ID.replace(prefix,''),10);
      if(!isNaN(num) && num>max) max=num;
    }
  }
  return prefix + String(max+1).padStart(3,'0');
}

function mergeNodes(existingNodes, incomingNodes){
  const existing = existingNodes.slice();
  const courseMap = {}; // incoming course ID -> existing course ID

  // build quick lookup by code/title
  const existingCourses = existing.filter(n=>n.TYPE==='COURSE');

  function findCourseMatch(incoming){
    const title = (incoming.TITLE||'').toLowerCase();
    const codeMatch = (incoming.TITLE||'').match(/(\d{3,6})/);
    for(const ec of existingCourses){
      if(codeMatch){
        if((ec.TITLE||'').includes(codeMatch[1])) return ec.ID;
      }
      if(((ec.TITLE||'').toLowerCase()).includes(title) || title.includes(((ec.TITLE||'').toLowerCase()))) return ec.ID;
    }
    return null;
  }

  for(const inc of incomingNodes){
    const n = normalizeNode(inc);
    if(n.TYPE==='COURSE'){
      const match = findCourseMatch(n);
      if(match){
        courseMap[n.ID]=match; // map incoming course to existing course
        continue; // skip adding duplicate course
      }
      // ensure unique ID
      if(existing.some(e=>e.ID===n.ID)){
        n.ID = getNextIdFor(existing, 'COURSE');
      }
      existing.push(n);
      existingCourses.push(n);
      courseMap[inc.ID]=n.ID;
    }
  }

  // now add non-course nodes, remapping parent IDs if they point to incoming course IDs
  for(const inc of incomingNodes){
    const n = normalizeNode(inc);
    if(n.TYPE==='COURSE') continue;
    // remap parent id
    if(n.PARENT_ID && courseMap[n.PARENT_ID]) n.PARENT_ID = courseMap[n.PARENT_ID];
    // if parent id empty but a course exists in mapping, try attach to last course added
    if(!n.PARENT_ID){
      // try attach to a matching course by scanning titles for course code
      const codeMatch = (n.DETAILS||n.TITLE||'').match(/(\d{3,6})/);
      if(codeMatch){
        const found = existingCourses.find(ec=> (ec.TITLE||'').includes(codeMatch[1]));
        if(found) n.PARENT_ID = found.ID;
      }
    }
    // ensure unique ID
    if(!n.ID || existing.some(e=>e.ID===n.ID)){
      n.ID = getNextIdFor(existing, n.TYPE || 'UNIT');
    }
    existing.push(n);
  }

  return existing;
}

function nodesToCSV(nodes){
  const headers = ['ID','PARENT_ID','TYPE','TITLE','HOURS_OR_MARKS','DETAILS','STATUS_TAG'];
  const lines = [headers.join(',')];
  for(const n of nodes){
    const row = headers.map(h=>quoteCsv(n[h]||''));
    lines.push(row.join(','));
  }
  return lines.join('\n');
}

// Basic raw syllabus parser
function cleanText(text){ return String(text||'').replace(/\s+/g,' ').trim(); }
function skipLine(text){
  const clean = cleanText(text.replace(/\|/g,' '));
  if(!clean) return true;
  if(clean.startsWith('|')) return true;
  if(/^[-\s|]+$/.test(text)) return true;
  if(/^(Total|Semester|Program Outcomes|Savitribai|Faculty|Syllabus for|Course\s+Name|Teaching|Examination|Credits?)\b/i.test(clean)) return true;
  return false;
}
function parseCourseLine(text){
  const line = String(text).trim().replace(/\|/g,' ');
  if(!line || /^\d{3,6}\s*$/.test(line)) return null;
  if(/^(Total|Semester|Program Outcomes|Savitribai|Faculty|Syllabus for|Course\s+Name|Teaching|Examination|Credits?)\b/i.test(line)) return null;
  const match = line.match(/^(\d{3,6})\s+(.+?)(?:\s{2,}(-|\d+(?:\.\d+)?)(?=\s|$)|$)/);
  if(!match) return null;
  const code = match[1];
  const title = match[2].trim();
  if(title.length < 4) return null;
  const hours = match[3] && match[3] !== '-' ? (match[3].match(/\d/) ? `${match[3]} Hrs` : match[3]) : '';
  return {code,title,hours};
}
function parseUnitLine(text){
  const line = cleanText(text.replace(/\|/g,' '));
  const match = line.match(/^(Unit\s+[IVX\d]+)[:\.]?\s*-?\s*(.*?)(?:\s+(\d+\s*Hrs?)\.?\s*)?$/i);
  if(!match) return null;
  const title = match[1].toUpperCase().replace(/\s+/g,' ').replace(/I{1,3}|V|X/, m => m).trim();
  let tail = match[2].trim();
  if(tail) tail = ': ' + tail;
  return {title: title + tail, hours: match[3] || ''};
}
function parseCoLine(text){
  const line = cleanText(text.replace(/\|/g,' '));
  const match = line.match(/^(CO\s*\d+)[:\)\.-]?\s*(.+)$/i);
  if(!match) return null;
  return {label: match[1].toUpperCase(), text: match[2].trim()};
}
function parseLabLine(text){
  const line = cleanText(text.replace(/\|/g,' '));
  if(/\b(lab|practical|tutorial|tut)\b/i.test(line)) return line;
  return null;
}
function parseRawSyllabus(text){
  const lines = text.split(/\r?\n/);
  const nodes = [];
  let course = null;
  let counters={COURSE:0,UNIT:0,CO:0,LAB:0,TUT:0};
  function next(type){ counters[type]++; return uid(type.slice(0,3)+"", counters[type]); }

  for(let i=0;i<lines.length;i++){
    const raw = lines[i];
    if(!raw) continue;
    if(skipLine(raw)) continue;
    const line = raw.trim();
    const codeLabel = line.match(/(?:Course\s*Code|Code)[:\-]?\s*(\d{3,6})/i);
    if(codeLabel){
      const nextLine = (lines[i+1] || '').trim();
      const titleText = nextLine && !/^\d{3,6}\s+/.test(nextLine) ? cleanText(nextLine) : '';
      const id = 'CRS'+String(counters.COURSE+1).padStart(3,'0'); counters.COURSE++;
      course = {ID:id,PARENT_ID:'',TYPE:'COURSE',TITLE: titleText ? `${codeLabel[1]}: ${titleText}` : `${codeLabel[1]}`,HOURS_OR_MARKS:'',DETAILS:'',STATUS_TAG:'PENDING'};
      nodes.push(course);
      continue;
    }
    const courseMatch = parseCourseLine(line);
    if(courseMatch){
      const id = 'CRS'+String(counters.COURSE+1).padStart(3,'0'); counters.COURSE++;
      course = {ID:id,PARENT_ID:'',TYPE:'COURSE',TITLE:`${courseMatch.code}: ${courseMatch.title}`,HOURS_OR_MARKS:courseMatch.hours,DETAILS:'',STATUS_TAG:'PENDING'};
      nodes.push(course);
      continue;
    }
    if(!course) continue;
    const unitMatch = parseUnitLine(line);
    if(unitMatch){
      const id = 'UNT'+String(counters.UNIT+1).padStart(3,'0'); counters.UNIT++;
      nodes.push({ID:id,PARENT_ID:course.ID,TYPE:'UNIT',TITLE:unitMatch.title,HOURS_OR_MARKS:unitMatch.hours,DETAILS:'',STATUS_TAG:'PENDING'});
      continue;
    }
    const coMatch = parseCoLine(line);
    if(coMatch){
      const id = 'CO'+String(counters.CO+1).padStart(3,'0'); counters.CO++;
      nodes.push({ID:id,PARENT_ID:course.ID,TYPE:'CO',TITLE:coMatch.label,HOURS_OR_MARKS:'',DETAILS:coMatch.text,STATUS_TAG:'PENDING'});
      continue;
    }
    const labMatch = parseLabLine(line);
    if(labMatch){
      const kind = /tutorial|tut/i.test(labMatch) ? 'TUT' : 'LAB';
      const id = kind + String(counters[kind] + 1).padStart(3,'0'); counters[kind]++;
      nodes.push({ID:id,PARENT_ID:course.ID,TYPE:kind,TITLE:labMatch,HOURS_OR_MARKS:'',DETAILS:'',STATUS_TAG:'PENDING'});
      continue;
    }
    if(nodes.length>0){
      const last = nodes[nodes.length-1];
      last.DETAILS = (last.DETAILS ? last.DETAILS + '\n' : '') + cleanText(line);
    }
  }
  return nodes;
}

// Import multiple markdown files from File input
function parseMultipleMarkdownFiles(fileList){
  return Promise.all(Array.from(fileList).map(f => new Promise((res,rej)=>{
    const r = new FileReader();
    r.onload = e => res(parseRawSyllabus(String(e.target.result)));
    r.onerror = rej;
    r.readAsText(f);
  })));
}

// Sample dataset
const SAMPLE = [
  {ID:'CRS001',PARENT_ID:'',TYPE:'COURSE',TITLE:'404193: Innovation and Entrepreneurship',HOURS_OR_MARKS:'3 Hrs',DETAILS:'Fourth Year SPPU',STATUS_TAG:'PENDING'},
  {ID:'CO001',PARENT_ID:'CRS001',TYPE:'CO',TITLE:'CO1',HOURS_OR_MARKS:'',DETAILS:'Understand entrepreneurship basics',STATUS_TAG:'PENDING'},
  {ID:'CO002',PARENT_ID:'CRS001',TYPE:'CO',TITLE:'CO2',HOURS_OR_MARKS:'',DETAILS:'Develop business model',STATUS_TAG:'PENDING'},
  {ID:'UNT001',PARENT_ID:'CRS001',TYPE:'UNIT',TITLE:'Unit I: Entrepreneurship',HOURS_OR_MARKS:'10 Hrs',DETAILS:'Topics A,B',STATUS_TAG:'PENDING'},
  {ID:'CRS002',PARENT_ID:'',TYPE:'COURSE',TITLE:'Digital Business Management',HOURS_OR_MARKS:'3 Hrs',DETAILS:'Fourth Year elective',STATUS_TAG:'PENDING'},
  {ID:'CO003',PARENT_ID:'CRS002',TYPE:'CO',TITLE:'CO1',HOURS_OR_MARKS:'',DETAILS:'Digital strategies',STATUS_TAG:'PENDING'},
];

function App(){
  const [nodes,setNodes] = useState(()=>{
    try{
      const raw = localStorage.getItem(STORAGE_KEY);
      if(raw) return JSON.parse(raw).map(normalizeNode);
    }catch(e){}
    return SAMPLE.map(normalizeNode);
  });
  const [search,setSearch]=useState('');
  const [statusFilter,setStatusFilter]=useState('ALL');
  const [showPaste,setShowPaste]=useState(false);
  const [expandedIds,setExpandedIds] = useState(() => new Set());
  const [expandedGroups,setExpandedGroups] = useState(() => new Set());
  const [scale,setScale] = useState(1);
  const [pan,setPan] = useState({x:0,y:0});
  const [simpleView,setSimpleView] = useState(false);
  const panRef = useRef({dragging:false,startX:0,startY:0,origX:0,origY:0});
  const pasteRef = useRef();
  const svgWrapRef = useRef();

  useEffect(()=>{
    // auto-fit when nodes load or when switching back to SVG view
    if(!simpleView){
      const t = setTimeout(()=>{ fitToView(); }, 120);
      return ()=>clearTimeout(t);
    }
  }, [nodes.length, simpleView]);

  useEffect(()=>{
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nodes));
  },[nodes]);

  function updateNode(id,changes){
    setNodes(ns => ns.map(n=> n.ID===id ? {...n,...changes} : n));
  }

  function toggleStatus(id,tag){
    updateNode(id,{STATUS_TAG:tag});
  }

  function handleImportCSV(file){
    const reader = new FileReader();
    reader.onload = e => {
      try{
        const parsed = csvToNodes(e.target.result);
        setNodes(ns => mergeNodes(ns, parsed));
      }catch(err){
        alert('Failed to parse CSV');
      }
    };
    reader.readAsText(file);
  }

  async function handleImportMDFiles(files){
    try{
      const arrays = await parseMultipleMarkdownFiles(files);
      const incoming = arrays.flat();
      setNodes(ns => mergeNodes(ns, incoming));
    }catch(e){
      console.error(e);
      alert('Failed to import markdown files');
    }
  }

  function handleExport(){
    const csv = nodesToCSV(nodes);
    download('Record.csv', csv);
  }

  function handlePasteImport(){
    const txt = pasteRef.current.value;
    const parsed = parseRawSyllabus(txt);
    if(parsed.length>0){
      setNodes(ns => mergeNodes(ns, parsed));
      setShowPaste(false);
    }else{
      alert('No structured items detected in pasted text');
    }
  }

  function cycleStatus(id){
    const order = ['PENDING','IN_PROGRESS','COMPLETED','X'];
    const n = nodes.find(x=>x.ID===id);
    if(!n) return;
    const idx = order.indexOf(n.STATUS_TAG||'PENDING');
    const next = order[(idx+1)%order.length];
    toggleStatus(id,next);
  }

  function toggleExpand(id){
    setExpandedIds(prev=>{
      const next = new Set(Array.from(prev));
      if(next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }

  function toggleGroup(courseId, group){
    const key = `${courseId}::${group}`;
    setExpandedGroups(prev=>{
      const next = new Set(Array.from(prev));
      if(next.has(key)) next.delete(key); else next.add(key);
      return next;
    });
  }

  function resetView(){
    setScale(1);
    setPan({x:0,y:0});
  }

  function fitToView(){
    try{
      const wrap = svgWrapRef.current;
      if(!wrap) return;
      const rect = wrap.getBoundingClientRect();
      const cw = Math.max(300, rect.width-24);
      const ch = Math.max(200, rect.height-24);
      const s = Math.min(cw/svgWidth, ch/svgHeight) * 0.95;
      const limited = Math.max(0.25, Math.min(2.5, s));
      const px = (cw - (svgWidth*limited))/2;
      const py = (ch - (svgHeight*limited))/2;
      setScale(limited);
      setPan({x: px, y: py});
    }catch(e){
      console.warn('fitToView failed',e);
    }
  }

  function handleWheel(e){
    if(e.ctrlKey) return; // allow ctrl+wheel for browser zoom
    e.preventDefault();
    const delta = -e.deltaY/500;
    setScale(s=>Math.min(3, Math.max(0.4, +(s*(1+delta)).toFixed(3))));
  }

  function onMouseDownPan(e){
    panRef.current.dragging = true;
    panRef.current.startX = e.clientX;
    panRef.current.startY = e.clientY;
    panRef.current.origX = pan.x;
    panRef.current.origY = pan.y;
  }

  function onMouseMovePan(e){
    if(!panRef.current.dragging) return;
    const dx = e.clientX - panRef.current.startX;
    const dy = e.clientY - panRef.current.startY;
    setPan({x: panRef.current.origX + dx, y: panRef.current.origY + dy});
  }

  function onMouseUpPan(){
    panRef.current.dragging = false;
  }

  const courses = nodes.filter(n=>n.TYPE==='COURSE');

  function filteredChildren(parentId){
    return nodes.filter(n=>n.PARENT_ID===parentId && (statusFilter==='ALL' || n.STATUS_TAG===statusFilter) && (search==='' || (n.TITLE||'').toLowerCase().includes(search.toLowerCase()) || (n.DETAILS||'').toLowerCase().includes(search.toLowerCase()) || (n.ID||'').toLowerCase().includes(search.toLowerCase())));
  }

  function typeBadgeColor(type){
    switch(type){
      case 'COURSE': return 'bg-indigo-600';
      case 'UNIT': return 'bg-blue-500';
      case 'CO': return 'bg-emerald-500';
      case 'LAB': return 'bg-amber-400 text-black';
      case 'TUT': return 'bg-purple-500';
      default: return 'bg-slate-500';
    }
  }

  // layout for SVG flow
  const nodeW = 260, nodeH = 72, hSpacing = 48, vSpacing = 18;
  const maxChildren = Math.max(0, ...courses.map(c=> filteredChildren(c.ID).length));
  const svgWidth = Math.max(900, courses.length*(nodeW+hSpacing)+100);
  const svgHeight = Math.max(240, 140 + maxChildren*(nodeH+vSpacing));

  return React.createElement('div', {className:'p-6 min-h-screen'},
    React.createElement('header', {className:'mb-6'},
      React.createElement('div',{className:'nav-bar card-shadow p-4 rounded-lg flex items-center gap-4'},
      React.createElement('input',{placeholder:'Search title, ID or details',className:'flex-1 p-2 rounded bg-card text-slate-100 border border-slate-700',value:search,onChange:e=>setSearch(e.target.value)}),
      React.createElement('select',{value:statusFilter,onChange:e=>setStatusFilter(e.target.value),className:'p-2 rounded bg-card'},
        React.createElement('option', {value:'ALL'}, 'ALL'),
        React.createElement('option', {value:'COMPLETED'}, 'COMPLETED'),
        React.createElement('option', {value:'IN_PROGRESS'}, 'IN_PROGRESS'),
        React.createElement('option', {value:'PENDING'}, 'PENDING'),
        React.createElement('option', {value:'X'}, 'X')),
      React.createElement('label', {className:'bg-card p-2 rounded cursor-pointer flex items-center gap-2'},
        React.createElement('input',{type:'file',accept:'.csv',style:{display:'none'},onChange:e=>{if(e.target.files[0]) handleImportCSV(e.target.files[0])}}), React.createElement('span',null,'📁 Load CSV')),
      React.createElement('label', {className:'bg-card p-2 rounded cursor-pointer flex items-center gap-2'},
        React.createElement('input',{type:'file',accept:'.md',multiple:true,style:{display:'none'},onChange:e=>{if(e.target.files.length) handleImportMDFiles(e.target.files)}}), React.createElement('span',null,'📄 Load MDs')),
      React.createElement('div', {className:'flex gap-2'},
        React.createElement('button',{className:'bg-card p-2 rounded',onClick:()=>setScale(s=>Math.min(3, +(s*1.2).toFixed(2)))}, 'Zoom +'),
        React.createElement('button',{className:'bg-card p-2 rounded',onClick:()=>setScale(s=>Math.max(0.25, +(s/1.2).toFixed(2)))}, 'Zoom -'),
        React.createElement('button',{className:'bg-card p-2 rounded',onClick:fitToView}, 'Fit'),
        React.createElement('button',{className:'bg-card p-2 rounded',onClick:resetView}, 'Reset')
      ),
      React.createElement('label',{className:'flex items-center gap-2 text-sm'},
        React.createElement('input',{type:'checkbox',checked:simpleView,onChange: e=> setSimpleView(e.target.checked)}), React.createElement('span',null,'Simple Flow')
      ),
      React.createElement('button',{className:'bg-card p-2 rounded',onClick:()=>setShowPaste(true)}, '📋 Paste Raw Syllabus'),
      React.createElement('button',{className:'bg-card p-2 rounded',onClick:handleExport}, '💾 Export CSV')
      )
    ),
    ),
    React.createElement('main', null,
      courses.length===0 ? React.createElement('div', null, 'No courses loaded') : (
        simpleView ? React.createElement('div',{className:'space-y-4'},
          courses.map(c=> React.createElement('div',{key:c.ID, className:'p-3 rounded bg-card border border-slate-700'},
            React.createElement('div',{className:'flex items-center justify-between'},
              React.createElement('div',null, React.createElement('div',{className:'font-bold text-slate-100'}, c.TITLE), React.createElement('div',{className:'text-slate-400 text-sm'}, c.ID+' • '+c.HOURS_OR_MARKS)),
              React.createElement('div',null,
                React.createElement('button',{className:'bg-card p-2 rounded mr-2',onClick:()=>toggleExpand(c.ID)}, expandedIds.has(c.ID)?'Collapse':'Expand'),
                React.createElement('button',{className:'bg-card p-2 rounded',onClick:()=>cycleStatus(c.ID)}, c.STATUS_TAG)
              )
            ),
            expandedIds.has(c.ID) && React.createElement('div',{className:'mt-2 space-y-2'},
              filteredChildren(c.ID).map(ch=> React.createElement('div',{key:ch.ID, className:'p-2 rounded bg-[#021025] flex items-center justify-between'}, React.createElement('div',null, React.createElement('div',{className:'font-semibold text-slate-100'}, ch.TITLE), React.createElement('div',{className:'text-slate-400 text-xs'}, ch.ID+' • '+ch.TYPE)), React.createElement('div',null, React.createElement('button',{className:'bg-card p-1 rounded',onClick:()=>cycleStatus(ch.ID)}, ch.STATUS_TAG))))
            )
          )) : React.createElement('div', {className:'overflow-auto rounded', style:{background:'#071124',padding:12}},
          React.createElement('div',{ref:svgWrapRef, onWheel:handleWheel,onMouseDown:onMouseDownPan,onMouseMove:onMouseMovePan,onMouseUp:onMouseUpPan,onMouseLeave:onMouseUpPan,style:{overflow:'hidden'}},
            React.createElement('svg',{width:'100%',viewBox:`0 0 ${svgWidth} ${svgHeight}`,xmlns:'http://www.w3.org/2000/svg',style:{background:'#071124', borderRadius:8}},
            React.createElement('g',{transform:`translate(${pan.x},${pan.y}) scale(${scale})`},
          // dynamic layout per course with collapsible groups
          ...courses.flatMap((c,ci)=>{
            const cx = 50 + ci*(nodeW+hSpacing);
            let y = 20;
            const elems = [];
            const statusColor = c.STATUS_TAG==='COMPLETED' ? '#16a34a' : c.STATUS_TAG==='IN_PROGRESS' ? '#f59e0b' : '#475569';
            // course node with expand icon
            elems.push(React.createElement('g',{key:`course-${c.ID}`, transform:`translate(${cx},${y})`, style:{cursor:'pointer'}},
              React.createElement('rect',{x:0,y:0,width:nodeW,height:nodeH,rx:10,fill:'#0f172a',stroke: statusColor, strokeWidth:2}),
              React.createElement('text',{x:12,y:20,fill:'#e6eef8',fontSize:14,fontWeight:700}, c.TITLE.substring(0,60)),
              React.createElement('text',{x:12,y:40,fill:'#94a3b8',fontSize:12}, c.ID+' • '+c.HOURS_OR_MARKS),
              React.createElement('rect',{x:nodeW-36,y:18,width:24,height:24,rx:6,fill:'#0b1220',stroke:'#334155',onClick:(e)=>{e.stopPropagation(); toggleExpand(c.ID);}}),
              React.createElement('text',{x:nodeW-28,y:36,fill:'#94a3b8',fontSize:14,fontWeight:700, onClick:(e)=>e.stopPropagation()}, expandedIds.has(c.ID)?'-':'+')
            ));
            y += nodeH + 12;

            if(expandedIds.has(c.ID)){
              const children = filteredChildren(c.ID);
              const groups = {};
              for(const ch of children){
                const g = ch.TYPE || 'OTHER';
                groups[g] = groups[g]||[];
                groups[g].push(ch);
              }
              const groupOrder = ['UNIT','CO','LAB','TUT','OTHER'];
              for(const g of groupOrder){
                if(!groups[g] || groups[g].length===0) continue;
                const key = `${c.ID}::${g}`;
                // group header box
                elems.push(React.createElement('g',{key:`group-${c.ID}-${g}`, transform:`translate(${cx+20},${y})`, style:{cursor:'pointer'}, onClick:()=>toggleGroup(c.ID,g)},
                  React.createElement('rect',{x:0,y:0,width:nodeW-40,height:40,rx:8,fill:'#071226',stroke:'#293241'}),
                  React.createElement('text',{x:10,y:24,fill:'#cbd5e1',fontSize:13,fontWeight:700}, g+' ('+groups[g].length+')'),
                  React.createElement('text',{x:nodeW-72,y:24,fill:'#94a3b8',fontSize:12}, expandedGroups.has(key)?'v':'>')
                ));
                y += 44;
                if(expandedGroups.has(key)){
                  for(const ch of groups[g]){
                    const statusColorCh = ch.STATUS_TAG==='COMPLETED' ? '#16a34a' : ch.STATUS_TAG==='IN_PROGRESS' ? '#f59e0b' : '#475569';
                    // outer group positions the item, inner g handles animation
                    const anim = {transform: 'translateY(0px)', opacity: 1};
                    elems.push(React.createElement('g',{key:`item-${ch.ID}`, transform:`translate(${cx+40},${y})`},
                      React.createElement('g',{className:'svg-anim', style:Object.assign({cursor:'pointer'}, anim), onClick:()=>cycleStatus(ch.ID)},
                        React.createElement('rect',{x:0,y:0,width:nodeW-80,height:56,rx:6,fill:'#071226',stroke:statusColorCh}),
                        React.createElement('text',{x:8,y:22,fill:'#e6eef8',fontSize:12,fontWeight:600}, ch.TITLE.substring(0,50)),
                        React.createElement('text',{x:8,y:40,fill:'#94a3b8',fontSize:11}, ch.ID+' • '+ch.TYPE)
                      )
                    ));
                    y += 64;
                  }
                } else {
                  // collapsed: still render with hidden/translated style for smooth collapse animation
                  for(const ch of groups[g]){
                    const statusColorCh = ch.STATUS_TAG==='COMPLETED' ? '#16a34a' : ch.STATUS_TAG==='IN_PROGRESS' ? '#f59e0b' : '#475569';
                    const anim = {transform: 'translateY(-8px)', opacity: 0};
                    elems.push(React.createElement('g',{key:`item-${ch.ID}`, transform:`translate(${cx+40},${y})`},
                      React.createElement('g',{className:'svg-anim', style:Object.assign({cursor:'pointer'}, anim)},
                        React.createElement('rect',{x:0,y:0,width:nodeW-80,height:56,rx:6,fill:'#071226',stroke:statusColorCh}),
                        React.createElement('text',{x:8,y:22,fill:'#e6eef8',fontSize:12,fontWeight:600}, ch.TITLE.substring(0,50)),
                        React.createElement('text',{x:8,y:40,fill:'#94a3b8',fontSize:11}, ch.ID+' • '+ch.TYPE)
                      )
                    ));
                    y += 64;
                  }
                }
              }
            }

            return elems;
          })
          )
        )
      )
    ),
    showPaste && React.createElement('div',{className:'fixed inset-0 flex items-center justify-center bg-black/60'},
      React.createElement('div',{className:'w-full max-w-2xl p-4 rounded-lg',style:{background:'#0f172a'}},
        React.createElement('h3', {className:'text-lg font-bold mb-2'}, 'Paste Raw Syllabus Markdown'),
        React.createElement('textarea',{ref:pasteRef,rows:12,className:'w-full p-2 bg-card rounded text-slate-100 mb-2',placeholder:'Paste syllabus here...'}),
        React.createElement('div',{className:'flex justify-end gap-2'},
          React.createElement('button',{className:'bg-card p-2 rounded',onClick:()=>setShowPaste(false)}, 'Cancel'),
          React.createElement('button',{className:'bg-emerald-600 p-2 rounded',onClick:handlePasteImport}, 'Import')
        )
      )
    )
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
