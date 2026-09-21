#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_premium1.py
# Purpose: Premium business apps, batch 1 (ids 118+).
#
# These are the "Premium Applications" - full professional
# reports rendered in the browser, with formulas, charts,
# benchmarks, stage presets, month-over-month compare, a
# spreadsheet import and a one-click Download PDF (the
# browser's own print-to-PDF, isolated to the report).
#
# NOTE: every financial app here carries an explicit
# "this is an estimate, not advice" line in its info panel.
# That is deliberate and should stay.
# ============================================

from toolkit import tool, ws, info, html_block

PAGES = []

# ---------------------------------------------------------------
# Scoped styles for the SaaS Metrics report island (#saas-app).
# Every rule is prefixed with #saas-app so it can never touch the
# rest of the site, and the design tokens live on #saas-app (not
# :root) for the same reason.
# ---------------------------------------------------------------
SAAS_STYLE = r"""<style>
  #saas-app{
    --bg:#0B1120; --surface:#131C31; --surface-2:#0F1728; --panel:#0d1526; --border:#233149;
    --text:#E8ECF5; --muted:#8A97AD; --faint:#5C6B85;
    --indigo:#6366F1; --indigo-2:#818CF8; --cyan:#22D3EE; --violet:#A78BFA;
    --good:#34D399; --warn:#FBBF24; --bad:#F87171; --grid:#1c2740;
    --smono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
    --ssans:'Inter',-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;
    background:var(--bg); color:var(--text); font-family:var(--ssans); line-height:1.55;
    border:1px solid var(--border); border-radius:18px; padding:20px; display:block;
    -webkit-font-smoothing:antialiased;
  }
  #saas-app *{box-sizing:border-box;}
  #saas-app .note{font-size:12px;color:var(--faint);border:1px dashed var(--border);border-radius:10px;padding:8px 12px;margin:0 0 18px;text-align:center;}
  #saas-app .print-head{display:none;}
  #saas-app .card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:20px;margin-bottom:18px;break-inside:avoid;}
  #saas-app .eyebrow{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--cyan);display:block;margin:0 0 12px;}
  #saas-app .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px 16px;}
  #saas-app .grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px 16px;}
  #saas-app .field{display:flex;flex-direction:column;gap:6px;margin-bottom:12px;}
  #saas-app .field:last-child{margin-bottom:0;}
  #saas-app .field label{font-size:13px;color:var(--muted);font-weight:500;}
  #saas-app .field input,#saas-app .field select{background:var(--surface-2);border:1px solid var(--border);border-radius:10px;color:var(--text);font:600 15px/1.2 var(--smono);padding:11px 12px;width:100%;}
  #saas-app .field select{font-family:var(--ssans);cursor:pointer;}
  #saas-app .field input:focus,#saas-app .field select:focus{outline:none;border-color:var(--indigo);box-shadow:0 0 0 3px rgba(99,102,241,.25);}
  #saas-app .divider{height:1px;background:var(--border);margin:16px 0;border:0;}
  #saas-app .status{font-size:13px;color:var(--muted);font-family:var(--smono);margin:4px 2px 0;}
  #saas-app .status.ok{color:var(--good);} #saas-app .status.err{color:var(--bad);}
  #saas-app details.imp{margin-top:14px;border:1px solid var(--border);border-radius:10px;padding:10px 12px;background:var(--surface-2);}
  #saas-app details.imp summary{cursor:pointer;font-size:12px;color:var(--cyan);font-weight:700;letter-spacing:.03em;list-style:none;}
  #saas-app details.imp summary::-webkit-details-marker{display:none;}
  #saas-app details.imp summary::before{content:'+ ';font-family:var(--smono);}
  #saas-app details.imp[open] summary::before{content:'- ';}
  #saas-app .imp .ihelp{font-size:11px;color:var(--faint);margin:8px 0;line-height:1.55;}
  #saas-app .imp textarea{width:100%;min-height:78px;background:var(--panel);border:1px solid var(--border);border-radius:8px;color:var(--text);font:500 12px/1.5 var(--smono);padding:10px;resize:vertical;}
  #saas-app .imp .irow{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;}
  #saas-app .exec{display:grid;grid-template-columns:200px 1fr;gap:20px;align-items:center;}
  #saas-app .score{display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:16px;}
  #saas-app .score .ring{position:relative;width:118px;height:118px;}
  #saas-app .score .num{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
  #saas-app .score .num b{font:800 30px/1 var(--smono);}
  #saas-app .score .num span{font-size:11px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;}
  #saas-app .verdict{font-size:13px;font-weight:700;margin-top:10px;padding:3px 12px;border-radius:20px;}
  #saas-app .callouts{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}
  #saas-app .callout{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:13px 14px;border-left:3px solid var(--muted);}
  #saas-app .callout.good{border-left-color:var(--good);} #saas-app .callout.warn{border-left-color:var(--warn);} #saas-app .callout.bad{border-left-color:var(--bad);}
  #saas-app .callout .k{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;}
  #saas-app .callout .v{font:700 17px/1.2 var(--smono);margin:3px 0;}
  #saas-app .callout .d{font-size:12px;color:var(--muted);line-height:1.4;}
  #saas-app .stagenote{font-size:12px;color:var(--muted);margin:-4px 0 14px;line-height:1.5;}
  #saas-app .stagenote b{color:var(--cyan);font-weight:700;}
  #saas-app .tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;}
  #saas-app .tile{background:var(--surface-2);border:1px solid var(--border);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:2px;min-width:0;}
  #saas-app .tile.primary{background:linear-gradient(150deg,rgba(99,102,241,.20),rgba(34,211,238,.08));border-color:#33436a;}
  #saas-app .tile .v{font:700 18px/1.15 var(--smono);letter-spacing:-.01em;font-variant-numeric:tabular-nums;word-break:break-word;}
  #saas-app .tile .l{font-size:11px;color:var(--muted);line-height:1.3;}
  #saas-app .tile .bm{font-size:10px;color:var(--faint);margin-top:1px;}
  #saas-app .tile .dl{font-size:10.5px;font-weight:700;font-family:var(--smono);margin-top:2px;min-height:13px;}
  #saas-app .dl.up{color:var(--good);} #saas-app .dl.down{color:var(--bad);} #saas-app .dl.flat{color:var(--faint);}
  #saas-app .v.good{color:var(--good);} #saas-app .v.warn{color:var(--warn);} #saas-app .v.bad{color:var(--bad);}
  #saas-app .section-title{font-size:17px;font-weight:700;margin:0 0 3px;letter-spacing:-.01em;}
  #saas-app .section-sub{font-size:13px;color:var(--muted);margin:0 0 16px;}
  #saas-app .split{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start;}
  #saas-app .fstack{display:flex;flex-direction:column;gap:10px;}
  #saas-app .fcard{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:12px 14px;border-left:3px solid var(--indigo);}
  #saas-app .fcard.good{border-left-color:var(--good);} #saas-app .fcard.warn{border-left-color:var(--warn);} #saas-app .fcard.bad{border-left-color:var(--bad);}
  #saas-app .fcard .fn{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:5px;}
  #saas-app .fcard .fn b{font-size:14px;font-weight:600;}
  #saas-app .fcard .fn .res{font:700 16px var(--smono);font-variant-numeric:tabular-nums;white-space:nowrap;}
  #saas-app .res.good{color:var(--good);} #saas-app .res.warn{color:var(--warn);} #saas-app .res.bad{color:var(--bad);}
  #saas-app .fcard .formula{font:500 12px/1.6 var(--smono);color:var(--muted);word-break:break-word;}
  #saas-app .fcard .formula .sub{color:var(--text);}
  #saas-app .fcard .interp{font-size:12px;color:var(--muted);margin-top:6px;line-height:1.45;}
  #saas-app .fcard .bench{font-size:11px;color:var(--cyan);margin-top:5px;font-weight:600;}
  #saas-app .chart-wrap{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px;}
  #saas-app .chart-title{font-size:13px;font-weight:600;margin:0 0 1px;}
  #saas-app .chart-sub{font-size:11px;color:var(--muted);margin:0 0 8px;}
  #saas-app svg{display:block;width:100%;height:auto;}
  #saas-app .lc-row{display:grid;grid-template-columns:52px 1fr auto;align-items:center;gap:10px;margin-bottom:10px;}
  #saas-app .lc-row .lbl{font-size:12px;color:var(--muted);}
  #saas-app .lc-track{background:var(--surface-2);border-radius:7px;height:24px;overflow:hidden;}
  #saas-app .lc-fill{height:100%;border-radius:7px;transition:width .3s;}
  #saas-app .lc-row .val{font:600 13px var(--smono);}
  #saas-app .lc-caption{font-size:12px;color:var(--muted);margin-top:2px;}
  #saas-app .lc-caption b{color:var(--text);}
  #saas-app .solver{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
  #saas-app .scard{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px;border-top:3px solid var(--violet);}
  #saas-app .scard .st{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;font-weight:700;margin-bottom:6px;}
  #saas-app .scard .sv{font:700 15px/1.35 var(--ssans);}
  #saas-app .scard .sv b{color:var(--cyan);font-family:var(--smono);}
  #saas-app .scard .sd{font-size:12px;color:var(--muted);margin-top:5px;line-height:1.45;}
  #saas-app .read{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px;font-size:14px;line-height:1.7;}
  #saas-app .read h4{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--cyan);}
  #saas-app .read .r{display:flex;gap:9px;align-items:flex-start;margin-bottom:8px;}
  #saas-app .read .r:last-child{margin-bottom:0;}
  #saas-app .dot{width:7px;height:7px;border-radius:50%;flex:none;margin-top:7px;background:var(--muted);}
  #saas-app .dot.good{background:var(--good);} #saas-app .dot.warn{background:var(--warn);} #saas-app .dot.bad{background:var(--bad);}
  #saas-app .actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px;}
  #saas-app button.btn{font:600 14px var(--ssans);border-radius:10px;padding:11px 18px;cursor:pointer;border:1px solid var(--border);background:var(--surface-2);color:var(--text);}
  #saas-app button.btn:hover{border-color:var(--indigo);}
  #saas-app button.btn.primary{background:linear-gradient(145deg,var(--indigo),#4f46e5);border-color:transparent;color:#fff;}
  #saas-app button.btn.small{font-size:12px;padding:8px 12px;}
  #saas-app .toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%) translateY(20px);opacity:0;background:#0c1424;border:1px solid var(--border);color:var(--text);padding:10px 16px;border-radius:10px;font-size:13px;transition:opacity .2s,transform .2s;pointer-events:none;z-index:60;}
  #saas-app .toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
  @media (max-width:720px){
    #saas-app .split,#saas-app .exec,#saas-app .callouts,#saas-app .tiles,#saas-app .grid2,#saas-app .grid3,#saas-app .solver{grid-template-columns:1fr;}
    #saas-app .tiles{grid-template-columns:1fr 1fr;}
  }
  @media print{
    body *{visibility:hidden !important;}
    #saas-app,#saas-app *{visibility:visible !important;}
    #saas-app{position:absolute;left:0;top:0;width:100%;border:0;padding:0;
      --bg:#fff;--surface:#fff;--surface-2:#f8fafc;--panel:#f8fafc;--border:#d6dce6;--text:#0f172a;--muted:#475569;--faint:#64748b;--cyan:#0e7490;--grid:#e2e8f0;--violet:#7c3aed;
      background:#fff;color:#0f172a;}
    #saas-app #inputCard,#saas-app .actions,#saas-app .note,#saas-app .toast{display:none !important;}
    #saas-app .card{border:1px solid #e2e8f0;box-shadow:none;padding:14px;margin-bottom:12px;}
    #saas-app .print-head{display:flex !important;justify-content:space-between;align-items:flex-end;margin-bottom:14px;border-bottom:2px solid var(--indigo);padding-bottom:10px;}
    #saas-app .print-head .pt{font-size:20px;font-weight:800;margin:0;}
    #saas-app .print-head .pco{font-size:14px;font-weight:600;margin:2px 0 0;color:var(--indigo);}
    #saas-app .print-head .pm{font-size:11px;color:var(--muted);margin:2px 0 0;text-align:right;}
    #saas-app *{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
    @page{margin:12mm;}
  }
</style>"""

