see the update is still not working plus not the dialog I want the features I told to be modified in my program html for u : <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Operations Co-pilot</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script> 
    <script> 
        window.SOTO_SERVER_URL = ""; 
        window.sotoFileData = []; 
         
        function loadScript(src) { 
            return new Promise((resolve) => { 
                const script = document.createElement('script'); 
                script.src = src + "?t=" + new Date().getTime(); 
                script.onload = () => resolve(true); 
                script.onerror = () => resolve(false); 
                document.head.appendChild(script); 
            }); 
        } 
    </script> 
    <script> 
        tailwind.config = { 
            theme: { 
                extend: { 
                    fontFamily: { 
                        sans: ['Plus Jakarta Sans', 'sans-serif'], 
                        mono: ['JetBrains Mono', 'monospace'], 
                    } 
                } 
            } 
        } 
    </script> 
    <style> 
        body { 
            background-color: #FFFFFF; 
            font-family: 'Plus Jakarta Sans', sans-serif; 
        } 
        /* Custom scrollbar */ 
        ::-webkit-scrollbar { 
            width: 6px; 
            height: 6px; 
        } 
        ::-webkit-scrollbar-track { 
            background: transparent; 
        } 
        ::-webkit-scrollbar-thumb { 
            background: #cbd5e1; 
            border-radius: 4px; 
        } 
        ::-webkit-scrollbar-thumb:hover { 
            background: #94a3b8; 
        } 
        .animate-fade-in { 
            animation: fadeIn 0.2s ease-out; 
        } 
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(4px); } 
            to { opacity: 1; transform: translateY(0); } 
        } 
    </style> 
</head> 
<body class="min-h-screen flex flex-col text-slate-800 bg-white"> 
 
    <!-- Top Navigation Bar / Large Search Section --> 
    <header class="bg-white border-b border-slate-100 sticky top-0 z-50 px-6 py-4 shadow-sm"> 
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6"> 
            <div class="flex items-center gap-3 shrink-0"> 
                <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center font-bold text-white shadow-md shadow-blue-500/20 text-xl"> 
                    📁 
                </div> 
                <div> 
                    <h1 class="text-xl font-extrabold tracking-tight text-slate-900">SOTO File Co-pilot</h1> 
                    <p class="text-[11px] text-slate-400 font-medium">Deterministic File Dictionary & Operations</p> 
                </div> 
            </div> 
             
            <!-- Large Prominent Blue Search Bar --> 
            <div class="flex-1 w-full max-w-3xl relative"> 
                <input type="text" id="searchBar" placeholder="Search files, extensions, folders, paths..."  
                    class="w-full pl-6 pr-12 py-3.5 rounded-2xl text-slate-900 bg-slate-50 border-2 border-transparent focus:border-blue-500 focus:bg-white focus:outline-none shadow-sm focus:ring-4 focus:ring-blue-500/10 transition-all text-base" 
                    oninput="filterData()"> 
                <span class="absolute right-5 top-4.5 text-slate-400 text-lg">🔍</span> 
            </div> 
             
            <div class="flex items-center gap-2"> 
                <button onclick="triggerUpdate()" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-5 rounded-xl shadow-sm hover:shadow transition-all flex items-center gap-2 text-sm"> 
                    <span>🔄</span> Update Matrix 
                </button> 
            </div> 
        </div> 
    </header> 
 
    <!-- Main Content Area --> 
    <div class="flex flex-1 overflow-hidden max-w-7xl w-full mx-auto"> 
         
        <!-- Left panel: Filters, Tree & Path Management --> 
        <aside class="w-80 border-r border-slate-100 p-6 overflow-y-auto flex flex-col gap-6 bg-slate-50/50"> 
             
            <!-- Target Directories Manager --> 
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 
                <div class="flex justify-between items-center mb-3"> 
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Targets List</h3> 
                    <button onclick="browseNewFolder()" class="text-xs text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-0.5"> 
                        ➕ Add Folder 
                    </button> 
                </div> 
                <div id="targetPathsContainer" class="space-y-1 max-h-40 overflow-y-auto pr-1"> 
                    <!-- Target paths loaded here --> 
                    <div class="text-xs text-slate-400 italic">No target paths configured.</div> 
                </div> 
            </div> 
 
            <!-- Stats Dashboard summary --> 
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Indexed Stats</h3> 
                <div class="grid grid-cols-2 gap-3 mb-4"> 
                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100"> 
                        <span class="block text-[10px] text-slate-400 font-bold uppercase">Total Files</span> 
                        <span id="statFiles" class="text-lg font-extrabold text-slate-800">0</span> 
                    </div> 
                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100"> 
                        <span class="block text-[10px] text-slate-400 font-bold uppercase">Total Folders</span> 
                        <span id="statFolders" class="text-lg font-extrabold text-slate-800">0</span> 
                    </div> 
                </div> 
                <h4 class="text-xs font-bold text-slate-500 mb-2">Top Extensions</h4> 
                <div id="extensionFilters" class="flex flex-wrap gap-1.5"> 
                    <!-- Dynamic extension tags --> 
                </div> 
            </div> 
 
            <!-- Folder Reconstitution Tools --> 
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Recreate Folder Tree</h3> 
                <div class="space-y-3"> 
                    <div> 
                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Source Folder</label> 
                        <input type="text" id="recreateSrc" placeholder="e.g. C:\Users\..." class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 
                    </div> 
                    <div> 
                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Destination Target</label> 
                        <input type="text" id="recreateDest" placeholder="e.g. D:\ClonedFolder" class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 
                    </div> 
                    <button onclick="triggerRecreateStructure()" class="w-full bg-slate-800 hover:bg-slate-900 text-white font-bold py-2 rounded-lg text-xs transition"> 
                        🛠️ Clone Empty Folders Structure 
                    </button> 
                </div> 
            </div> 
 
            <!-- Advanced Segregation Tools --> 
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Advanced Segregation</h3> 
                <div class="space-y-3"> 
                    <div> 
                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Source Directory</label> 
                        <input type="text" id="segSrc" placeholder="e.g. C:\Downloads" class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 
                    </div> 
                    <div> 
                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Destination Directory</label> 
                        <input type="text" id="segDest" placeholder="e.g. C:\Sorted" class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 
                    </div> 
                    <div class="grid grid-cols-2 gap-2"> 
                        <div> 
                            <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Rule Type</label> 
                            <select id="segRuleType" class="w-full text-xs px-2 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 
                                <option value="extension">Extension</option> 
                                <option value="size">Size (>= MB)</option> 
                                <option value="date">Age (>= Days)</option> 
                            </select> 
                        </div> 
                        <div> 
                            <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Value</label> 
                            <input type="text" id="segRuleVal" placeholder=".pdf or 10 or 30" class="w-full text-xs px-2 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 
                        </div> 
                    </div> 
                    <button onclick="triggerAdvancedSegregation()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg text-xs transition"> 
                        📦 Execute Segregate Move 
                    </button> 
                </div> 
            </div> 
 
            <!-- Optional Directory Tree Collapsible Section --> 
            <div> 
                <div class="flex justify-between items-center mb-3"> 
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Directory Navigation</h3> 
                    <button onclick="toggleTreeCollapse()" class="text-xs text-blue-600 hover:underline">Toggle Tree</button> 
                </div> 
                <div id="treeWrapper" class="transition-all duration-200 max-h-[300px] overflow-y-auto"> 
                    <div id="treeContainer" class="text-xs font-mono text-slate-600 space-y-1"></div> 
                </div> 
            </div> 
 
        </aside> 
 
        <!-- Right / Main panel: File Card List --> 
        <main class="flex-1 p-6 overflow-y-auto bg-slate-50 flex flex-col"> 
            <div id="searchHeading" class="mb-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Showing Search Results</div> 
             
            <div id="resultsGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"> 
                <!-- Dynamically populated cards --> 
            </div> 
             
            <div id="emptyState" class="hidden flex-1 flex-col items-center justify-center py-20 text-center"> 
                <span class="text-5xl mb-4">🔍</span> 
                <h3 class="text-lg font-bold text-slate-700">No matching files found</h3> 
                <p class="text-sm text-slate-400 max-w-sm mt-1">Try refining your filters or verify your directories are indexed in the target list.</p> 
            </div> 
        </main> 
 
    </div> 
 
    <!-- Script Layer --> 
    <script> 
        let allItems = []; 
        let targetsList = []; 
 
        window.onload = async () => { 
            // Dynamically load scripts with cache busting before initializing 
            await loadScript('server_config.js'); 
            await loadScript('file_data.js'); 
 
            loadTargets(); 
            if (window.sotoFileData && window.sotoFileData.length > 0) { 
                parseLoadedData(window.sotoFileData); 
            } else { 
                fetch('File.csv') 
                    .then(res => { 
                        if (!res.ok) throw new Error("CSV file not found"); 
                        return res.text(); 
                    }) 
                    .then(parseCSV) 
                    .catch(err => { 
                        console.error("Could not load File.csv:", err); 
                        document.getElementById('resultsGrid').innerHTML = ''; 
                        document.getElementById('emptyState').classList.remove('hidden'); 
                    }); 
            } 
        }; 
 
        // Helper to check if server config is active 
        function getApiUrl() { 
            return window.SOTO_SERVER_URL ? window.SOTO_SERVER_URL + '/api' : '/api'; 
        } 
 
        // Load targets from backend json or localStorage fallback 
        async function loadTargets() { 
            let serverSuccess = false; 
            try { 
                const res = await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ action: "get_targets" }) 
                }); 
                const data = await res.json(); 
                if(data.status === "success" && data.targets) { 
                    targetsList = data.targets; 
                    localStorage.setItem('soto_targets', JSON.stringify(targetsList)); 
                    serverSuccess = true; 
                } 
            } catch(e) { 
                console.warn("Could not reach Python API server. Using localStorage fallback."); 
            } 
 
            if (!serverSuccess) { 
                const localTargets = localStorage.getItem('soto_targets'); 
                if (localTargets) { 
                    targetsList = JSON.parse(localTargets); 
                } 
            } 
            renderTargets(); 
        } 
 
        function renderTargets() { 
            const container = document.getElementById('targetPathsContainer'); 
            if(targetsList.length === 0) { 
                container.innerHTML = `<div class="text-xs text-slate-400 italic">No target paths configured.</div>`; 
                return; 
            } 
            container.innerHTML = targetsList.map(t => ` 
                <div class="flex items-center justify-between gap-2 p-1.5 hover:bg-slate-100 rounded-lg group transition-all"> 
                    <span class="text-xs font-mono text-slate-600 truncate flex-1" title="${t}">${t}</span> 
                    <button onclick="removeTarget('${t.replace(/\\/g, '\\\\')}')" class="text-slate-400 hover:text-red-500 text-xs font-bold px-1 rounded transition opacity-0 group-hover:opacity-100">❌</button> 
                </div> 
            `).join(''); 
        } 
 
        async function browseNewFolder() { 
            // Since the user prefers zero-server architecture, we skip any backend calls. 
            // Prompt user for a folder path manually. 
            const path = prompt("Enter target directory path (e.g., X:\\Alexander):"); 
            if (!path) return; // User cancelled. 
            const normalized = path.trim(); 
            if (!normalized) return; 
            // Update localStorage targets list. 
            let targets = []; 
            const stored = localStorage.getItem('soto_targets'); 
            if (stored) { 
                try { targets = JSON.parse(stored); } catch(e) { targets = []; } 
            } 
            if (!targets.includes(normalized)) { 
                targets.push(normalized); 
                localStorage.setItem('soto_targets', JSON.stringify(targets)); 
            } 
            // Update global variable and UI. 
            targetsList = targets; 
            renderTargets(); 
            // Also set the source fields for other tools. 
            document.getElementById('recreateSrc').value = normalized; 
            document.getElementById('segSrc').value = normalized; 
        } 
 
        async function removeTarget(path) { 
            try { 
                await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ action: "remove_target", path: path }) 
                }); 
            } catch(e) { 
                console.warn("Could not reach Python API server to remove target:", e); 
            } 
            targetsList = targetsList.filter(t => t !== path); 
            localStorage.setItem('soto_targets', JSON.stringify(targetsList)); 
            renderTargets(); 
        } 
 
        // CSV parsing with quoting support 
        function parseCSVLine(text) { 
            let p = '', c = []; 
            let insideQuote = false; 
            for (let i = 0; i < text.length; i++) { 
                let char = text[i]; 
                if (char === '"') { 
                    insideQuote = !insideQuote; 
                } else if (char === ',' && !insideQuote) { 
                    c.push(p); 
                    p = ''; 
                } else { 
                    p += char; 
                } 
            } 
            c.push(p); 
            return c.map(val => { 
                val = val.trim(); 
                if (val.startsWith('"') && val.endsWith('"')) { 
                    val = val.substring(1, val.length - 1); 
                } 
                return val; 
            }); 
        } 
 
        function parseCSV(csvText) { 
            allItems = []; 
            const lines = csvText.split('\n'); 
            let exts = {}; 
            let fileCount = 0; 
            let folderCount = 0; 
 
            for(let i = 1; i < lines.length; i++) { 
                const line = lines[i].trim(); 
                if(!line) continue; 
                 
                const cols = parseCSVLine(line); 
                if(cols.length < 2 || cols[0] === 'CHN') continue; 
                 
                const basePath = cols[0]; 
                for(let j = 2; j < cols.length; j++) { 
                    const item = cols[j].trim(); 
                    if(!item) continue; 
 
                    const isDeleted = item.startsWith("[DELETED"); 
                    const isFolder = item.startsWith("*"); 
                    const name = isFolder ? item.substring(1) : (isDeleted ? item.split(']_')[1] : item); 
                    const ext = (!isFolder && name.includes('.')) ? '.' + name.split('.').pop().toLowerCase() : 'folder'; 
                     
                    if (isFolder) { 
                        folderCount++; 
                    } else { 
                        fileCount++; 
                        if (!isDeleted) { 
                            exts[ext] = (exts[ext] || 0) + 1; 
                        } 
                    } 
 
                    allItems.push({ 
                        name: name, 
                        path: basePath + '\\' + name, 
                        parent: basePath, 
                        isFolder: isFolder, 
                        isDeleted: isDeleted, 
                        ext: ext 
                    }); 
                } 
            } 
 
            document.getElementById('statFiles').innerText = fileCount; 
            document.getElementById('statFolders').innerText = folderCount; 
 
            renderExtensions(exts); 
            filterData(); 
            buildTree(); 
        } 
 
        function parseLoadedData(dataList) { 
            allItems = dataList; 
            let exts = {}; 
            let fileCount = 0; 
            let folderCount = 0; 
 
            allItems.forEach(item => { 
                if (item.isFolder) { 
                    folderCount++; 
                } else { 
                    fileCount++; 
                    if (!item.isDeleted && item.ext) { 
                        exts[item.ext] = (exts[item.ext] || 0) + 1; 
                    } 
                } 
            }); 
 
            document.getElementById('statFiles').innerText = fileCount; 
            document.getElementById('statFolders').innerText = folderCount; 
 
            renderExtensions(exts); 
            filterData(); 
            buildTree(); 
        } 
 
        function renderExtensions(exts) { 
            const container = document.getElementById('extensionFilters'); 
            const sorted = Object.entries(exts).sort((a,b) => b[1] - a[1]).slice(0, 16); 
            container.innerHTML = sorted.map(([ext, count]) => ` 
                <button onclick="document.getElementById('searchBar').value='${ext}'; filterData()"  
                 class="px-2.5 py-1 bg-white border border-slate-200 text-slate-600 rounded-lg text-xs font-semibold hover:border-blue-500 hover:text-blue-600 shadow-sm transition-all"> 
                 ${ext} <span class="text-[10px] text-slate-400 font-bold ml-1">${count}</span> 
                </button> 
            `).join(''); 
        } 
 
        function filterData() { 
            const query = document.getElementById('searchBar').value.toLowerCase().trim(); 
            const grid = document.getElementById('resultsGrid'); 
            const emptyState = document.getElementById('emptyState'); 
             
            let filtered = allItems; 
            if (query) { 
                filtered = allItems.filter(i =>  
                    i.name.toLowerCase().includes(query) ||  
                    i.ext.includes(query) ||  
                    i.parent.toLowerCase().includes(query) 
                ); 
            } 
 
            // Slice to 100 for fast UI rendering 
            const renderList = filtered.slice(0, 100); 
 
            if(renderList.length === 0) { 
                grid.innerHTML = ''; 
                emptyState.classList.remove('hidden'); 
                document.getElementById('searchHeading').innerText = `No items found`; 
            } else { 
                emptyState.classList.add('hidden'); 
                document.getElementById('searchHeading').innerText = `Showing ${renderList.length} of ${filtered.length} matches`; 
                 
                grid.innerHTML = renderList.map(item => ` 
                    <div class="animate-fade-in bg-white p-4 rounded-2xl border border-slate-100 flex flex-col justify-between hover:border-blue-400/60 hover:shadow-lg hover:shadow-blue-500/5 transition-all duration-200 relative group"> 
                        <div class="flex items-start gap-3.5 mb-4"> 
                            <div class="text-3xl shrink-0 select-none">${item.isDeleted ? '🗑️' : (item.isFolder ? '📁' : getEmojiForExt(item.ext))}</div> 
                            <div class="overflow-hidden"> 
                                <h4 class="font-bold text-slate-800 text-sm truncate" title="${item.name}">${item.name}</h4> 
                                <p class="text-[10px] text-slate-400 font-mono truncate select-all" title="${item.parent}">${item.parent}</p> 
                            </div> 
                        </div> 
                        <div class="flex justify-between items-center gap-2"> 
                            <span class="text-[9px] font-bold px-2 py-1 rounded-lg tracking-wider ${item.isDeleted ? 'bg-red-50 text-red-600 border border-red-100' : (item.isFolder ? 'bg-amber-50 text-amber-600 border border-amber-100' : 'bg-slate-50 text-slate-500 border border-slate-100')}"> 
                                ${item.isDeleted ? 'DELETED' : (item.isFolder ? 'FOLDER' : item.ext.toUpperCase())} 
                            </span> 
                            <div class="flex gap-1.5 opacity-90 group-hover:opacity-100 transition-opacity"> 
                                <button onclick="openFolderInOS('${item.path.replace(/\\/g, '\\\\')}')" class="bg-slate-50 text-slate-600 hover:bg-slate-100 hover:text-slate-900 p-2 rounded-lg text-xs font-bold transition" title="Show in folder"> 
                                    📂 
                                </button> 
                                <button onclick="openFileInOS('${item.path.replace(/\\/g, '\\\\')}')" class="bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1"> 
                                    OPEN 
                                </button> 
                            </div> 
                        </div> 
                    </div> 
                `).join(''); 
            } 
        } 
 
        function getEmojiForExt(ext) { 
            const map = { 
                '.pdf': '📕', 
                '.docx': '📘', 
                '.doc': '📘', 
                '.xlsx': '📗', 
                '.xls': '📗', 
                '.csv': '📗', 
                '.png': '🖼️', 
                '.jpg': '🖼️', 
                '.jpeg': '🖼️', 
                '.gif': '🖼️', 
                '.txt': '📄', 
                '.md': '📝', 
                '.zip': '📦', 
                '.rar': '📦', 
                '.exe': '⚙️', 
                '.py': '🐍', 
                '.html': '🌐' 
            }; 
            return map[ext] || '📄'; 
        } 
 
        function buildTree() { 
            const tree = document.getElementById('treeContainer'); 
            const uniquePaths = [...new Set(allItems.map(i => i.parent))].slice(0, 40); 
            tree.innerHTML = uniquePaths.map(p => { 
                const folderName = p.split('\\').pop() || p; 
                return ` 
                    <div class="truncate py-1 px-2 hover:bg-slate-100 rounded-lg cursor-pointer flex items-center gap-1.5 text-slate-700 transition"  
                         onclick="document.getElementById('searchBar').value='${folderName}'; filterData()"  
                         title="${p}"> 
                        <span class="text-amber-500 text-sm">📁</span> 
                        <span class="font-medium truncate">${folderName}</span> 
                    </div> 
                `; 
            }).join(''); 
        } 
 
        function toggleTreeCollapse() { 
            const tree = document.getElementById('treeWrapper'); 
            tree.classList.toggle('hidden'); 
        } 
 
        // Bridge commands 
        async function openFileInOS(path) { 
            try { 
                const res = await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ action: "open_file", path: path }) 
                }); 
                const data = await res.json(); 
                if(data.status === "error") alert(data.msg); 
            } catch(e) { 
                alert("Failed to communicate with Python server. Run copilot_server.py to enable file opening."); 
            } 
        } 
 
        async function openFolderInOS(path) { 
            try { 
                const res = await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ action: "open_folder", path: path }) 
                }); 
                const data = await res.json(); 
                if(data.status === "error") alert(data.msg); 
            } catch(e) { 
                alert("Failed to communicate with Python server. Run copilot_server.py to enable folder highlighting."); 
            } 
        } 
 
        async function triggerUpdate() { 
            document.body.style.cursor = 'wait'; 
            try { 
                await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ action: "update_index" }) 
                }); 
                window.location.reload(); 
            } catch(e) { 
                alert("Failed to update index. Check python terminal console."); 
                document.body.style.cursor = 'default'; 
            } 
        } 
 
        async function triggerRecreateStructure() { 
            const src = document.getElementById('recreateSrc').value.trim(); 
            const dest = document.getElementById('recreateDest').value.trim(); 
            if(!src || !dest) { 
                alert("Please supply both source and destination paths."); 
                return; 
            } 
            try { 
                const res = await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ action: "recreate_structure", src_path: src, dest_path: dest }) 
                }); 
                const data = await res.json(); 
                alert(data.msg || (data.status === "success" ? "Done!" : "Error occurred")); 
            } catch(e) { 
                alert("Failed: " + e); 
            } 
        } 
 
        async function triggerAdvancedSegregation() { 
            const src = document.getElementById('segSrc').value.trim(); 
            const dest = document.getElementById('segDest').value.trim(); 
            const ruleType = document.getElementById('segRuleType').value; 
            const ruleVal = document.getElementById('segRuleVal').value.trim(); 
             
            if(!src || !dest || !ruleVal) { 
                alert("Please supply source, destination, and rule values."); 
                return; 
            } 
            try { 
                const res = await fetch(getApiUrl(), { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({  
                        action: "segregate_advanced",  
                        src_path: src,  
                        dest_path: dest,  
                        rule_type: ruleType,  
                        rule_value: ruleVal  
                    }) 
                }); 
                const data = await res.json(); 
                alert(data.msg || (data.status === "success" ? "Done!" : "Error occurred")); 
                triggerUpdate(); 
            } catch(e) { 
                alert("Failed: " + e); 
            } 
        } 
    </script> 
