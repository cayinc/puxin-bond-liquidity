import json

# Read JSON data
with open("page_data.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)

json_str = json.dumps(all_data, ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>普信债流动性数据平台</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #f0f2f5;
  color: #1f2937;
  min-height: 100vh;
}

/* ===== Header ===== */
header {
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  padding: 20px 32px;
  box-shadow: 0 2px 8px rgba(29,78,216,.35);
}
header h1 { color:#fff; font-size:22px; font-weight:700; letter-spacing:.5px; }
header p  { color:rgba(255,255,255,.7); font-size:13px; margin-top:4px; }

/* ===== Tab Nav ===== */
.tab-nav {
  display:flex; gap:0; background:#fff;
  border-bottom:2px solid #e5e7eb; padding:0 32px;
  box-shadow:0 1px 4px rgba(0,0,0,.06);
}
.tab-btn {
  padding:14px 24px; border:none; background:none; cursor:pointer;
  font-size:14px; font-weight:500; color:#6b7280;
  border-bottom:2px solid transparent; margin-bottom:-2px;
  transition:color .2s,border-color .2s; white-space:nowrap;
}
.tab-btn:hover { color:#1d4ed8; }
.tab-btn.active { color:#1d4ed8; border-bottom-color:#1d4ed8; font-weight:600; }

/* ===== Content ===== */
.content { padding:24px 32px; }
.tab-panel { display:none; }
.tab-panel.active { display:block; animation:fadeIn .25s ease; }
@keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

/* ===== Card ===== */
.card {
  background:#fff; border-radius:10px;
  box-shadow:0 1px 4px rgba(0,0,0,.08);
  overflow:hidden; margin-bottom:20px;
}
.card-header {
  padding:16px 20px; border-bottom:1px solid #f3f4f6;
  display:flex; align-items:center; gap:10px; background:#fafafa;
}
.card-header h2 { font-size:15px; font-weight:600; color:#1f2937; }
.card-header .badge {
  background:#dbeafe; color:#1d4ed8;
  font-size:12px; padding:2px 8px; border-radius:20px; font-weight:500;
}
.card-header .sub-title { font-size:13px; color:#6b7280; margin-left:4px; }
.card-header { justify-content:space-between; }
.card-actions { display:flex; align-items:center; gap:8px; margin-left:auto; }
.card-body { padding:16px 20px; }

/* ===== Table ===== */
.table-wrap { overflow-x:auto; max-height:540px; padding-top:2px; }
table { width:100%; border-collapse:collapse; font-size:13px; table-layout:fixed; }
thead { position:sticky; top:0; z-index:10; }
thead th {
  background:#1d4ed8; color:#fff; padding:10px 12px;
  text-align:center; font-weight:600; white-space:nowrap;
  border-right:1px solid rgba(255,255,255,.15); overflow:hidden;
}
thead th:first-child { text-align:left; }
thead th.th-dark { background:#1e40af; font-size:12px; }
thead th.th-sum  { background:#b45309; }
tbody tr:nth-child(even) { background:#f9fafb; }
tbody tr:hover { background:#eff6ff; }
tbody td {
  padding:8px 12px; border-bottom:1px solid #f0f0f0;
  text-align:right; white-space:nowrap; color:#374151;
  overflow:hidden; text-overflow:ellipsis;
  background:#fff;
}
tbody td:first-child { text-align:left; color:#6b7280; font-size:12px; }
td.positive { color:#059669; font-weight:500; }
td.negative { color:#dc2626; font-weight:500; }
td.sum-cell  { background:#fef9e7; font-weight:600; }
#s3-table { width:auto; margin:0 auto; }

/* ===== Sort toggle button ===== */
.sort-btn {
  display:inline-flex; align-items:center; gap:4px;
  padding:4px 12px; border-radius:6px; border:1.5px solid #d1d5db;
  background:#fff; color:#374151; font-size:12px; cursor:pointer;
  transition:all .15s; user-select:none; font-weight:500;
}
.sort-btn:hover { border-color:#1d4ed8; color:#1d4ed8; }
.sort-btn .arrow { font-size:14px; line-height:1; transition:transform .2s; }
.sort-btn.desc .arrow { transform:rotate(180deg); }

/* ===== Pagination ===== */
.pagination {
  display:flex; align-items:center; justify-content:flex-end;
  gap:6px; padding:12px 0 0;
}
.pagination span { font-size:13px; color:#6b7280; padding:0 8px; }
.pg-btn {
  border:1px solid #d1d5db; background:#fff; color:#374151;
  padding:6px 14px; border-radius:6px; cursor:pointer;
  font-size:13px; transition:all .15s;
}
.pg-btn:hover:not(:disabled) { background:#1d4ed8; color:#fff; border-color:#1d4ed8; }
.pg-btn:disabled { opacity:.4; cursor:not-allowed; }

/* ===== Filter bar (Sheet3) ===== */
.filter-bar {
  display:flex; flex-wrap:wrap; gap:16px; align-items:flex-start;
  padding:16px 20px; border-bottom:1px solid #f3f4f6; background:#f8faff;
}
.filter-group label {
  display:block; font-size:12px; font-weight:600; color:#6b7280;
  margin-bottom:6px; text-transform:uppercase; letter-spacing:.5px;
}
.chip-group { display:flex; flex-wrap:wrap; gap:6px; }
.chip {
  padding:5px 14px; border-radius:20px; border:1.5px solid #d1d5db;
  background:#fff; color:#374151; font-size:13px; cursor:pointer;
  transition:all .15s; user-select:none;
}
.chip:hover { border-color:#1d4ed8; color:#1d4ed8; }
.chip.active { background:#1d4ed8; border-color:#1d4ed8; color:#fff; font-weight:600; }
.chip.chip-sum { border-color:#d97706; color:#92400e; }
.chip.chip-sum.active { background:#d97706; border-color:#d97706; color:#fff; }

/* ===== Sheet3 view-toggle ===== */
.view-toggle {
  display:inline-flex; border:1.5px solid #d1d5db; border-radius:8px;
  overflow:hidden; background:#f9fafb;
}
.view-toggle button {
  padding:5px 16px; border:none; background:transparent;
  font-size:13px; cursor:pointer; color:#6b7280;
  transition:background .15s,color .15s; font-weight:500;
}
.view-toggle button.active {
  background:#1d4ed8; color:#fff; font-weight:600;
}
.view-toggle button:not(:last-child) { border-right:1px solid #d1d5db; }

/* ===== Sheet3 detail-chart box ===== */
.detail-chart-wrap {
  padding:0 20px 16px; display:none;
}
.detail-chart-wrap.show { display:block; }
.detail-chart-title {
  font-size:13px; font-weight:600; color:#374151;
  padding:12px 0 4px;
}

/* ===== Chart controls (Sheet4) ===== */
.chart-controls {
  display:flex; flex-wrap:wrap; gap:10px; align-items:center;
  padding:14px 20px; border-bottom:1px solid #f3f4f6; background:#f8faff;
}
.chart-controls label { font-size:13px; color:#6b7280; font-weight:500; }
.rng-btn {
  padding:5px 14px; border-radius:6px; border:1.5px solid #d1d5db;
  background:#fff; color:#374151; font-size:13px; cursor:pointer; transition:all .15s;
}
.rng-btn:hover { border-color:#1d4ed8; color:#1d4ed8; }
.rng-btn.active { background:#1d4ed8; border-color:#1d4ed8; color:#fff; font-weight:600; }
#chart4 { width:100%; height:460px; }

/* ===== Sheet4 latest table ===== */
.latest-title {
  font-size:14px; font-weight:600; color:#374151;
  padding:14px 20px 8px; border-top:1px solid #f3f4f6;
}

/* ===== Responsive ===== */
@media(max-width:768px){
  .content{ padding:16px; }
  header{ padding:16px; }
  .tab-nav{ padding:0 8px; overflow-x:auto; }
  .tab-btn{ padding:12px 14px; font-size:13px; }
}
</style>
</head>
<body>

<header>
  <h1>📊 普信债流动性数据平台</h1>
  <p>数据截至 2026-05-09</p>
</header>

<nav class="tab-nav">
  <button class="tab-btn active" onclick="switchTab(0)">TKN统计</button>
  <button class="tab-btn" onclick="switchTab(1)">换手率 MA7</button>
  <button class="tab-btn" onclick="switchTab(2)">机构净买入</button>
  <button class="tab-btn" onclick="switchTab(3)">普信 &amp; 二永换手率趋势</button>
</nav>

<div class="content">

  <!-- ===== Sheet1 ===== -->
  <div class="tab-panel active" id="panel0">
    <div class="card">
      <div class="card-header">
        <div style="display:flex;align-items:center;gap:10px;">
          <h2>TKN 统计数据</h2>
          <span class="badge" id="s1-badge">--</span>
        </div>
        <div class="card-actions">
          <button class="sort-btn desc" id="s1-sort" onclick="toggleSort1()">新 → 旧<span class="arrow">↑</span></button>
        </div>
      </div>
      <div style="padding:16px 20px;">
        <div class="table-wrap" style="max-height:400px;">
          <table id="s1-table">
            <thead id="s1-thead"></thead>
            <tbody id="s1-tbody"></tbody>
          </table>
        </div>
        <div class="pagination" id="s1-pg"></div>
      </div>
      <div style="padding:0 20px 16px;">
        <div id="chart1" style="width:100%;height:380px;"></div>
      </div>
    </div>
  </div>

  <!-- ===== Sheet2: 换手率MA7 only ===== -->
  <div class="tab-panel" id="panel1">
    <div class="card">
      <div class="card-header">
        <div style="display:flex;align-items:center;gap:10px;">
          <h2>换手率 MA7</h2>
          <span class="badge" id="s2-badge">--</span>
          <span class="sub-title">按待偿期限分组 · 7日移动均值</span>
        </div>
        <div class="card-actions">
          <button class="sort-btn desc" id="s2-sort" onclick="toggleSort2()">新 → 旧<span class="arrow">↑</span></button>
        </div>
      </div>
      <div style="padding:0 20px 0;">
        <div class="table-wrap" style="max-height:360px;">
          <table id="s2-table">
            <colgroup>
              <col style="width:110px">
              <col style="width:90px"><col style="width:90px"><col style="width:90px">
              <col style="width:90px"><col style="width:90px"><col style="width:90px">
            </colgroup>
            <thead id="s2-thead"></thead>
            <tbody id="s2-tbody"></tbody>
          </table>
        </div>
        <div class="pagination" id="s2-pg"></div>
      </div>
      <div style="padding:0 20px 16px;">
        <div id="chart2" style="width:100%;height:380px;"></div>
      </div>
    </div>
  </div>

  <!-- ===== Sheet3 ===== -->
  <div class="tab-panel" id="panel2">
    <div class="card">
      <!-- 顶部标题栏 -->
      <div class="card-header">
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <h2>机构净买入普信债</h2>
          <span class="badge" id="s3-badge">--</span>
          <span class="sub-title">单位：亿元</span>
        </div>
        <div class="card-actions">
          <!-- 视图切换 -->
          <div class="view-toggle" id="s3-view-toggle">
            <button class="active" onclick="switchS3View('left',this)">按机构</button>
            <button onclick="switchS3View('right',this)">按期限</button>
          </div>
          <button class="sort-btn desc" id="s3-sort" onclick="toggleSort3()">新 → 旧<span class="arrow">↑</span></button>
        </div>
      </div>

      <!-- 筛选栏（左视图：机构+期限；右视图：期限+机构） -->
      <div class="filter-bar" id="s3-filter-bar">
        <div class="filter-group" id="s3-fg-primary">
          <label id="s3-label-primary">机构</label>
          <div class="chip-group" id="s3-chips-primary"></div>
        </div>
        <div class="filter-group" id="s3-fg-secondary">
          <label id="s3-label-secondary">期限</label>
          <div class="chip-group" id="s3-chips-secondary"></div>
        </div>
      </div>

      <!-- 汇总图（默认显示，选中具体值后切换为详情图） -->
      <div style="padding:0 20px 8px;" id="s3-summary-chart-wrap">
        <div id="chart3" style="width:100%;height:380px;"></div>
      </div>

      <!-- 详情图（选中具体机构/期限时显示） -->
      <div class="detail-chart-wrap" id="s3-detail-chart-wrap">
        <div class="detail-chart-title" id="s3-detail-title">-- 详情图 --</div>
        <div id="chart3d" style="width:100%;height:360px;"></div>
      </div>

      <!-- 表格 -->
      <div style="padding:0 20px 0; border-top:1px solid #f3f4f6;">
        <div class="table-wrap" id="s3-wrap" style="max-height:360px;">
          <table id="s3-table">
            <thead id="s3-thead"></thead>
            <tbody id="s3-tbody"></tbody>
          </table>
        </div>
        <div class="pagination" id="s3-pg"></div>
      </div>
    </div>
  </div>

  <!-- ===== Sheet4 ===== -->
  <div class="tab-panel" id="panel3">
    <div class="card">
      <div class="card-header">
        <h2>普信债 &amp; 二永债 · 日度换手率趋势</h2>
        <span class="badge" id="s4-badge">-- 个交易日</span>
      </div>
      <div class="chart-controls">
        <label>时间范围：</label>
        <button class="rng-btn active" data-range="all">全部</button>
        <button class="rng-btn" data-range="1y">近1年</button>
        <button class="rng-btn" data-range="6m">近6月</button>
        <button class="rng-btn" data-range="3m">近3月</button>
        <button class="rng-btn" data-range="1m">近1月</button>
      </div>
      <div id="chart4"></div>
      <div class="latest-title">📋 最新 20 个交易日数据</div>
      <div style="padding:0 20px 16px">
        <table id="s4-latest-table" style="width:360px">
          <thead>
            <tr>
              <th style="width:130px">日期</th>
              <th style="width:115px">普信债 (%)</th>
              <th style="width:115px">二永债 (%)</th>
            </tr>
          </thead>
          <tbody id="s4-latest-body"></tbody>
        </table>
      </div>
    </div>
  </div>

</div>

<script>
const RAW = """ + json_str + r""";

/* =========================================================
   Utility
   ========================================================= */
function fmt(v) { return (v === null || v === undefined) ? '-' : v; }
function fmtDate(v) { return (v && v.length > 10) ? v.slice(0,10) : (v||'-'); }
function cc(v) {
  const n = parseFloat(v);
  if (isNaN(n) || v === null) return '';
  return n > 0 ? 'positive' : n < 0 ? 'negative' : '';
}
function tooltipHeader(axisValue) {
  const v = axisValue && axisValue.length > 10 ? axisValue.slice(0,10) : axisValue;
  return `<div style="font-size:13px;font-weight:600;margin-bottom:6px">${v}</div>`;
}

/* =========================================================
   Tab switching
   ========================================================= */
let chart4Ready = false, chart2Ready = false, chart3Ready = false;
let currentRange = 'all';

function switchTab(idx) {
  document.querySelectorAll('.tab-btn').forEach((b,i) => b.classList.toggle('active', i===idx));
  document.querySelectorAll('.tab-panel').forEach((p,i) => p.classList.toggle('active', i===idx));
  setTimeout(() => {
    if (idx === 0 && window._chart1) window._chart1.resize();
    if (idx === 1) {
      if (!chart2Ready) { initChart2(); chart2Ready = true; }
      else if (window._chart2) window._chart2.resize();
    }
    if (idx === 2) {
      if (!chart3Ready) { initChart3(); chart3Ready = true; }
      else if (window._chart3) window._chart3.resize();
      if (window._chart3d) window._chart3d.resize();
    }
    if (idx === 3) {
      if (!chart4Ready) { initChart4(); chart4Ready = true; }
      else if (window._chart4) window._chart4.resize();
    }
  }, 50);
}

/* =========================================================
   Pagination helper
   ========================================================= */
function buildPagination(id, total, page, per, cb) {
  const tp = Math.ceil(total / per);
  document.getElementById(id).innerHTML = `
    <span>第 ${page}/${tp} 页，共 ${total} 条</span>
    <button class="pg-btn" onclick="${cb}(1)" ${page===1?'disabled':''}>首页</button>
    <button class="pg-btn" onclick="${cb}(${page-1})" ${page===1?'disabled':''}>上一页</button>
    <button class="pg-btn" onclick="${cb}(${page+1})" ${page===tp?'disabled':''}>下一页</button>
    <button class="pg-btn" onclick="${cb}(${tp})" ${page===tp?'disabled':''}>末页</button>`;
}

/* =========================================================
   Sheet1: TKN统计
   ========================================================= */
let s1p = 1, chart1Ready = false, s1Data = [], s1Desc = true;
function toggleSort1() {
  s1Desc = !s1Desc;
  const btn = document.getElementById('s1-sort');
  btn.className = 'sort-btn' + (s1Desc ? ' desc' : '');
  btn.innerHTML = (s1Desc ? '新 → 旧' : '旧 → 新') + '<span class="arrow">↑</span>';
  s1p = 1; s1Data.reverse(); s1Render();
}
function initSheet1() {
  const d = RAW.sheet1;
  s1Data = [...d.data].reverse();
  document.getElementById('s1-badge').textContent = s1Data.length + ' 条';
  document.getElementById('s1-thead').innerHTML =
    '<tr>' + d.headers.map(h => `<th>${h}</th>`).join('') + '</tr>';
  s1Render();
  if (!chart1Ready) { initChart1(); chart1Ready = true; }
}
function s1Render(p) {
  if (p) s1p = p;
  const st = (s1p-1)*50;
  document.getElementById('s1-tbody').innerHTML =
    s1Data.slice(st, st+50).map(row =>
      '<tr>' + row.map((c,i) => `<td class="${i>0?cc(c):''}">${fmt(c)}</td>`).join('') + '</tr>'
    ).join('');
  buildPagination('s1-pg', s1Data.length, s1p, 50, 's1Render');
}
function initChart1() {
  const d = RAW.sheet1;
  const chart = echarts.init(document.getElementById('chart1'));
  const xData = d.data.map(row => row[2]);
  const option = {
    backgroundColor:'#fff',
    tooltip:{
      trigger:'axis', axisPointer:{ type:'cross' },
      formatter(params){
        let h = tooltipHeader(params[0].axisValue);
        params.forEach(p => {
          let v = p.value;
          if (v === null || v === undefined) v = '-';
          else if (p.seriesName.includes('占比')) v = (+v).toFixed(2) + '%';
          h += `<div style="display:flex;align-items:center;gap:6px;margin-top:3px">
            <span style="display:inline-block;width:10px;height:10px;border-radius:${p.seriesType==='line'?'50%':'2px'};background:${p.color}"></span>
            <span style="color:#374151">${p.seriesName}</span>
            <span style="margin-left:auto;font-weight:600;color:${p.color}">${v}</span></div>`;
        });
        return h;
      },
      backgroundColor:'#fff', borderColor:'#e5e7eb', borderWidth:1, padding:[10,14],
      extraCssText:'box-shadow:0 4px 12px rgba(0,0,0,.12);border-radius:8px;'
    },
    legend:{ top:12, right:20, itemWidth:14, itemHeight:14, textStyle:{fontSize:13,color:'#374151'} },
    grid:{ top:60, left:64, right:64, bottom:80 },
    xAxis:{
      type:'category', data:xData,
      axisLabel:{color:'#9ca3af',fontSize:11,rotate:30,formatter:v=>v.length>10?v.slice(0,10):v},
      axisLine:{lineStyle:{color:'#e5e7eb'}},
      axisTick:{show:false}, splitLine:{show:false}
    },
    yAxis:[
      {
        type:'value', name:'笔数',
        nameTextStyle:{color:'#9ca3af',fontSize:12},
        axisLine:{show:false}, axisTick:{show:false},
        axisLabel:{color:'#9ca3af',fontSize:11},
        splitLine:{lineStyle:{color:'#f3f4f6',type:'dashed'}}
      },
      {
        type:'value', name:'TKN占比(%)',
        nameTextStyle:{color:'#9ca3af',fontSize:12},
        axisLine:{show:false}, axisTick:{show:false},
        axisLabel:{color:'#9ca3af',fontSize:11,formatter:v=>(+v).toFixed(1)+'%'},
        splitLine:{show:false}, min:0, max:100
      }
    ],
    series:[
      {
        name:'TKN笔数', type:'bar', yAxisIndex:0,
        data: d.data.map(row => { const v = parseInt(row[4]); return isNaN(v) ? null : v; }),
        itemStyle:{color:'#3b82f6',borderRadius:[4,4,0,0]}, barWidth:'40%'
      },
      {
        name:'GVN笔数', type:'bar', yAxisIndex:0,
        data: d.data.map(row => { const v = parseInt(row[5]); return isNaN(v) ? null : v; }),
        itemStyle:{color:'#ef4444',borderRadius:[4,4,0,0]}, barWidth:'40%'
      },
      {
        name:'TKN占比', type:'line', yAxisIndex:1,
        smooth:true, symbol:'circle', symbolSize:4,
        data: d.data.map(row => { const v = parseFloat(row[6]); return isNaN(v) ? null : (+v*100).toFixed(2); }),
        lineStyle:{width:2,color:'#f59e0b'}, itemStyle:{color:'#f59e0b'}
      }
    ]
  };
  chart.setOption(option);
  window._chart1 = chart;
}

/* =========================================================
   Sheet2 Chart: 换手率MA7 折线图
   ========================================================= */
function initChart2() {
  const d = RAW.sheet2;
  const rows = d.data.filter(row => row.slice(13,19).some(v => v !== null && v !== undefined));
  const xData = rows.map(r => r[0]);
  const S2_NAMES  = ['整体','(0,1)Y','[1,3)Y','[3,5)Y','[5,7)Y','[7,+)Y'];
  const S2_COLORS = ['#1d4ed8','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4'];
  const series = S2_NAMES.map((name, i) => ({
    name, type:'line', smooth:true, symbol:'none',
    lineStyle:{ width:2, color:S2_COLORS[i] },
    itemStyle:{ color:S2_COLORS[i] },
    data: rows.map(r => { const v = parseFloat(r[13+i]); return isNaN(v) ? null : (v * 100).toFixed(4); })
  }));
  const chart = echarts.init(document.getElementById('chart2'));
  chart.setOption({
    backgroundColor:'#fff',
    tooltip:{
      trigger:'axis',
      formatter(params){
        let h = tooltipHeader(params[0].axisValue);
        params.forEach(p => {
          const v = p.value===null||p.value===undefined ? '-' : (+p.value).toFixed(4)+'%';
          h += `<div style="display:flex;align-items:center;gap:6px;margin-top:3px">
            <span style="display:inline-block;width:10px;height:2px;background:${p.color};border-radius:1px"></span>
            <span style="color:#374151">${p.seriesName}</span>
            <span style="margin-left:auto;font-weight:600;color:${p.color}">${v}</span></div>`;
        });
        return h;
      },
      backgroundColor:'#fff', borderColor:'#e5e7eb', borderWidth:1, padding:[10,14],
      extraCssText:'box-shadow:0 4px 12px rgba(0,0,0,.12);border-radius:8px;'
    },
    legend:{ top:10, left:20, right:20, itemWidth:20, itemHeight:3, textStyle:{fontSize:13,color:'#374151'} },
    grid:{ top:60, left:80, right:30, bottom:80 },
    dataZoom:[
      { type:'slider', bottom:10, height:24, borderColor:'#e5e7eb',
        fillerColor:'rgba(29,78,216,.1)', handleStyle:{color:'#1d4ed8'},
        textStyle:{color:'#6b7280',fontSize:11} },
      { type:'inside', throttle:50 }
    ],
    xAxis:{
      type:'category', data:xData,
      axisLabel:{color:'#9ca3af',fontSize:11,rotate:30,formatter:v=>v.length>10?v.slice(0,10):v},
      axisLine:{lineStyle:{color:'#e5e7eb'}},
      axisTick:{show:false}, splitLine:{show:false}
    },
    yAxis:{
      type:'value', axisLine:{show:false}, axisTick:{show:false},
      axisLabel:{color:'#9ca3af',fontSize:11,formatter:v=>(+v).toFixed(2)+'%'},
      splitLine:{lineStyle:{color:'#f3f4f6',type:'dashed'}}
    },
    series
  });
  window._chart2 = chart;
}

/* =========================================================
   Sheet2 Table
   ========================================================= */
let s2p = 1, s2Data = [], s2Desc = true;
const S2_SUBS = ['整体','(0,1)','[1,3)','[3,5)','[5,7)','[7,+)'];
function toggleSort2() {
  s2Desc = !s2Desc;
  const btn = document.getElementById('s2-sort');
  btn.className = 'sort-btn' + (s2Desc ? ' desc' : '');
  btn.innerHTML = (s2Desc ? '新 → 旧' : '旧 → 新') + '<span class="arrow">↑</span>';
  s2p = 1; s2Data.reverse(); s2Render();
}
function initSheet2() {
  const d = RAW.sheet2;
  s2Data = d.data.filter(row => row.slice(13, 19).some(v => v !== null && v !== undefined)).reverse();
  document.getElementById('s2-badge').textContent = s2Data.length + ' 条';
  document.getElementById('s2-thead').innerHTML =
    '<tr><th>日期</th>' + S2_SUBS.map(s => `<th>${s}</th>`).join('') + '</tr>';
  s2Render();
}
function s2Render(p) {
  if (p) s2p = p;
  const st = (s2p-1)*50;
  document.getElementById('s2-tbody').innerHTML =
    s2Data.slice(st, st+50).map(row => {
      const ma7 = row.slice(13, 19);
      return '<tr><td>' + fmtDate(fmt(row[0])) + '</td>'
        + ma7.map(c => `<td class="${cc(c)}">${fmt(c)}</td>`).join('') + '</tr>';
    }).join('');
  buildPagination('s2-pg', s2Data.length, s2p, 50, 's2Render');
}

/* =========================================================
   Sheet3: 两种视图 + 汇总/详情图
   =========================================================
   s3View = 'left' | 'right'
   左视图: 主键=机构(left_institutions+summary_labels), 副键=期限(left_maturities+合计)
   右视图: 主键=期限(right_maturities), 副键=机构(right_institutions)

   图逻辑:
   - 未选具体主键 → 显示汇总堆叠图(chart3), 隐藏详情图(chart3d)
   - 选中具体主键(非"全部") → 隐藏汇总图, 显示详情图(chart3d)
     左视图选机构 → 该机构各期限净买入折线图
     左视图选合计机构 → 该合计机构的净买入时间序列
     右视图选期限 → 该期限下各机构净买入堆叠图
   ========================================================= */

let s3p = 1, s3Desc = true;
let s3View = 'left'; // 'left' | 'right'
let s3Primary = null;   // 选中的主键值(机构 or 期限)
let s3Secondary = null; // 选中的副键值(期限 or 机构)
let _s3dates = [], _s3cols = [], _s3grid = [];

// 颜色配置
const S3_INST_COLORS  = ['#3b82f6','#10b981','#94a3b8','#f59e0b','#8b5cf6','#ef4444'];
const S3_MAT_COLORS   = ['#1d4ed8','#0891b2','#059669','#d97706','#dc2626','#7c3aed'];
const S3_INST_NAMES_RIGHT = ['农商行','券商','保险','基金','理财','其他产品'];
const S3_MAT_NAMES_RIGHT  = ['≦1Y','1-3Y','3-5Y','5-7Y','7-10Y','10-15Y'];

function switchS3View(view, el) {
  s3View = view;
  s3Primary = null; s3Secondary = null; s3p = 1;
  document.querySelectorAll('#s3-view-toggle button').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  buildS3Chips();
  s3Pivot();
  s3Render();
  updateS3Chart();
}

function toggleSort3() {
  s3Desc = !s3Desc;
  const btn = document.getElementById('s3-sort');
  btn.className = 'sort-btn' + (s3Desc ? ' desc' : '');
  btn.innerHTML = (s3Desc ? '新 → 旧' : '旧 → 新') + '<span class="arrow">↑</span>';
  s3p = 1; _s3dates.reverse(); _s3grid.reverse(); s3Render();
}

function initSheet3() {
  buildS3Chips();
  s3Pivot();
  s3Render();
  // 汇总图在切换到此tab时初始化
}

function buildS3Chips() {
  const d = RAW.sheet3;
  if (s3View === 'left') {
    document.getElementById('s3-label-primary').textContent = '机构';
    document.getElementById('s3-label-secondary').textContent = '期限';
    const pc = document.getElementById('s3-chips-primary');
    pc.innerHTML = '<div class="chip active" onclick="setS3Primary(null,this)">全部</div>'
      + d.left_institutions.map(x => `<div class="chip" onclick="setS3Primary('${x}',this)">${x}</div>`).join('')
      + d.left_summary_labels.map(x => `<div class="chip chip-sum" onclick="setS3Primary('${x}',this)">${x.replace('-合计','')+'（合计）'}</div>`).join('');
    const sc = document.getElementById('s3-chips-secondary');
    sc.innerHTML = '<div class="chip active" onclick="setS3Secondary(null,this)">全部</div>'
      + d.left_maturities.map(x => `<div class="chip" onclick="setS3Secondary('${x}',this)">${x}</div>`).join('')
      + `<div class="chip chip-sum" onclick="setS3Secondary('合计',this)">合计</div>`;
  } else {
    document.getElementById('s3-label-primary').textContent = '期限';
    document.getElementById('s3-label-secondary').textContent = '机构';
    const pc = document.getElementById('s3-chips-primary');
    pc.innerHTML = '<div class="chip active" onclick="setS3Primary(null,this)">全部</div>'
      + d.right_maturities.map(x => `<div class="chip" onclick="setS3Primary('${x}',this)">${x}</div>`).join('');
    const sc = document.getElementById('s3-chips-secondary');
    sc.innerHTML = '<div class="chip active" onclick="setS3Secondary(null,this)">全部</div>'
      + d.right_institutions.map(x => `<div class="chip" onclick="setS3Secondary('${x}',this)">${x}</div>`).join('');
  }
}

function setS3Primary(v, el) {
  s3Primary = v; s3p = 1;
  // 如果选了合计chip，把显示名转回内部key
  if (v && v.endsWith('（合计）')) s3Primary = v.replace('（合计）','') + '-合计';
  document.querySelectorAll('#s3-chips-primary .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  s3Pivot(); s3Render(); updateS3Chart();
}
function setS3Secondary(v, el) {
  s3Secondary = v; s3p = 1;
  document.querySelectorAll('#s3-chips-secondary .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  s3Pivot(); s3Render();
  // 副键筛选不切换图，但若已有详情图需刷新
  if (s3Primary !== null) updateS3Chart();
}

function s3GetRecords() {
  const d = RAW.sheet3;
  if (s3View === 'left') {
    return d.left_records.filter(r =>
      (s3Primary === null || r.institution === s3Primary) &&
      (s3Secondary === null || r.maturity === s3Secondary)
    );
  } else {
    return d.right_records.filter(r =>
      (s3Primary === null || r.maturity === r.maturity && r.maturity === s3Primary) &&
      (s3Secondary === null || r.institution === s3Secondary)
    ).filter(r =>
      (s3Primary === null || r.maturity === s3Primary) &&
      (s3Secondary === null || r.institution === s3Secondary)
    );
  }
}

function s3Pivot() {
  const records = s3GetRecords();
  const dateIdx = {}, dates = [];
  records.forEach(r => { if (!(r.date in dateIdx)) { dateIdx[r.date]=dates.length; dates.push(r.date); }});
  const colIdx = {}, cols = [];
  records.forEach(r => {
    const k = r.institution+'|'+r.maturity;
    if (!(k in colIdx)) {
      colIdx[k] = cols.length;
      cols.push({inst:r.institution, mat:r.maturity, sum: r.is_summary||false});
    }
  });
  const grid = dates.map(() => new Array(cols.length).fill(null));
  records.forEach(r => { grid[dateIdx[r.date]][colIdx[r.institution+'|'+r.maturity]] = r.value; });
  if (s3Desc) { dates.reverse(); grid.reverse(); }
  _s3dates = dates; _s3cols = cols; _s3grid = grid;

  // 重建 colgroup + thead
  const TABLE_DATE_W = 120, COL_W = 90;
  const table = document.getElementById('s3-table');
  const oldCg = table.querySelector('colgroup');
  if (oldCg) table.removeChild(oldCg);
  const cg = document.createElement('colgroup');
  const cd = document.createElement('col'); cd.style.width = TABLE_DATE_W + 'px'; cg.appendChild(cd);
  cols.forEach(() => { const c = document.createElement('col'); c.style.width = COL_W + 'px'; cg.appendChild(c); });
  table.insertBefore(cg, table.firstChild);
  table.style.width = (TABLE_DATE_W + cols.length * COL_W) + 'px';

  // 表头（左视图：机构/期限；右视图：期限/机构）
  const thead = document.getElementById('s3-thead');
  if (s3View === 'left') {
    thead.innerHTML = '<tr><th style="width:'+TABLE_DATE_W+'px;min-width:'+TABLE_DATE_W+'px">日期</th>'
      + cols.map(c => {
          const cls = c.sum ? 'th-sum' : '';
          return `<th class="${cls}" style="width:${COL_W}px;min-width:${COL_W}px">${c.inst}<br><small>${c.mat}</small></th>`;
        }).join('') + '</tr>';
  } else {
    thead.innerHTML = '<tr><th style="width:'+TABLE_DATE_W+'px;min-width:'+TABLE_DATE_W+'px">日期</th>'
      + cols.map(c => {
          return `<th style="width:${COL_W}px;min-width:${COL_W}px">${c.mat}<br><small>${c.inst}</small></th>`;
        }).join('') + '</tr>';
  }
  document.getElementById('s3-badge').textContent = dates.length + ' 个交易周';
}

function s3Render(p) {
  if (p) s3p = p;
  const st = (s3p-1)*50;
  const pageRows  = _s3dates.slice(st, st+50);
  const pageGrid  = _s3grid.slice(st, st+50);
  document.getElementById('s3-tbody').innerHTML = pageRows.map((date, ri) =>
    '<tr><td style="white-space:nowrap">' + fmtDate(date) + '</td>'
    + pageGrid[ri].map((cell, ci) => {
        const cls = (_s3cols[ci].sum ? 'sum-cell ' : '') + cc(cell);
        return `<td class="${cls}">${fmt(cell)}</td>`;
      }).join('')
    + '</tr>'
  ).join('');
  buildPagination('s3-pg', _s3dates.length, s3p, 50, 's3Render');
}

/* ------ 图表更新逻辑 ------ */
function updateS3Chart() {
  if (s3Primary === null) {
    // 显示汇总图
    document.getElementById('s3-summary-chart-wrap').style.display = '';
    document.getElementById('s3-detail-chart-wrap').classList.remove('show');
    if (!chart3Ready) { initChart3(); chart3Ready = true; }
    else if (window._chart3) window._chart3.resize();
  } else {
    // 显示详情图
    document.getElementById('s3-summary-chart-wrap').style.display = 'none';
    document.getElementById('s3-detail-chart-wrap').classList.add('show');
    renderDetailChart();
    setTimeout(()=>{ if(window._chart3d) window._chart3d.resize(); }, 60);
  }
}

/* ------ 汇总堆叠图 (chart3) ------ */
function initChart3() {
  const d = RAW.sheet3;
  const summaryLabels = ['农商行-合计','保险-合计','其他-合计','基金-合计','理财-合计','证券公司-合计'];

  const allDates = [...new Set(
    d.left_records.filter(r => r.is_summary && r.maturity==='合计').map(r => r.date)
  )].sort();
  const xData = allDates.map(dt => dt.slice(0,10));

  const series = summaryLabels.map((lbl, i) => {
    const dm = {};
    d.left_records.filter(r => r.institution===lbl && r.is_summary && r.maturity==='合计')
                  .forEach(r => { dm[r.date] = r.value; });
    return {
      name: lbl.replace('-合计',''),
      type: 'bar', stack: 'total',
      data: allDates.map(dt => { const v = dm[dt]; return (v===null||v===undefined) ? 0 : +v.toFixed(2); }),
      itemStyle:{ color:S3_INST_COLORS[i] },
      emphasis:{ focus:'series' }
    };
  });

  const chart = echarts.init(document.getElementById('chart3'));
  chart.setOption({
    backgroundColor:'#fff',
    tooltip:{
      trigger:'axis', axisPointer:{type:'shadow'},
      formatter(params){
        let h = tooltipHeader(params[0].axisValue);
        let total = 0;
        params.forEach(p => {
          if (p.value===0) return;
          total += p.value;
          const sign = p.value>0?'+':'', cls = p.value>0?'#059669':'#dc2626';
          h += `<div style="display:flex;align-items:center;gap:6px;margin-top:3px">
            <span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${p.color}"></span>
            <span style="color:#374151">${p.seriesName}</span>
            <span style="margin-left:auto;font-weight:600;color:${cls}">${sign}${p.value}</span></div>`;
        });
        const tc = total>=0?'#059669':'#dc2626';
        h += `<div style="border-top:1px solid #f3f4f6;margin-top:6px;padding-top:6px;display:flex;justify-content:space-between;font-weight:700">
          <span style="color:#374151">合计</span><span style="color:${tc}">${total>=0?'+':''}${total.toFixed(2)} 亿</span></div>`;
        return h;
      },
      backgroundColor:'#fff', borderColor:'#e5e7eb', borderWidth:1, padding:[10,14],
      extraCssText:'box-shadow:0 4px 12px rgba(0,0,0,.12);border-radius:8px;'
    },
    legend:{ top:10, left:20, right:20, itemWidth:14, itemHeight:14, textStyle:{fontSize:13,color:'#374151'} },
    grid:{ top:60, left:68, right:30, bottom:80 },
    dataZoom:[
      { type:'slider', bottom:10, height:24, borderColor:'#e5e7eb',
        fillerColor:'rgba(29,78,216,.1)', handleStyle:{color:'#1d4ed8'},
        textStyle:{color:'#6b7280',fontSize:11} },
      { type:'inside', throttle:50 }
    ],
    xAxis:{
      type:'category', data:xData,
      axisLabel:{color:'#9ca3af',fontSize:11,rotate:30,formatter:v=>v.length>10?v.slice(0,10):v},
      axisLine:{lineStyle:{color:'#e5e7eb'}},
      axisTick:{show:false}, splitLine:{show:false}
    },
    yAxis:{
      type:'value', name:'净买入（亿元）',
      nameTextStyle:{color:'#9ca3af',fontSize:12},
      axisLine:{show:false}, axisTick:{show:false},
      axisLabel:{color:'#9ca3af',fontSize:11},
      splitLine:{lineStyle:{color:'#f3f4f6',type:'dashed'}}
    },
    series
  });
  window._chart3 = chart;
}

/* ------ 详情图 (chart3d) ------ */
function renderDetailChart() {
  const d = RAW.sheet3;
  let titleStr = '', series = [], xData = [], chartType = 'line';

  if (s3View === 'left') {
    // 左视图选中机构 → 各期限净买入随时间折线图
    const inst = s3Primary;
    const isSummary = inst.endsWith('-合计');

    if (isSummary) {
      // 合计机构：单条折线
      document.getElementById('s3-detail-title').textContent = `📈 ${inst.replace('-合计','')} · 净买入合计（亿元）`;
      const recs = d.left_records.filter(r => r.institution===inst && r.is_summary);
      const allDates = [...new Set(recs.map(r=>r.date))].sort();
      xData = allDates.map(dt=>dt.slice(0,10));
      const dm = {}; recs.forEach(r=>{ dm[r.date]=r.value; });
      series = [{
        name: inst.replace('-合计',''),
        type:'bar',
        data: allDates.map(dt=>{ const v=dm[dt]; return (v===null||v===undefined)?null:+v.toFixed(2); }),
        itemStyle:{ color:'#1d4ed8', borderRadius:[4,4,0,0] },
        emphasis:{ focus:'self' }
      }];
      chartType = 'bar';
    } else {
      // 普通机构：各期限折线
      document.getElementById('s3-detail-title').textContent = `📊 ${inst} · 各期限净买入（亿元）`;
      const MATS = d.left_maturities;
      const allDates = [...new Set(
        d.left_records.filter(r=>r.institution===inst && !r.is_summary).map(r=>r.date)
      )].sort();
      xData = allDates.map(dt=>dt.slice(0,10));
      series = MATS.map((mat, mi) => {
        const dm = {};
        d.left_records.filter(r=>r.institution===inst && r.maturity===mat && !r.is_summary)
                      .forEach(r=>{ dm[r.date]=r.value; });
        return {
          name: mat, type:'line', smooth:true, symbol:'none',
          lineStyle:{ width:2, color:S3_MAT_COLORS[mi] },
          itemStyle:{ color:S3_MAT_COLORS[mi] },
          data: allDates.map(dt=>{ const v=dm[dt]; return (v===null||v===undefined)?null:+v.toFixed(2); })
        };
      });
    }

  } else {
    // 右视图选中期限 → 该期限下各机构堆叠柱状图
    const mat = s3Primary;
    document.getElementById('s3-detail-title').textContent = `📊 期限 ${mat} · 各机构净买入（亿元）`;
    const INSTS = d.right_institutions;
    const allDates = [...new Set(
      d.right_records.filter(r=>r.maturity===mat).map(r=>r.date)
    )].sort();
    xData = allDates.map(dt=>dt.slice(0,10));
    series = INSTS.map((inst, ii) => {
      const dm = {};
      d.right_records.filter(r=>r.maturity===mat && r.institution===inst)
                     .forEach(r=>{ dm[r.date]=r.value; });
      return {
        name: inst, type:'bar', stack:'total',
        data: allDates.map(dt=>{ const v=dm[dt]; return (v===null||v===undefined)?0:+v.toFixed(2); }),
        itemStyle:{ color:S3_INST_COLORS[ii] },
        emphasis:{ focus:'series' }
      };
    });
    chartType = 'bar';
  }

  // 渲染
  if (!window._chart3d) {
    window._chart3d = echarts.init(document.getElementById('chart3d'));
  }
  window._chart3d.setOption({
    backgroundColor:'#fff',
    tooltip:{
      trigger:'axis',
      axisPointer:{ type: chartType==='bar' ? 'shadow' : 'line' },
      formatter(params){
        let h = tooltipHeader(params[0].axisValue);
        let total = 0;
        params.forEach(p => {
          if (p.value===null||p.value===undefined) return;
          const v = p.value;
          total += v;
          const sign = v>0?'+':'', cls=v>0?'#059669':'#dc2626';
          h += `<div style="display:flex;align-items:center;gap:6px;margin-top:3px">
            <span style="display:inline-block;width:10px;height:${chartType==='bar'?'10':'2'}px;border-radius:2px;background:${p.color}"></span>
            <span style="color:#374151">${p.seriesName}</span>
            <span style="margin-left:auto;font-weight:600;color:${cls}">${sign}${v.toFixed(2)}</span></div>`;
        });
        if (params.length > 1) {
          const tc=total>=0?'#059669':'#dc2626';
          h+=`<div style="border-top:1px solid #f3f4f6;margin-top:6px;padding-top:6px;display:flex;justify-content:space-between;font-weight:700">
              <span style="color:#374151">合计</span><span style="color:${tc}">${total>=0?'+':''}${total.toFixed(2)} 亿</span></div>`;
        }
        return h;
      },
      backgroundColor:'#fff', borderColor:'#e5e7eb', borderWidth:1, padding:[10,14],
      extraCssText:'box-shadow:0 4px 12px rgba(0,0,0,.12);border-radius:8px;'
    },
    legend:{ top:10, left:20, right:20, itemWidth:14, itemHeight:14, textStyle:{fontSize:13,color:'#374151'} },
    grid:{ top:60, left:68, right:30, bottom:80 },
    dataZoom:[
      { type:'slider', bottom:10, height:24, borderColor:'#e5e7eb',
        fillerColor:'rgba(29,78,216,.1)', handleStyle:{color:'#1d4ed8'},
        textStyle:{color:'#6b7280',fontSize:11} },
      { type:'inside', throttle:50 }
    ],
    xAxis:{
      type:'category', data:xData,
      axisLabel:{color:'#9ca3af',fontSize:11,rotate:30},
      axisLine:{lineStyle:{color:'#e5e7eb'}},
      axisTick:{show:false}, splitLine:{show:false}
    },
    yAxis:{
      type:'value', name:'净买入（亿元）',
      nameTextStyle:{color:'#9ca3af',fontSize:12},
      axisLine:{show:false}, axisTick:{show:false},
      axisLabel:{color:'#9ca3af',fontSize:11},
      splitLine:{lineStyle:{color:'#f3f4f6',type:'dashed'}}
    },
    series
  }, true);
}

/* =========================================================
   Sheet4: ECharts + latest-20 table
   ========================================================= */
function initChart4() {
  window._chart4 = echarts.init(document.getElementById('chart4'));
  document.getElementById('s4-badge').textContent = RAW.sheet4.dates.length + ' 个交易日';
  document.querySelectorAll('.rng-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.rng-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      currentRange = this.dataset.range;
      applyRange(currentRange);
    });
  });
  applyRange('all');
  renderLatest20();
}

function applyRange(range) {
  const d = RAW.sheet4;
  const allDates = d.dates;
  const total = allDates.length;
  let from = 0;
  if (range !== 'all') {
    const mMap = {'1y':12,'6m':6,'3m':3,'1m':1};
    const months = mMap[range];
    const last = new Date(allDates[total-1]);
    const cut  = new Date(last);
    cut.setMonth(cut.getMonth() - months);
    from = allDates.findIndex(dt => new Date(dt) >= cut);
    if (from < 0) from = 0;
  }
  const dates  = allDates.slice(from);
  const series = d.series.map(s => s.data.slice(from));
  const option = {
    backgroundColor:'#fff',
    tooltip:{
      trigger:'axis',
      formatter(params){
        let h = tooltipHeader(params[0].axisValue);
        params.forEach(p => {
          const v = p.value===null ? '-' : (+p.value).toFixed(4)+'%';
          h += `<div style="display:flex;align-items:center;gap:6px;margin-top:3px">
            <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${p.color}"></span>
            <span style="color:#374151">${p.seriesName}</span>
            <span style="margin-left:auto;font-weight:600;color:${p.color}">${v}</span></div>`;
        }); return h;
      },
      backgroundColor:'#fff', borderColor:'#e5e7eb', borderWidth:1, padding:[10,14],
      extraCssText:'box-shadow:0 4px 12px rgba(0,0,0,.12);border-radius:8px;'
    },
    legend:{ top:12, right:20, itemWidth:14, itemHeight:14, textStyle:{fontSize:13,color:'#374151'} },
    grid:{ top:60, left:64, right:30, bottom:80 },
    dataZoom:[
      { type:'slider', bottom:10, height:28, borderColor:'#e5e7eb',
        fillerColor:'rgba(29,78,216,.1)', handleStyle:{color:'#1d4ed8'},
        textStyle:{color:'#6b7280',fontSize:11}, startValue:dates[0], endValue:dates[dates.length-1] },
      { type:'inside', throttle:50 }
    ],
    xAxis:{
      type:'category', data:dates,
      axisLine:{lineStyle:{color:'#e5e7eb'}},
      axisLabel:{color:'#9ca3af',fontSize:11,rotate:30,formatter:v=>v.length>10?v.slice(0,10):v},
      axisTick:{show:false}, splitLine:{show:false}
    },
    yAxis:{
      type:'value', name:'换手率（%）',
      nameTextStyle:{color:'#9ca3af',fontSize:12},
      axisLine:{show:false}, axisTick:{show:false},
      axisLabel:{color:'#9ca3af',fontSize:11,formatter:v=>v.toFixed(2)+'%'},
      splitLine:{lineStyle:{color:'#f3f4f6',type:'dashed'}}
    },
    series: d.series.map((s,si) => ({
      name:s.name, type:'line', data:series[si],
      smooth:true, symbol:'none',
      lineStyle:{width:2,color:s.color},
      itemStyle:{color:s.color},
      areaStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[
        {offset:0,color:s.color+'28'},{offset:1,color:s.color+'05'}
      ]}}
    }))
  };
  window._chart4.setOption(option, true);
}

function renderLatest20() {
  const d = RAW.sheet4;
  const n = d.dates.length;
  const rows = [];
  for (let i = n-1; i >= Math.max(0, n-20); i--) {
    rows.push([d.dates[i], d.series[0].data[i], d.series[1].data[i]]);
  }
  document.getElementById('s4-latest-body').innerHTML = rows.map(r => {
    const px = r[1]===null?'-':(+r[1]).toFixed(4)+'%';
    const ey = r[2]===null?'-':(+r[2]).toFixed(4)+'%';
    return `<tr>
      <td style="text-align:left;white-space:nowrap">${fmtDate(r[0])}</td>
      <td class="${cc(r[1])}">${px}</td>
      <td class="${cc(r[2])}">${ey}</td>
    </tr>`;
  }).join('');
}

window.addEventListener('resize', () => {
  if (window._chart1) window._chart1.resize();
  if (window._chart2) window._chart2.resize();
  if (window._chart3) window._chart3.resize();
  if (window._chart3d) window._chart3d.resize();
  if (window._chart4) window._chart4.resize();
});

/* =========================================================
   Init
   ========================================================= */
initSheet1();
initSheet2();
initSheet3();
</script>
</body>
</html>"""

# Write HTML
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ index.html 生成完成，大小: {len(html)/1024:.1f} KB")
