/**
 * WA错题本 - 前端交互逻辑
 * v0.0.1 MVP 版本
 */

const API_BASE = '/api/v1';
const resultBox = document.getElementById('result');
const mistakeList = document.getElementById('mistakeList');

// ====== API 调用封装 ======

async function apiCall(method, path, body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(`${API_BASE}${path}`, options);
    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || `HTTP ${res.status}`);
    }
    return data;
}

// ====== 提交分析 ======

document.getElementById('submitBtn').addEventListener('click', async () => {
    const url = document.getElementById('url').value.trim();
    const platform = document.getElementById('platform').value;

    if (!url) {
        alert('请输入提交链接');
        return;
    }

    const btn = document.getElementById('submitBtn');
    btn.textContent = '分析中...';
    btn.disabled = true;

    resultBox.style.display = 'block';
    resultBox.textContent = '正在抓取代码并分析...';

    try {
        const result = await apiCall('POST', '/submissions', { url, platform });

        resultBox.innerHTML = `
📌 题目: ${result.submission?.problem_name || '未知'}
📝 平台: ${result.submission?.platform || platform}
🔍 状态: ${result.submission?.status || 'WA'}

错误分类: ${result.error_category}
严重程度: ${result.error_severity === 'low' ? '🟡 低级错误' : '🔴 深层问题'}

📋 错误概述:
${result.error_summary}

📖 详细分析:
${result.error_detail}

💡 建议:
${result.suggestion || '无'}
        `;

        // 刷新列表
        loadMistakes();
    } catch (err) {
        resultBox.textContent = `❌ 分析失败: ${err.message}`;
    } finally {
        btn.textContent = '开始分析';
        btn.disabled = false;
    }
});

// ====== 加载错题列表 ======

async function loadMistakes() {
    mistakeList.innerHTML = '<div class="loading">加载中...</div>';

    try {
        const mistakes = await apiCall('GET', '/mistakes?limit=20');

        if (mistakes.length === 0) {
            mistakeList.innerHTML = '<div class="loading">暂无错题记录</div>';
            return;
        }

        mistakeList.innerHTML = mistakes.map(m => `
            <div class="mistake-item">
                <div class="mistake-title">
                    ${m.submission?.problem_name || '未知题目'}
                </div>
                <div class="mistake-meta">
                    ${m.submission?.platform || '?'} ·
                    ${m.error_category} ·
                    ${m.resolved ? '✅ 已解决' : '❌ 未解决'} ·
                    ${new Date(m.created_at).toLocaleDateString()}
                </div>
            </div>
        `).join('');
    } catch (err) {
        mistakeList.innerHTML = `<div class="loading">加载失败: ${err.message}</div>`;
    }
}

// ====== 页面加载时获取统计 ======

document.addEventListener('DOMContentLoaded', () => {
    loadMistakes();
});