</body> 
</html>in indexer: import os 
import csv 
from datetime import datetime 
 
 
class FileIndexer: 
    """ 
    AX File Operations Co-pilot 
 
    File.csv is the ONLY persistent source of truth. 
 
    Structure: 
 
        Path | Folder | F1 | F2 | F3 | ... 
 
    Files: 
        report.pdf 
 
    Folders: 
        *Documents 
 
    Deleted entries: 
        D_20260817_1530_report.pdf 
        D_20260817_1530_*Documents 
 
    The Path column always retains the real historical path. 
    """ 
 
    DELETED_PREFIX = "D_" 
    FOLDER_PREFIX = "*" 
 
    def __init__(self, output_file="File.csv", row_limit=999999): 
        self.script_dir = os.path.dirname( 
            os.path.abspath(__file__) 
        ) 
 
        self.output_file = os.path.join( 
            self.script_dir, 
            output_file 
        ) 
 
        self.row_limit = row_limit 
 
    # ========================================================= 
    # PUBLIC 
    # ========================================================= 
 
    def add_target(self, target_path): 
        """ 
        Add and immediately index a target directory. 
 
        The target becomes the highest-level Path in File.csv. 
        """ 
 
        target_path = self._normalise_path(target_path) 
 
        if not os.path.isdir(target_path): 
            print( 
                f"[INDEXER] Invalid folder: {target_path}" 
            ) 
            return False 
 
        records = self._load_csv() 
 
        if self._target_exists_or_overlaps( 
            target_path, 
            records 
        ): 
            print( 
                f"[INDEXER] Target already indexed " 
                f"or overlaps an existing target:\n" 
                f"{target_path}" 
            ) 
            return False 
 
        print( 
            f"[INDEXER] Indexing target:\n" 
            f"{target_path}" 
        ) 
 
        new_records = self._scan_tree( 
            target_path 
        ) 
 
        records.extend(new_records) 
 
        records = self._deduplicate_records( 
            records 
        ) 
 
        self._write_csv(records) 
 
        print( 
            f"[INDEXER] Added {len(new_records)} directories." 
        ) 
 
        return True 
 
    def update(self): 
        """ 
        Incrementally reconcile the existing CSV with 
        the current filesystem. 
 
        Existing directories: 
            - files checked 
            - folders checked 
            - new files detected 
            - new folders detected 
            - deleted files marked 
            - deleted folders marked 
 
        New directories are automatically discovered. 
        """ 
 
        print("[INDEXER] Updating File.csv...") 
 
        records = self._load_csv() 
 
        if not records: 
            print( 
                "[INDEXER] File.csv contains no indexed directories." 
            ) 
            return False 
 
        roots = self._find_roots(records) 
 
        updated = self._reconcile( 
            records, 
            roots 
        ) 
 
        updated = self._deduplicate_records( 
            updated 
        ) 
 
        self._write_csv(updated) 
 
        print( 
            f"[INDEXER] Update complete." 
        ) 
 
        print( 
            f"[INDEXER] Indexed directories: " 
            f"{len(updated)}" 
        ) 
 
        return True 
 
    def scan(self, target_dirs): 
        """ 
        Compatibility method for older code. 
        """ 
 
        for target in target_dirs: 
            self.add_target(target) 
 
    # ========================================================= 
    # SCANNING 
    # ========================================================= 
 
    def _scan_tree(self, target): 
        records = [] 
 
        for current_path, dirnames, filenames in os.walk( 
            target 
        ): 
 
            dirnames.sort( 
                key=str.lower 
            ) 
 
            filenames.sort( 
                key=str.lower 
            ) 
 
            records.append( 
                { 
                    "Path": self._normalise_path( 
                        current_path 
                    ), 
                    "Folder": self._folder_name( 
                        current_path 
                    ), 
                    "Items": self._build_items( 
                        filenames, 
                        dirnames 
                    ) 
                } 
            ) 
 
        return records 
 
    def _build_items( 
        self, 
        filenames, 
        dirnames 
    ): 
        """ 
        Files first. 
        Folders last. 
        """ 
 
        files = sorted( 
            filenames, 
            key=str.lower 
        ) 
 
        folders = sorted( 
            dirnames, 
            key=str.lower 
        ) 
 
        return ( 
            files + 
            [ 
                self.FOLDER_PREFIX + folder 
                for folder in folders 
            ] 
        ) 
 
    # ========================================================= 
    # RECONCILIATION 
    # ========================================================= 
 
    def _reconcile( 
        self, 
        records, 
        roots 
    ): 
        """ 
        Reconcile the complete indexed tree. 
 
        Existing historical records are retained. 
        """ 
 
        old_by_path = { 
            self._normalise_path( 
                record["Path"] 
            ): record 
            for record in records 
        } 
 
        current_paths = set() 
 
        updated = [] 
 
        # ----------------------------------------------------- 
        # 1. Re-scan all directories which still exist. 
        # ----------------------------------------------------- 
 
        for path, old_record in old_by_path.items(): 
 
            if os.path.isdir(path): 
 
                current_paths.add(path) 
 
                new_record = self._reconcile_directory( 
                    path, 
                    old_record 
                ) 
 
                updated.append( 
                    new_record 
                ) 
 
        # ----------------------------------------------------- 
        # 2. Discover new directories. 
        # ----------------------------------------------------- 
 
        discovered = {} 
 
        for root in roots: 
 
            if not os.path.isdir(root): 
                continue 
 
            for current_path, dirnames, filenames in os.walk( 
                root 
            ): 
 
                path = self._normalise_path( 
                    current_path 
                ) 
 
                if path in current_paths: 
                    continue 
 
                if path in discovered: 
                    continue 
 
                dirnames.sort( 
                    key=str.lower 
                ) 
 
                filenames.sort( 
                    key=str.lower 
                ) 
 
                discovered[path] = { 
                    "Path": path, 
                    "Folder": self._folder_name( 
                        current_path 
                    ), 
                    "Items": self._build_items( 
                        filenames, 
                        dirnames 
                    ) 
                } 
 
        updated.extend( 
            discovered.values() 
        ) 
 
        # ----------------------------------------------------- 
        # 3. Preserve deleted directory rows. 
        # ----------------------------------------------------- 
 
        for path, old_record in old_by_path.items(): 
 
            if path not in current_paths: 
 
                deleted_record = ( 
                    self._preserve_deleted_directory( 
                        old_record 
                    ) 
                ) 
 
                updated.append( 
                    deleted_record 
                ) 
 
        return updated 
 
    def _reconcile_directory( 
        self, 
        path, 
        old_record 
    ): 
        """ 
        Compare one existing directory against 
        its previous CSV representation. 
        """ 
 
        try: 
            entries = os.listdir(path) 
 
        except (PermissionError, OSError) as error: 
 
            print( 
                f"[INDEXER] Access denied: " 
                f"{path} -> {error}" 
            ) 
 
            return old_record 
 
        current_files = [] 
        current_folders = [] 
 
        for entry in entries: 
 
            full_path = os.path.join( 
                path, 
                entry 
            ) 
 
            try: 
 
                if os.path.isdir(full_path): 
                    current_folders.append(entry) 
 
                elif os.path.isfile(full_path): 
                    current_files.append(entry) 
 
            except OSError: 
                continue 
 
        current_files.sort( 
            key=str.lower 
        ) 
 
        current_folders.sort( 
            key=str.lower 
        ) 
 
        current_items = self._build_items( 
            current_files, 
            current_folders 
        ) 
 
        old_items = old_record.get( 
            "Items", 
            [] 
        ) 
 
        deleted_items = self._find_deleted_items( 
            old_items, 
            current_items 
        ) 
 
        final_items = ( 
            current_items + 
            deleted_items 
        ) 
 
        return { 
            "Path": path, 
            "Folder": self._folder_name(path), 
            "Items": self._sort_items( 
                final_items 
            ) 
        } 
 
    # ========================================================= 
    # DELETION 
    # ========================================================= 
 
    def _find_deleted_items( 
        self, 
        old_items, 
        current_items 
    ): 
        """ 
        Preserve previously deleted items. 
 
        A live item missing from the current filesystem 
        receives a D_DATE marker. 
 
        Existing D_DATE entries remain untouched. 
        """ 
 
        timestamp = datetime.now().strftime( 
            "%Y%m%d_%H%M" 
        ) 
 
        current_set = set( 
            current_items 
        ) 
 
        deleted = [] 
 
        for old_item in old_items: 
 
            # Already deleted. 
            if old_item.startswith( 
                self.DELETED_PREFIX 
            ): 
                deleted.append( 
                    old_item 
                ) 
                continue 
 
            if old_item not in current_set: 
 
                deleted.append( 
                    self._make_deleted_marker( 
                        old_item, 
                        timestamp 
                    ) 
                ) 
 
        return deleted 
 
    def _make_deleted_marker( 
        self, 
        item, 
        timestamp 
    ): 
        return ( 
            f"{self.DELETED_PREFIX}" 
            f"{timestamp}_" 
            f"{item}" 
        ) 
 
    def _preserve_deleted_directory( 
        self, 
        record 
    ): 
        """ 
        Preserve a directory which no longer exists. 
 
        Its Path remains intact so its historical location 
        can still be searched/opened/displayed. 
        """ 
 
        folder = record.get( 
            "Folder", 
            "" 
        ) 
 
        if not folder.startswith( 
            self.DELETED_PREFIX 
        ): 
            timestamp = datetime.now().strftime( 
                "%Y%m%d_%H%M" 
            ) 
 
            folder = ( 
                f"{self.DELETED_PREFIX}" 
                f"{timestamp}_" 
                f"{folder}" 
            ) 
 
        preserved_items = [] 
 
        for item in record.get( 
            "Items", 
            [] 
        ): 
 
            if item.startswith( 
                self.DELETED_PREFIX 
            ): 
                preserved_items.append( 
                    item 
                ) 
 
            else: 
                timestamp = datetime.now().strftime( 
                    "%Y%m%d_%H%M" 
                ) 
 
                preserved_items.append( 
                    self._make_deleted_marker( 
                        item, 
                        timestamp 
                    ) 
                ) 
 
        return { 
            "Path": record["Path"], 
            "Folder": folder, 
            "Items": preserved_items 
        } 
 
    # ========================================================= 
    # ROOTS 
    # ========================================================= 
 
    def _find_roots( 
        self, 
        records 
    ): 
        """ 
        Infer top-level indexed targets from File.csv. 
 
        Example: 
 
            C:\\Data 
            C:\\Data\\Projects 
            C:\\Data\\Projects\\Python 
 
        Root: 
 
            C:\\Data 
        """ 
 
        paths = sorted( 
            { 
                self._normalise_path( 
                    record["Path"] 
                ) 
                for record in records 
            }, 
            key=len 
        ) 
 
        roots = [] 
 
        for path in paths: 
 
            if not any( 
                self._is_subpath( 
                    path, 
                    root 
                ) 
                for root in roots 
            ): 
                roots.append( 
                    path 
                ) 
 
        return roots 
 
    # ========================================================= 
    # TARGET VALIDATION 
    # ========================================================= 
 
    def _target_exists_or_overlaps( 
        self, 
        target, 
        records 
    ): 
        target = self._normalise_path( 
            target 
        ) 
 
        roots = self._find_roots( 
            records 
        ) 
 
        for root in roots: 
 
            if root == target: 
                return True 
 
            if self._is_subpath( 
                target, 
                root 
            ): 
                return True 
 
            if self._is_subpath( 
                root, 
                target 
            ): 
                return True 
 
        return False 
 
    # ========================================================= 
    # CSV LOAD 
    # ========================================================= 
 
    def _load_csv(self): 
        records = [] 
 
        current_file = self.output_file 
 
        visited = set() 
 
        while current_file: 
 
            current_file = os.path.abspath( 
                current_file 
            ) 
 
            if current_file in visited: 
                print( 
                    "[INDEXER] CSV chain loop detected." 
                ) 
                break 
 
            visited.add( 
                current_file 
            ) 
 
            if not os.path.exists( 
                current_file 
            ): 
                break 
 
            next_file = None 
 
            try: 
 
                with open( 
                    current_file, 
                    "r", 
                    newline="", 
                    encoding="utf-8", 
                    errors="replace" 
                ) as file: 
 
                    reader = csv.reader( 
                        file 
                    ) 
 
                    next( 
                        reader, 
                        None 
                    ) 
 
                    for row in reader: 
 
                        if not row: 
                            continue 
 
                        if row[0] == "CHN": 
 
                            if len(row) >= 2: 
 
                                next_file = row[1] 
 
                                if not os.path.isabs( 
                                    next_file 
                                ): 
                                    next_file = os.path.join( 
                                        self.script_dir, 
                                        next_file 
                                    ) 
 
                            continue 
 
                        if len(row) < 2: 
                            continue 
 
                        records.append( 
                            { 
                                "Path": row[0], 
                                "Folder": row[1], 
                                "Items": [ 
                                    item 
                                    for item in row[2:] 
                                    if item 
                                ] 
                            } 
                        ) 
 
            except Exception as error: 
 
                print( 
                    f"[INDEXER] CSV read error: " 
                    f"{error}" 
                ) 
 
                break 
 
            current_file = next_file 
 
        return records 
 
    # ========================================================= 
    # CSV WRITE 
    # ========================================================= 
 
    def _write_csv( 
        self, 
        records 
    ): 
        if not records: 
            print( 
                "[INDEXER] Nothing to write." 
            ) 
            return 
 
        records.sort( 
            key=lambda record: ( 
                len(record["Path"]), 
                record["Path"].lower() 
            ) 
        ) 
 
        max_items = max( 
            len(record["Items"]) 
            for record in records 
        ) 
 
        headers = ( 
            ["Path", "Folder"] + 
            [ 
                f"F{i + 1}" 
                for i in range(max_items) 
            ] 
        ) 
 
        self._remove_chain_files() 
 
        file_number = 1 
        row_count = 0 
 
        current_file = self.output_file 
 
        handle = open( 
            current_file, 
            "w", 
            newline="", 
            encoding="utf-8" 
        ) 
 
        writer = csv.writer( 
            handle 
        ) 
 
        writer.writerow( 
            headers 
        ) 
 
        try: 
 
            for record in records: 
 
                if row_count >= self.row_limit: 
 
                    next_file = ( 
                        self._chain_filename( 
                            file_number + 1 
                        ) 
                    ) 
 
                    writer.writerow( 
                        [ 
                            "CHN", 
                            next_file 
                        ] 
                    ) 
 
                    handle.close() 
 
                    file_number += 1 
                    row_count = 0 
 
                    current_file = ( 
                        self._chain_filename( 
                            file_number 
                        ) 
                    ) 
 
                    handle = open( 
                        current_file, 
                        "w", 
                        newline="", 
                        encoding="utf-8" 
                    ) 
 
                    writer = csv.writer( 
                        handle 
                    ) 
 
                    writer.writerow( 
                        headers 
                    ) 
 
                row = [ 
                    record["Path"], 
                    record["Folder"] 
                ] 
 
                row.extend( 
                    record["Items"] 
                ) 
 
                while len(row) < len(headers): 
                    row.append("") 
 
                writer.writerow( 
                    row 
                ) 
 
                row_count += 1 
 
        finally: 
 
            handle.close() 
 
        print( 
            f"[INDEXER] File.csv written: " 
            f"{len(records)} directories." 
        ) 
 
    def _chain_filename( 
        self, 
        number 
    ): 
        base, extension = os.path.splitext( 
            self.output_file 
        ) 
 
        return os.path.basename( 
            f"{base}_{number}{extension}" 
        ) 
 
    def _remove_chain_files(self): 
 
        base, extension = os.path.splitext( 
            self.output_file 
        ) 
 
        number = 2 
 
        while True: 
 
            filename = ( 
                f"{base}_{number}{extension}" 
            ) 
 
            if not os.path.exists( 
                filename 
            ): 
                break 
 
            try: 
                os.remove( 
                    filename 
                ) 
            except OSError: 
                pass 
 
            number += 1 
 
    # ========================================================= 
    # UTILITIES 
    # ========================================================= 
 
    def _folder_name( 
        self, 
        path 
    ): 
        name = os.path.basename( 
            os.path.normpath(path) 
        ) 
 
        return name or path 
 
    def _sort_items( 
        self, 
        items 
    ): 
        """ 
        Live files 
        live folders 
        deleted entries 
        """ 
 
        live_files = [] 
        live_folders = [] 
        deleted = [] 
 
        for item in items: 
 
            if item.startswith( 
                self.DELETED_PREFIX 
            ): 
                deleted.append( 
                    item 
                ) 
 
            elif item.startswith( 
                self.FOLDER_PREFIX 
            ): 
                live_folders.append( 
                    item 
                ) 
 
            else: 
                live_files.append( 
                    item 
                ) 
 
        live_files.sort( 
            key=str.lower 
        ) 
 
        live_folders.sort( 
            key=str.lower 
        ) 
 
        deleted.sort( 
            key=str.lower 
        ) 
 
        return ( 
            live_files + 
            live_folders + 
            deleted 
        ) 
 
    def _deduplicate_records( 
        self, 
        records 
    ): 
        unique = {} 
 
        for record in records: 
 
            path = self._normalise_path( 
                record["Path"] 
            ) 
 
            record["Path"] = path 
 
            unique[path] = record 
 
        return list( 
            unique.values() 
        ) 
 
    def _normalise_path( 
        self, 
        path 
    ): 
        return os.path.normcase( 
            os.path.normpath( 
                os.path.abspath(path) 
            ) 
        ) 
 
    def _is_subpath( 
        self, 
        child, 
        parent 
    ): 
        child = self._normalise_path( 
            child 
        ) 
 
        parent = self._normalise_path( 
            parent 
        ) 
 
        if child == parent: 
            return True 
 
        parent = ( 
            parent.rstrip(os.sep) 
            + os.sep 
        ) 
 
        return child.startswith( 
            parent 
        ) 
 
 
