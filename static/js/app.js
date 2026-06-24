/**
 * WA错题本 - 前端交互逻辑
 * v0.0.1 MVP 版本
 */

const API_BASE = '/api/v1';
const resultBox = document.getElementById('result');
const mistakeList = document.getElementById('mistakeList');
const mistakeCount = document.getElementById('mistakeCount');
const toggleManualBtn = document.getElementById('toggleManualBtn');
const manualInput = document.getElementById('manualInput');

// ====== 工具函数 ======

function getErrorMessage(data) {
    if (typeof data === 'string') return data;
    if (data && data.error) {
        if (typeof data.error === 'string') return data.error;
        if (typeof data.error === 'object') return JSON.stringify(data.error);
    }
    if (data && data.detail) return data.detail;
    return '未知错误';
}

function formatCategory(cat) {
    const names = {
        logic_error: '逻辑错误',
        boundary: '边界条件',
        overflow: '整数溢出',
        uninitialized: '未初始化',
        complexity: '复杂度超限',
        precision: '精度问题',
        io_format: '输入输出格式',
        memory: '内存超限',
        typo: '拼写笔误',
        modular: '取模错误',
        graph: '图论细节',
        dp: 'DP状态/转移',
    };
    return names[cat] || cat;
}

function formatSeverity(sev) {
    if (sev === 'low') return '🟡 低级错误';
    if (sev === 'high') return '🔴 深层问题';
    return sev;
}

// ====== API 调用封装 ======

async function apiCall(method, path, body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(`${API_BASE}${path}`, options);
    let data = null;
    const text = await res.text();
    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = text;
        }
    }

    if (!res.ok) {
        throw new Error(getErrorMessage(data) || `HTTP ${res.status}`);
    }
    return data;
}

// ====== 手动模式切换 ======

toggleManualBtn.addEventListener('click', () => {
    const isHidden = manualInput.style.display === 'none';
    manualInput.style.display = isHidden ? 'block' : 'none';
    toggleManualBtn.textContent = isHidden
        ? '- 收起手动输入'
        : '+ 无法自动抓取？手动粘贴代码';
});

// ====== 提交分析 ======

document.getElementById('submitBtn').addEventListener('click', async () => {
    const url = document.getElementById('url').value.trim();
    const platform = document.getElementById('platform').value;
    const code = document.getElementById('codeInput').value.trim();
    const problemName = document.getElementById('problemName').value.trim();

    if (!url) {
        alert('请输入提交链接');
        return;
    }

    const btn = document.getElementById('submitBtn');
    btn.textContent = '分析中...';
    btn.disabled = true;

    resultBox.style.display = 'block';
    resultBox.textContent = '正在分析...';

    try {
        const payload = { url, platform };
        if (code) payload.code = code;
        if (problemName) payload.problem_name = problemName;

        const result = await apiCall('POST', '/submissions', payload);
        renderResult(result);
        loadMistakes();
    } catch (err) {
        resultBox.innerHTML = `<span class="error-text">❌ 分析失败: ${err.message}</span>`;
    } finally {
        btn.textContent = '开始分析';
        btn.disabled = false;
    }
});

function renderResult(result) {
    const sub = result.submission || {};
    resultBox.innerHTML = `
        <div class="result-header">
            <strong>📌 ${sub.problem_name || '未知题目'}</strong>
            <span class="badge">${sub.platform || '?'}</span>
            <span class="badge">${sub.status || 'WA'}</span>
        </div>
        <div class="result-body">
            <p><strong>错误分类:</strong> ${formatCategory(result.error_category)}</p>
            <p><strong>严重程度:</strong> ${formatSeverity(result.error_severity)}</p>
            <h4>📋 错误概述</h4>
            <p>${result.error_summary}</p>
            <h4>📖 详细分析</h4>
            <p>${result.error_detail}</p>
            <h4>💡 建议</h4>
            <p>${result.suggestion || '无'}</p>
        </div>
    `;
}

// ====== 加载错题列表 ======

async function loadMistakes() {
    mistakeList.innerHTML = '<div class="loading">加载中...</div>';

    try {
        const mistakes = await apiCall('GET', '/mistakes?limit=20');
        mistakeCount.textContent = mistakes.length;

        if (mistakes.length === 0) {
            mistakeList.innerHTML = '<div class="loading">暂无错题记录</div>';
            return;
        }

        mistakeList.innerHTML = mistakes.map(m => `
            <div class="mistake-item" data-id="${m.id}">
                <div class="mistake-main">
                    <div class="mistake-title">${m.submission?.problem_name || '未知题目'}</div>
                    <div class="mistake-meta">
                        ${m.submission?.platform || '?'} ·
                        ${formatCategory(m.error_category)} ·
                        ${m.resolved ? '✅ 已解决' : '❌ 未解决'} ·
                        ${new Date(m.created_at).toLocaleDateString()}
                    </div>
                </div>
                <div class="mistake-actions">
                    <button class="btn-small" onclick="getHint(${m.id})">提示</button>
                    ${!m.resolved ? `<button class="btn-small resolve" onclick="resolveMistake(${m.id})">标记解决</button>` : ''}
                    <button class="btn-small danger" onclick="deleteMistake(${m.id})">删除</button>
                </div>
            </div>
            <div id="hint-${m.id}" class="hint-box" style="display: none;"></div>
        `).join('');
    } catch (err) {
        mistakeList.innerHTML = `<div class="loading">加载失败: ${err.message}</div>`;
    }
}

// ====== 错题操作 ======

window.getHint = async (id) => {
    const hintBox = document.getElementById(`hint-${id}`);
    try {
        const data = await apiCall('POST', `/mistakes/${id}/hint`);
        hintBox.style.display = 'block';
        hintBox.innerHTML = `<strong>提示 ${data.index}:</strong> ${data.hint}<br><small>剩余 ${data.remaining} 条</small>`;
    } catch (err) {
        hintBox.style.display = 'block';
        hintBox.innerHTML = `<span class="error-text">${err.message}</span>`;
    }
};

window.resolveMistake = async (id) => {
    if (!confirm('确定标记为已解决吗？')) return;
    try {
        await apiCall('PATCH', `/mistakes/${id}/resolve`);
        loadMistakes();
    } catch (err) {
        alert(err.message);
    }
};

window.deleteMistake = async (id) => {
    if (!confirm('确定删除这条错题吗？')) return;
    try {
        await apiCall('DELETE', `/mistakes/${id}`);
        loadMistakes();
    } catch (err) {
        alert(err.message);
    }
};

// ====== 页面加载时初始化 ======

document.addEventListener('DOMContentLoaded', () => {
    loadMistakes();
});
