/**
 * WA错题本 - 前端交互逻辑 (Gemini 风格 + AI 聊天 + 数据仪表盘)
 */

const API_BASE = '/api/v1';

// ====== DOM ======
const $ = id => document.getElementById(id);
const sidebarList = $('mistakeList');
const welcomeScreen = $('welcomeScreen');
const chatView = $('chatView');
const detailView = $('detailView');
const summaryView = $('summaryView');
const chatMessages = $('chatMessages');
const chatInput = $('chatInput');
const sendBtn = $('sendBtn');
const platformSelect = $('platformSelect');
const settingsModal = $('settingsModal');
const toastContainer = $('toastContainer');

// Chart 实例引用（用于销毁重建）
let catPieChart = null;
let sevBarChart = null;
let trendLineChart = null;

// ====== State ======
let allMistakes = [];
let categoryNames = {};
let currentMistakeId = null;
let currentFilter = '';
let currentSettings = loadSettings();
let chatHistory = [];
let isChatMode = false;

function loadSettings() {
    const defaults = {
        aiProvider: 'mock',
        aiApiKey: '',
        aiBaseUrl: '',
        aiModel: '',
        globalPrompt: '你是一位资深的 OI/ACM 竞赛教练。擅长代码分析、算法讲解、竞赛答疑。请用中文回答，使用标准 Markdown 格式。',
    };
    try { return { ...defaults, ...JSON.parse(localStorage.getItem('waSettings') || '{}') }; }
    catch { return defaults; }
}
function saveSettings(s) { currentSettings = s; localStorage.setItem('waSettings', JSON.stringify(s)); }

// ====== Utils ======
function esc(s) { if (!s) return ''; const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

function fmtCat(c) { return categoryNames[c] || c; }

/** 把内部分类显示为 WA(思路错误) / RE(除以零) 等格式 */
function fmtStatusBadge(c, resolved) {
    if (resolved) return 'AC';
    const map = {
        'CE': 'CE',
        'RE_div0': 'RE(除以零)',
        'RE_oob': 'RE(越界访问)',
        'WA_logic': 'WA(思路错误)',
        'WA_code': 'WA(代码错误)',
        'TLE': 'TLE',
        'MLE': 'MLE',
    };
    return map[c] || c;
}

function fmtTime() {
    const now = new Date();
    return `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
}

async function apiCall(method, path, body = null) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${API_BASE}${path}`, opts);
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch { data = text; }
    if (!res.ok) throw new Error(typeof data === 'string' ? data : (data?.error || data?.detail || `HTTP ${res.status}`));
    return data;
}

// ====== 标准 Markdown 渲染器 ======
function renderMarkdown(text) {
    if (!text) return '';
    let html = esc(text);

    // 代码块（优先处理）
    html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => `<pre><code class="language-${lang || 'text'}">${esc(code)}</code></pre>`);

    // 标题
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // 引用
    html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');

    // 无序列表
    html = html.replace(/(?:^|\n)(?:-\s|\*\s|\+\s)(.+?)(?=\n(?:-\s|\*\s|\+\s)|\n\n|$)/gs, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // 有序列表
    html = html.replace(/(?:^|\n)\d+\.\s(.+?)(?=\n\d+\.\s|\n\n|$)/gs, '<li>$1</li>');

    // 粗体、斜体
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // 行内代码
    html = html.replace(/`(.+?)`/g, '<code>$1</code>');

    // 表格（简化版）
    html = html.replace(/\|(.+?)\|\n\|[-:\s|]+\|\n((?:\|.+?\|\n?)+)/g, (match, header, rows) => {
        const ths = header.split('|').map(h => `<th>${h.trim()}</th>`).join('');
        const trs = rows.trim().split('\n').map(row => {
            const tds = row.slice(1, -1).split('|').map(c => `<td>${c.trim()}</td>`).join('');
            return `<tr>${tds}</tr>`;
        }).join('');
        return `<table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>`;
    });

    // 换行
    html = html.replace(/\n/g, '<br>');

    // 把连续 br 包裹在 p 里（简单段落化）
    html = html.split(/(<pre>[\s\S]*?<\/pre>|<table>[\s\S]*?<\/table>|<blockquote>.*?<\/blockquote>|<h\d>.*?<\/h\d>|<ul>.*?<\/ul>)/g)
        .map(part => {
            if (part.startsWith('<pre>') || part.startsWith('<table>') || part.startsWith('<blockquote>') || part.startsWith('<h') || part.startsWith('<ul>')) return part;
            if (!part.trim()) return '';
            return part.split(/<br><br>/).map(p => p.trim() ? `<p>${p}</p>` : '').join('');
        })
        .join('');

    return `<div class="ai-md">${html}</div>`;
}