# ---------------------------------------------------------------
# The report markup (island). No <h1> here - the tool page shell
# already provides the page heading.
# ---------------------------------------------------------------
SAAS_MARKUP = r"""<div id="saas-app">
  <p class="note">Everything runs in your browser - nothing you type is uploaded. "Download PDF" opens your browser's print dialog; choose "Save as PDF" to keep a copy of the report.</p>

  <div class="print-head">
    <div><p class="pt">SaaS Financial Performance Report</p><p class="pco" id="print-co"></p></div>
    <p class="pm" id="print-meta">123miniapps.online</p>
  </div>

  <div class="card" id="inputCard">
    <span class="eyebrow">Report details</span>
    <div class="grid3">
      <div class="field"><label for="coName">Company name (optional)</label><input id="coName" type="text" placeholder="Acme Inc"></div>
      <div class="field"><label for="period">Reporting period (optional)</label><input id="period" type="text" placeholder="e.g. March 2026"></div>
      <div class="field"><label for="currency">Currency</label><select id="currency">
        <option value="USD">USD - US Dollar ($)</option>
        <option value="EUR">EUR - Euro (&euro;)</option>
        <option value="GBP">GBP - British Pound (&pound;)</option>
        <option value="INR">INR - Indian Rupee (&#8377;)</option>
        <option value="PKR">PKR - Pakistani Rupee (&#8360;)</option>
        <option value="AED">AED - UAE Dirham</option>
        <option value="AUD">AUD - Australian Dollar</option>
        <option value="CAD">CAD - Canadian Dollar</option>
        <option value="SGD">SGD - Singapore Dollar</option>
      </select></div>
      <div class="field"><label for="stage">Company stage (benchmark set)</label><select id="stage">
        <option value="auto">Auto - blended benchmarks</option>
        <option value="seed">Seed / pre-product-market-fit</option>
        <option value="seriesa">Series A / early growth</option>
        <option value="growth">Growth / scaleup</option>
        <option value="mature">Mature / profitable</option>
      </select></div>
    </div>
    <hr class="divider">
    <span class="eyebrow">Your figures (one month)</span>
    <div class="grid2">
      <div class="field"><label for="startMRR">Starting MRR</label><input id="startMRR" type="number" value="50000"></div>
      <div class="field"><label for="newMRR">New MRR</label><input id="newMRR" type="number" value="8000"></div>
      <div class="field"><label for="expMRR">Expansion MRR</label><input id="expMRR" type="number" value="3000"></div>
      <div class="field"><label for="conMRR">Contraction MRR</label><input id="conMRR" type="number" value="1200"></div>
      <div class="field"><label for="churnMRR">Churned MRR</label><input id="churnMRR" type="number" value="2500"></div>
      <div class="field"><label for="custStart">Customers at start</label><input id="custStart" type="number" value="500"></div>
      <div class="field"><label for="custNew">New customers</label><input id="custNew" type="number" value="70"></div>
      <div class="field"><label for="custChurn">Churned customers</label><input id="custChurn" type="number" value="25"></div>
      <div class="field"><label for="margin">Gross margin (%)</label><input id="margin" type="number" value="80"></div>
      <div class="field"><label for="cac">CAC per customer</label><input id="cac" type="number" value="1200"></div>
      <div class="field"><label for="opMargin">Operating margin (%)</label><input id="opMargin" type="number" value="5"></div>
    </div>
    <details class="imp">
      <summary>Paste / import figures from a spreadsheet</summary>
      <p class="ihelp">Paste labelled lines (e.g. <code>Starting MRR: 50000</code>, one per line), or paste a single row of 11 numbers in the field order above (comma, tab or space separated). Then press Import.</p>
      <textarea id="csvIn" placeholder="Starting MRR: 50000&#10;New MRR: 8000&#10;Expansion MRR: 3000&#10;...&#10;&#10;- or -&#10;&#10;50000, 8000, 3000, 1200, 2500, 500, 70, 25, 80, 1200, 5"></textarea>
      <div class="irow">
        <button class="btn small primary" id="import" type="button">Import figures</button>
        <button class="btn small" id="fillTemplate" type="button">Insert labelled template</button>
      </div>
    </details>
    <p class="status" id="status">Adjust any figure to rebuild the report.</p>
  </div>

  <div class="card">
    <span class="eyebrow">Executive summary</span>
    <div class="exec">
      <div class="score">
        <div class="ring"><svg viewBox="0 0 120 120" id="scoreRing"></svg><div class="num"><b id="scoreNum">-</b><span>Health</span></div></div>
        <div class="verdict" id="verdictPill">-</div>
      </div>
      <div class="callouts" id="callouts"></div>
    </div>
  </div>

  <div class="card">
    <span class="eyebrow">Key metrics at a glance</span>
    <p class="stagenote" id="stageNote"></p>
    <div class="tiles">
      <div class="tile primary"><span class="v" id="m-endmrr">-</span><span class="l">Ending MRR</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-arr">-</span><span class="l">ARR</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-net">-</span><span class="l">Net new MRR</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-growth">-</span><span class="l">MRR growth</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-nrr">-</span><span class="l">Net rev retention</span><span class="bm" id="bm-nrr">typical 100-120%</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-grr">-</span><span class="l">Gross rev retention</span><span class="bm">good &ge; 90%</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-gchurn">-</span><span class="l">Gross MRR churn</span><span class="bm" id="bm-gchurn">good &lt; 3%/mo</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-logo">-</span><span class="l">Logo churn</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-arpa">-</span><span class="l">ARPA / mo</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-ltv">-</span><span class="l">LTV</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-ratio">-</span><span class="l">LTV : CAC</span><span class="bm" id="bm-ratio">target &ge; 3:1</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-payback">-</span><span class="l">CAC payback</span><span class="bm" id="bm-payback">target &lt; 12 mo</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-quick">-</span><span class="l">Quick ratio</span><span class="bm" id="bm-quick">strong &ge; 4</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-lifetime">-</span><span class="l">Avg lifetime (mo)</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-rule40">-</span><span class="l">Rule of 40</span><span class="bm">target &ge; 40</span><span class="dl"></span></div>
      <div class="tile"><span class="v" id="m-arpaGP">-</span><span class="l">Gross profit / cust</span><span class="dl"></span></div>
    </div>
  </div>

  <div class="card">
    <p class="section-title">1 &middot; Recurring revenue</p>
    <p class="section-sub">The recurring revenue you earn each month, and how it moved.</p>
    <div class="split">
      <div class="fstack" id="f-rev"></div>
      <div class="chart-wrap">
        <p class="chart-title">MRR movement this month</p>
        <p class="chart-sub">Starting MRR (indigo) grows with new &amp; expansion (green), shrinks with contraction &amp; churn (red).</p>
        <svg id="waterfall" viewBox="0 0 640 300" preserveAspectRatio="xMidYMid meet"></svg>
        <p class="chart-title" style="margin-top:14px">12-month MRR forecast</p>
        <p class="chart-sub" id="fc-sub">If this month's net growth rate holds.</p>
        <svg id="forecast" viewBox="0 0 460 230" preserveAspectRatio="xMidYMid meet"></svg>
      </div>
    </div>
  </div>

  <div class="card">
    <p class="section-title">2 &middot; Churn &amp; retention</p>
    <p class="section-sub">How much revenue and how many customers you keep - the engine behind SaaS compounding.</p>
    <div class="split">
      <div class="fstack" id="f-ret"></div>
      <div class="chart-wrap">
        <p class="chart-title">Customer retention decay</p>
        <p class="chart-sub" id="ret-sub">A cohort of 100 customers at your current logo churn.</p>
        <svg id="retention" viewBox="0 0 460 230" preserveAspectRatio="xMidYMid meet"></svg>
      </div>
    </div>
  </div>

  <div class="card">
    <p class="section-title">3 &middot; Customer economics</p>
    <p class="section-sub">What a customer is worth, what they cost to acquire, and how fast you earn it back.</p>
    <div class="split">
      <div class="fstack" id="f-econ"></div>
      <div class="chart-wrap">
        <p class="chart-title">Earning back CAC</p>
        <p class="chart-sub">Cumulative gross profit per customer vs the cost to acquire them.</p>
        <svg id="payback" viewBox="0 0 460 230" preserveAspectRatio="xMidYMid meet"></svg>
        <div style="height:14px"></div>
        <p class="chart-title">LTV vs CAC</p>
        <div class="lc-row"><span class="lbl">LTV</span><div class="lc-track"><div class="lc-fill" id="bar-ltv" style="width:0;background:linear-gradient(90deg,#34D399,#22D3EE)"></div></div><span class="val" id="val-ltv">-</span></div>
        <div class="lc-row"><span class="lbl">CAC</span><div class="lc-track"><div class="lc-fill" id="bar-cac" style="width:0;background:linear-gradient(90deg,#6366F1,#818cf8)"></div></div><span class="val" id="val-cac">-</span></div>
        <p class="lc-caption" id="lc-caption">-</p>
      </div>
    </div>
  </div>

  <div class="card">
    <p class="section-title">4 &middot; Lifetime value &amp; growth efficiency</p>
    <p class="section-sub">Why churn dominates LTV, and whether growth and profitability are in balance.</p>
    <div class="split">
      <div class="fstack" id="f-eff"></div>
      <div class="chart-wrap">
        <p class="chart-title">How churn destroys LTV</p>
        <p class="chart-sub">LTV at different monthly churn rates, holding ARPA and margin fixed. Your rate is highlighted.</p>
        <svg id="sensitivity" viewBox="0 0 460 240" preserveAspectRatio="xMidYMid meet"></svg>
      </div>
    </div>
  </div>

  <div class="card">
    <span class="eyebrow" style="color:var(--violet)">What it would take &middot; targets</span>
    <p class="section-sub" style="margin-bottom:14px">The specific change in each lever needed to hit your stage's SaaS benchmark.</p>
    <div class="solver" id="solver"></div>
  </div>

  <div class="card">
    <div class="read" id="read"><h4>Strategic read</h4><div>Fill in your figures above to generate the analysis.</div></div>
  </div>

  <div class="actions">
    <button class="btn primary" id="dl" type="button">Download PDF</button>
    <button class="btn" id="baseline" type="button">Save as baseline</button>
    <button class="btn" id="share" type="button">Copy shareable link</button>
    <button class="btn" id="copy" type="button">Copy summary</button>
    <button class="btn" id="example" type="button">Load example</button>
    <button class="btn" id="reset" type="button">Clear</button>
  </div>

  <div class="toast" id="toast"></div>
</div>"""