# ============================================================= 
# DIRECT EXECUTION 
# ============================================================= 
 
if __name__ == "__main__": 
 
    indexer = FileIndexer() 
 
    print() 
    print("AX FILE OPERATIONS CO-PILOT") 
    print("============================") 
    print("1. Add folder") 
    print("2. Update") 
    print("3. Exit") 
    print() 
 
    choice = input( 
        "Select: " 
    ).strip() 
 
    if choice == "1": 
 
        path = input( 
            "Folder path: " 
        ).strip().strip('"') 
 
        indexer.add_target( 
            path 
        ) 
 
    elif choice == "2": 
 
        indexer.update() server: import os 
import json 
import shutil 
import socket 
import subprocess 
import threading 
import webbrowser 
import time 
 
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer 
from urllib.parse import urlparse 
 
from file_indexer import FileIndexer 
 
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
 
HTML_FILE = os.path.join( 
    BASE_DIR, 
    "file_copilot.html" 
) 
 
DATA_FILE = os.path.join( 
    BASE_DIR, 
    "file_data.js" 
) 
 
CSV_FILE = os.path.join( 
    BASE_DIR, 
    "File.csv" 
) 
 
 
class AXFileServer: 
    """ 
    AX File Operations Co-pilot backend. 
 
    Persistent state: 
        File.csv 
 
    Derived state: 
        file_data.js 
 
    File.csv is always treated as the authoritative 
    representation of the indexed filesystem. 
    """ 
 
    def __init__(self): 
        self.indexer = FileIndexer( 
            "File.csv" 
        ) 
 
        self.lock = threading.RLock() 
 
    # ========================================================= 
    # CSV / INDEX DATA 
    # ========================================================= 
 
    def get_records(self): 
        return self.indexer._load_csv() 
 
    def generate_browser_data(self): 
        """ 
        Convert File.csv records into a flat browser dataset. 
 
        This file is only a cache/transport artifact. 
        It is never treated as persistent state. 
        """ 
 
        records = self.get_records() 
 
        items = [] 
 
        for record in records: 
 
            parent = record.get( 
                "Path", 
                "" 
            ) 
 
            if not parent: 
                continue 
 
            for item in record.get( 
                "Items", 
                [] 
            ): 
 
                if not item: 
                    continue 
 
                is_deleted = item.startswith( 
                    self.indexer.DELETED_PREFIX 
                ) 
 
                is_folder = ( 
                    item.startswith( 
                        self.indexer.FOLDER_PREFIX 
                    ) 
                    and not is_deleted 
                ) 
 
                # ------------------------------------------------- 
                # Decode display name. 
                # ------------------------------------------------- 
 
                if is_deleted: 
 
                    name = self._deleted_display_name( 
                        item 
                    ) 
 
                elif is_folder: 
 
                    name = item[1:] 
 
                else: 
 
                    name = item 
 
                # ------------------------------------------------- 
                # Deleted entries must retain their historical 
                # parent/path semantics. 
                # ------------------------------------------------- 
 
                if is_deleted: 
 
                    full_path = os.path.join( 
                        parent, 
                        name 
                    ) 
 
                else: 
 
                    full_path = os.path.join( 
                        parent, 
                        name 
                    ) 
 
                extension = "" 
 
                if is_folder: 
 
                    extension = "folder" 
 
                elif "." in name: 
 
                    extension = ( 
                        "." 
                        + name.rsplit( 
                            ".", 
                            1 
                        )[1].lower() 
                    ) 
 
                items.append( 
                    { 
                        "name": name, 
                        "path": full_path, 
                        "parent": parent, 
                        "isFolder": is_folder, 
                        "isDeleted": is_deleted, 
                        "ext": extension 
                    } 
                ) 
 
        browser_data = ( 
            "window.axFileData = " 
            + json.dumps( 
                items, 
                indent=2, 
                ensure_ascii=False 
            ) 
            + ";\n" 
        ) 
 
        try: 
 
            with open( 
                DATA_FILE, 
                "w", 
                encoding="utf-8" 
            ) as file: 
 
                file.write( 
                    browser_data 
                ) 
 
        except OSError as error: 
 
            print( 
                "[SERVER] Could not generate file_data.js:", 
                error 
            ) 
 
        return items 
 
    def _deleted_display_name( 
        self, 
        item 
    ): 
        """ 
        Convert: 
 
            D_20260817_1530_report.pdf 
 
        into: 
 
            report.pdf 
 
        while leaving malformed historical markers intact. 
        """ 
 
        parts = item.split( 
            "_", 
            3 
        ) 
 
        if len(parts) == 4: 
 
            return parts[3] 
 
        return item 
 
    # ========================================================= 
    # TARGETS 
    # ========================================================= 
 
    def get_targets(self): 
        """ 
        Targets are inferred exclusively from File.csv. 
 
        No separate target database is maintained. 
        """ 
 
        records = self.get_records() 
 
        if not records: 
            return [] 
 
        paths = sorted( 
            { 
                self._normalise( 
                    record["Path"] 
                ) 
                for record in records 
                if record.get("Path") 
            }, 
            key=lambda value: ( 
                len(value), 
                value.lower() 
            ) 
        ) 
 
        targets = [] 
 
        for path in paths: 
 
            if not any( 
                self._is_subpath( 
                    path, 
                    root 
                ) 
                for root in targets 
            ): 
 
                targets.append( 
                    path 
                ) 
 
        return targets 
 
    # ========================================================= 
    # ADD FOLDER 
    # ========================================================= 
 
    def add_folder( 
        self, 
        path 
    ): 
        path = self._normalise( 
            path 
        ) 
 
        if not os.path.isdir(path): 
 
            return ( 
                False, 
                "Folder does not exist." 
            ) 
 
        with self.lock: 
 
            result = self.indexer.add_target( 
                path 
            ) 
 
            if result: 
 
                self.generate_browser_data() 
 
                return ( 
                    True, 
                    "Folder indexed successfully." 
                ) 
 
            return ( 
                False, 
                "Folder could not be indexed. " 
                "It may already be indexed or overlap " 
                "an existing target." 
            ) 
 
    # ========================================================= 
    # UPDATE 
    # ========================================================= 
 
    def update(self): 
 
        with self.lock: 
 
            result = self.indexer.update() 
 
            if result: 
 
                self.generate_browser_data() 
 
                return ( 
                    True, 
                    "Index updated successfully." 
                ) 
 
            return ( 
                False, 
                "Index update failed." 
            ) 
 
    # ========================================================= 
    # OPEN FILE 
    # ========================================================= 
 
    def open_file( 
        self, 
        path 
    ): 
 
        if not path: 
 
            return ( 
                False, 
                "File path required." 
            ) 
 
        path = self._normalise( 
            path 
        ) 
 
        if not os.path.isfile(path): 
 
            return ( 
                False, 
                "File does not exist." 
            ) 
 
        try: 
 
            os.startfile( 
                path 
            ) 
 
            return ( 
                True, 
                "File opened." 
            ) 
 
        except Exception as error: 
 
            return ( 
                False, 
                str(error) 
            ) 
 
    # ========================================================= 
    # OPEN FOLDER 
    # ========================================================= 
 
    def open_folder( 
        self, 
        path 
    ): 
 
        if not path: 
 
            return ( 
                False, 
                "Path required." 
            ) 
 
        path = self._normalise( 
            path 
        ) 
 
        # ----------------------------------------------------- 
        # If the supplied path is a file, open Explorer with 
        # that file selected. 
        # ----------------------------------------------------- 
 
        if os.path.isfile(path): 
 
            try: 
 
                subprocess.Popen( 
                    [ 
                        "explorer.exe", 
                        "/select,", 
                        path 
                    ] 
                ) 
 
                return ( 
                    True, 
                    "File location opened." 
                ) 
 
            except Exception as error: 
 
                return ( 
                    False, 
                    str(error) 
                ) 
 
        # ----------------------------------------------------- 
        # Normal directory. 
        # ----------------------------------------------------- 
 
        if os.path.isdir(path): 
 
            try: 
 
                os.startfile( 
                    path 
                ) 
 
                return ( 
                    True, 
                    "Folder opened." 
                ) 
 
            except Exception as error: 
 
                return ( 
                    False, 
                    str(error) 
                ) 
 
        return ( 
            False, 
            "Path does not exist." 
        ) 
 
    # ========================================================= 
    # FOLDER STRUCTURE CLONING 
    # ========================================================= 
 
    def recreate_structure( 
        self, 
        source, 
        destination 
    ): 
 
        source = self._normalise( 
            source 
        ) 
 
        destination = self._normalise( 
            destination 
        ) 
 
        if not os.path.isdir(source): 
 
            return ( 
                False, 
                "Source folder does not exist." 
            ) 
 
        if source == destination: 
 
            return ( 
                False, 
                "Source and destination cannot be identical." 
            ) 
 
        try: 
 
            for current_path, dirnames, _ in os.walk( 
                source 
            ): 
 
                relative = os.path.relpath( 
                    current_path, 
                    source 
                ) 
 
                if relative == ".": 
 
                    target = destination 
 
                else: 
 
                    target = os.path.join( 
                        destination, 
                        relative 
                    ) 
 
                os.makedirs( 
                    target, 
                    exist_ok=True 
                ) 
 
            # The destination may itself be an indexed target. 
            # Reconcile all known targets afterward. 
 
            self.indexer.update() 
            self.generate_browser_data() 
 
            return ( 
                True, 
                "Folder structure recreated." 
            ) 
 
        except Exception as error: 
 
            return ( 
                False, 
                str(error) 
            ) 
 
    # ========================================================= 
    # FILE SEGREGATION 
    # ========================================================= 
 
    def segregate( 
        self, 
        source, 
        mode, 
        value=None, 
        destination=None 
    ): 
 
        source = self._normalise( 
            source 
        ) 
 
        if not os.path.isdir(source): 
 
            return ( 
                False, 
                "Source folder does not exist." 
            ) 
 
        if destination: 
 
            destination = self._normalise( 
                destination 
            ) 
 
        else: 
 
            destination = source 
 
        mode = str( 
            mode or "" 
        ).strip().lower() 
 
        try: 
 
            moved = 0 
 
            # ------------------------------------------------- 
            # Only files directly inside source are processed. 
            # ------------------------------------------------- 
 
            for filename in os.listdir( 
                source 
            ): 
 
                source_path = os.path.join( 
                    source, 
                    filename 
                ) 
 
                if not os.path.isfile( 
                    source_path 
                ): 
 
                    continue 
 
                # ============================================= 
                # EXTENSION 
                # ============================================= 
 
                if mode == "extension": 
 
                    extension = os.path.splitext( 
                        filename 
                    )[1].lower() 
 
                    if not extension: 
 
                        folder_name = ( 
                            "NO_EXTENSION" 
                        ) 
 
                    else: 
 
                        folder_name = ( 
                            extension[1:] 
                            .upper() 
                        ) 
 
                    target_folder = os.path.join( 
                        destination, 
                        folder_name 
                    ) 
 
                    os.makedirs( 
                        target_folder, 
                        exist_ok=True 
                    ) 
 
                    target_path = ( 
                        self._safe_destination( 
                            target_folder, 
                            filename 
                        ) 
                    ) 
 
                    shutil.move( 
                        source_path, 
                        target_path 
                    ) 
 
                    moved += 1 
 
                # ============================================= 
                # SIZE 
                # ============================================= 
 
                elif mode == "size": 
 
                    if value is None: 
 
                        return ( 
                            False, 
                            "Size value required." 
                        ) 
 
                    try: 
 
                        threshold = float( 
                            value 
                        ) 
 
                    except ValueError: 
 
                        return ( 
                            False, 
                            "Size value must be numeric." 
                        ) 
 
                    size_mb = ( 
                        os.path.getsize( 
                            source_path 
                        ) 
                        / ( 
                            1024 * 1024 
                        ) 
                    ) 
 
                    if size_mb < threshold: 
 
                        continue 
 
                    target_folder = os.path.join( 
                        destination, 
                        f"OVER_{threshold:g}MB" 
                    ) 
 
                    os.makedirs( 
                        target_folder, 
                        exist_ok=True 
                    ) 
 
                    target_path = ( 
                        self._safe_destination( 
                            target_folder, 
                            filename 
                        ) 
                    ) 
 
                    shutil.move( 
                        source_path, 
                        target_path 
                    ) 
 
                    moved += 1 
 
                # ============================================= 
                # AGE 
                # ============================================= 
 
                elif mode in ( 
                    "age", 
                    "date" 
                ): 
 
                    if value is None: 
 
                        return ( 
                            False, 
                            "Age value required." 
                        ) 
 
                    try: 
 
                        threshold = float( 
                            value 
                        ) 
 
                    except ValueError: 
 
                        return ( 
                            False, 
                            "Age value must be numeric." 
                        ) 
 
                    age_seconds = ( 
                        time.time() 
                        - os.path.getmtime( 
                            source_path 
                        ) 
                    ) 
 
                    age_days = ( 
                        age_seconds 
                        / 86400 
                    ) 
 
                    if age_days < threshold: 
 
                        continue 
 
                    target_folder = os.path.join( 
                        destination, 
                        f"OLDER_{threshold:g}_DAYS" 
                    ) 
 
                    os.makedirs( 
                        target_folder, 
                        exist_ok=True 
                    ) 
 
                    target_path = ( 
                        self._safe_destination( 
                            target_folder, 
                            filename 
                        ) 
                    ) 
 
                    shutil.move( 
                        source_path, 
                        target_path 
                    ) 
 
                    moved += 1 
 
                else: 
 
                    return ( 
                        False, 
                        f"Unknown segregation mode: {mode}" 
                    ) 
 
            # ------------------------------------------------- 
            # Filesystem changed. 
            # CSV must now be reconciled. 
            # ------------------------------------------------- 
 
            self.indexer.update() 
            self.generate_browser_data() 
 
            return ( 
                True, 
                f"{moved} file(s) moved." 
            ) 
 
        except Exception as error: 
 
            return ( 
                False, 
                str(error) 
            ) 
 
    # ========================================================= 
    # SAFE FILE MOVING 
    # ========================================================= 
 
    def _safe_destination( 
        self, 
        folder, 
        filename 
    ): 
 
        target = os.path.join( 
            folder, 
            filename 
        ) 
 
        if not os.path.exists( 
            target 
        ): 
 
            return target 
 
        base, extension = os.path.splitext( 
            filename 
        ) 
 
        counter = 1 
 
        while True: 
 
            new_name = ( 
                f"{base}_{counter}" 
                f"{extension}" 
            ) 
 
            target = os.path.join( 
                folder, 
                new_name 
            ) 
 
            if not os.path.exists( 
                target 
            ): 
 
                return target 
 
            counter += 1 
 
    # ========================================================= 
    # FOLDER BROWSER 
    # ========================================================= 
 
    def browse_folder(self): 
 
        try: 
 
            import tkinter as tk 
            from tkinter import filedialog 
 
            root = tk.Tk() 
            root.withdraw() 
            root.attributes( 
                "-topmost", 
                True 
            ) 
 
            path = filedialog.askdirectory() 
 
            root.destroy() 
 
            return path or "" 
 
        except Exception as error: 
 
            print( 
                "[SERVER] Folder browser error:", 
                error 
            ) 
 
            return "" 
 
    # ========================================================= 
    # PATH UTILITIES 
    # ========================================================= 
 
    def _normalise( 
        self, 
        path 
    ): 
 
        return os.path.normpath( 
            os.path.abspath( 
                os.path.expanduser( 
                    str(path) 
                ) 
            ) 
        ) 
 
    def _is_subpath( 
        self, 
        child, 
        parent 
    ): 
 
        child = self._normalise( 
            child 
        ) 
 
        parent = self._normalise( 
            parent 
        ) 
 
        if child == parent: 
 
            return True 
 
        parent = ( 
            parent.rstrip( 
                os.sep 
            ) 
            + os.sep 
        ) 
 
        return child.startswith( 
            parent 
        ) 
 
 
# ============================================================= 
# HTTP HANDLER 
# ============================================================= 
 