// ====== Toast ======
function toast(title, msg, type = 'info', dur = 3000) {
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.innerHTML = `<div class="toast-title">${esc(title)}</div><div class="toast-message">${esc(msg)}</div>`;
    toastContainer.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateX(16px)'; setTimeout(() => el.remove(), 220); }, dur);
}

// ====== Modal ======
function openModal(title, html, buttons) {
    $('modalTitle').textContent = title;
    $('modalBody').innerHTML = html;
    $('modalFooter').innerHTML = '';
    if (!buttons) {
        const b = document.createElement('button'); b.className = 'btn-modal-primary'; b.textContent = '确定'; b.onclick = closeModal;
        $('modalFooter').appendChild(b);
    } else {
        buttons.forEach(btn => {
            const el = document.createElement('button');
            el.className = btn.primary ? 'btn-modal-primary' : 'btn-modal-secondary';
            el.textContent = btn.text;
            el.onclick = () => { if (btn.onClick) btn.onClick(); if (btn.close !== false) closeModal(); };
            $('modalFooter').appendChild(el);
        });
    }
    $('modalOverlay').style.display = 'flex';
}
function closeModal() { $('modalOverlay').style.display = 'none'; }
$('modalClose').onclick = closeModal;
$('modalOverlay').addEventListener('click', e => { if (e.target === $('modalOverlay')) closeModal(); });

// ====== Settings ======
function openSettings() {
    const s = currentSettings;
    $('settingsBody').innerHTML = `
        <div class="settings-form">
            <div class="form-group"><label>AI 分析模式</label><select id="spProvider"><option value="mock" ${s.aiProvider==='mock'?'selected':''}>内置 Mock AI（离线可用）</option><option value="openai" ${s.aiProvider==='openai'?'selected':''}>OpenAI 兼容 API</option></select></div>
            <div class="form-group"><label>API Base URL</label><input type="text" id="spBaseUrl" value="${esc(s.aiBaseUrl)}" placeholder="https://api.openai.com/v1"></div>
            <div class="form-group"><label>API Key</label><input type="password" id="spKey" value="${esc(s.aiApiKey)}" placeholder="sk-..."></div>
            <div class="form-group"><label>模型名称</label><input type="text" id="spModel" value="${esc(s.aiModel)}" placeholder="gpt-4o-mini / deepseek-chat"></div>
            <div class="form-group"><label>系统提示词</label><textarea id="spPrompt" rows="4">${esc(s.globalPrompt)}</textarea></div>
        </div>`;
    $('settingsFooter').innerHTML = `<button class="btn-modal-secondary" onclick="closeSettings()">取消</button><button class="btn-modal-primary" onclick="saveSettingsForm()">保存</button>`;
    settingsModal.style.display = 'flex';
}
window.closeSettings = () => { settingsModal.style.display = 'none'; };
window.saveSettingsForm = () => {
    saveSettings({
        aiProvider: document.getElementById('spProvider').value,
        aiBaseUrl: document.getElementById('spBaseUrl').value.trim(),
        aiApiKey: document.getElementById('spKey').value.trim(),
        aiModel: document.getElementById('spModel').value.trim(),
        globalPrompt: document.getElementById('spPrompt').value.trim(),
    });
    closeSettings();
    toast('设置已保存', '', 'success');
};
$('settingsBtn').addEventListener('click', openSettings);