# ---------------------------------------------------------------
# The engine. Identical maths to the tested preview, wrapped in
# DOMContentLoaded, with lookups + design tokens scoped to
# #saas-app, and Download PDF wired to the browser's print-to-PDF.
# ---------------------------------------------------------------
SAAS_SCRIPT = r"""
document.addEventListener('DOMContentLoaded', function(){
  var APP=document.getElementById('saas-app'); if(!APP) return;
  const $=id=>APP.querySelector('#'+id);
  const IDS=['startMRR','newMRR','expMRR','conMRR','churnMRR','custStart','custNew','custChurn','margin','cac','opMargin'];
  const ALL=IDS.concat(['currency','stage','coName','period']);
  const SYM={USD:'$',EUR:'€',GBP:'£',INR:'₹',PKR:'₨',AED:'AED ',AUD:'A$',CAD:'C$',SGD:'S$'};
  let CUR='USD';

  const STAGES={
    auto:   {label:'Auto (blended)',        churnGood:3,   churnOk:5, nrrGood:100, nrrOk:90,  ratioGood:3, paybackGood:12, paybackOk:18, growthTarget:8,  quickGood:4, note:'General SaaS benchmarks, not tuned to a stage.'},
    seed:   {label:'Seed / pre-PMF',        churnGood:5,   churnOk:8, nrrGood:90,  nrrOk:80,  ratioGood:2, paybackGood:18, paybackOk:24, growthTarget:15, quickGood:4, note:'Growth is weighted heavily and higher churn is tolerated - efficiency comes later.'},
    seriesa:{label:'Series A / early growth',churnGood:4,  churnOk:6, nrrGood:100, nrrOk:90,  ratioGood:3, paybackGood:15, paybackOk:20, growthTarget:10, quickGood:4, note:'Both fast growth and the first signs of efficient economics are expected.'},
    growth: {label:'Growth / scaleup',      churnGood:2.5, churnOk:4, nrrGood:105, nrrOk:95,  ratioGood:3, paybackGood:12, paybackOk:18, growthTarget:7,  quickGood:4, note:'Retention and payback are held to a high bar while growth stays strong.'},
    mature: {label:'Mature / profitable',   churnGood:1.5, churnOk:3, nrrGood:110, nrrOk:100, ratioGood:3, paybackGood:12, paybackOk:15, growthTarget:4,  quickGood:3, note:'Low churn, expansion-led retention and clear profitability are the priority over raw growth.'}
  };
  let B=STAGES.auto;

  const num=v=>{const n=parseFloat(String(v).replace(/[, ]/g,''));return isNaN(n)?NaN:n;};
  const $v=id=>num($(id).value);
  const fmt=(n,p=2)=>Number(n).toLocaleString(undefined,{minimumFractionDigits:p,maximumFractionDigits:p});
  const money=n=>{try{return Number(n).toLocaleString(undefined,{style:'currency',currency:CUR,maximumFractionDigits:Math.abs(n)>=1000?0:2});}catch(e){return (SYM[CUR]||'')+fmt(n,0);}};
  const kfmt=n=>{const a=Math.abs(n),s=n<0?'-':'',sym=SYM[CUR]||'';if(a>=1e6)return s+sym+fmt(a/1e6,2).replace(/\.?0+$/,'')+'M';if(a>=1e3)return s+sym+fmt(a/1e3,1).replace(/\.0$/,'')+'k';return s+sym+fmt(a,0);};
  const pct=(n,p=1)=>fmt(n,p)+'%';
  const css=v=>getComputedStyle(APP).getPropertyValue(v).trim();
  const set=(id,t,cls)=>{const el=$(id);if(el){el.textContent=t;el.className='v'+(cls?' '+cls:'');}};
  let summary='';

  function fcard(name,formula,result,status,interp,bench){
    return '<div class="fcard '+status+'"><div class="fn"><b>'+name+'</b><span class="res '+status+'">'+result+'</span></div>'+
      '<div class="formula">'+formula+'</div>'+(interp?'<div class="interp">'+interp+'</div>':'')+(bench?'<div class="bench">Benchmark: '+bench+'</div>':'')+'</div>';
  }

  function lineChart(id,ys,o){
    o=o||{};const W=460,H=(id==='sensitivity')?240:230,pl=48,pr=16,pt=16,pb=34;
    const iw=W-pl-pr,ih=H-pt-pb;
    const ymax=o.ymax||Math.max.apply(null,ys)*1.1||1, ymin=o.ymin||0;
    const n=ys.length,X=i=>pl+(n<=1?0:i/(n-1)*iw),Y=v=>pt+(1-(v-ymin)/(ymax-ymin))*ih;
    const col=o.color||css('--cyan'),grid=css('--grid'),mut=css('--muted'),txt=css('--text');
    let g='';
    for(let k=0;k<=4;k++){const val=ymin+(ymax-ymin)*k/4,y=Y(val);
      g+='<line x1="'+pl+'" y1="'+y.toFixed(1)+'" x2="'+(W-pr)+'" y2="'+y.toFixed(1)+'" stroke="'+grid+'" stroke-width="1"/>';
      g+='<text x="'+(pl-6)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="end" font-size="10" fill="'+mut+'" font-family="'+css('--smono')+'">'+(o.yfmt?o.yfmt(val):val.toFixed(0))+'</text>';}
    let path='';ys.forEach((v,i)=>{path+=(i===0?'M':'L')+' '+X(i).toFixed(1)+' '+Y(v).toFixed(1)+' ';});
    if(o.area!==false){g+='<path d="'+path+'L '+X(n-1).toFixed(1)+' '+Y(ymin)+' L '+X(0).toFixed(1)+' '+Y(ymin)+' Z" fill="'+col+'" opacity="0.14"/>';}
    g+='<path d="'+path.trim()+'" fill="none" stroke="'+col+'" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>';
    if(o.threshold!=null){const y=Y(o.threshold);
      g+='<line x1="'+pl+'" y1="'+y.toFixed(1)+'" x2="'+(W-pr)+'" y2="'+y.toFixed(1)+'" stroke="'+css('--bad')+'" stroke-width="1.5" stroke-dasharray="5 4"/>';
      g+='<text x="'+(W-pr)+'" y="'+(y-5).toFixed(1)+'" text-anchor="end" font-size="10" fill="'+css('--bad')+'" font-family="'+css('--smono')+'">'+o.thLabel+'</text>';}
    if(o.markerIdx!=null&&o.markerIdx>=0&&o.markerIdx<n){const mx=X(o.markerIdx),my=Y(ys[o.markerIdx]);
      g+='<line x1="'+mx.toFixed(1)+'" y1="'+pt+'" x2="'+mx.toFixed(1)+'" y2="'+(H-pb)+'" stroke="'+col+'" stroke-width="1" stroke-dasharray="3 3" opacity=".6"/>';
      g+='<circle cx="'+mx.toFixed(1)+'" cy="'+my.toFixed(1)+'" r="4.5" fill="'+col+'" stroke="'+css('--panel')+'" stroke-width="2"/>';
      if(o.markerLabel)g+='<text x="'+mx.toFixed(1)+'" y="'+(my-10).toFixed(1)+'" text-anchor="middle" font-size="10.5" font-weight="700" fill="'+txt+'" font-family="'+css('--smono')+'">'+o.markerLabel+'</text>';}
    g+='<circle cx="'+X(n-1).toFixed(1)+'" cy="'+Y(ys[n-1]).toFixed(1)+'" r="3.5" fill="'+col+'"/>';
    (o.xLabels||[]).forEach(t=>{g+='<text x="'+X(t.i).toFixed(1)+'" y="'+(H-pb+18)+'" text-anchor="middle" font-size="10" fill="'+mut+'">'+t.label+'</text>';});
    $(id).innerHTML=g;
  }

  function drawWaterfall(start,nw,exp,con,churn,end){
    const W=640,H=300,pl=14,pr=14,pt=26,pb=48,iw=W-pl-pr,ih=H-pt-pb;
    const steps=[{l:'Start',v:start,t:'total'},{l:'New',v:nw,t:'pos'},{l:'Expansion',v:exp,t:'pos'},{l:'Contraction',v:-con,t:'neg'},{l:'Churn',v:-churn,t:'neg'},{l:'Ending',v:end,t:'total'}];
    let run=start,bars=[],peak=Math.max(start,end,1);
    steps.forEach(s=>{let lo,hi;if(s.t==='total'){lo=0;hi=s.v;}else{if(s.v>=0){lo=run;hi=run+s.v;}else{lo=run+s.v;hi=run;}run+=s.v;}peak=Math.max(peak,hi,lo);bars.push(Object.assign({},s,{lo:lo,hi:hi}));});
    const sc=ih/(peak*1.14),Y=v=>pt+(peak*1.14-v)*sc,slot=iw/6,bw=slot*0.54;
    const cg=css('--good'),cb=css('--bad'),ct=css('--indigo'),cgr=css('--grid'),cm=css('--muted'),cx=css('--text');
    let g='<line x1="'+pl+'" y1="'+Y(0).toFixed(1)+'" x2="'+(W-pr)+'" y2="'+Y(0).toFixed(1)+'" stroke="'+cgr+'" stroke-width="1"/>';
    bars.forEach((b,i)=>{const c=pl+slot*i+slot/2,x=c-bw/2,top=Y(b.hi),bot=Y(b.lo),h=Math.max(2,bot-top);
      const fill=b.t==='total'?ct:(b.t==='pos'?cg:cb);
      g+='<rect x="'+x.toFixed(1)+'" y="'+top.toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+h.toFixed(1)+'" rx="3" fill="'+fill+'"/>';
      const lvl=Y(b.t==='pos'?b.hi:(b.t==='neg'?b.lo:b.hi));
      if(i<5)g+='<line x1="'+(c+bw/2).toFixed(1)+'" y1="'+lvl.toFixed(1)+'" x2="'+(pl+slot*(i+1)+slot/2-bw/2).toFixed(1)+'" y2="'+lvl.toFixed(1)+'" stroke="'+cm+'" stroke-width="1" stroke-dasharray="3 3" opacity=".5"/>';
      const vl=(b.t==='pos'?'+':'')+kfmt(b.t==='neg'?b.v:Math.abs(b.v));
      g+='<text x="'+c.toFixed(1)+'" y="'+(top-7).toFixed(1)+'" text-anchor="middle" font-size="11.5" font-weight="600" fill="'+cx+'" font-family="'+css('--smono')+'">'+vl+'</text>';
      g+='<text x="'+c.toFixed(1)+'" y="'+(H-pb+19)+'" text-anchor="middle" font-size="11" fill="'+cm+'">'+b.l+'</text>';});
    $('waterfall').innerHTML=g;
  }

  function drawSensitivity(arpa,gm,cur){
    const W=460,H=240,pl=48,pr=16,pt=18,pb=40,iw=W-pl-pr,ih=H-pt-pb;
    const rates=[1,2,3,5,8],ltvs=rates.map(r=>arpa*gm*(1/(r/100)));
    const ymax=Math.max.apply(null,ltvs)*1.12||1,Y=v=>pt+(1-v/ymax)*ih;
    const grid=css('--grid'),mut=css('--muted'),txt=css('--text');
    let g='';
    for(let k=0;k<=4;k++){const val=ymax*k/4,y=Y(val);g+='<line x1="'+pl+'" y1="'+y.toFixed(1)+'" x2="'+(W-pr)+'" y2="'+y.toFixed(1)+'" stroke="'+grid+'" stroke-width="1"/>';g+='<text x="'+(pl-6)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="end" font-size="10" fill="'+mut+'" font-family="'+css('--smono')+'">'+kfmt(val)+'</text>';}
    const slot=iw/rates.length,bw=slot*0.5;
    rates.forEach((r,i)=>{const c=pl+slot*i+slot/2,x=c-bw/2,y=Y(ltvs[i]),h=Math.max(2,Y(0)-y);
      const near=cur!=null&&Math.abs(cur-r)<0.75;
      const fill=near?css('--cyan'):(r<=2?css('--good'):r<=3?css('--indigo'):r<=5?css('--warn'):css('--bad'));
      g+='<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+h.toFixed(1)+'" rx="3" fill="'+fill+'"'+(near?' stroke="'+txt+'" stroke-width="1.5"':'')+'/>';
      g+='<text x="'+c.toFixed(1)+'" y="'+(y-6).toFixed(1)+'" text-anchor="middle" font-size="10.5" font-weight="600" fill="'+txt+'" font-family="'+css('--smono')+'">'+kfmt(ltvs[i])+'</text>';
      g+='<text x="'+c.toFixed(1)+'" y="'+(H-pb+18)+'" text-anchor="middle" font-size="11" fill="'+(near?css('--cyan'):mut)+'" font-family="'+css('--smono')+'"'+(near?' font-weight="700"':'')+'>'+r+'%</text>';});
    g+='<text x="'+(pl+iw/2)+'" y="'+(H-6)+'" text-anchor="middle" font-size="10" fill="'+mut+'">monthly churn rate</text>';
    $('sensitivity').innerHTML=g;
  }

  function ring(score){
    const R=52,C=2*Math.PI*R,off=C*(1-score/100),col=score>=70?css('--good'):score>=45?css('--warn'):css('--bad');
    $('scoreRing').innerHTML='<circle cx="60" cy="60" r="'+R+'" fill="none" stroke="'+css('--grid')+'" stroke-width="10"/>'+
      '<circle cx="60" cy="60" r="'+R+'" fill="none" stroke="'+col+'" stroke-width="10" stroke-linecap="round" stroke-dasharray="'+C.toFixed(1)+'" stroke-dashoffset="'+off.toFixed(1)+'" transform="rotate(-90 60 60)"/>';
    $('scoreNum').style.color=col;
  }

  function scard(t,v,d){return '<div class="scard"><div class="st">'+t+'</div><div class="sv">'+v+'</div>'+(d?'<div class="sd">'+d+'</div>':'')+'</div>';}

  let baseline=null, curMetrics=null;
  const INV={'m-gchurn':1,'m-logo':1,'m-payback':1};
  const UP='▲', DN='▼';
  function fmtDelta(id,type,cur,base){
    const d=cur-base; if(!isFinite(d)) return '';
    const eps=Math.max(1e-9,Math.abs(base)*0.0005);
    let txt;
    if(type==='money') txt=(d>=0?'+':'')+kfmt(d);
    else if(type==='pp') txt=(d>=0?'+':'')+fmt(d,1)+'pp';
    else if(type==='x')  txt=(d>=0?'+':'')+fmt(d,1)+'x';
    else if(type==='mo') txt=(d>=0?'+':'')+fmt(d,1)+'mo';
    else txt=(d>=0?'+':'')+fmt(d,0);
    let cls='flat',arrow='';
    if(Math.abs(d)>eps){const improved=INV[id]?d<0:d>0;cls=improved?'up':'down';arrow=(d>0?UP:DN)+' ';}
    return '<span class="'+cls+'">'+(cls==='flat'?'':arrow)+txt+' vs base</span>';
  }
  function renderDeltas(){
    if(!curMetrics) return;
    Object.keys(curMetrics).forEach(id=>{
      const el=$(id); if(!el) return;
      const dlEl=el.parentNode.querySelector('.dl'); if(!dlEl) return;
      if(!baseline||!baseline[id]){dlEl.className='dl';dlEl.innerHTML='';return;}
      const cur=curMetrics[id][0], type=curMetrics[id][1], base=baseline[id][0];
      if(!isFinite(cur)||!isFinite(base)){dlEl.className='dl';dlEl.innerHTML='';return;}
      dlEl.className='dl';
      dlEl.innerHTML=fmtDelta(id,type,cur,base);
    });
  }
  function saveBaseline(){
    if(baseline){baseline=null;$('baseline').textContent='Save as baseline';renderDeltas();toast('Baseline cleared');return;}
    baseline=JSON.parse(JSON.stringify(curMetrics||{}));
    $('baseline').textContent='Clear baseline';renderDeltas();
    toast('Baseline saved - change any figure to see the movement');
  }

  function calc(){
    CUR=$('currency').value||'USD';
    B=STAGES[$('stage').value]||STAGES.auto;
    const s=$v('startMRR');
    if(isNaN(s)||s<=0){$('status').textContent='Enter a starting MRR greater than zero.';$('status').className='status err';return;}
    const nw=$v('newMRR')||0,exp=$v('expMRR')||0,con=$v('conMRR')||0,ch=$v('churnMRR')||0;
    const cs=$v('custStart')||0,cn=$v('custNew')||0,cc=$v('custChurn')||0;
    const gm=(isNaN($v('margin'))?80:$v('margin'))/100,cac=$v('cac'),opM=$('opMargin').value.trim()===''?null:$v('opMargin');

    const netNew=nw+exp-con-ch,end=s+netNew,arr=end*12,growth=netNew/s*100;
    const nrr=(s+exp-con-ch)/s*100,grr=(s-con-ch)/s*100,gCh=ch/s*100;
    const logo=cs>0?cc/cs*100:NaN,custEnd=cs+cn-cc,arpa=custEnd>0?end/custEnd:NaN;
    const mFrac=gCh/100,life=mFrac>0?1/mFrac:Infinity;
    const gpc=!isNaN(arpa)?arpa*gm:NaN;
    const ltv=isFinite(life)&&!isNaN(arpa)?arpa*gm*life:NaN;
    const ratio=(cac>0&&!isNaN(ltv))?ltv/cac:NaN;
    const payback=(cac>0&&gpc>0)?cac/gpc:NaN;
    const quick=(con+ch)>0?(nw+exp)/(con+ch):Infinity;
    const rule40=opM==null?null:growth+opM;

    set('m-endmrr',money(end));set('m-arr',money(arr));
    set('m-net',(netNew>=0?'+':'')+money(netNew),netNew>=0?'good':'bad');
    set('m-growth',(growth>=0?'+':'')+pct(growth),growth>=0?'good':'bad');
    set('m-nrr',pct(nrr),nrr>=B.nrrGood?'good':nrr>=B.nrrOk?'warn':'bad');
    set('m-grr',pct(grr),grr>=90?'good':grr>=80?'warn':'bad');
    set('m-gchurn',pct(gCh),gCh<=B.churnGood?'good':gCh<=B.churnOk?'warn':'bad');
    set('m-logo',isNaN(logo)?'-':pct(logo),isNaN(logo)?'':logo<=B.churnGood?'good':logo<=B.churnOk?'warn':'bad');
    set('m-arpa',isNaN(arpa)?'-':money(arpa));set('m-ltv',isNaN(ltv)?'-':money(ltv));
    set('m-ratio',isNaN(ratio)?'-':fmt(ratio,1)+':1',isNaN(ratio)?'':ratio>=B.ratioGood?'good':ratio>=1?'warn':'bad');
    set('m-payback',isNaN(payback)?'-':fmt(payback,1)+'mo',isNaN(payback)?'':payback<=B.paybackGood?'good':payback<=B.paybackOk?'warn':'bad');
    set('m-quick',isFinite(quick)?fmt(quick,1):'∞',isFinite(quick)?(quick>=B.quickGood?'good':quick>=1?'warn':'bad'):'good');
    set('m-lifetime',isFinite(life)?fmt(life,0):'∞');
    set('m-rule40',rule40==null?'-':(rule40>=0?'+':'')+pct(rule40,0),rule40==null?'':rule40>=40?'good':'warn');
    set('m-arpaGP',isNaN(gpc)?'-':money(gpc));

    $('bm-nrr').innerHTML='good &ge; '+B.nrrGood+'%';
    $('bm-gchurn').innerHTML='good &lt; '+B.churnGood+'%/mo';
    $('bm-ratio').innerHTML='target &ge; '+B.ratioGood+':1';
    $('bm-payback').innerHTML='target &lt; '+B.paybackGood+' mo';
    $('bm-quick').innerHTML='strong &ge; '+B.quickGood;
    $('stageNote').innerHTML='Benchmarks tuned for: <b>'+B.label+'</b>. '+B.note;

    const M=money;
    $('f-rev').innerHTML=
      fcard('Ending MRR','MRR<sub>end</sub> = Start + New + Expansion &minus; Contraction &minus; Churn<br><span class="sub">= '+M(s)+' + '+M(nw)+' + '+M(exp)+' &minus; '+M(con)+' &minus; '+M(ch)+'</span>',M(end),'good','Monthly recurring revenue at the end of the period.')+
      fcard('Net new MRR','Net new = (New + Expansion) &minus; (Contraction + Churn)<br><span class="sub">= '+M(nw+exp)+' &minus; '+M(con+ch)+'</span>',(netNew>=0?'+':'')+M(netNew),netNew>=0?'good':'bad','The truest single measure of whether the month grew or shrank.')+
      fcard('MRR growth rate','g = Net new MRR &divide; Start MRR<br><span class="sub">= '+M(netNew)+' &divide; '+M(s)+'</span>',(growth>=0?'+':'')+pct(growth),growth>=0?'good':'bad','Monthly organic growth of recurring revenue.','this stage targets ~'+B.growthTarget+'%/mo')+
      fcard('ARR','ARR = Ending MRR &times; 12<br><span class="sub">= '+M(end)+' &times; 12</span>',M(arr),'good','Annual run-rate: current MRR projected across a year.');

    $('f-ret').innerHTML=
      fcard('Gross MRR churn','= Churned MRR &divide; Start MRR<br><span class="sub">= '+M(ch)+' &divide; '+M(s)+'</span>',pct(gCh),gCh<=B.churnGood?'good':gCh<=B.churnOk?'warn':'bad','The raw monthly leak rate of recurring revenue.','&lt; '+B.churnGood+'%/mo at this stage')+
      fcard('Net revenue retention','NRR = (Start + Expansion &minus; Contraction &minus; Churn) &divide; Start<br><span class="sub">= '+M(s+exp-con-ch)+' &divide; '+M(s)+'</span>',pct(nrr),nrr>=B.nrrGood?'good':nrr>=B.nrrOk?'warn':'bad','Above 100% = your existing base grows on its own.','&ge; '+B.nrrGood+'% at this stage')+
      fcard('Gross revenue retention','GRR = (Start &minus; Contraction &minus; Churn) &divide; Start<br><span class="sub">= '+M(s-con-ch)+' &divide; '+M(s)+'</span>',pct(grr),grr>=90?'good':grr>=80?'warn':'bad','Retention with expansion stripped out; caps at 100%.','&ge; 90% is strong')+
      fcard('Customer (logo) churn','= Churned customers &divide; Customers at start<br><span class="sub">= '+fmt(cc,0)+' &divide; '+fmt(cs,0)+'</span>',isNaN(logo)?'-':pct(logo),isNaN(logo)?'':logo<=B.churnGood?'good':logo<=B.churnOk?'warn':'bad','Share of customers lost this month.')+
      fcard('Avg customer lifetime','L = 1 &divide; monthly churn<br><span class="sub">= 1 &divide; '+fmt(mFrac,4)+'</span>',isFinite(life)?fmt(life,0)+' mo':'∞','good','Expected months a customer stays, at this churn.');

    $('f-econ').innerHTML=
      fcard('ARPA','ARPA = Ending MRR &divide; Customers<br><span class="sub">= '+M(end)+' &divide; '+fmt(custEnd,0)+'</span>',isNaN(arpa)?'-':M(arpa),'good','Average monthly revenue per customer.')+
      fcard('Gross profit / customer','= ARPA &times; Gross margin<br><span class="sub">= '+(isNaN(arpa)?'-':M(arpa))+' &times; '+pct(gm*100,0)+'</span>',isNaN(gpc)?'-':M(gpc),'good','Monthly profit each customer contributes.','SaaS gross margin typically 70-85%')+
      fcard('CAC','Cost to acquire one customer',M(cac),'warn','Fully-loaded sales &amp; marketing cost per new customer.')+
      fcard('CAC payback','= CAC &divide; (ARPA &times; margin)<br><span class="sub">= '+M(cac)+' &divide; '+(isNaN(gpc)?'-':M(gpc))+'</span>',isNaN(payback)?'-':fmt(payback,1)+' mo',isNaN(payback)?'':payback<=B.paybackGood?'good':payback<=B.paybackOk?'warn':'bad','Months to earn back the cost of a customer.','&lt; '+B.paybackGood+' months at this stage');

    $('f-eff').innerHTML=
      fcard('Customer lifetime value','LTV = ARPA &times; margin &times; lifetime<br><span class="sub">= '+(isNaN(arpa)?'-':M(arpa))+' &times; '+pct(gm*100,0)+' &times; '+(isFinite(life)?fmt(life,0):'∞')+' mo</span>',isNaN(ltv)?'-':M(ltv),'good','Gross profit a customer produces over their lifetime.')+
      fcard('LTV : CAC','= LTV &divide; CAC<br><span class="sub">= '+(isNaN(ltv)?'-':M(ltv))+' &divide; '+M(cac)+'</span>',isNaN(ratio)?'-':fmt(ratio,1)+' : 1',isNaN(ratio)?'':ratio>=B.ratioGood?'good':ratio>=1?'warn':'bad','Value returned for every unit of acquisition cost.','target &ge; '+B.ratioGood+':1')+
      fcard('Quick ratio','= (New + Expansion) &divide; (Contraction + Churn)<br><span class="sub">= '+M(nw+exp)+' &divide; '+M(con+ch)+'</span>',isFinite(quick)?fmt(quick,1):'∞',isFinite(quick)?(quick>=B.quickGood?'good':quick>=1?'warn':'bad'):'good','Revenue added for every unit lost.','&ge; '+B.quickGood+' is strong')+
      fcard('Rule of 40','= Growth rate + Operating margin<br><span class="sub">= '+pct(growth)+' + '+(opM==null?'-':pct(opM))+'</span>',rule40==null?'-':(rule40>=0?'+':'')+pct(rule40,0),rule40==null?'':rule40>=40?'good':'warn','Growth plus profit should total at least 40%.','target &ge; 40');

    drawWaterfall(s,nw,exp,con,ch,end);
    const g=growth/100,fys=[];for(let t=0;t<=12;t++)fys.push(end*Math.pow(1+g,t));
    lineChart('forecast',fys,{color:css('--indigo'),yfmt:kfmt,xLabels:[{i:0,label:'now'},{i:6,label:'6 mo'},{i:12,label:'12 mo'}],markerIdx:12,markerLabel:kfmt(fys[12])});
    $('fc-sub').textContent='At '+pct(growth)+'/mo, MRR reaches '+kfmt(fys[12])+' in 12 months.';
    const c=(isNaN(logo)?gCh:logo)/100||mFrac,rys=[];for(let t=0;t<=24;t++)rys.push(100*Math.pow(1-(isNaN(c)?mFrac:c),t));
    const llife=(isNaN(c)?mFrac:c)>0?1/(isNaN(c)?mFrac:c):Infinity;
    lineChart('retention',rys,{color:css('--cyan'),ymax:100,yfmt:v=>v.toFixed(0)+'%',xLabels:[{i:0,label:'0'},{i:12,label:'12 mo'},{i:24,label:'24 mo'}],markerIdx:isFinite(llife)&&llife<=24?Math.round(llife):null,markerLabel:isFinite(llife)&&llife<=24?'~'+fmt(llife,0)+' mo':''});
    $('ret-sub').textContent='At '+(isNaN(logo)?pct(gCh):pct(logo))+' monthly churn, half the cohort is gone by ~'+(isFinite(llife)?fmt(Math.log(0.5)/Math.log(1-(isNaN(c)?mFrac:c)),0):'-')+' months.';
    const N=Math.max(6,Math.min(36,Math.ceil((isNaN(payback)?12:payback)*1.6))),pys=[];for(let t=0;t<=N;t++)pys.push((isNaN(gpc)?0:gpc)*t);
    lineChart('payback',pys,{color:css('--good'),yfmt:kfmt,threshold:isNaN(cac)?null:cac,thLabel:'CAC '+kfmt(cac),xLabels:[{i:0,label:'0'},{i:Math.round(N/2),label:Math.round(N/2)+' mo'},{i:N,label:N+' mo'}],markerIdx:(!isNaN(payback)&&payback<=N)?Math.round(payback):null,markerLabel:!isNaN(payback)?fmt(payback,1)+' mo':''});
    drawSensitivity(isNaN(arpa)?0:arpa,gm,gCh);

    const mx=Math.max(isNaN(ltv)?0:ltv,isNaN(cac)?0:cac,1);
    $('bar-ltv').style.width=(isNaN(ltv)?0:Math.max(2,ltv/mx*100))+'%';
    $('bar-cac').style.width=(isNaN(cac)?0:Math.max(2,cac/mx*100))+'%';
    $('val-ltv').textContent=isNaN(ltv)?'-':money(ltv);$('val-cac').textContent=isNaN(cac)?'-':money(cac);
    $('lc-caption').innerHTML=isNaN(ratio)?'Add CAC and churn to compare value against cost.':'Each customer returns <b>'+fmt(ratio,1)+' : 1</b> on acquisition cost.';

    const sol=[];
    if(!isNaN(arpa)&&cac>0&&gpc>0){
      const maxChurn=arpa*gm/(B.ratioGood*cac)*100;
      if(!isNaN(ratio)&&ratio>=B.ratioGood) sol.push(scard('LTV:CAC target ('+B.ratioGood+':1)','Already met at <b>'+fmt(ratio,1)+':1</b>.','Your churn can rise to about <b>'+fmt(maxChurn,1)+'%</b>/mo before the ratio drops below '+B.ratioGood+':1.'));
      else sol.push(scard('To reach LTV:CAC of '+B.ratioGood+':1','Cut monthly churn to <b>'+fmt(Math.max(0,maxChurn),2)+'%</b> (from '+fmt(gCh,1)+'%), <span style="color:var(--muted)">or</span> cut CAC to <b>'+money(ltv/B.ratioGood)+'</b>.','At current ARPA and margin, that is what lifts each customer past the '+B.ratioGood+'x return bar.'));
    }
    if(gpc>0){
      const maxCac=B.paybackGood*gpc;
      if(!isNaN(payback)&&payback<=B.paybackGood) sol.push(scard('CAC payback target ('+B.paybackGood+' mo)','Already met at <b>'+fmt(payback,1)+' mo</b>.','CAC could rise to <b>'+money(maxCac)+'</b> and still pay back within '+B.paybackGood+' months.'));
      else sol.push(scard('To reach '+B.paybackGood+'-month payback','Reduce CAC to <b>'+money(maxCac)+'</b> (from '+money(cac)+'), <span style="color:var(--muted)">or</span> lift gross profit/customer to <b>'+money(cac/B.paybackGood)+'</b>/mo.','Payback = CAC divided by monthly gross profit per customer.'));
    }
    if(nrr<100){const gap=(100-nrr)/100*s;sol.push(scard('To reach 100% NRR','Recover <b>'+money(gap)+'</b>/mo of net churn, or add it as expansion.','That closes the gap between your '+pct(nrr)+' and the 100% break-even line where the base self-sustains.'));}
    else sol.push(scard('NRR self-sustaining','Met at <b>'+pct(nrr)+'</b>.','Your existing customers already grow without new logos - protect and expand them.'));
    if(rule40!=null&&rule40<40){sol.push(scard('To reach Rule of 40','Add <b>'+fmt(40-rule40,0)+' points</b> of growth or operating margin.','Growth+margin currently totals '+fmt(rule40,0)+'; the benchmark is 40.'));}
    $('solver').innerHTML=sol.slice(0,4).join('');

    let score=0;
    score+=Math.max(0,Math.min(25,(nrr-(B.nrrOk-10))/40*25));
    score+=Math.max(0,Math.min(20,(isNaN(ratio)?0:ratio)/B.ratioGood*20));
    score+=Math.max(0,Math.min(15,payback>0?(B.paybackGood/Math.max(payback,1))*15:0));
    score+=Math.max(0,Math.min(15,(B.churnOk-gCh)/B.churnOk*15));
    score+=Math.max(0,Math.min(15,(isFinite(quick)?quick:8)/B.quickGood*15));
    score+=Math.max(0,Math.min(10,growth/B.growthTarget*10));
    score=Math.round(Math.max(0,Math.min(100,score)));
    ring(score);$('scoreNum').textContent=score;
    const vp=$('verdictPill');
    if(score>=70){vp.textContent='Healthy';vp.style.background='rgba(52,211,153,.16)';vp.style.color=css('--good');}
    else if(score>=45){vp.textContent='Mixed';vp.style.background='rgba(251,191,36,.16)';vp.style.color=css('--warn');}
    else{vp.textContent='At risk';vp.style.background='rgba(248,113,113,.16)';vp.style.color=css('--bad');}

    const cands=[
      {k:'Net revenue retention',v:pct(nrr),s:nrr>=B.nrrGood?'good':nrr>=B.nrrOk?'warn':'bad',d:nrr>=100?'Existing customers grow on their own.':'Existing base is leaking; expansion is not covering churn.'},
      {k:'LTV : CAC',v:isNaN(ratio)?'-':fmt(ratio,1)+':1',s:isNaN(ratio)?'warn':ratio>=B.ratioGood?'good':ratio>=1?'warn':'bad',d:ratio>=B.ratioGood?'Acquisition is comfortably profitable.':ratio>=1?'Only modestly profitable per customer.':'You lose money on each customer.'},
      {k:'CAC payback',v:isNaN(payback)?'-':fmt(payback,1)+' mo',s:isNaN(payback)?'warn':payback<=B.paybackGood?'good':'warn',d:payback<=B.paybackGood?'Acquisition cost is recovered quickly.':'Long payback ties up cash.'},
      {k:'Gross MRR churn',v:pct(gCh),s:gCh<=B.churnGood?'good':gCh<=B.churnOk?'warn':'bad',d:gCh<=B.churnGood?'Revenue leak is well controlled.':'Churn is eating into growth.'},
    ];
    cands.sort((a,b)=>({bad:0,warn:1,good:2}[a.s]-{bad:0,warn:1,good:2}[b.s]));
    $('callouts').innerHTML=cands.slice(0,3).map(c=>'<div class="callout '+c.s+'"><div class="k">'+c.k+'</div><div class="v">'+c.v+'</div><div class="d">'+c.d+'</div></div>').join('');

    const notes=[];
    notes.push([netNew>=0?'good':'bad',netNew>=0?'Net new MRR is positive - the month grew recurring revenue by '+money(netNew)+'.':'Net new MRR is negative - churn and contraction outran new and expansion revenue.']);
    notes.push([nrr>=B.nrrGood?'good':nrr>=B.nrrOk?'warn':'bad',nrr>=110?'Net revenue retention above 110% is the compounding engine of elite SaaS - prioritise expansion.':nrr>=100?'NRR at or above 100% is healthy; the base grows without new logos.':nrr>=B.nrrOk?'NRR of '+pct(nrr)+' is leaking - closing the gap to 100% is worth more than new-logo growth right now.':'NRR below '+B.nrrOk+'% means new sales are filling a leaking bucket; fix retention first.']);
    if(!isNaN(ratio))notes.push([ratio>=B.ratioGood?'good':ratio>=1?'warn':'bad',ratio>=B.ratioGood?'LTV:CAC of '+fmt(ratio,1)+':1 supports spending more to grow.':ratio>=1?'LTV:CAC of '+fmt(ratio,1)+':1 is thin - improve retention or ARPA before scaling spend.':'LTV:CAC below 1:1 - pause acquisition until unit economics turn positive.']);
    if(gCh>B.churnOk)notes.push(['bad','At '+pct(gCh)+' monthly churn, average lifetime is only '+(isFinite(life)?fmt(life,0):'-')+' months - churn is the single biggest lever on LTV (see the sensitivity chart).']);
    if(rule40!=null)notes.push([rule40>=40?'good':'warn',rule40>=40?'Rule of 40 score of '+fmt(rule40,0)+' shows growth and profitability are in balance.':'Rule of 40 score of '+fmt(rule40,0)+' is under 40 - lift growth or margin to reach the benchmark.']);
    $('read').innerHTML='<h4>Strategic read</h4>'+notes.map(n=>'<div class="r"><span class="dot '+n[0]+'"></span><span>'+n[1]+'</span></div>').join('');

    const co=$('coName').value.trim();
    $('print-co').textContent=co||'';
    try{$('print-meta').innerHTML=(co?'':'123miniapps.online<br>')+($('period').value.trim()?'Period: '+$('period').value.trim()+'<br>':'')+'Stage: '+B.label+'<br>Generated '+new Date().toLocaleDateString(undefined,{year:'numeric',month:'long',day:'numeric'})+(co?'<br>123miniapps.online':'');}catch(e){}

    summary=['SaaS Financial Performance'+(co?' - '+co:'')+($('period').value.trim()?' ('+$('period').value.trim()+')':''),'Stage benchmarks: '+B.label,'Health score: '+score+'/100 ('+vp.textContent+')',
      'Ending MRR '+money(end)+' | ARR '+money(arr)+' | Net new '+money(netNew)+' ('+pct(growth)+')',
      'NRR '+pct(nrr)+' | GRR '+pct(grr)+' | Gross churn '+pct(gCh)+' | Logo churn '+(isNaN(logo)?'-':pct(logo)),
      'ARPA '+(isNaN(arpa)?'-':money(arpa))+' | LTV '+(isNaN(ltv)?'-':money(ltv))+' | LTV:CAC '+(isNaN(ratio)?'-':fmt(ratio,1)+':1')+' | Payback '+(isNaN(payback)?'-':fmt(payback,1)+'mo'),
      'Quick ratio '+(isFinite(quick)?fmt(quick,1):'inf')+(rule40!=null?' | Rule of 40 '+pct(rule40,0):''),'','via 123miniapps.online'].join('\n');
    $('status').textContent='Health '+score+'/100  -  Ending MRR '+money(end)+'  -  ARR '+money(arr);$('status').className='status ok';

    curMetrics={
      'm-endmrr':[end,'money'],'m-arr':[arr,'money'],'m-net':[netNew,'money'],'m-growth':[growth,'pp'],
      'm-nrr':[nrr,'pp'],'m-grr':[grr,'pp'],'m-gchurn':[gCh,'pp'],'m-logo':[logo,'pp'],
      'm-arpa':[arpa,'money'],'m-ltv':[ltv,'money'],'m-ratio':[ratio,'x'],'m-payback':[payback,'mo'],
      'm-quick':[isFinite(quick)?quick:NaN,'x'],'m-lifetime':[isFinite(life)?life:NaN,'mo'],
      'm-rule40':[rule40==null?NaN:rule40,'pp'],'m-arpaGP':[gpc,'money']
    };
    renderDeltas();
  }

  const EX={startMRR:50000,newMRR:8000,expMRR:3000,conMRR:1200,churnMRR:2500,custStart:500,custNew:70,custChurn:25,margin:80,cac:1200,opMargin:5};
  function toast(m){const t=$('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1900);}

  const SYN={
    startmrr:'startMRR',startingmrr:'startMRR',
    newmrr:'newMRR',newrevenue:'newMRR',newmrrrevenue:'newMRR',
    expansionmrr:'expMRR',expansion:'expMRR',expmrr:'expMRR',upsellmrr:'expMRR',
    contractionmrr:'conMRR',contraction:'conMRR',conmrr:'conMRR',downgrademrr:'conMRR',
    churnedmrr:'churnMRR',churnmrr:'churnMRR',churnedrevenue:'churnMRR',churnrevenue:'churnMRR',lostmrr:'churnMRR',
    customersatstart:'custStart',custstart:'custStart',startingcustomers:'custStart',customersstart:'custStart',
    newcustomers:'custNew',custnew:'custNew',customersnew:'custNew',customersadded:'custNew',
    churnedcustomers:'custChurn',custchurn:'custChurn',customerschurned:'custChurn',lostcustomers:'custChurn',customerslost:'custChurn',
    grossmargin:'margin',margin:'margin',grossmarginpct:'margin',
    cac:'cac',cacpercustomer:'cac',acquisitioncost:'cac',customeracquisitioncost:'cac',
    operatingmargin:'opMargin',opmargin:'opMargin',operatingmarginpct:'opMargin'
  };
  function doImport(){
    const txt=$('csvIn').value;
    if(!txt.trim()){toast('Paste some figures first');return;}
    const found={};
    txt.split(/\r?\n/).forEach(line=>{
      if(!line.trim())return;
      let parts;
      if(/[:=\t]/.test(line))parts=line.split(/[:=\t]/);
      else if(line.includes(','))parts=line.split(',');
      else return;
      if(parts.length<2)return;
      const key=parts[0].toLowerCase().replace(/[^a-z]/g,'');
      const val=parseFloat(parts.slice(1).join(' ').replace(/[^0-9.\-]/g,''));
      if(SYN[key]&&!isNaN(val))found[SYN[key]]=val;
    });
    let keys=Object.keys(found);
    if(keys.length===0){
      const nums=(txt.match(/-?\d+(?:\.\d+)?/g)||[]).map(Number);
      if(nums.length>=IDS.length){IDS.forEach((id,i)=>found[id]=nums[i]);keys=Object.keys(found);}
    }
    if(keys.length===0){toast('Could not read any figures - check the format');return;}
    keys.forEach(id=>{if($(id))$(id).value=found[id];});
    calc();
    toast('Imported '+keys.length+' field'+(keys.length>1?'s':''));
  }
  const TEMPLATE='Starting MRR: 50000\nNew MRR: 8000\nExpansion MRR: 3000\nContraction MRR: 1200\nChurned MRR: 2500\nCustomers at start: 500\nNew customers: 70\nChurned customers: 25\nGross margin: 80\nCAC: 1200\nOperating margin: 5';

  function shareUrl(){
    const o={};ALL.forEach(k=>{const el=$(k);if(el&&el.value!=='')o[k]=el.value;});
    try{return 'https://www.123miniapps.online/tools/saas-metrics-analyzer.html?d='+encodeURIComponent(btoa(unescape(encodeURIComponent(JSON.stringify(o)))));}catch(e){return 'https://www.123miniapps.online/tools/saas-metrics-analyzer.html';}
  }
  function loadFromUrl(){
    try{const p=new URLSearchParams(location.search).get('d');if(!p)return;
      const o=JSON.parse(decodeURIComponent(escape(atob(decodeURIComponent(p)))));
      ALL.forEach(k=>{if(o[k]!=null&&$(k))$(k).value=o[k];});
    }catch(e){}
  }

  ALL.forEach(id=>{const el=$(id);if(el)el.addEventListener('input',calc);});
  $('currency').addEventListener('change',calc);
  $('stage').addEventListener('change',calc);
  $('import').addEventListener('click',doImport);
  $('fillTemplate').addEventListener('click',()=>{$('csvIn').value=TEMPLATE;toast('Template inserted - edit the numbers, then Import');});
  $('baseline').addEventListener('click',saveBaseline);
  $('example').addEventListener('click',()=>{Object.keys(EX).forEach(k=>$(k).value=EX[k]);calc();toast('Example loaded');});
  $('reset').addEventListener('click',()=>{IDS.forEach(id=>$(id).value='');$('status').textContent='Enter a starting MRR greater than zero.';});
  $('dl').addEventListener('click',()=>{try{window.print();}catch(e){}});
  $('share').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(shareUrl());toast('Shareable link copied');}catch(e){toast('Copy not available');}});
  $('copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(summary);toast('Summary copied');}catch(e){toast('Copy not available');}});

  loadFromUrl();
  calc();
});
"""