class RequestHandler( 
    BaseHTTPRequestHandler 
): 
 
    server_version = "AX-File-CoPilot/2.0" 
 
    # ========================================================= 
    # RESPONSE HELPERS 
    # ========================================================= 
 
    def _send_json( 
        self, 
        data, 
        status=200 
    ): 
 
        payload = json.dumps( 
            data, 
            indent=2, 
            ensure_ascii=False 
        ).encode( 
            "utf-8" 
        ) 
 
        self.send_response( 
            status 
        ) 
 
        self.send_header( 
            "Content-Type", 
            "application/json; charset=utf-8" 
        ) 
 
        self.send_header( 
            "Cache-Control", 
            "no-store" 
        ) 
 
        self.send_header( 
            "Content-Length", 
            str(len(payload)) 
        ) 
 
        self.end_headers() 
 
        self.wfile.write( 
            payload 
        ) 
 
    def _send_file( 
        self, 
        path, 
        content_type 
    ): 
 
        if not os.path.isfile( 
            path 
        ): 
 
            self.send_error( 
                404, 
                "File not found" 
            ) 
 
            return 
 
        try: 
 
            with open( 
                path, 
                "rb" 
            ) as file: 
 
                data = file.read() 
 
        except OSError as error: 
 
            self.send_error( 
                500, 
                str(error) 
            ) 
 
            return 
 
        self.send_response( 
            200 
        ) 
 
        self.send_header( 
            "Content-Type", 
            content_type 
        ) 
 
        self.send_header( 
            "Cache-Control", 
            "no-store" 
        ) 
 
        self.send_header( 
            "Content-Length", 
            str(len(data)) 
        ) 
 
        self.end_headers() 
 
        self.wfile.write( 
            data 
        ) 
 
    def _read_json(self): 
 
        try: 
 
            length = int( 
                self.headers.get( 
                    "Content-Length", 
                    "0" 
                ) 
            ) 
 
            if length <= 0: 
 
                return {} 
 
            raw = self.rfile.read( 
                length 
            ) 
 
            return json.loads( 
                raw.decode( 
                    "utf-8" 
                ) 
            ) 
 
        except Exception: 
 
            return {} 
 
    def _api_error( 
        self, 
        message, 
        status=400 
    ): 
 
        self._send_json( 
            { 
                "success": False, 
                "error": message 
            }, 
            status 
        ) 
 
    # ========================================================= 
    # GET 
    # ========================================================= 
 
    def do_GET(self): 
 
        parsed = urlparse( 
            self.path 
        ) 
 
        path = parsed.path 
 
        app = self.server.ax_app 
 
        # ----------------------------------------------------- 
        # MAIN PAGE 
        # ----------------------------------------------------- 
 
        if path == "/": 
 
            self._send_file( 
                HTML_FILE, 
                "text/html; charset=utf-8" 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # BROWSER DATA 
        # ----------------------------------------------------- 
 
        if path == "/api/data": 
 
            try: 
 
                with app.lock: 
 
                    data = ( 
                        app.generate_browser_data() 
                    ) 
 
                    targets = ( 
                        app.get_targets() 
                    ) 
 
                self._send_json( 
                    { 
                        "success": True, 
                        "data": data, 
                        "targets": targets 
                    } 
                ) 
 
            except Exception as error: 
 
                self._send_json( 
                    { 
                        "success": False, 
                        "error": str(error) 
                    }, 
                    500 
                ) 
 
            return 
 
        # ----------------------------------------------------- 
        # TARGETS 
        # ----------------------------------------------------- 
 
        if path == "/api/targets": 
 
            self._send_json( 
                { 
                    "success": True, 
                    "targets": app.get_targets() 
                } 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # FOLDER BROWSER 
        # ----------------------------------------------------- 
 
        if path == "/api/browse-folder": 
 
            selected = ( 
                app.browse_folder() 
            ) 
 
            self._send_json( 
                { 
                    "success": bool( 
                        selected 
                    ), 
                    "path": selected 
                } 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # GENERATED BROWSER DATA 
        # ----------------------------------------------------- 
 
        if path == "/file_data.js": 
 
            if not os.path.isfile( 
                DATA_FILE 
            ): 
 
                app.generate_browser_data() 
 
            self._send_file( 
                DATA_FILE, 
                "application/javascript; charset=utf-8" 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # SERVER CONFIG 
        # ----------------------------------------------------- 
 
        if path == "/server_config.js": 
 
            payload = ( 
                "window.SOTO_SERVER_URL = '';\n" 
                "window.AX_SERVER_ACTIVE = true;\n" 
            ).encode( 
                "utf-8" 
            ) 
 
            self.send_response( 
                200 
            ) 
 
            self.send_header( 
                "Content-Type", 
                "application/javascript; charset=utf-8" 
            ) 
 
            self.send_header( 
                "Cache-Control", 
                "no-store" 
            ) 
 
            self.send_header( 
                "Content-Length", 
                str(len(payload)) 
            ) 
 
            self.end_headers() 
 
            self.wfile.write( 
                payload 
            ) 
 
            return 
 
        self.send_error( 
            404, 
            "Not found" 
        ) 
 
    # ========================================================= 
    # POST 
    # ========================================================= 
 
    def do_POST(self): 
 
        parsed = urlparse( 
            self.path 
        ) 
 
        path = parsed.path 
 
        body = self._read_json() 
 
        app = self.server.ax_app 
 
        # ----------------------------------------------------- 
        # ADD FOLDER 
        # ----------------------------------------------------- 
 
        if path == "/api/add-folder": 
 
            folder = body.get( 
                "path" 
            ) 
 
            if not folder: 
 
                self._api_error( 
                    "Folder path required." 
                ) 
 
                return 
 
            success, message = ( 
                app.add_folder( 
                    folder 
                ) 
            ) 
 
            self._send_json( 
                { 
                    "success": success, 
                    "message": message, 
                    "targets": app.get_targets() 
                }, 
                200 if success else 400 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # UPDATE 
        # ----------------------------------------------------- 
 
        if path == "/api/update": 
 
            success, message = ( 
                app.update() 
            ) 
 
            self._send_json( 
                { 
                    "success": success, 
                    "message": message 
                }, 
                200 if success else 500 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # OPEN FILE 
        # ----------------------------------------------------- 
 
        if path == "/api/open-file": 
 
            success, message = ( 
                app.open_file( 
                    body.get( 
                        "path", 
                        "" 
                    ) 
                ) 
            ) 
 
            self._send_json( 
                { 
                    "success": success, 
                    "message": message 
                }, 
                200 if success else 400 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # OPEN FOLDER 
        # ----------------------------------------------------- 
 
        if path == "/api/open-folder": 
 
            success, message = ( 
                app.open_folder( 
                    body.get( 
                        "path", 
                        "" 
                    ) 
                ) 
            ) 
 
            self._send_json( 
                { 
                    "success": success, 
                    "message": message 
                }, 
                200 if success else 400 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # RECREATE STRUCTURE 
        # ----------------------------------------------------- 
 
        if path == "/api/recreate-structure": 
 
            source = body.get( 
                "source", 
                body.get( 
                    "src_path", 
                    "" 
                ) 
            ) 
 
            destination = body.get( 
                "destination", 
                body.get( 
                    "dest_path", 
                    "" 
                ) 
            ) 
 
            success, message = ( 
                app.recreate_structure( 
                    source, 
                    destination 
                ) 
            ) 
 
            self._send_json( 
                { 
                    "success": success, 
                    "message": message 
                }, 
                200 if success else 400 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # SEGREGATION 
        # ----------------------------------------------------- 
 
        if path == "/api/segregate": 
 
            source = body.get( 
                "source", 
                body.get( 
                    "src_path", 
                    "" 
                ) 
            ) 
 
            destination = body.get( 
                "destination", 
                body.get( 
                    "dest_path", 
                    "" 
                ) 
            ) 
 
            mode = body.get( 
                "mode", 
                body.get( 
                    "rule_type", 
                    "" 
                ) 
            ) 
 
            value = body.get( 
                "value", 
                body.get( 
                    "rule_value" 
                ) 
            ) 
 
            success, message = ( 
                app.segregate( 
                    source, 
                    mode, 
                    value, 
                    destination 
                ) 
            ) 
 
            self._send_json( 
                { 
                    "success": success, 
                    "message": message 
                }, 
                200 if success else 400 
            ) 
 
            return 
 
        # ----------------------------------------------------- 
        # LEGACY ACTION ROUTING 
        # 
        # This keeps compatibility with the current HTML while 
        # allowing the server to use the cleaner endpoint API. 
        # ----------------------------------------------------- 
 
        if path == "/api": 
 
            action = body.get( 
                "action", 
                "" 
            ) 
 
            # --------------------------------------------- 
            # GET TARGETS 
            # --------------------------------------------- 
 
            if action == "get_targets": 
 
                self._send_json( 
                    { 
                        "success": True, 
                        "status": "success", 
                        "targets": app.get_targets() 
                    } 
                ) 
 
                return 
 
            # --------------------------------------------- 
            # UPDATE 
            # --------------------------------------------- 
 
            if action == "update_index": 
 
                success, message = ( 
                    app.update() 
                ) 
 
                self._send_json( 
                    { 
                        "success": success, 
                        "status": ( 
                            "success" 
                            if success 
                            else "error" 
                        ), 
                        "message": message, 
                        "msg": message 
                    } 
                ) 
 
                return 
 
            # --------------------------------------------- 
            # OPEN FILE 
            # --------------------------------------------- 
 
            if action == "open_file": 
 
                success, message = ( 
                    app.open_file( 
                        body.get( 
                            "path", 
                            "" 
                        ) 
                    ) 
                ) 
 
                self._send_json( 
                    { 
                        "success": success, 
                        "status": ( 
                            "success" 
                            if success 
                            else "error" 
                        ), 
                        "message": message, 
                        "msg": message 
                    } 
                ) 
 
                return 
 
            # --------------------------------------------- 
            # OPEN FOLDER 
            # --------------------------------------------- 
 
            if action == "open_folder": 
 
                success, message = ( 
                    app.open_folder( 
                        body.get( 
                            "path", 
                            "" 
                        ) 
                    ) 
                ) 
 
                self._send_json( 
                    { 
                        "success": success, 
                        "status": ( 
                            "success" 
                            if success 
                            else "error" 
                        ), 
                        "message": message, 
                        "msg": message 
                    } 
                ) 
 
                return 
 
            # --------------------------------------------- 
            # RECREATE STRUCTURE 
            # --------------------------------------------- 
 
            if action == "recreate_structure": 
 
                success, message = ( 
                    app.recreate_structure( 
                        body.get( 
                            "src_path", 
                            "" 
                        ), 
                        body.get( 
                            "dest_path", 
                            "" 
                        ) 
                    ) 
                ) 
 
                self._send_json( 
                    { 
                        "success": success, 
                        "status": ( 
                            "success" 
                            if success 
                            else "error" 
                        ), 
                        "message": message, 
                        "msg": message 
                    } 
                ) 
 
                return 
 
            # --------------------------------------------- 
            # ADVANCED SEGREGATION 
            # --------------------------------------------- 
 
            if action == "segregate_advanced": 
 
                success, message = ( 
                    app.segregate( 
                        body.get( 
                            "src_path", 
                            "" 
                        ), 
                        body.get( 
                            "rule_type", 
                            "" 
                        ), 
                        body.get( 
                            "rule_value" 
                        ), 
                        body.get( 
                            "dest_path" 
                        ) 
                    ) 
                ) 
 
                self._send_json( 
                    { 
                        "success": success, 
                        "status": ( 
                            "success" 
                            if success 
                            else "error" 
                        ), 
                        "message": message, 
                        "msg": message 
                    } 
                ) 
 
                return 
 
            # --------------------------------------------- 
            # REMOVE TARGET 
            # 
            # Deliberately does not mutate File.csv. 
            # 
            # A target is not a separate database object. 
            # Removing it from a UI list would otherwise 
            # contradict the CSV-only architecture. 
            # --------------------------------------------- 
 
            if action == "remove_target": 
 
                self._send_json( 
                    { 
                        "success": False, 
                        "status": "error", 
                        "message": ( 
                            "Targets are derived from File.csv " 
                            "and cannot be removed independently." 
                        ), 
                        "msg": ( 
                            "Targets are derived from File.csv " 
                            "and cannot be removed independently." 
                        ) 
                    }, 
                    400 
                ) 
 
                return 
 
            self._send_json( 
                { 
                    "success": False, 
                    "status": "error", 
                    "message": ( 
                        f"Unknown API action: {action}" 
                    ), 
                    "msg": ( 
                        f"Unknown API action: {action}" 
                    ) 
                }, 
                404 
            ) 
 
            return 
 
        self.send_error( 
            404, 
            "Not found" 
        ) 
 
    # ========================================================= 
    # LOGGING 
    # ========================================================= 
 
    def log_message( 
        self, 
        format, 
        *args 
    ): 
 
        print( 
            "[HTTP]", 
            format % args 
        ) 
 
 
# ============================================================= 
# SERVER STARTUP 
# ============================================================= 
 
def find_free_port(): 
 
    socket_obj = socket.socket( 
        socket.AF_INET, 
        socket.SOCK_STREAM 
    ) 
 
    try: 
 
        socket_obj.bind( 
            ( 
                "127.0.0.1", 
                0 
            ) 
        ) 
 
        return socket_obj.getsockname()[1] 
 
    finally: 
 
        socket_obj.close() 
 
 
def start_server(): 
 
    app = AXFileServer() 
 
    # --------------------------------------------------------- 
    # Generate derived browser data if the persistent index 
    # already exists. 
    # --------------------------------------------------------- 
 
    if os.path.isfile( 
        CSV_FILE 
    ): 
 
        try: 
 
            app.generate_browser_data() 
 
        except Exception as error: 
 
            print( 
                "[SERVER] Initial data generation failed:", 
                error 
            ) 
 
    port = find_free_port() 
 
    server = ThreadingHTTPServer( 
        ( 
            "127.0.0.1", 
            port 
        ), 
        RequestHandler 
    ) 
 
    server.ax_app = app 
 
    url = ( 
        f"http://127.0.0.1:{port}/" 
    ) 
 
    print() 
    print( 
        "========================================" 
    ) 
    print( 
        "       AX FILE OPERATIONS CO-PILOT" 
    ) 
    print( 
        "========================================" 
    ) 
    print() 
    print( 
        f"File index : {CSV_FILE}" 
    ) 
    print( 
        f"Server     : {url}" 
    ) 
    print() 
    print( 
        "Persistent state : File.csv" 
    ) 
    print( 
        "Browser cache    : file_data.js" 
    ) 
    print() 
    print( 
        "Press CTRL+C to stop the server." 
    ) 
    print() 
 
    threading.Timer( 
        0.8, 
        lambda: webbrowser.open( 
            url 
        ) 
    ).start() 
 
    try: 
 
        server.serve_forever() 
 
    except KeyboardInterrupt: 
 
        print() 
        print( 
            "[SERVER] Shutting down..." 
        ) 
 
    finally: 
 
        server.server_close() 
 
 
if __name__ == "__main__": 
 
    start_server() can u please add the features I have demanded for 
### 1. CSV is the single source of truth

There should be one authoritative index:

`File.csv`

Potentially followed by:

`File_2.csv`, `File_3.csv`, etc. only when the CSV row limit is reached.

No `targets.json` should be required for the indexing model.

The target folders themselves should be represented in `File.csv`.

### 2. Add Target Folder

When the user clicks:

`+ ADD FOLDER`

the program opens the Windows folder browser.

Suppose the user selects:

`D:\Projects`

The system should immediately make `D:\Projects` an indexed root.

It should then scan:

`D:\Projects`
→ files
→ folders
→ subfolders
→ files inside subfolders
→ deeper subfolders
→ etc.

The complete hierarchy becomes part of `File.csv`.

### 3. Folder hierarchy representation

Your original idea is essentially a lightweight filesystem graph represented using CSV.

For example:

```text
Path                         Folder       F1          F2          F3
D:\Projects                  Projects     main.py     README.md   *src
D:\Projects\src              src          test.py     *utils
D:\Projects\src\utils        utils        helper.py
```

The important rule is:

`*folder_name`

means that the item is a folder and therefore points to another `Path` row.

Files remain unchanged:

```text
main.py
README.md
test.py
```

Folders become:

```text
*src
*utils
```

And folders are always placed after files within the same row.

This is one of the central design decisions of the project.

### 4. Initial indexing

The first time a target is added:

```text
ADD FOLDER
      ↓
Select folder
      ↓
Scan complete hierarchy
      ↓
Create/update File.csv
```

The system should not merely record the selected folder.

It must actually index everything underneath it.

### 5. Update / Rescan

This is where the current implementation is conceptually incomplete.

When the user presses:

`UPDATE`

the system should NOT blindly recreate the entire CSV from scratch.

Instead, conceptually:

```text
Existing File.csv
        ↓
Read existing indexed paths
        ↓
Check those paths on disk
        ↓
Detect:
    new files
    deleted files
    new folders
    deleted folders
    renamed/moved items
        ↓
Update File.csv
```

The filesystem is the external state.

`File.csv` is the recorded index of that state.

So the update operation reconciles:

```text
REAL FILESYSTEM
       ↕
   File.csv
```

That distinction is important.

### 6. New files

Suppose the CSV currently contains:

```text
D:\Projects\src    src    test.py    *utils
```

and someone creates:

```text
D:\Projects\src    src    test.py    new.py    *utils
```

After UPDATE:

```text
D:\Projects\src    src    test.py    new.py    *utils
```

The new file is incorporated.

### 7. New folders

If:

```text
D:\Projects\src\new_folder
```

is created, UPDATE should discover it and create its corresponding `Path` record.

For example:

```text
D:\Projects\src
D:\Projects\src\new_folder
```

The parent row contains:

```text
*new_folder
```

### 8. Deleted files

Your original requirement is stronger than simply removing deleted files.

If:

```text
report.pdf
```

was previously indexed and subsequently deleted, the CSV should retain evidence of the deletion.

Something along the lines of:

```text
[DELETED_20260817_1530]_report.pdf
```

This gives you a basic historical ledger.

I would preserve this behaviour, but later we should define exactly how deleted folders are represented because deleting a folder can imply hundreds of deleted descendants.

### 9. File/folder distinction

The `*` convention should remain.

It is simple and fits your CSV-oriented design:

```text
F1    report.pdf
F2    image.png
F3    *Documents
F4    *Projects
```

No additional database field is necessary just to identify folders.

### 10. Search

The browser GUI should search the CSV-derived index.

Search should eventually support:

```text
filename
folder
extension
path
```

For example:

`report`

could find:

```text
report.pdf
monthly_report.docx
report_backup.zip
```

### 11. Extension statistics

Because the index already knows filenames, the system can derive:

```text
.pdf     428
.docx    152
.py       93
.jpg     731
.mp4     204
```

This should be generated from the CSV/index rather than maintained separately.

### 12. File information

Selecting a file can show information such as:

```text
Name
Extension
Full Path
Parent Folder
Size
Created
Modified
```

This does not necessarily need to be permanently stored in `File.csv`.

The CSV can remain lightweight while the GUI obtains detailed metadata from the OS when requested.

That is closer to your original intention.

### 13. Open file

Clicking a result should allow:

`OPEN`

which launches the file using the operating system's default application.

### 14. Show in folder

Another operation:

`SHOW IN FOLDER`

should open Windows Explorer and highlight the selected file.

The current `copilot_server.py` already attempts this with Explorer. 

### 15. Directory tree

The GUI should be able to construct a visual tree from:

```text
Path
+
*folder references
```

For example:

```text
D:
└── Projects
    ├── README.md
    ├── main.py
    ├── src
    │   ├── test.py
    │   └── utils
    │       └── helper.py
    └── assets
        └── image.png
```

This is a visual representation of the CSV, not a second source of truth.

### 16. Folder structure cloning

Because the CSV contains every folder path, the program can reconstruct only the directories.

Example:

```text
Original
D:\Projects
├── src
│   └── utils
├── assets
└── documentation
```

Clone to:

```text
E:\Backup
├── src
│   └── utils
├── assets
└── documentation
```

No files need to be copied.

### 17. File segregation

This is a separate operational feature.

Example:

```text
Downloads
├── a.pdf
├── b.pdf
├── c.docx
├── d.jpg
└── e.png
```

The system could create:

```text
Downloads
├── PDF
│   ├── a.pdf
│   └── b.pdf
├── DOCX
│   └── c.docx
└── IMAGE
    ├── d.jpg
    └── e.png
```

Your current server already has an extension segregation implementation. 

### 18. Advanced segregation

Later, the same mechanism can operate on:

```text
Extension
Size
Age / modified date
```

For example:

```text
Move files > 500 MB
Move files older than 180 days
Move all PDFs
```

The current implementation has these three rule types, although they currently operate directly on the filesystem rather than being driven by the CSV index. 

### 19. Target management

This is where I would change the current design significantly.

Currently:

```text
targets.json
     ↓
target folders
```

The current server explicitly reads and writes `targets.json` for `get_targets`, `add_target`, `remove_target`, and folder browsing. 

Your intended model appears to be:

```text
File.csv
   ↓
Indexed root paths
   ↓
Complete hierarchy
```

Therefore, target management should eventually derive its information from `File.csv`.

### 20. Automatic update

Your original idea has two update triggers:

```text
MANUAL
   UPDATE button
```

and eventually:

```text
SYSTEM STARTUP
   ↓
AX File Operations
   ↓
UPDATE INDEX
```

I would keep startup indexing as a future feature rather than making it part of the first stable version.

### 21. CSV chaining

Your `CHN` idea is valid.

For example:

```text
File.csv
     ↓
reaches limit
     ↓
CHN | File_2.csv
```

then:

```text
File_2.csv
     ↓
CHN | File_3.csv
```

The application treats them as one logical index.

This is particularly important because the CSV format itself has a practical spreadsheet row limit.see the update is still not working plus not the dialog I want the features I told to be modified in my program html for u : <!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>File Operations Co-pilot</title>

    <!-- Google Fonts -->

    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <script src="https://cdn.tailwindcss.com"></script> 

    <script> 

        window.SOTO_SERVER_URL = ""; 

        window.sotoFileData = []; 

         

        function loadScript(src) { 

            return new Promise((resolve) => { 

                const script = document.createElement('script'); 

                script.src = src + "?t=" + new Date().getTime(); 

                script.onload = () => resolve(true); 

                script.onerror = () => resolve(false); 

                document.head.appendChild(script); 

            }); 

        } 

    </script> 

    <script> 

        tailwind.config = { 

            theme: { 

                extend: { 

                    fontFamily: { 

                        sans: ['Plus Jakarta Sans', 'sans-serif'], 

                        mono: ['JetBrains Mono', 'monospace'], 

                    } 

                } 

            } 

        } 

    </script> 

    <style> 

        body { 

            background-color: #FFFFFF; 

            font-family: 'Plus Jakarta Sans', sans-serif; 

        } 

        /* Custom scrollbar */ 

        ::-webkit-scrollbar { 

            width: 6px; 

            height: 6px; 

        } 

        ::-webkit-scrollbar-track { 

            background: transparent; 

        } 

        ::-webkit-scrollbar-thumb { 

            background: #cbd5e1; 

            border-radius: 4px; 

        } 

        ::-webkit-scrollbar-thumb:hover { 

            background: #94a3b8; 

        } 

        .animate-fade-in { 

            animation: fadeIn 0.2s ease-out; 

        } 

        @keyframes fadeIn { 

            from { opacity: 0; transform: translateY(4px); } 

            to { opacity: 1; transform: translateY(0); } 

        } 

    </style> 

</head> 

<body class="min-h-screen flex flex-col text-slate-800 bg-white"> 

 

    <!-- Top Navigation Bar / Large Search Section --> 

    <header class="bg-white border-b border-slate-100 sticky top-0 z-50 px-6 py-4 shadow-sm"> 

        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6"> 

            <div class="flex items-center gap-3 shrink-0"> 

                <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center font-bold text-white shadow-md shadow-blue-500/20 text-xl"> 

                    📁 

                </div> 

                <div> 

                    <h1 class="text-xl font-extrabold tracking-tight text-slate-900">SOTO File Co-pilot</h1> 

                    <p class="text-[11px] text-slate-400 font-medium">Deterministic File Dictionary & Operations</p> 

                </div> 

            </div> 

             

            <!-- Large Prominent Blue Search Bar --> 

            <div class="flex-1 w-full max-w-3xl relative"> 

                <input type="text" id="searchBar" placeholder="Search files, extensions, folders, paths..."  

                    class="w-full pl-6 pr-12 py-3.5 rounded-2xl text-slate-900 bg-slate-50 border-2 border-transparent focus:border-blue-500 focus:bg-white focus:outline-none shadow-sm focus:ring-4 focus:ring-blue-500/10 transition-all text-base" 

                    oninput="filterData()"> 

                <span class="absolute right-5 top-4.5 text-slate-400 text-lg">🔍</span> 

            </div> 

             

            <div class="flex items-center gap-2"> 

                <button onclick="triggerUpdate()" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-5 rounded-xl shadow-sm hover:shadow transition-all flex items-center gap-2 text-sm"> 

                    <span>🔄</span> Update Matrix 

                </button> 

            </div> 

        </div> 

    </header> 

 

    <!-- Main Content Area --> 

    <div class="flex flex-1 overflow-hidden max-w-7xl w-full mx-auto"> 

         

        <!-- Left panel: Filters, Tree & Path Management --> 

        <aside class="w-80 border-r border-slate-100 p-6 overflow-y-auto flex flex-col gap-6 bg-slate-50/50"> 

             

            <!-- Target Directories Manager --> 

            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 

                <div class="flex justify-between items-center mb-3"> 

                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Targets List</h3> 

                    <button onclick="browseNewFolder()" class="text-xs text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-0.5"> 

                        ➕ Add Folder 

                    </button> 

                </div> 

                <div id="targetPathsContainer" class="space-y-1 max-h-40 overflow-y-auto pr-1"> 

                    <!-- Target paths loaded here --> 

                    <div class="text-xs text-slate-400 italic">No target paths configured.</div> 

                </div> 

            </div> 

 

            <!-- Stats Dashboard summary --> 

            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 

                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Indexed Stats</h3> 

                <div class="grid grid-cols-2 gap-3 mb-4"> 

                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100"> 

                        <span class="block text-[10px] text-slate-400 font-bold uppercase">Total Files</span> 

                        <span id="statFiles" class="text-lg font-extrabold text-slate-800">0</span> 

                    </div> 

                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100"> 

                        <span class="block text-[10px] text-slate-400 font-bold uppercase">Total Folders</span> 

                        <span id="statFolders" class="text-lg font-extrabold text-slate-800">0</span> 

                    </div> 

                </div> 

                <h4 class="text-xs font-bold text-slate-500 mb-2">Top Extensions</h4> 

                <div id="extensionFilters" class="flex flex-wrap gap-1.5"> 

                    <!-- Dynamic extension tags --> 

                </div> 

            </div> 

 

            <!-- Folder Reconstitution Tools --> 

            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 

                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Recreate Folder Tree</h3> 

                <div class="space-y-3"> 

                    <div> 

                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Source Folder</label> 

                        <input type="text" id="recreateSrc" placeholder="e.g. C:\Users\..." class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 

                    </div> 

                    <div> 

                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Destination Target</label> 

                        <input type="text" id="recreateDest" placeholder="e.g. D:\ClonedFolder" class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 

                    </div> 

                    <button onclick="triggerRecreateStructure()" class="w-full bg-slate-800 hover:bg-slate-900 text-white font-bold py-2 rounded-lg text-xs transition"> 

                        🛠️ Clone Empty Folders Structure 

                    </button> 

                </div> 

            </div> 

 

            <!-- Advanced Segregation Tools --> 

            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm"> 

                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Advanced Segregation</h3> 

                <div class="space-y-3"> 

                    <div> 

                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Source Directory</label> 

                        <input type="text" id="segSrc" placeholder="e.g. C:\Downloads" class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 

                    </div> 

                    <div> 

                        <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Destination Directory</label> 

                        <input type="text" id="segDest" placeholder="e.g. C:\Sorted" class="w-full text-xs px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 

                    </div> 

                    <div class="grid grid-cols-2 gap-2"> 

                        <div> 

                            <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Rule Type</label> 

                            <select id="segRuleType" class="w-full text-xs px-2 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 

                                <option value="extension">Extension</option> 

                                <option value="size">Size (>= MB)</option> 

                                <option value="date">Age (>= Days)</option> 

                            </select> 

                        </div> 

                        <div> 

                            <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1">Value</label> 

                            <input type="text" id="segRuleVal" placeholder=".pdf or 10 or 30" class="w-full text-xs px-2 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-blue-500"> 

                        </div> 

                    </div> 

                    <button onclick="triggerAdvancedSegregation()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg text-xs transition"> 

                        📦 Execute Segregate Move 

                    </button> 

                </div> 

            </div> 

 

            <!-- Optional Directory Tree Collapsible Section --> 

            <div> 

                <div class="flex justify-between items-center mb-3"> 

                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Directory Navigation</h3> 

                    <button onclick="toggleTreeCollapse()" class="text-xs text-blue-600 hover:underline">Toggle Tree</button> 

                </div> 

                <div id="treeWrapper" class="transition-all duration-200 max-h-[300px] overflow-y-auto"> 

                    <div id="treeContainer" class="text-xs font-mono text-slate-600 space-y-1"></div> 

                </div> 

            </div> 

 

        </aside> 

 

        <!-- Right / Main panel: File Card List --> 

        <main class="flex-1 p-6 overflow-y-auto bg-slate-50 flex flex-col"> 

            <div id="searchHeading" class="mb-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Showing Search Results</div> 

             

            <div id="resultsGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"> 

                <!-- Dynamically populated cards --> 

            </div> 

             

            <div id="emptyState" class="hidden flex-1 flex-col items-center justify-center py-20 text-center"> 

                <span class="text-5xl mb-4">🔍</span> 

                <h3 class="text-lg font-bold text-slate-700">No matching files found</h3> 

                <p class="text-sm text-slate-400 max-w-sm mt-1">Try refining your filters or verify your directories are indexed in the target list.</p> 

            </div> 

        </main> 

 

    </div> 

 

    <!-- Script Layer --> 

    <script> 

        let allItems = []; 

        let targetsList = []; 

 

        window.onload = async () => { 

            // Dynamically load scripts with cache busting before initializing 

            await loadScript('server_config.js'); 

            await loadScript('file_data.js'); 

 

            loadTargets(); 

            if (window.sotoFileData && window.sotoFileData.length > 0) { 

                parseLoadedData(window.sotoFileData); 

            } else { 

                fetch('File.csv') 

                    .then(res => { 

                        if (!res.ok) throw new Error("CSV file not found"); 

                        return res.text(); 

                    }) 

                    .then(parseCSV) 

                    .catch(err => { 

                        console.error("Could not load File.csv:", err); 

                        document.getElementById('resultsGrid').innerHTML = ''; 

                        document.getElementById('emptyState').classList.remove('hidden'); 

                    }); 

            } 

        }; 

 

        // Helper to check if server config is active 

        function getApiUrl() { 

            return window.SOTO_SERVER_URL ? window.SOTO_SERVER_URL + '/api' : '/api'; 

        } 

 

        // Load targets from backend json or localStorage fallback 

        async function loadTargets() { 

            let serverSuccess = false; 

            try { 

                const res = await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({ action: "get_targets" }) 

                }); 

                const data = await res.json(); 

                if(data.status === "success" && data.targets) { 

                    targetsList = data.targets; 

                    localStorage.setItem('soto_targets', JSON.stringify(targetsList)); 

                    serverSuccess = true; 

                } 

            } catch(e) { 

                console.warn("Could not reach Python API server. Using localStorage fallback."); 

            } 

 

            if (!serverSuccess) { 

                const localTargets = localStorage.getItem('soto_targets'); 

                if (localTargets) { 

                    targetsList = JSON.parse(localTargets); 

                } 

            } 

            renderTargets(); 

        } 

 

        function renderTargets() { 

            const container = document.getElementById('targetPathsContainer'); 

            if(targetsList.length === 0) { 

                container.innerHTML = `<div class="text-xs text-slate-400 italic">No target paths configured.</div>`; 

                return; 

            } 

            container.innerHTML = targetsList.map(t => ` 

                <div class="flex items-center justify-between gap-2 p-1.5 hover:bg-slate-100 rounded-lg group transition-all"> 

                    <span class="text-xs font-mono text-slate-600 truncate flex-1" title="${t}">${t}</span> 

                    <button onclick="removeTarget('${t.replace(/\\/g, '\\\\')}')" class="text-slate-400 hover:text-red-500 text-xs font-bold px-1 rounded transition opacity-0 group-hover:opacity-100">❌</button> 

                </div> 

            `).join(''); 

        } 

 

        async function browseNewFolder() { 

            // Since the user prefers zero-server architecture, we skip any backend calls. 

            // Prompt user for a folder path manually. 

            const path = prompt("Enter target directory path (e.g., X:\\Alexander):"); 

            if (!path) return; // User cancelled. 

            const normalized = path.trim(); 

            if (!normalized) return; 

            // Update localStorage targets list. 

            let targets = []; 

            const stored = localStorage.getItem('soto_targets'); 

            if (stored) { 

                try { targets = JSON.parse(stored); } catch(e) { targets = []; } 

            } 

            if (!targets.includes(normalized)) { 

                targets.push(normalized); 

                localStorage.setItem('soto_targets', JSON.stringify(targets)); 

            } 

            // Update global variable and UI. 

            targetsList = targets; 

            renderTargets(); 

            // Also set the source fields for other tools. 

            document.getElementById('recreateSrc').value = normalized; 

            document.getElementById('segSrc').value = normalized; 

        } 

 

        async function removeTarget(path) { 

            try { 

                await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({ action: "remove_target", path: path }) 

                }); 

            } catch(e) { 

                console.warn("Could not reach Python API server to remove target:", e); 

            } 

            targetsList = targetsList.filter(t => t !== path); 

            localStorage.setItem('soto_targets', JSON.stringify(targetsList)); 

            renderTargets(); 

        } 

 

        // CSV parsing with quoting support 

        function parseCSVLine(text) { 

            let p = '', c = []; 

            let insideQuote = false; 

            for (let i = 0; i < text.length; i++) { 

                let char = text[i]; 

                if (char === '"') { 

                    insideQuote = !insideQuote; 

                } else if (char === ',' && !insideQuote) { 

                    c.push(p); 

                    p = ''; 

                } else { 

                    p += char; 

                } 

            } 

            c.push(p); 

            return c.map(val => { 

                val = val.trim(); 

                if (val.startsWith('"') && val.endsWith('"')) { 

                    val = val.substring(1, val.length - 1); 

                } 

                return val; 

            }); 

        } 

 

        function parseCSV(csvText) { 

            allItems = []; 

            const lines = csvText.split('\n'); 

            let exts = {}; 

            let fileCount = 0; 

            let folderCount = 0; 

 

            for(let i = 1; i < lines.length; i++) { 

                const line = lines[i].trim(); 

                if(!line) continue; 

                 

                const cols = parseCSVLine(line); 

                if(cols.length < 2 || cols[0] === 'CHN') continue; 

                 

                const basePath = cols[0]; 

                for(let j = 2; j < cols.length; j++) { 

                    const item = cols[j].trim(); 

                    if(!item) continue; 

 

                    const isDeleted = item.startsWith("[DELETED"); 

                    const isFolder = item.startsWith("*"); 

                    const name = isFolder ? item.substring(1) : (isDeleted ? item.split(']_')[1] : item); 

                    const ext = (!isFolder && name.includes('.')) ? '.' + name.split('.').pop().toLowerCase() : 'folder'; 

                     

                    if (isFolder) { 

                        folderCount++; 

                    } else { 

                        fileCount++; 

                        if (!isDeleted) { 

                            exts[ext] = (exts[ext] || 0) + 1; 

                        } 

                    } 

 

                    allItems.push({ 

                        name: name, 

                        path: basePath + '\\' + name, 

                        parent: basePath, 

                        isFolder: isFolder, 

                        isDeleted: isDeleted, 

                        ext: ext 

                    }); 

                } 

            } 

 

            document.getElementById('statFiles').innerText = fileCount; 

            document.getElementById('statFolders').innerText = folderCount; 

 

            renderExtensions(exts); 

            filterData(); 

            buildTree(); 

        } 

 

        function parseLoadedData(dataList) { 

            allItems = dataList; 

            let exts = {}; 

            let fileCount = 0; 

            let folderCount = 0; 

 

            allItems.forEach(item => { 

                if (item.isFolder) { 

                    folderCount++; 

                } else { 

                    fileCount++; 

                    if (!item.isDeleted && item.ext) { 

                        exts[item.ext] = (exts[item.ext] || 0) + 1; 

                    } 

                } 

            }); 

 

            document.getElementById('statFiles').innerText = fileCount; 

            document.getElementById('statFolders').innerText = folderCount; 

 

            renderExtensions(exts); 

            filterData(); 

            buildTree(); 

        } 

 

        function renderExtensions(exts) { 

            const container = document.getElementById('extensionFilters'); 

            const sorted = Object.entries(exts).sort((a,b) => b[1] - a[1]).slice(0, 16); 

            container.innerHTML = sorted.map(([ext, count]) => ` 

                <button onclick="document.getElementById('searchBar').value='${ext}'; filterData()"  

                 class="px-2.5 py-1 bg-white border border-slate-200 text-slate-600 rounded-lg text-xs font-semibold hover:border-blue-500 hover:text-blue-600 shadow-sm transition-all"> 

                 ${ext} <span class="text-[10px] text-slate-400 font-bold ml-1">${count}</span> 

                </button> 

            `).join(''); 

        } 

 

        function filterData() { 

            const query = document.getElementById('searchBar').value.toLowerCase().trim(); 

            const grid = document.getElementById('resultsGrid'); 

            const emptyState = document.getElementById('emptyState'); 

             

            let filtered = allItems; 

            if (query) { 

                filtered = allItems.filter(i =>  

                    i.name.toLowerCase().includes(query) ||  

                    i.ext.includes(query) ||  

                    i.parent.toLowerCase().includes(query) 

                ); 

            } 

 

            // Slice to 100 for fast UI rendering 

            const renderList = filtered.slice(0, 100); 

 

            if(renderList.length === 0) { 

                grid.innerHTML = ''; 

                emptyState.classList.remove('hidden'); 

                document.getElementById('searchHeading').innerText = `No items found`; 

            } else { 

                emptyState.classList.add('hidden'); 

                document.getElementById('searchHeading').innerText = `Showing ${renderList.length} of ${filtered.length} matches`; 

                 

                grid.innerHTML = renderList.map(item => ` 

                    <div class="animate-fade-in bg-white p-4 rounded-2xl border border-slate-100 flex flex-col justify-between hover:border-blue-400/60 hover:shadow-lg hover:shadow-blue-500/5 transition-all duration-200 relative group"> 

                        <div class="flex items-start gap-3.5 mb-4"> 

                            <div class="text-3xl shrink-0 select-none">${item.isDeleted ? '🗑️' : (item.isFolder ? '📁' : getEmojiForExt(item.ext))}</div> 

                            <div class="overflow-hidden"> 

                                <h4 class="font-bold text-slate-800 text-sm truncate" title="${item.name}">${item.name}</h4> 

                                <p class="text-[10px] text-slate-400 font-mono truncate select-all" title="${item.parent}">${item.parent}</p> 

                            </div> 

                        </div> 

                        <div class="flex justify-between items-center gap-2"> 

                            <span class="text-[9px] font-bold px-2 py-1 rounded-lg tracking-wider ${item.isDeleted ? 'bg-red-50 text-red-600 border border-red-100' : (item.isFolder ? 'bg-amber-50 text-amber-600 border border-amber-100' : 'bg-slate-50 text-slate-500 border border-slate-100')}"> 

                                ${item.isDeleted ? 'DELETED' : (item.isFolder ? 'FOLDER' : item.ext.toUpperCase())} 

                            </span> 

                            <div class="flex gap-1.5 opacity-90 group-hover:opacity-100 transition-opacity"> 

                                <button onclick="openFolderInOS('${item.path.replace(/\\/g, '\\\\')}')" class="bg-slate-50 text-slate-600 hover:bg-slate-100 hover:text-slate-900 p-2 rounded-lg text-xs font-bold transition" title="Show in folder"> 

                                    📂 

                                </button> 

                                <button onclick="openFileInOS('${item.path.replace(/\\/g, '\\\\')}')" class="bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1"> 

                                    OPEN 

                                </button> 

                            </div> 

                        </div> 

                    </div> 

                `).join(''); 

            } 

        } 

 

        function getEmojiForExt(ext) { 

            const map = { 

                '.pdf': '📕', 

                '.docx': '📘', 

                '.doc': '📘', 

                '.xlsx': '📗', 

                '.xls': '📗', 

                '.csv': '📗', 

                '.png': '🖼️', 

                '.jpg': '🖼️', 

                '.jpeg': '🖼️', 

                '.gif': '🖼️', 

                '.txt': '📄', 

                '.md': '📝', 

                '.zip': '📦', 

                '.rar': '📦', 

                '.exe': '⚙️', 

                '.py': '🐍', 

                '.html': '🌐' 

            }; 

            return map[ext] || '📄'; 

        } 

 

        function buildTree() { 

            const tree = document.getElementById('treeContainer'); 

            const uniquePaths = [...new Set(allItems.map(i => i.parent))].slice(0, 40); 

            tree.innerHTML = uniquePaths.map(p => { 

                const folderName = p.split('\\').pop() || p; 

                return ` 

                    <div class="truncate py-1 px-2 hover:bg-slate-100 rounded-lg cursor-pointer flex items-center gap-1.5 text-slate-700 transition"  

                         onclick="document.getElementById('searchBar').value='${folderName}'; filterData()"  

                         title="${p}"> 

                        <span class="text-amber-500 text-sm">📁</span> 

                        <span class="font-medium truncate">${folderName}</span> 

                    </div> 

                `; 

            }).join(''); 

        } 

 

        function toggleTreeCollapse() { 

            const tree = document.getElementById('treeWrapper'); 

            tree.classList.toggle('hidden'); 

        } 

 

        // Bridge commands 

        async function openFileInOS(path) { 

            try { 

                const res = await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({ action: "open_file", path: path }) 

                }); 

                const data = await res.json(); 

                if(data.status === "error") alert(data.msg); 

            } catch(e) { 

                alert("Failed to communicate with Python server. Run copilot_server.py to enable file opening."); 

            } 

        } 

 

        async function openFolderInOS(path) { 

            try { 

                const res = await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({ action: "open_folder", path: path }) 

                }); 

                const data = await res.json(); 

                if(data.status === "error") alert(data.msg); 

            } catch(e) { 

                alert("Failed to communicate with Python server. Run copilot_server.py to enable folder highlighting."); 

            } 

        } 

 

        async function triggerUpdate() { 

            document.body.style.cursor = 'wait'; 

            try { 

                await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({ action: "update_index" }) 

                }); 

                window.location.reload(); 

            } catch(e) { 

                alert("Failed to update index. Check python terminal console."); 

                document.body.style.cursor = 'default'; 

            } 

        } 

 

        async function triggerRecreateStructure() { 

            const src = document.getElementById('recreateSrc').value.trim(); 

            const dest = document.getElementById('recreateDest').value.trim(); 

            if(!src || !dest) { 

                alert("Please supply both source and destination paths."); 

                return; 

            } 

            try { 

                const res = await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({ action: "recreate_structure", src_path: src, dest_path: dest }) 

                }); 

                const data = await res.json(); 

                alert(data.msg || (data.status === "success" ? "Done!" : "Error occurred")); 

            } catch(e) { 

                alert("Failed: " + e); 

            } 

        } 

 

        async function triggerAdvancedSegregation() { 

            const src = document.getElementById('segSrc').value.trim(); 

            const dest = document.getElementById('segDest').value.trim(); 

            const ruleType = document.getElementById('segRuleType').value; 

            const ruleVal = document.getElementById('segRuleVal').value.trim(); 

             

            if(!src || !dest || !ruleVal) { 

                alert("Please supply source, destination, and rule values."); 

                return; 

            } 

            try { 

                const res = await fetch(getApiUrl(), { 

                    method: 'POST', 

                    headers: {'Content-Type': 'application/json'}, 

                    body: JSON.stringify({  

                        action: "segregate_advanced",  

                        src_path: src,  

                        dest_path: dest,  

                        rule_type: ruleType,  

                        rule_value: ruleVal  

                    }) 

                }); 

                const data = await res.json(); 

                alert(data.msg || (data.status === "success" ? "Done!" : "Error occurred")); 

                triggerUpdate(); 

            } catch(e) { 

                alert("Failed: " + e); 

            } 

        } 

    </script> 