// ====== Nav Filter ======
document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        loadMistakes();
    });
});

// ====== 视图切换 ======
function showView(viewName) {
    welcomeScreen.style.display = 'none';
    chatView.style.display = 'none';
    detailView.style.display = 'none';
    summaryView.style.display = 'none';

    if (viewName === 'welcome') { welcomeScreen.style.display = 'flex'; isChatMode = false; }
    else if (viewName === 'chat') { chatView.style.display = 'block'; isChatMode = true; }
    else if (viewName === 'detail') { detailView.style.display = 'block'; isChatMode = false; }
    else if (viewName === 'summary') { summaryView.style.display = 'block'; isChatMode = false; }
}

// ====== 新建分析 ======
$('newMistakeBtn').addEventListener('click', () => {
    openModal('新建分析', `
        <div class="settings-form">
            <div class="form-group"><label>OJ 平台</label><select id="mPlatform"><option value="codeforces">Codeforces</option><option value="luogu">洛谷</option></select></div>
            <div class="form-group"><label>提交链接</label><input type="text" id="mUrl" placeholder="https://codeforces.com/contest/xxx/submission/xxx"></div>
            <div class="form-group"><label>题目名称（可选）</label><input type="text" id="mProblemName" placeholder=""></div>
            <div class="form-group"><label>代码（可选）</label><textarea id="mCode" rows="6" placeholder="粘贴代码..."></textarea></div>
        </div>`, [
        { text: '取消' },
        { text: '开始分析', primary: true, onClick: async () => {
            const url = document.getElementById('mUrl').value.trim();
            if (!url) { toast('缺少链接', '请输入提交链接', 'warning'); return; }
            await doAnalysis({ url, platform: document.getElementById('mPlatform').value, code: document.getElementById('mCode').value.trim(), problem_name: document.getElementById('mProblemName').value.trim() });
        }}
    ]);
});

// ====== 发送处理 ======
sendBtn.addEventListener('click', handleSend);
chatInput.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } });

async function handleSend() {
    const val = chatInput.value.trim();
    if (!val) return;
    const isURL = /^https?:\/\//i.test(val);
    if (isURL) { chatInput.value = ''; autoResizeInput(); await doAnalysis({ url: val, platform: platformSelect.value }); }
    else { chatInput.value = ''; autoResizeInput(); await doChat(val); }
}