INFO = info(
    features=[
        "Every core SaaS metric from one month of figures: MRR, ARR, net new MRR and growth rate",
        "Retention and churn: NRR, GRR, gross MRR churn, logo churn and average customer lifetime",
        "Unit economics: ARPA, gross profit per customer, LTV, CAC, LTV:CAC and CAC payback",
        "Quick ratio and the Rule of 40, each colour-coded against a benchmark",
        "A 0-100 health score, an executive summary and a plain-English strategic read",
        "Five charts: an MRR waterfall, a 12-month forecast, retention decay, CAC payback and LTV sensitivity",
        "Stage presets (seed to mature), month-over-month compare, spreadsheet import and one-click Download PDF",
    ],
    howto=[
        "Enter one month of revenue movement: starting MRR, new, expansion, contraction and churned MRR.",
        "Add your customer counts, gross margin and CAC (operating margin is optional, for the Rule of 40).",
        "Pick your company stage so the benchmarks and health score are tuned to what is realistic for you.",
        "Read the report: the health score and callouts up top, then every metric with its formula, benchmark and chart.",
        "Use Save as baseline to compare next month, or Download PDF to save a clean, branded report.",
    ],
    background_title="What the SaaS Metrics Analyzer measures, and why it matters",
    background_paragraphs=[
        "Software-as-a-service businesses live or die by a small set of recurring-revenue metrics, but those "
        "numbers only mean something in relation to each other and to a benchmark. This analyzer takes a single "
        "month of movement - how much recurring revenue you started with, what you added through new and expansion "
        "sales, and what you lost to contraction and churn - and turns it into a complete financial-performance "
        "report. It computes monthly recurring revenue (MRR), annual run-rate (ARR), net new MRR and your growth "
        "rate, then the retention picture: net revenue retention (NRR), gross revenue retention (GRR), gross MRR "
        "churn and customer (logo) churn.",
        "From there it derives the unit economics that decide whether growth is worth paying for: average revenue "
        "per account (ARPA), lifetime value (LTV), customer acquisition cost (CAC), the all-important LTV:CAC ratio "
        "and CAC payback period, plus the quick ratio and the Rule of 40. Every figure is shown with the exact "
        "formula behind it and colour-coded against a benchmark, so you can see not just what your numbers are but "
        "whether they are healthy for a company at your stage. A target solver even tells you the specific change "
        "in churn, CAC or expansion needed to hit each benchmark.",
        "Everything is computed in your browser from the figures you type - nothing is uploaded, and there is no "
        "account or sign-up. The result is a report you would normally build by hand in a spreadsheet, generated "
        "in seconds, with charts and a plain-English read you can hand to a co-founder, board member or investor. "
        "This is an analytical tool for planning and understanding your metrics, not financial, investment or "
        "accounting advice.",
    ],
)