</body> 

</html>in indexer: import os 

import csv 

from datetime import datetime 

 

 

class FileIndexer: 

    """ 

    AX File Operations Co-pilot 

 

    File.csv is the ONLY persistent source of truth. 

 

    Structure: 

 

        Path | Folder | F1 | F2 | F3 | ... 

 

    Files: 

        report.pdf 

 

    Folders: 

        *Documents 

 

    Deleted entries: 

        D_20260817_1530_report.pdf 

        D_20260817_1530_*Documents 

 

    The Path column always retains the real historical path. 

    """ 

 

    DELETED_PREFIX = "D_" 

    FOLDER_PREFIX = "*" 

 

    def __init__(self, output_file="File.csv", row_limit=999999): 

        self.script_dir = os.path.dirname( 

            os.path.abspath(__file__) 

        ) 

 

        self.output_file = os.path.join( 

            self.script_dir, 

            output_file 

        ) 

 

        self.row_limit = row_limit 

 

    # ========================================================= 

    # PUBLIC 

    # ========================================================= 

 

    def add_target(self, target_path): 

        """ 

        Add and immediately index a target directory. 

 

        The target becomes the highest-level Path in File.csv. 

        """ 

 

        target_path = self._normalise_path(target_path) 

 

        if not os.path.isdir(target_path): 

            print( 

                f"[INDEXER] Invalid folder: {target_path}" 

            ) 

            return False 

 

        records = self._load_csv() 

 

        if self._target_exists_or_overlaps( 

            target_path, 

            records 

        ): 

            print( 

                f"[INDEXER] Target already indexed " 

                f"or overlaps an existing target:\n" 

                f"{target_path}" 

            ) 

            return False 

 

        print( 

            f"[INDEXER] Indexing target:\n" 

            f"{target_path}" 

        ) 

 

        new_records = self._scan_tree( 

            target_path 

        ) 

 

        records.extend(new_records) 

 

        records = self._deduplicate_records( 

            records 

        ) 

 

        self._write_csv(records) 

 

        print( 

            f"[INDEXER] Added {len(new_records)} directories." 

        ) 

 

        return True 

 

    def update(self): 

        """ 

        Incrementally reconcile the existing CSV with 

        the current filesystem. 

 

        Existing directories: 

            - files checked 

            - folders checked 

            - new files detected 

            - new folders detected 

            - deleted files marked 

            - deleted folders marked 

 

        New directories are automatically discovered. 

        """ 

 

        print("[INDEXER] Updating File.csv...") 

 

        records = self._load_csv() 

 

        if not records: 

            print( 

                "[INDEXER] File.csv contains no indexed directories." 

            ) 

            return False 

 

        roots = self._find_roots(records) 

 

        updated = self._reconcile( 

            records, 

            roots 

        ) 

 

        updated = self._deduplicate_records( 

            updated 

        ) 

 

        self._write_csv(updated) 

 

        print( 

            f"[INDEXER] Update complete." 

        ) 

 

        print( 

            f"[INDEXER] Indexed directories: " 

            f"{len(updated)}" 

        ) 

 

        return True 

 

    def scan(self, target_dirs): 

        """ 

        Compatibility method for older code. 

        """ 

 

        for target in target_dirs: 

            self.add_target(target) 

 

    # ========================================================= 

    # SCANNING 

    # ========================================================= 

 

    def _scan_tree(self, target): 

        records = [] 

 

        for current_path, dirnames, filenames in os.walk( 

            target 

        ): 

 

            dirnames.sort( 

                key=str.lower 

            ) 

 

            filenames.sort( 

                key=str.lower 

            ) 

 

            records.append( 

                { 

                    "Path": self._normalise_path( 

                        current_path 

                    ), 

                    "Folder": self._folder_name( 

                        current_path 

                    ), 

                    "Items": self._build_items( 

                        filenames, 

                        dirnames 

                    ) 

                } 

            ) 

 

        return records 

 

    def _build_items( 

        self, 

        filenames, 

        dirnames 

    ): 

        """ 

        Files first. 

        Folders last. 

        """ 

 

        files = sorted( 

            filenames, 

            key=str.lower 

        ) 

 

        folders = sorted( 

            dirnames, 

            key=str.lower 

        ) 

 

        return ( 

            files + 

            [ 

                self.FOLDER_PREFIX + folder 

                for folder in folders 

            ] 

        ) 

 

    # ========================================================= 

    # RECONCILIATION 

    # ========================================================= 

 

    def _reconcile( 

        self, 

        records, 

        roots 

    ): 

        """ 

        Reconcile the complete indexed tree. 

 

        Existing historical records are retained. 

        """ 

 

        old_by_path = { 

            self._normalise_path( 

                record["Path"] 

            ): record 

            for record in records 

        } 

 

        current_paths = set() 

 

        updated = [] 

 

        # ----------------------------------------------------- 

        # 1. Re-scan all directories which still exist. 

        # ----------------------------------------------------- 

 

        for path, old_record in old_by_path.items(): 

 

            if os.path.isdir(path): 

 

                current_paths.add(path) 

 

                new_record = self._reconcile_directory( 

                    path, 

                    old_record 

                ) 

 

                updated.append( 

                    new_record 

                ) 

 

        # ----------------------------------------------------- 

        # 2. Discover new directories. 

        # ----------------------------------------------------- 

 

        discovered = {} 

 

        for root in roots: 

 

            if not os.path.isdir(root): 

                continue 

 

            for current_path, dirnames, filenames in os.walk( 

                root 

            ): 

 

                path = self._normalise_path( 

                    current_path 

                ) 

 

                if path in current_paths: 

                    continue 

 

                if path in discovered: 

                    continue 

 

                dirnames.sort( 

                    key=str.lower 

                ) 

 

                filenames.sort( 

                    key=str.lower 

                ) 

 

                discovered[path] = { 

                    "Path": path, 

                    "Folder": self._folder_name( 

                        current_path 

                    ), 

                    "Items": self._build_items( 

                        filenames, 

                        dirnames 

                    ) 

                } 

 

        updated.extend( 

            discovered.values() 

        ) 

 

        # ----------------------------------------------------- 

        # 3. Preserve deleted directory rows. 

        # ----------------------------------------------------- 

 

        for path, old_record in old_by_path.items(): 

 

            if path not in current_paths: 

 

                deleted_record = ( 

                    self._preserve_deleted_directory( 

                        old_record 

                    ) 

                ) 

 

                updated.append( 

                    deleted_record 

                ) 

 

        return updated 

 

    def _reconcile_directory( 

        self, 

        path, 

        old_record 

    ): 

        """ 

        Compare one existing directory against 

        its previous CSV representation. 

        """ 

 

        try: 

            entries = os.listdir(path) 

 

        except (PermissionError, OSError) as error: 

 

            print( 

                f"[INDEXER] Access denied: " 

                f"{path} -> {error}" 

            ) 

 

            return old_record 

 

        current_files = [] 

        current_folders = [] 

 

        for entry in entries: 

 

            full_path = os.path.join( 

                path, 

                entry 

            ) 

 

            try: 

 

                if os.path.isdir(full_path): 

                    current_folders.append(entry) 

 

                elif os.path.isfile(full_path): 

                    current_files.append(entry) 

 

            except OSError: 

                continue 

 

        current_files.sort( 

            key=str.lower 

        ) 

 

        current_folders.sort( 

            key=str.lower 

        ) 

 

        current_items = self._build_items( 

            current_files, 

            current_folders 

        ) 

 

        old_items = old_record.get( 

            "Items", 

            [] 

        ) 

 

        deleted_items = self._find_deleted_items( 

            old_items, 

            current_items 

        ) 

 

        final_items = ( 

            current_items + 

            deleted_items 

        ) 

 

        return { 

            "Path": path, 

            "Folder": self._folder_name(path), 

            "Items": self._sort_items( 

                final_items 

            ) 

        } 

 

    # ========================================================= 

    # DELETION 

    # ========================================================= 

 

    def _find_deleted_items( 

        self, 

        old_items, 

        current_items 

    ): 

        """ 

        Preserve previously deleted items. 

 

        A live item missing from the current filesystem 

        receives a D_DATE marker. 

 

        Existing D_DATE entries remain untouched. 

        """ 

 

        timestamp = datetime.now().strftime( 

            "%Y%m%d_%H%M" 

        ) 

 

        current_set = set( 

            current_items 

        ) 

 

        deleted = [] 

 

        for old_item in old_items: 

 

            # Already deleted. 

            if old_item.startswith( 

                self.DELETED_PREFIX 

            ): 

                deleted.append( 

                    old_item 

                ) 

                continue 

 

            if old_item not in current_set: 

 

                deleted.append( 

                    self._make_deleted_marker( 

                        old_item, 

                        timestamp 

                    ) 

                ) 

 

        return deleted 

 

    def _make_deleted_marker( 

        self, 

        item, 

        timestamp 

    ): 

        return ( 

            f"{self.DELETED_PREFIX}" 

            f"{timestamp}_" 

            f"{item}" 

        ) 

 

    def _preserve_deleted_directory( 

        self, 

        record 

    ): 

        """ 

        Preserve a directory which no longer exists. 

 

        Its Path remains intact so its historical location 

        can still be searched/opened/displayed. 

        """ 

 

        folder = record.get( 

            "Folder", 

            "" 

        ) 

 

        if not folder.startswith( 

            self.DELETED_PREFIX 

        ): 

            timestamp = datetime.now().strftime( 

                "%Y%m%d_%H%M" 

            ) 

 

            folder = ( 

                f"{self.DELETED_PREFIX}" 

                f"{timestamp}_" 

                f"{folder}" 

            ) 

 

        preserved_items = [] 

 

        for item in record.get( 

            "Items", 

            [] 

        ): 

 

            if item.startswith( 

                self.DELETED_PREFIX 

            ): 

                preserved_items.append( 

                    item 

                ) 

 

            else: 

                timestamp = datetime.now().strftime( 

                    "%Y%m%d_%H%M" 

                ) 

 

                preserved_items.append( 

                    self._make_deleted_marker( 

                        item, 

                        timestamp 

                    ) 

                ) 

 

        return { 

            "Path": record["Path"], 

            "Folder": folder, 

            "Items": preserved_items 

        } 

 

    # ========================================================= 

    # ROOTS 

    # ========================================================= 

 

    def _find_roots( 

        self, 

        records 

    ): 

        """ 

        Infer top-level indexed targets from File.csv. 

 

        Example: 

 

            C:\\Data 

            C:\\Data\\Projects 

            C:\\Data\\Projects\\Python 

 

        Root: 

 

            C:\\Data 

        """ 

 

        paths = sorted( 

            { 

                self._normalise_path( 

                    record["Path"] 

                ) 

                for record in records 

            }, 

            key=len 

        ) 

 

        roots = [] 

 

        for path in paths: 

 

            if not any( 

                self._is_subpath( 

                    path, 

                    root 

                ) 

                for root in roots 

            ): 

                roots.append( 

                    path 

                ) 

 

        return roots 

 

    # ========================================================= 

    # TARGET VALIDATION 

    # ========================================================= 

 

    def _target_exists_or_overlaps( 

        self, 

        target, 

        records 

    ): 

        target = self._normalise_path( 

            target 

        ) 

 

        roots = self._find_roots( 

            records 

        ) 

 

        for root in roots: 

 

            if root == target: 

                return True 

 

            if self._is_subpath( 

                target, 

                root 

            ): 

                return True 

 

            if self._is_subpath( 

                root, 

                target 

            ): 

                return True 

 

        return False 

 

    # ========================================================= 

    # CSV LOAD 

    # ========================================================= 

 

    def _load_csv(self): 

        records = [] 

 

        current_file = self.output_file 

 

        visited = set() 

 

        while current_file: 

 

            current_file = os.path.abspath( 

                current_file 

            ) 

 

            if current_file in visited: 

                print( 

                    "[INDEXER] CSV chain loop detected." 

                ) 

                break 

 

            visited.add( 

                current_file 

            ) 

 

            if not os.path.exists( 

                current_file 

            ): 

                break 

 

            next_file = None 

 

            try: 

 

                with open( 

                    current_file, 

                    "r", 

                    newline="", 

                    encoding="utf-8", 

                    errors="replace" 

                ) as file: 

 

                    reader = csv.reader( 

                        file 

                    ) 

 

                    next( 

                        reader, 

                        None 

                    ) 

 

                    for row in reader: 

 

                        if not row: 

                            continue 

 

                        if row[0] == "CHN": 

 

                            if len(row) >= 2: 

 

                                next_file = row[1] 

 

                                if not os.path.isabs( 

                                    next_file 

                                ): 

                                    next_file = os.path.join( 

                                        self.script_dir, 

                                        next_file 

                                    ) 

 

                            continue 

 

                        if len(row) < 2: 

                            continue 

 

                        records.append( 

                            { 

                                "Path": row[0], 

                                "Folder": row[1], 

                                "Items": [ 

                                    item 

                                    for item in row[2:] 

                                    if item 

                                ] 

                            } 

                        ) 

 

            except Exception as error: 

 

                print( 

                    f"[INDEXER] CSV read error: " 

                    f"{error}" 

                ) 

 

                break 

 

            current_file = next_file 

 

        return records 

 

    # ========================================================= 

    # CSV WRITE 

    # ========================================================= 

 

    def _write_csv( 

        self, 

        records 

    ): 

        if not records: 

            print( 

                "[INDEXER] Nothing to write." 

            ) 

            return 

 

        records.sort( 

            key=lambda record: ( 

                len(record["Path"]), 

                record["Path"].lower() 

            ) 

        ) 

 

        max_items = max( 

            len(record["Items"]) 

            for record in records 

        ) 

 

        headers = ( 

            ["Path", "Folder"] + 

            [ 

                f"F{i + 1}" 

                for i in range(max_items) 

            ] 

        ) 

 

        self._remove_chain_files() 

 

        file_number = 1 

        row_count = 0 

 

        current_file = self.output_file 

 

        handle = open( 

            current_file, 

            "w", 

            newline="", 

            encoding="utf-8" 

        ) 

 

        writer = csv.writer( 

            handle 

        ) 

 

        writer.writerow( 

            headers 

        ) 

 

        try: 

 

            for record in records: 

 

                if row_count >= self.row_limit: 

 

                    next_file = ( 

                        self._chain_filename( 

                            file_number + 1 

                        ) 

                    ) 

 

                    writer.writerow( 

                        [ 

                            "CHN", 

                            next_file 

                        ] 

                    ) 

 

                    handle.close() 

 

                    file_number += 1 

                    row_count = 0 

 

                    current_file = ( 

                        self._chain_filename( 

                            file_number 

                        ) 

                    ) 

 

                    handle = open( 

                        current_file, 

                        "w", 

                        newline="", 

                        encoding="utf-8" 

                    ) 

 

                    writer = csv.writer( 

                        handle 

                    ) 

 

                    writer.writerow( 

                        headers 

                    ) 

 

                row = [ 

                    record["Path"], 

                    record["Folder"] 

                ] 

 

                row.extend( 

                    record["Items"] 

                ) 

 

                while len(row) < len(headers): 

                    row.append("") 

 

                writer.writerow( 

                    row 

                ) 

 

                row_count += 1 

 

        finally: 

 

            handle.close() 

 

        print( 

            f"[INDEXER] File.csv written: " 

            f"{len(records)} directories." 

        ) 

 

    def _chain_filename( 

        self, 

        number 

    ): 

        base, extension = os.path.splitext( 

            self.output_file 

        ) 

 

        return os.path.basename( 

            f"{base}_{number}{extension}" 

        ) 

 

    def _remove_chain_files(self): 

 

        base, extension = os.path.splitext( 

            self.output_file 

        ) 

 

        number = 2 

 

        while True: 

 

            filename = ( 

                f"{base}_{number}{extension}" 

            ) 

 

            if not os.path.exists( 

                filename 

            ): 

                break 

 

            try: 

                os.remove( 

                    filename 

                ) 

            except OSError: 

                pass 

 

            number += 1 

 

    # ========================================================= 

    # UTILITIES 

    # ========================================================= 

 

    def _folder_name( 

        self, 

        path 

    ): 

        name = os.path.basename( 

            os.path.normpath(path) 

        ) 

 

        return name or path 

 

    def _sort_items( 

        self, 

        items 

    ): 

        """ 

        Live files 

        live folders 

        deleted entries 

        """ 

 

        live_files = [] 

        live_folders = [] 

        deleted = [] 

 

        for item in items: 

 

            if item.startswith( 

                self.DELETED_PREFIX 

            ): 

                deleted.append( 

                    item 

                ) 

 

            elif item.startswith( 

                self.FOLDER_PREFIX 

            ): 

                live_folders.append( 

                    item 

                ) 

 

            else: 

                live_files.append( 

                    item 

                ) 

 

        live_files.sort( 

            key=str.lower 

        ) 

 

        live_folders.sort( 

            key=str.lower 

        ) 

 

        deleted.sort( 

            key=str.lower 

        ) 

 

        return ( 

            live_files + 

            live_folders + 

            deleted 

        ) 

 

    def _deduplicate_records( 

        self, 

        records 

    ): 

        unique = {} 

 

        for record in records: 

 

            path = self._normalise_path( 

                record["Path"] 

            ) 

 

            record["Path"] = path 

 

            unique[path] = record 

 

        return list( 

            unique.values() 

        ) 

 

    def _normalise_path( 

        self, 

        path 

    ): 

        return os.path.normcase( 

            os.path.normpath( 

                os.path.abspath(path) 

            ) 

        ) 

 

    def _is_subpath( 

        self, 

        child, 

        parent 

    ): 

        child = self._normalise_path( 

            child 

        ) 

 

        parent = self._normalise_path( 

            parent 

        ) 

 

        if child == parent: 

            return True 

 

        parent = ( 

            parent.rstrip(os.sep) 

            + os.sep 

        ) 

 

        return child.startswith( 

            parent 

        ) 

 

 