function autoResizeInput() { chatInput.style.height = 'auto'; chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px'; }
chatInput.addEventListener('input', autoResizeInput);

// ====== AI 聊天 ======

function appendMessage(role, content, isMarkdown = false) {
    const row = document.createElement('div');
    row.className = `msg-row ${role}`;

    const bubbleHtml = role === 'ai' && isMarkdown
        ? renderMarkdown(content)
        : `<div class="msg-bubble"><p>${esc(content)}</p></div>`;

    const avatar = role === 'user'
        ? '<div class="msg-avatar">👤</div>'
        : '<div class="msg-avatar" style="display:none"></div>';

    row.innerHTML = `${avatar}<div class="msg-content">${bubbleHtml}<div class="msg-time">${fmtTime()}</div></div>`;
    chatMessages.appendChild(row);
    scrollToBottom();
}

function showTyping() {
    const row = document.createElement('div');
    row.className = 'msg-row ai'; row.id = 'typingRow';
    row.innerHTML = `<div class="msg-content"><div class="ai-md"><div class="typing-indicator"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div></div></div>`;
    chatMessages.appendChild(row); scrollToBottom();
}
function hideTyping() { const el = $('typingRow'); if (el) el.remove(); }
function scrollToBottom() { requestAnimationFrame(() => { chatView.scrollTop = chatView.scrollHeight; }); }

async function doChat(userMsg) {
    showView('chat');
    appendMessage('user', userMsg);
    chatHistory.push({ role: 'user', content: userMsg });
    showTyping(); sendBtn.disabled = true;

    try {
        const result = await apiCall('POST', '/chat', { messages: chatHistory, ai_config: buildAiConfig() });
        hideTyping();
        const reply = result.reply || result.error || '(无回复)';
        appendMessage('ai', reply, true);
        chatHistory.push({ role: 'assistant', content: reply });
    } catch (err) {
        hideTyping();
        appendMessage('ai', `抱歉，出错了：${err.message}`, true);
    } finally { sendBtn.disabled = false; chatInput.focus(); }
}

// ====== 每题一结 ======
$('perQuestionBtn').addEventListener('click', doPerQuestionSummary);

async function doPerQuestionSummary() {
    // 如果当前在详情页，直接基于当前错题；否则让用户选择或生成所有错题的总结
    let targetMistake = null;
    if (currentMistakeId) {
        targetMistake = allMistakes.find(m => m.id === currentMistakeId);
    }

    // 如果不在详情页且列表里只有一条，直接用那条
    if (!targetMistake && allMistakes.length === 1) {
        targetMistake = allMistakes[0];
    }

    if (!targetMistake) {
        // 弹窗让用户选择
        if (!allMistakes.length) { toast('没有错题', '请先分析至少一道错题', 'warning'); return; }
        openModal('选择题目', `
            <div class="settings-form">
                <div class="form-group"><label>选择要生成小结的题目</label><select id="pqSelect">${allMistakes.map(m => `<option value="${m.id}">${esc(m.submission?.problem_name || '未知题目')} - ${esc(fmtCat(m.error_category))}</option>`).join('')}</select></div>
            </div>`, [
            { text: '取消' },
            { text: '生成每题一结', primary: true, onClick: async () => {
                const id = parseInt(document.getElementById('pqSelect').value);
                const m = allMistakes.find(x => x.id === id);
                if (m) await generatePerQuestionTable(m);
            }}
        ]);
        return;
    }

    await generatePerQuestionTable(targetMistake);
}

async function generatePerQuestionTable(mistake) {
    showView('chat');
    const sub = mistake.submission || {};
    const title = sub.problem_name || '未知题目';
    appendMessage('user', `请为「${title}」生成每题一结表格`);
    showTyping(); sendBtn.disabled = true;

    const prompt = `请为以下错题生成一份名为「每题一结」的 Markdown 表格总结。表格至少包含：题目、错误类型、错误原因、改正措施、同类题防范建议。\n\n题目：${title}\n平台：${sub.platform || '?'}\n状态：${mistake.resolved ? 'AC' : (sub.status || 'WA')}\n错误分类：${fmtCat(mistake.error_category)}\n错误概述：${mistake.error_summary}\n详细分析：${mistake.error_detail}\n修改建议：${mistake.suggestion || '无'}`;

    try {
        const result = await apiCall('POST', '/chat', {
            messages: [{ role: 'user', content: prompt }],
            ai_config: buildAiConfig(),
        });
        hideTyping();
        appendMessage('ai', result.reply || '(生成失败)', true);
        chatHistory.push({ role: 'user', content: prompt });
        chatHistory.push({ role: 'assistant', content: result.reply });
    } catch (err) {
        hideTyping();
        appendMessage('ai', `生成失败：${err.message}`, true);
    } finally {
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// ====== 分析提交 ======
async function doAnalysis({ url, platform, code, problem_name }) {
    sendBtn.disabled = true;
    try {
        const payload = { url, platform };
        if (code) payload.code = code;
        if (problem_name) payload.problem_name = problem_name;
        if (currentSettings.aiProvider !== 'mock' && currentSettings.aiApiKey) payload.ai_config = buildAiConfig();

        const result = await apiCall('POST', '/submissions', payload);
        showDetail(result);
        await Promise.all([loadMistakes(), loadStats()]);
        toast('分析完成', `已识别为「${fmtCat(result.error_category)}」`, 'success');
    } catch (err) { toast('分析失败', err.message, 'error'); }
    finally { sendBtn.disabled = false; }
}

function buildAiConfig() {
    if (currentSettings.aiProvider === 'mock') return null;
    if (!currentSettings.aiApiKey) return null;
    return { provider: currentSettings.aiProvider, base_url: currentSettings.aiBaseUrl, api_key: currentSettings.aiApiKey, model: currentSettings.aiModel, prompt: currentSettings.globalPrompt };
}

// ====== Detail View ======
function showDetail(mistake) {
    const sub = mistake.submission || {};
    currentMistakeId = mistake.id;
    showView('detail');
    $('detailTitle').textContent = sub.problem_name || '未知题目';
    $('detailPlatform').textContent = (sub.platform || '?').toUpperCase();
    $('detailStatus').textContent = fmtStatusBadge(mistake.error_category, mistake.resolved);
    $('detailStatus').className = 'badge ' + (mistake.resolved ? 'success' : '');
    $('detailCategory').textContent = fmtCat(mistake.error_category);
    $('detailSummary').textContent = mistake.error_summary;
    $('detailDetail').textContent = mistake.error_detail;
    $('detailSuggestion').textContent = mistake.suggestion || '无';

    // AI 错误点
    const aiPoints = mistake.error_points || [];
    $('aiErrorPoints').innerHTML = aiPoints.length
        ? aiPoints.map(p => `<li>${esc(p)}</li>`).join('')
        : '<li style="color:var(--text-dim);list-style:none">暂无 AI 错误点</li>';

    // 手动补充错误点
    $('reflectionInput').value = mistake.reflection || '';
    $('reflectionStatus').textContent = '';
    $('saveReflectionBtn').onclick = () => saveReflection(mistake.id);

    $('hintBox').style.display = 'none';
    $('hintBtn').onclick = () => getHint(mistake.id);
    $('resolveBtn').onclick = () => resolveMistake(mistake.id);
    $('resolveBtn').textContent = mistake.resolved ? '✅ 已 AC' : '✅ 标记 AC';
    $('resolveBtn').disabled = !!mistake.resolved;
    $('deleteBtn').onclick = () => deleteMistake(mistake.id);
    highlightEntry(mistake.id);
    detailView.querySelector('.detail-scroll').scrollTop = 0;
}

async function saveReflection(id) {
    const content = $('reflectionInput').value.trim();
    try {
        await apiCall('PATCH', `/mistakes/${id}/reflection`, { reflection: content });
        $('reflectionStatus').textContent = '已保存';
        // 更新本地缓存
        const m = allMistakes.find(x => x.id === id);
        if (m) m.reflection = content;
        toast('补充错误点已保存', '', 'success');
    } catch (err) {
        $('reflectionStatus').textContent = '保存失败';
        toast('保存失败', err.message, 'error');
    }
}

function highlightEntry(id) {
    document.querySelectorAll('.mistake-entry').forEach(el => el.classList.toggle('active', parseInt(el.dataset.id) === id));
}

// ====== Mistake Operations ======
async function getHint(id) {
    const box = $('hintBox');
    try {
        const data = await apiCall('POST', `/mistakes/${id}/hint`);
        box.style.display = 'block';
        box.innerHTML = `<strong>提示 ${data.index}:</strong> ${esc(data.hint)}<br><small>剩余 ${data.remaining} 条</small>`;
    } catch (e) { box.style.display = 'block'; box.innerHTML = `<span style="color:var(--danger)">${esc(e.message)}</span>`; }
}

async function resolveMistake(id) {
    try {
        await apiCall('PATCH', `/mistakes/${id}/resolve`);
        toast('操作成功', '已标记为 AC', 'success');
        await Promise.all([loadMistakes(), loadStats()]);
        if (currentMistakeId === id) {
            const updated = allMistakes.find(m => m.id === id);
            if (updated) showDetail(updated);
        }
    } catch (e) { toast('失败', e.message, 'error'); }
}

async function deleteMistake(id) {
    try {
        await apiCall('DELETE', `/mistakes/${id}`);
        toast('已删除', '错题已移除', 'success');
        currentMistakeId = null; showView('welcome');
        await Promise.all([loadMistakes(), loadStats()]);
    } catch (e) { toast('删除失败', e.message, 'error'); }
}

// ====== 学习小结仪表盘 ======
$('summaryBtn').addEventListener('click', doSummary);

async function doSummary() {
    showView('summary');
    $('summaryDate').textContent = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
    $('kpiTotal').textContent = '...';
    $('aiSummaryText').textContent = '正在加载数据并生成诊断报告...';

    try {
        const [stats, mistakes] = await Promise.all([
            apiCall('GET', '/stats'),
            apiCall('GET', '/mistakes?limit=200'),
        ]);

        renderKPI(stats, mistakes);
        renderCharts(stats, mistakes);
        renderTable(mistakes);
        await renderAISummary(stats, mistakes);
    } catch (err) {
        $('aiSummaryText').innerHTML = `<span style="color:var(--danger)">加载失败：${esc(err.message)}</span>`;
    }
}

function renderKPI(stats, mistakes) {
    const total = stats.total_mistakes;
    const resolved = stats.resolved_count ?? mistakes.filter(m => m.resolved).length;
    const unresolved = stats.unresolved_count ?? (total - resolved);
    const rate = total > 0 ? Math.round(resolved / total * 100) : 0;

    animateNumber('kpiTotal', total);
    animateNumber('kpiResolved', resolved);
    animateNumber('kpiUnresolved', unresolved);
    animateNumber('kpiHigh', resolved);
    $('kpiRate').textContent = rate + '%';
}

function animateNumber(id, target) {
    const el = $(id);
    const start = parseInt(el.textContent) || 0;
    const dur = 400;
    const t0 = performance.now();
    function step(t) {
        const p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(start + (target - start) * easeOut(p));
        if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}
function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

function renderCharts(stats, mistakes) {
    const catCount = {};
    mistakes.forEach(m => { catCount[m.error_category] = (catCount[m.error_category] || 0) + 1; });
    const catLabels = Object.keys(catCount).map(c => fmtCat(c));
    const catData = Object.values(catCount);
    const pieColors = ['#00d4ff','#a78bfa','#ff5a65','#fbbf24','#2dd4bf','#f472b6','#818cf8','#34d399','#fb923c','#c084fc','#60a5fa','#f87171'];

    if (catPieChart) catPieChart.destroy();
    catPieChart = new Chart($('catPieChart'), {
        type: 'doughnut',
        data: { labels: catLabels, datasets: [{ data: catData, backgroundColor: pieColors.slice(0, catLabels.length), borderWidth: 0, hoverOffset: 6 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#8b909d', font: { size: 11 }, padding: 10, usePointStyle: true, pointStyle: 'circle' } } }, cutout: '55%' }
    });

    const sevHigh = stats.by_severity?.high || 0;
    const sevLow = stats.by_severity?.low || 0;
    if (sevBarChart) sevBarChart.destroy();
    sevBarChart = new Chart($('sevBarChart'), {
        type: 'bar',
        data: { labels: ['深层问题', '低级错误'], datasets: [{ data: [sevHigh, sevLow], backgroundColor: ['rgba(255,90,101,.7)', 'rgba(251,191,36,.7)'], borderRadius: 8, barThickness: 40 }] },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,.04)' }, ticks: { color: '#5a5f6d' } }, x: { grid: { display: false }, ticks: { color: '#8b909d' } } }, plugins: { legend: { display: false } } }
    });

    const dateMap = {};
    mistakes.forEach(m => { const d = new Date(m.created_at).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }); dateMap[d] = (dateMap[d] || 0) + 1; });
    const sortedDates = Object.keys(dateMap).sort((a,b) => new Date('2024/' + a) - new Date('2024/' + b));
    const trendLabels = sortedDates.length > 14 ? sortedDates.slice(-14) : sortedDates;
    const trendData = trendLabels.map(d => dateMap[d]);

    if (trendLineChart) trendLineChart.destroy();
    trendLineChart = new Chart($('trendLineChart'), {
        type: 'line',
        data: { labels: trendLabels, datasets: [{ label: '新增错题', data: trendData, borderColor: '#00d4ff', backgroundColor: 'rgba(0,212,255,.08)', fill: true, tension: .35, pointRadius: 4, pointBackgroundColor: '#0a0b0e', pointBorderColor: '#00d4ff', pointBorderWidth: 2, pointHoverRadius: 6 }] },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,.04)' }, ticks: { color: '#5a5f6d', stepSize: 1 } }, x: { grid: { display: false }, ticks: { color: '#8b909d', maxRotation: 45 } } }, plugins: { legend: { display: false } } }
    });
}

function renderTable(mistakes) {
    const tbody = $('mistakeTableBody');
    if (!mistakes.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-dim);padding:24px">暂无记录</td></tr>'; return; }

    tbody.innerHTML = mistakes.map(m => {
        const sub = m.submission || {};
        const name = esc(sub.problem_name || '未知题目');
        const plat = esc((sub.platform || '?').toUpperCase());
        const cat = esc(fmtCat(m.error_category));
        const status = m.resolved
            ? '<span class="tag-resolved">AC</span>'
            : `<span class="tag-unresolved">${esc(fmtStatusBadge(m.error_category, false))}</span>`;
        const date = new Date(m.created_at).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        return `<tr onclick="selectMistake(${m.id})" style="cursor:pointer"><td>${name}</td><td>${plat}</td><td>${cat}</td><td>${status}</td><td style="color:var(--text-dim);white-space:nowrap">${date}</td></tr>`;
    }).join('');
}

async function renderAISummary(stats, mistakes) {
    try {
        const result = await apiCall('POST', '/chat/summary', buildAiConfig() || {});
        $('aiSummaryText').innerHTML = renderMarkdown(result.reply || result.error || '无法生成');
    } catch (err) {
        $('aiSummaryText').innerHTML = `<span style="color:var(--danger)">AI 诊断生成失败：${esc(err.message)}</span>`;
    }
}

// ====== Load Data ======
async function loadCategories() {
    try { categoryNames = await apiCall('GET', '/stats/categories'); }
    catch (e) { console.error('加载分类失败', e); }
}

async function loadStats() {
    try {
        const s = await apiCall('GET', '/stats');
        $('statTotal').textContent = s.total_mistakes;
        $('statUnresolved').textContent = s.unresolved_count ?? 0;
        $('statHigh').textContent = s.resolved_count ?? 0;
        $('sidebarFooter').textContent = `v0.0.3 · 共 ${s.total_mistakes} 条`;
    } catch (e) { console.error('统计加载失败', e); }
}

async function loadMistakes() {
    sidebarList.innerHTML = '<div class="list-loading">加载中...</div>';
    try {
        const params = new URLSearchParams({ limit: '100' });
        if (currentFilter !== '') params.set('resolved', currentFilter);
        const mistakes = await apiCall('GET', `/mistakes?${params.toString()}`);
        allMistakes = mistakes;
        renderSidebarList(mistakes);
    } catch (e) { sidebarList.innerHTML = `<div class="list-loading">加载失败: ${esc(e.message)}</div>`; }
}

function renderSidebarList(mistakes) {
    if (!mistakes.length) { sidebarList.innerHTML = '<div class="list-loading">暂无记录</div>'; return; }
    sidebarList.innerHTML = mistakes.map(m => {
        const sub = m.submission || {};
        const statusText = fmtStatusBadge(m.error_category, m.resolved);
        return `<div class="mistake-entry${m.id===currentMistakeId?' active':''}" data-id="${m.id}" onclick="selectMistake(${m.id})"><div class="entry-title">${esc(sub.problem_name||'未知题目')}</div><div class="entry-meta"><span>${esc(fmtCat(m.error_category))}</span><span class="entry-tag ${m.resolved?'resolved':'unresolved'}">${esc(statusText)}</span><span>${new Date(m.created_at).toLocaleDateString('zh-CN',{month:'short',day:'numeric'})}</span></div></div>`;
    }).join('');
}

window.selectMistake = async (id) => {
    const m = allMistakes.find(x => x.id === id);
    if (m) showDetail(m);
};

// ====== Init ======
document.addEventListener('DOMContentLoaded', async () => {
    await loadCategories();
    await Promise.all([loadMistakes(), loadStats()]);
});