FAQS = [
    ("Is the SaaS Metrics Analyzer really free?",
     "Yes, completely. It is free with no account, no sign-up and no usage limit. It carries the Premium label to "
     "indicate a deeper, professional-grade feature set - a full report with formulas, charts and benchmarks - not a price."),
    ("What figures do I need to use it?",
     "One month of movement: your starting MRR, new MRR, expansion MRR, contraction MRR and churned MRR, plus your "
     "customer counts (start, new, churned), gross margin and CAC. Operating margin is optional and only used for the Rule of 40."),
    ("What is a good LTV:CAC ratio and CAC payback?",
     "As a rule of thumb, an LTV:CAC ratio of 3:1 or higher and a CAC payback under 12 months are considered healthy "
     "for most SaaS businesses. The analyzer lets you pick a company stage, which adjusts these benchmarks - a seed-stage "
     "company is reasonably held to a gentler bar than a mature one."),
    ("How do I save or share the report?",
     "Use Download PDF to open your browser's print dialog and choose Save as PDF - it prints a clean, branded, "
     "report-only page with your company name and period. Copy shareable link creates a bookmarkable URL that reopens "
     "the report with your figures filled in, and Copy summary puts a text summary on your clipboard."),
    ("Is my data private?",
     "Completely. Every calculation runs locally in your browser using JavaScript. Your revenue and customer figures "
     "are never sent to a server - there is no server to receive them - so you can safely enter real company numbers."),
]

PAGES.append(tool(
    slug="saas-metrics-analyzer",
    name="SaaS Metrics Analyzer",
    icon="📈",
    cat="premium",
    title="SaaS Metrics Analyzer",
    description="Turn one month of revenue and customer movement into MRR, ARR, churn, NRR, LTV, CAC, payback and the Rule of 40, each read against its benchmark.",
    tagline="Enter one month of revenue and customer movement; get a full professional SaaS report with formulas, charts, benchmarks and a one-click PDF.",
    workspace=ws(html_block(SAAS_STYLE + "\n" + SAAS_MARKUP)),
    info_block=INFO,
    script=SAAS_SCRIPT,
    faqs=FAQS,
))