# ============================================================= 

# DIRECT EXECUTION 

# ============================================================= 

 

if __name__ == "__main__": 

 

    indexer = FileIndexer() 

 

    print() 

    print("AX FILE OPERATIONS CO-PILOT") 

    print("============================") 

    print("1. Add folder") 

    print("2. Update") 

    print("3. Exit") 

    print() 

 

    choice = input( 

        "Select: " 

    ).strip() 

 

    if choice == "1": 

 

        path = input( 

            "Folder path: " 

        ).strip().strip('"') 

 

        indexer.add_target( 

            path 

        ) 

 

    elif choice == "2": 

 

        indexer.update() server: import os 

import json 

import shutil 

import socket 

import subprocess 

import threading 

import webbrowser 

import time 

 

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer 

from urllib.parse import urlparse 

 

from file_indexer import FileIndexer 

 

 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

 

HTML_FILE = os.path.join( 

    BASE_DIR, 

    "file_copilot.html" 

) 

 

DATA_FILE = os.path.join( 

    BASE_DIR, 

    "file_data.js" 

) 

 

CSV_FILE = os.path.join( 

    BASE_DIR, 

    "File.csv" 

) 

 

 

class AXFileServer: 

    """ 

    AX File Operations Co-pilot backend. 

 

    Persistent state: 

        File.csv 

 

    Derived state: 

        file_data.js 

 

    File.csv is always treated as the authoritative 

    representation of the indexed filesystem. 

    """ 

 

    def __init__(self): 

        self.indexer = FileIndexer( 

            "File.csv" 

        ) 

 

        self.lock = threading.RLock() 

 

    # ========================================================= 

    # CSV / INDEX DATA 

    # ========================================================= 

 

    def get_records(self): 

        return self.indexer._load_csv() 

 

    def generate_browser_data(self): 

        """ 

        Convert File.csv records into a flat browser dataset. 

 

        This file is only a cache/transport artifact. 

        It is never treated as persistent state. 

        """ 

 

        records = self.get_records() 

 

        items = [] 

 

        for record in records: 

 

            parent = record.get( 

                "Path", 

                "" 

            ) 

 

            if not parent: 

                continue 

 

            for item in record.get( 

                "Items", 

                [] 

            ): 

 

                if not item: 

                    continue 

 

                is_deleted = item.startswith( 

                    self.indexer.DELETED_PREFIX 

                ) 

 

                is_folder = ( 

                    item.startswith( 

                        self.indexer.FOLDER_PREFIX 

                    ) 

                    and not is_deleted 

                ) 

 

                # ------------------------------------------------- 

                # Decode display name. 

                # ------------------------------------------------- 

 

                if is_deleted: 

 

                    name = self._deleted_display_name( 

                        item 

                    ) 

 

                elif is_folder: 

 

                    name = item[1:] 

 

                else: 

 

                    name = item 

 

                # ------------------------------------------------- 

                # Deleted entries must retain their historical 

                # parent/path semantics. 

                # ------------------------------------------------- 

 

                if is_deleted: 

 

                    full_path = os.path.join( 

                        parent, 

                        name 

                    ) 

 

                else: 

 

                    full_path = os.path.join( 

                        parent, 

                        name 

                    ) 

 

                extension = "" 

 

                if is_folder: 

 

                    extension = "folder" 

 

                elif "." in name: 

 

                    extension = ( 

                        "." 

                        + name.rsplit( 

                            ".", 

                            1 

                        )[1].lower() 

                    ) 

 

                items.append( 

                    { 

                        "name": name, 

                        "path": full_path, 

                        "parent": parent, 

                        "isFolder": is_folder, 

                        "isDeleted": is_deleted, 

                        "ext": extension 

                    } 

                ) 

 

        browser_data = ( 

            "window.axFileData = " 

            + json.dumps( 

                items, 

                indent=2, 

                ensure_ascii=False 

            ) 

            + ";\n" 

        ) 

 

        try: 

 

            with open( 

                DATA_FILE, 

                "w", 

                encoding="utf-8" 

            ) as file: 

 

                file.write( 

                    browser_data 

                ) 

 

        except OSError as error: 

 

            print( 

                "[SERVER] Could not generate file_data.js:", 

                error 

            ) 

 

        return items 

 

    def _deleted_display_name( 

        self, 

        item 

    ): 

        """ 

        Convert: 

 

            D_20260817_1530_report.pdf 

 

        into: 

 

            report.pdf 

 

        while leaving malformed historical markers intact. 

        """ 

 

        parts = item.split( 

            "_", 

            3 

        ) 

 

        if len(parts) == 4: 

 

            return parts[3] 

 

        return item 

 

    # ========================================================= 

    # TARGETS 

    # ========================================================= 

 

    def get_targets(self): 

        """ 

        Targets are inferred exclusively from File.csv. 

 

        No separate target database is maintained. 

        """ 

 

        records = self.get_records() 

 

        if not records: 

            return [] 

 

        paths = sorted( 

            { 

                self._normalise( 

                    record["Path"] 

                ) 

                for record in records 

                if record.get("Path") 

            }, 

            key=lambda value: ( 

                len(value), 

                value.lower() 

            ) 

        ) 

 

        targets = [] 

 

        for path in paths: 

 

            if not any( 

                self._is_subpath( 

                    path, 

                    root 

                ) 

                for root in targets 

            ): 

 

                targets.append( 

                    path 

                ) 

 

        return targets 

 

    # ========================================================= 

    # ADD FOLDER 

    # ========================================================= 

 

    def add_folder( 

        self, 

        path 

    ): 

        path = self._normalise( 

            path 

        ) 

 

        if not os.path.isdir(path): 

 

            return ( 

                False, 

                "Folder does not exist." 

            ) 

 

        with self.lock: 

 

            result = self.indexer.add_target( 

                path 

            ) 

 

            if result: 

 

                self.generate_browser_data() 

 

                return ( 

                    True, 

                    "Folder indexed successfully." 

                ) 

 

            return ( 

                False, 

                "Folder could not be indexed. " 

                "It may already be indexed or overlap " 

                "an existing target." 

            ) 

 

    # ========================================================= 

    # UPDATE 

    # ========================================================= 

 

    def update(self): 

 

        with self.lock: 

 

            result = self.indexer.update() 

 

            if result: 

 

                self.generate_browser_data() 

 

                return ( 

                    True, 

                    "Index updated successfully." 

                ) 

 

            return ( 

                False, 

                "Index update failed." 

            ) 

 

    # ========================================================= 

    # OPEN FILE 

    # ========================================================= 

 

    def open_file( 

        self, 

        path 

    ): 

 

        if not path: 

 

            return ( 

                False, 

                "File path required." 

            ) 

 

        path = self._normalise( 

            path 

        ) 

 

        if not os.path.isfile(path): 

 

            return ( 

                False, 

                "File does not exist." 

            ) 

 

        try: 

 

            os.startfile( 

                path 

            ) 

 

            return ( 

                True, 

                "File opened." 

            ) 

 

        except Exception as error: 

 

            return ( 

                False, 

                str(error) 

            ) 

 

    # ========================================================= 

    # OPEN FOLDER 

    # ========================================================= 

 

    def open_folder( 

        self, 

        path 

    ): 

 

        if not path: 

 

            return ( 

                False, 

                "Path required." 

            ) 

 

        path = self._normalise( 

            path 

        ) 

 

        # ----------------------------------------------------- 

        # If the supplied path is a file, open Explorer with 

        # that file selected. 

        # ----------------------------------------------------- 

 

        if os.path.isfile(path): 

 

            try: 

 

                subprocess.Popen( 

                    [ 

                        "explorer.exe", 

                        "/select,", 

                        path 

                    ] 

                ) 

 

                return ( 

                    True, 

                    "File location opened." 

                ) 

 

            except Exception as error: 

 

                return ( 

                    False, 

                    str(error) 

                ) 

 

        # ----------------------------------------------------- 

        # Normal directory. 

        # ----------------------------------------------------- 

 

        if os.path.isdir(path): 

 

            try: 

 

                os.startfile( 

                    path 

                ) 

 

                return ( 

                    True, 

                    "Folder opened." 

                ) 

 

            except Exception as error: 

 

                return ( 

                    False, 

                    str(error) 

                ) 

 

        return ( 

            False, 

            "Path does not exist." 

        ) 

 

    # ========================================================= 

    # FOLDER STRUCTURE CLONING 

    # ========================================================= 

 

    def recreate_structure( 

        self, 

        source, 

        destination 

    ): 

 

        source = self._normalise( 

            source 

        ) 

 

        destination = self._normalise( 

            destination 

        ) 

 

        if not os.path.isdir(source): 

 

            return ( 

                False, 

                "Source folder does not exist." 

            ) 

 

        if source == destination: 

 

            return ( 

                False, 

                "Source and destination cannot be identical." 

            ) 

 

        try: 

 

            for current_path, dirnames, _ in os.walk( 

                source 

            ): 

 

                relative = os.path.relpath( 

                    current_path, 

                    source 

                ) 

 

                if relative == ".": 

 

                    target = destination 

 

                else: 

 

                    target = os.path.join( 

                        destination, 

                        relative 

                    ) 

 

                os.makedirs( 

                    target, 

                    exist_ok=True 

                ) 

 

            # The destination may itself be an indexed target. 

            # Reconcile all known targets afterward. 

 

            self.indexer.update() 

            self.generate_browser_data() 

 

            return ( 

                True, 

                "Folder structure recreated." 

            ) 

 

        except Exception as error: 

 

            return ( 

                False, 

                str(error) 

            ) 

 

    # ========================================================= 

    # FILE SEGREGATION 

    # ========================================================= 

 

    def segregate( 

        self, 

        source, 

        mode, 

        value=None, 

        destination=None 

    ): 

 

        source = self._normalise( 

            source 

        ) 

 

        if not os.path.isdir(source): 

 

            return ( 

                False, 

                "Source folder does not exist." 

            ) 

 

        if destination: 

 

            destination = self._normalise( 

                destination 

            ) 

 

        else: 

 

            destination = source 

 

        mode = str( 

            mode or "" 

        ).strip().lower() 

 

        try: 

 

            moved = 0 

 

            # ------------------------------------------------- 

            # Only files directly inside source are processed. 

            # ------------------------------------------------- 

 

            for filename in os.listdir( 

                source 

            ): 

 

                source_path = os.path.join( 

                    source, 

                    filename 

                ) 

 

                if not os.path.isfile( 

                    source_path 

                ): 

 

                    continue 

 

                # ============================================= 

                # EXTENSION 

                # ============================================= 

 

                if mode == "extension": 

 

                    extension = os.path.splitext( 

                        filename 

                    )[1].lower() 

 

                    if not extension: 

 

                        folder_name = ( 

                            "NO_EXTENSION" 

                        ) 

 

                    else: 

 

                        folder_name = ( 

                            extension[1:] 

                            .upper() 

                        ) 

 

                    target_folder = os.path.join( 

                        destination, 

                        folder_name 

                    ) 

 

                    os.makedirs( 

                        target_folder, 

                        exist_ok=True 

                    ) 

 

                    target_path = ( 

                        self._safe_destination( 

                            target_folder, 

                            filename 

                        ) 

                    ) 

 

                    shutil.move( 

                        source_path, 

                        target_path 

                    ) 

 

                    moved += 1 

 

                # ============================================= 

                # SIZE 

                # ============================================= 

 

                elif mode == "size": 

 

                    if value is None: 

 

                        return ( 

                            False, 

                            "Size value required." 

                        ) 

 

                    try: 

 

                        threshold = float( 

                            value 

                        ) 

 

                    except ValueError: 

 

                        return ( 

                            False, 

                            "Size value must be numeric." 

                        ) 

 

                    size_mb = ( 

                        os.path.getsize( 

                            source_path 

                        ) 

                        / ( 

                            1024 * 1024 

                        ) 

                    ) 

 

                    if size_mb < threshold: 

 

                        continue 

 

                    target_folder = os.path.join( 

                        destination, 

                        f"OVER_{threshold:g}MB" 

                    ) 

 

                    os.makedirs( 

                        target_folder, 

                        exist_ok=True 

                    ) 

 

                    target_path = ( 

                        self._safe_destination( 

                            target_folder, 

                            filename 

                        ) 

                    ) 

 

                    shutil.move( 

                        source_path, 

                        target_path 

                    ) 

 

                    moved += 1 

 

                # ============================================= 

                # AGE 

                # ============================================= 

 

                elif mode in ( 

                    "age", 

                    "date" 

                ): 

 

                    if value is None: 

 

                        return ( 

                            False, 

                            "Age value required." 

                        ) 

 

                    try: 

 

                        threshold = float( 

                            value 

                        ) 

 

                    except ValueError: 

 

                        return ( 

                            False, 

                            "Age value must be numeric." 

                        ) 

 

                    age_seconds = ( 

                        time.time() 

                        - os.path.getmtime( 

                            source_path 

                        ) 

                    ) 

 

                    age_days = ( 

                        age_seconds 

                        / 86400 

                    ) 

 

                    if age_days < threshold: 

 

                        continue 

 

                    target_folder = os.path.join( 

                        destination, 

                        f"OLDER_{threshold:g}_DAYS" 

                    ) 

 

                    os.makedirs( 

                        target_folder, 

                        exist_ok=True 

                    ) 

 

                    target_path = ( 

                        self._safe_destination( 

                            target_folder, 

                            filename 

                        ) 

                    ) 

 

                    shutil.move( 

                        source_path, 

                        target_path 

                    ) 

 

                    moved += 1 

 

                else: 

 

                    return ( 

                        False, 

                        f"Unknown segregation mode: {mode}" 

                    ) 

 

            # ------------------------------------------------- 

            # Filesystem changed. 

            # CSV must now be reconciled. 

            # ------------------------------------------------- 

 

            self.indexer.update() 

            self.generate_browser_data() 

 

            return ( 

                True, 

                f"{moved} file(s) moved." 

            ) 

 

        except Exception as error: 

 

            return ( 

                False, 

                str(error) 

            ) 

 

    # ========================================================= 

    # SAFE FILE MOVING 

    # ========================================================= 

 

    def _safe_destination( 

        self, 

        folder, 

        filename 

    ): 

 

        target = os.path.join( 

            folder, 

            filename 

        ) 

 

        if not os.path.exists( 

            target 

        ): 

 

            return target 

 

        base, extension = os.path.splitext( 

            filename 

        ) 

 

        counter = 1 

 

        while True: 

 

            new_name = ( 

                f"{base}_{counter}" 

                f"{extension}" 

            ) 

 

            target = os.path.join( 

                folder, 

                new_name 

            ) 

 

            if not os.path.exists( 

                target 

            ): 

 

                return target 

 

            counter += 1 

 

    # ========================================================= 

    # FOLDER BROWSER 

    # ========================================================= 

 

    def browse_folder(self): 

 

        try: 

 

            import tkinter as tk 

            from tkinter import filedialog 

 

            root = tk.Tk() 

            root.withdraw() 

            root.attributes( 

                "-topmost", 

                True 

            ) 

 

            path = filedialog.askdirectory() 

 

            root.destroy() 

 

            return path or "" 

 

        except Exception as error: 

 

            print( 

                "[SERVER] Folder browser error:", 

                error 

            ) 

 

            return "" 

 

    # ========================================================= 

    # PATH UTILITIES 

    # ========================================================= 

 

    def _normalise( 

        self, 

        path 

    ): 

 

        return os.path.normpath( 

            os.path.abspath( 

                os.path.expanduser( 

                    str(path) 

                ) 

            ) 

        ) 

 

    def _is_subpath( 

        self, 

        child, 

        parent 

    ): 

 

        child = self._normalise( 

            child 

        ) 

 

        parent = self._normalise( 

            parent 

        ) 

 

        if child == parent: 

 

            return True 

 

        parent = ( 

            parent.rstrip( 

                os.sep 

            ) 

            + os.sep 

        ) 

 

        return child.startswith( 

            parent 

        ) 

 

 

# ============================================================= 

# HTTP HANDLER 

# ============================================================= 

 

class RequestHandler( 

    BaseHTTPRequestHandler 

): 

 

    server_version = "AX-File-CoPilot/2.0" 

 

    # ========================================================= 

    # RESPONSE HELPERS 

    # ========================================================= 

 

    def _send_json( 

        self, 

        data, 

        status=200 

    ): 

 

        payload = json.dumps( 

            data, 

            indent=2, 

            ensure_ascii=False 

        ).encode( 

            "utf-8" 

        ) 

 

        self.send_response( 

            status 

        ) 

 

        self.send_header( 

            "Content-Type", 

            "application/json; charset=utf-8" 

        ) 

 

        self.send_header( 

            "Cache-Control", 

            "no-store" 

        ) 

 

        self.send_header( 

            "Content-Length", 

            str(len(payload)) 

        ) 

 

        self.end_headers() 

 

        self.wfile.write( 

            payload 

        ) 

 

    def _send_file( 

        self, 

        path, 

        content_type 

    ): 

 

        if not os.path.isfile( 

            path 

        ): 

 

            self.send_error( 

                404, 

                "File not found" 

            ) 

 

            return 

 

        try: 

 

            with open( 

                path, 

                "rb" 

            ) as file: 

 

                data = file.read() 

 

        except OSError as error: 

 

            self.send_error( 

                500, 

                str(error) 

            ) 

 

            return 

 

        self.send_response( 

            200 

        ) 

 

        self.send_header( 

            "Content-Type", 

            content_type 

        ) 

 

        self.send_header( 

            "Cache-Control", 

            "no-store" 

        ) 

 

        self.send_header( 

            "Content-Length", 

            str(len(data)) 

        ) 

 

        self.end_headers() 

 

        self.wfile.write( 

            data 

        ) 

 

    def _read_json(self): 

 

        try: 

 

            length = int( 

                self.headers.get( 

                    "Content-Length", 

                    "0" 

                ) 

            ) 

 

            if length <= 0: 

 

                return {} 

 

            raw = self.rfile.read( 

                length 

            ) 

 

            return json.loads( 

                raw.decode( 

                    "utf-8" 

                ) 

            ) 

 

        except Exception: 

 

            return {} 

 

    def _api_error( 

        self, 

        message, 

        status=400 

    ): 

 

        self._send_json( 

            { 

                "success": False, 

                "error": message 

            }, 

            status 

        ) 

 

    # ========================================================= 

    # GET 

    # ========================================================= 

 

    def do_GET(self): 

 

        parsed = urlparse( 

            self.path 

        ) 

 

        path = parsed.path 

 

        app = self.server.ax_app 

 

        # ----------------------------------------------------- 

        # MAIN PAGE 

        # ----------------------------------------------------- 

 

        if path == "/": 

 

            self._send_file( 

                HTML_FILE, 

                "text/html; charset=utf-8" 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # BROWSER DATA 

        # ----------------------------------------------------- 

 

        if path == "/api/data": 

 

            try: 

 

                with app.lock: 

 

                    data = ( 

                        app.generate_browser_data() 

                    ) 

 

                    targets = ( 

                        app.get_targets() 

                    ) 

 

                self._send_json( 

                    { 

                        "success": True, 

                        "data": data, 

                        "targets": targets 

                    } 

                ) 

 

            except Exception as error: 

 

                self._send_json( 

                    { 

                        "success": False, 

                        "error": str(error) 

                    }, 

                    500 

                ) 

 

            return 

 

        # ----------------------------------------------------- 

        # TARGETS 

        # ----------------------------------------------------- 

 

        if path == "/api/targets": 

 

            self._send_json( 

                { 

                    "success": True, 

                    "targets": app.get_targets() 

                } 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # FOLDER BROWSER 

        # ----------------------------------------------------- 

 

        if path == "/api/browse-folder": 

 

            selected = ( 

                app.browse_folder() 

            ) 

 

            self._send_json( 

                { 

                    "success": bool( 

                        selected 

                    ), 

                    "path": selected 

                } 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # GENERATED BROWSER DATA 

        # ----------------------------------------------------- 

 

        if path == "/file_data.js": 

 

            if not os.path.isfile( 

                DATA_FILE 

            ): 

 

                app.generate_browser_data() 

 

            self._send_file( 

                DATA_FILE, 

                "application/javascript; charset=utf-8" 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # SERVER CONFIG 

        # ----------------------------------------------------- 

 

        if path == "/server_config.js": 

 

            payload = ( 

                "window.SOTO_SERVER_URL = '';\n" 

                "window.AX_SERVER_ACTIVE = true;\n" 

            ).encode( 

                "utf-8" 

            ) 

 

            self.send_response( 

                200 

            ) 

 

            self.send_header( 

                "Content-Type", 

                "application/javascript; charset=utf-8" 

            ) 

 

            self.send_header( 

                "Cache-Control", 

                "no-store" 

            ) 

 

            self.send_header( 

                "Content-Length", 

                str(len(payload)) 

            ) 

 

            self.end_headers() 

 

            self.wfile.write( 

                payload 

            ) 

 

            return 

 

        self.send_error( 

            404, 

            "Not found" 

        ) 

 

    # ========================================================= 

    # POST 

    # ========================================================= 

 

    def do_POST(self): 

 

        parsed = urlparse( 

            self.path 

        ) 

 

        path = parsed.path 

 

        body = self._read_json() 

 

        app = self.server.ax_app 

 

        # ----------------------------------------------------- 

        # ADD FOLDER 

        # ----------------------------------------------------- 

 

        if path == "/api/add-folder": 

 

            folder = body.get( 

                "path" 

            ) 

 

            if not folder: 

 

                self._api_error( 

                    "Folder path required." 

                ) 

 

                return 

 

            success, message = ( 

                app.add_folder( 

                    folder 

                ) 

            ) 

 

            self._send_json( 

                { 

                    "success": success, 

                    "message": message, 

                    "targets": app.get_targets() 

                }, 

                200 if success else 400 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # UPDATE 

        # ----------------------------------------------------- 

 

        if path == "/api/update": 

 

            success, message = ( 

                app.update() 

            ) 

 

            self._send_json( 

                { 

                    "success": success, 

                    "message": message 

                }, 

                200 if success else 500 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # OPEN FILE 

        # ----------------------------------------------------- 

 

        if path == "/api/open-file": 

 

            success, message = ( 

                app.open_file( 

                    body.get( 

                        "path", 

                        "" 

                    ) 

                ) 

            ) 

 

            self._send_json( 

                { 

                    "success": success, 

                    "message": message 

                }, 

                200 if success else 400 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # OPEN FOLDER 

        # ----------------------------------------------------- 

 

        if path == "/api/open-folder": 

 

            success, message = ( 

                app.open_folder( 

                    body.get( 

                        "path", 

                        "" 

                    ) 

                ) 

            ) 

 

            self._send_json( 

                { 

                    "success": success, 

                    "message": message 

                }, 

                200 if success else 400 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # RECREATE STRUCTURE 

        # ----------------------------------------------------- 

 

        if path == "/api/recreate-structure": 

 

            source = body.get( 

                "source", 

                body.get( 

                    "src_path", 

                    "" 

                ) 

            ) 

 

            destination = body.get( 

                "destination", 

                body.get( 

                    "dest_path", 

                    "" 

                ) 

            ) 

 

            success, message = ( 

                app.recreate_structure( 

                    source, 

                    destination 

                ) 

            ) 

 

            self._send_json( 

                { 

                    "success": success, 

                    "message": message 

                }, 

                200 if success else 400 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # SEGREGATION 

        # ----------------------------------------------------- 

 

        if path == "/api/segregate": 

 

            source = body.get( 

                "source", 

                body.get( 

                    "src_path", 

                    "" 

                ) 

            ) 

 

            destination = body.get( 

                "destination", 

                body.get( 

                    "dest_path", 

                    "" 

                ) 

            ) 

 

            mode = body.get( 

                "mode", 

                body.get( 

                    "rule_type", 

                    "" 

                ) 

            ) 

 

            value = body.get( 

                "value", 

                body.get( 

                    "rule_value" 

                ) 

            ) 

 

            success, message = ( 

                app.segregate( 

                    source, 

                    mode, 

                    value, 

                    destination 

                ) 

            ) 

 

            self._send_json( 

                { 

                    "success": success, 

                    "message": message 

                }, 

                200 if success else 400 

            ) 

 

            return 

 

        # ----------------------------------------------------- 

        # LEGACY ACTION ROUTING 

        # 

        # This keeps compatibility with the current HTML while 

        # allowing the server to use the cleaner endpoint API. 

        # ----------------------------------------------------- 

 

        if path == "/api": 

 

            action = body.get( 

                "action", 

                "" 

            ) 

 

            # --------------------------------------------- 

            # GET TARGETS 

            # --------------------------------------------- 

 

            if action == "get_targets": 

 

                self._send_json( 

                    { 

                        "success": True, 

                        "status": "success", 

                        "targets": app.get_targets() 

                    } 

                ) 

 

                return 

 

            # --------------------------------------------- 

            # UPDATE 

            # --------------------------------------------- 

 

            if action == "update_index": 

 

                success, message = ( 

                    app.update() 

                ) 

 

                self._send_json( 

                    { 

                        "success": success, 

                        "status": ( 

                            "success" 

                            if success 

                            else "error" 

                        ), 

                        "message": message, 

                        "msg": message 

                    } 

                ) 

 

                return 

 

            # --------------------------------------------- 

            # OPEN FILE 

            # --------------------------------------------- 

 

            if action == "open_file": 

 

                success, message = ( 

                    app.open_file( 

                        body.get( 

                            "path", 

                            "" 

                        ) 

                    ) 

                ) 

 

                self._send_json( 

                    { 

                        "success": success, 

                        "status": ( 

                            "success" 

                            if success 

                            else "error" 

                        ), 

                        "message": message, 

                        "msg": message 

                    } 

                ) 

 

                return 

 

            # --------------------------------------------- 

            # OPEN FOLDER 

            # --------------------------------------------- 

 

            if action == "open_folder": 

 

                success, message = ( 

                    app.open_folder( 

                        body.get( 

                            "path", 

                            "" 

                        ) 

                    ) 

                ) 

 

                self._send_json( 

                    { 

                        "success": success, 

                        "status": ( 

                            "success" 

                            if success 

                            else "error" 

                        ), 

                        "message": message, 

                        "msg": message 

                    } 

                ) 

 

                return 

 

            # --------------------------------------------- 

            # RECREATE STRUCTURE 

            # --------------------------------------------- 

 

            if action == "recreate_structure": 

 

                success, message = ( 

                    app.recreate_structure( 

                        body.get( 

                            "src_path", 

                            "" 

                        ), 

                        body.get( 

                            "dest_path", 

                            "" 

                        ) 

                    ) 

                ) 

 

                self._send_json( 

                    { 

                        "success": success, 

                        "status": ( 

                            "success" 

                            if success 

                            else "error" 

                        ), 

                        "message": message, 

                        "msg": message 

                    } 

                ) 

 

                return 

 

            # --------------------------------------------- 

            # ADVANCED SEGREGATION 

            # --------------------------------------------- 

 

            if action == "segregate_advanced": 

 

                success, message = ( 

                    app.segregate( 

                        body.get( 

                            "src_path", 

                            "" 

                        ), 

                        body.get( 

                            "rule_type", 

                            "" 

                        ), 

                        body.get( 

                            "rule_value" 

                        ), 

                        body.get( 

                            "dest_path" 

                        ) 

                    ) 

                ) 

 

                self._send_json( 

                    { 

                        "success": success, 

                        "status": ( 

                            "success" 

                            if success 

                            else "error" 

                        ), 

                        "message": message, 

                        "msg": message 

                    } 

                ) 

 

                return 

 

            # --------------------------------------------- 

            # REMOVE TARGET 

            # 

            # Deliberately does not mutate File.csv. 

            # 

            # A target is not a separate database object. 

            # Removing it from a UI list would otherwise 

            # contradict the CSV-only architecture. 

            # --------------------------------------------- 

 

            if action == "remove_target": 

 

                self._send_json( 

                    { 

                        "success": False, 

                        "status": "error", 

                        "message": ( 

                            "Targets are derived from File.csv " 

                            "and cannot be removed independently." 

                        ), 

                        "msg": ( 

                            "Targets are derived from File.csv " 

                            "and cannot be removed independently." 

                        ) 

                    }, 

                    400 

                ) 

 

                return 

 

            self._send_json( 

                { 

                    "success": False, 

                    "status": "error", 

                    "message": ( 

                        f"Unknown API action: {action}" 

                    ), 

                    "msg": ( 

                        f"Unknown API action: {action}" 

                    ) 

                }, 

                404 

            ) 

 

            return 

 

        self.send_error( 

            404, 

            "Not found" 

        ) 

 

    # ========================================================= 

    # LOGGING 

    # ========================================================= 

 

    def log_message( 

        self, 

        format, 

        *args 

    ): 

 

        print( 

            "[HTTP]", 

            format % args 

        ) 

 

 

# ============================================================= 

# SERVER STARTUP 

# ============================================================= 

 

def find_free_port(): 

 

    socket_obj = socket.socket( 

        socket.AF_INET, 

        socket.SOCK_STREAM 

    ) 

 

    try: 

 

        socket_obj.bind( 

            ( 

                "127.0.0.1", 

                0 

            ) 

        ) 

 

        return socket_obj.getsockname()[1] 

 

    finally: 

 

        socket_obj.close() 

 

 

def start_server(): 

 

    app = AXFileServer() 

 

    # --------------------------------------------------------- 

    # Generate derived browser data if the persistent index 

    # already exists. 

    # --------------------------------------------------------- 

 

    if os.path.isfile( 

        CSV_FILE 

    ): 

 

        try: 

 

            app.generate_browser_data() 

 

        except Exception as error: 

 

            print( 

                "[SERVER] Initial data generation failed:", 

                error 

            ) 

 

    port = find_free_port() 

 

    server = ThreadingHTTPServer( 

        ( 

            "127.0.0.1", 

            port 

        ), 

        RequestHandler 

    ) 

 

    server.ax_app = app 

 

    url = ( 

        f"http://127.0.0.1:{port}/" 

    ) 

 

    print() 

    print( 

        "========================================" 

    ) 

    print( 

        "       AX FILE OPERATIONS CO-PILOT" 

    ) 

    print( 

        "========================================" 

    ) 

    print() 

    print( 

        f"File index : {CSV_FILE}" 

    ) 

    print( 

        f"Server     : {url}" 

    ) 

    print() 

    print( 

        "Persistent state : File.csv" 

    ) 

    print( 

        "Browser cache    : file_data.js" 

    ) 

    print() 

    print( 

        "Press CTRL+C to stop the server." 

    ) 

    print() 

 

    threading.Timer( 

        0.8, 

        lambda: webbrowser.open( 

            url 

        ) 

    ).start() 

 

    try: 

 

        server.serve_forever() 

 

    except KeyboardInterrupt: 

 

        print() 

        print( 

            "[SERVER] Shutting down..." 

        ) 

 

    finally: 

 

        server.server_close() 

 

 

if __name__ == "__main__": 

 

    start_server() can u please add the features I have demanded for 

### 1. CSV is the single source of truth



There should be one authoritative index:



`File.csv`



Potentially followed by:



`File_2.csv`, `File_3.csv`, etc. only when the CSV row limit is reached.



No `targets.json` should be required for the indexing model.



The target folders themselves should be represented in `File.csv`.



### 2. Add Target Folder



When the user clicks:



`+ ADD FOLDER`



the program opens the Windows folder browser.



Suppose the user selects:



`D:\Projects`



The system should immediately make `D:\Projects` an indexed root.



It should then scan:



`D:\Projects`

→ files

→ folders

→ subfolders

→ files inside subfolders

→ deeper subfolders

→ etc.



The complete hierarchy becomes part of `File.csv`.



### 3. Folder hierarchy representation



Your original idea is essentially a lightweight filesystem graph represented using CSV.



For example:



```text

Path                         Folder       F1          F2          F3

D:\Projects                  Projects     main.py     README.md   *src

D:\Projects\src              src          test.py     *utils

D:\Projects\src\utils        utils        helper.py

```



The important rule is:



`*folder_name`



means that the item is a folder and therefore points to another `Path` row.



Files remain unchanged:



```text

main.py

README.md

test.py

```



Folders become:



```text

*src

*utils

```



And folders are always placed after files within the same row.



This is one of the central design decisions of the project.



### 4. Initial indexing



The first time a target is added:



```text

ADD FOLDER

      ↓

Select folder

      ↓

Scan complete hierarchy

      ↓

Create/update File.csv

```



The system should not merely record the selected folder.



It must actually index everything underneath it.



### 5. Update / Rescan



This is where the current implementation is conceptually incomplete.



When the user presses:



`UPDATE`



the system should NOT blindly recreate the entire CSV from scratch.



Instead, conceptually:



```text

Existing File.csv

        ↓

Read existing indexed paths

        ↓

Check those paths on disk

        ↓

Detect:

    new files

    deleted files

    new folders

    deleted folders

    renamed/moved items

        ↓

Update File.csv

```



The filesystem is the external state.



`File.csv` is the recorded index of that state.



So the update operation reconciles:



```text

REAL FILESYSTEM

       ↕

   File.csv

```



That distinction is important.



### 6. New files



Suppose the CSV currently contains:



```text

D:\Projects\src    src    test.py    *utils

```



and someone creates:



```text

D:\Projects\src    src    test.py    new.py    *utils

```



After UPDATE:



```text

D:\Projects\src    src    test.py    new.py    *utils

```



The new file is incorporated.



### 7. New folders



If:



```text

D:\Projects\src\new_folder

```



is created, UPDATE should discover it and create its corresponding `Path` record.



For example:



```text

D:\Projects\src

D:\Projects\src\new_folder

```



The parent row contains:



```text

*new_folder

```



### 8. Deleted files



Your original requirement is stronger than simply removing deleted files.



If:



```text

report.pdf

```



was previously indexed and subsequently deleted, the CSV should retain evidence of the deletion.



Something along the lines of:



```text

[DELETED_20260817_1530]_report.pdf

```



This gives you a basic historical ledger.



I would preserve this behaviour, but later we should define exactly how deleted folders are represented because deleting a folder can imply hundreds of deleted descendants.



### 9. File/folder distinction



The `*` convention should remain.



It is simple and fits your CSV-oriented design:



```text

F1    report.pdf

F2    image.png

F3    *Documents

F4    *Projects

```



No additional database field is necessary just to identify folders.



### 10. Search



The browser GUI should search the CSV-derived index.



Search should eventually support:



```text

filename

folder

extension

path

```



For example:



`report`



could find:



```text

report.pdf

monthly_report.docx

report_backup.zip

```



### 11. Extension statistics



Because the index already knows filenames, the system can derive:



```text

.pdf     428

.docx    152

.py       93

.jpg     731

.mp4     204

```



This should be generated from the CSV/index rather than maintained separately.



### 12. File information



Selecting a file can show information such as:



```text

Name

Extension

Full Path

Parent Folder

Size

Created

Modified

```



This does not necessarily need to be permanently stored in `File.csv`.



The CSV can remain lightweight while the GUI obtains detailed metadata from the OS when requested.



That is closer to your original intention.



### 13. Open file



Clicking a result should allow:



`OPEN`



which launches the file using the operating system's default application.



### 14. Show in folder



Another operation:



`SHOW IN FOLDER`



should open Windows Explorer and highlight the selected file.



The current `copilot_server.py` already attempts this with Explorer. 



### 15. Directory tree



The GUI should be able to construct a visual tree from:



```text

Path

+

*folder references

```



For example:



```text

D:

└── Projects

    ├── README.md

    ├── main.py

    ├── src

    │   ├── test.py

    │   └── utils

    │       └── helper.py

    └── assets

        └── image.png

```



This is a visual representation of the CSV, not a second source of truth.



### 16. Folder structure cloning



Because the CSV contains every folder path, the program can reconstruct only the directories.



Example:



```text

Original

D:\Projects

├── src

│   └── utils

├── assets

└── documentation

```



Clone to:



```text

E:\Backup

├── src

│   └── utils

├── assets

└── documentation

```



No files need to be copied.



### 17. File segregation



This is a separate operational feature.



Example:



```text

Downloads

├── a.pdf

├── b.pdf

├── c.docx

├── d.jpg

└── e.png

```



The system could create:



```text

Downloads

├── PDF

│   ├── a.pdf

│   └── b.pdf

├── DOCX

│   └── c.docx

└── IMAGE

    ├── d.jpg

    └── e.png

```



Your current server already has an extension segregation implementation. 



### 18. Advanced segregation



Later, the same mechanism can operate on:



```text

Extension

Size

Age / modified date

```



For example:



```text

Move files > 500 MB

Move files older than 180 days

Move all PDFs

```



The current implementation has these three rule types, although they currently operate directly on the filesystem rather than being driven by the CSV index. 



### 19. Target management



This is where I would change the current design significantly.



Currently:



```text

targets.json

     ↓

target folders

```



The current server explicitly reads and writes `targets.json` for `get_targets`, `add_target`, `remove_target`, and folder browsing. 



Your intended model appears to be:



```text

File.csv

   ↓

Indexed root paths

   ↓

Complete hierarchy

```



Therefore, target management should eventually derive its information from `File.csv`.



### 20. Automatic update



Your original idea has two update triggers:



```text

MANUAL

   UPDATE button

```



and eventually:



```text

SYSTEM STARTUP

   ↓

AX File Operations

   ↓

UPDATE INDEX

```



I would keep startup indexing as a future feature rather than making it part of the first stable version.



### 21. CSV chaining



Your `CHN` idea is valid.



For example:



```text

File.csv

     ↓

reaches limit

     ↓

CHN | File_2.csv

```



then:



```text

File_2.csv

     ↓

CHN | File_3.csv

```



The application treats them as one logical index.



This is particularly important because the CSV format itself has a practical spreadsheet row limit. Don't create anything on repo


