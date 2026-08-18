import sys
from pathlib import Path
import io
import csv
import html

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import streamlit as st
from agent.agent import run_document_agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CDE Governance Workspace",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# ENTERPRISE UI / UX
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #070b14;
        --panel: #0d1422;
        --panel-2: #111a2b;
        --panel-3: #151f31;
        --line: rgba(148,163,184,.16);
        --text: #f8fafc;
        --muted: #94a3b8;
        --blue: #38bdf8;
        --blue-2: #60a5fa;
        --green: #34d399;
        --amber: #fbbf24;
        --red: #fb7185;
    }

    .stApp {
        background:
            radial-gradient(circle at 82% 0%, rgba(56,189,248,.09), transparent 28%),
            radial-gradient(circle at 12% 8%, rgba(96,165,250,.06), transparent 24%),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1580px;
        padding-top: 1.15rem;
        padding-bottom: 4rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b111d 0%, #090e18 100%);
        border-right: 1px solid rgba(148,163,184,.12);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.1rem; }
    .sidebar-brand {
        display:flex; align-items:center; gap:.65rem;
        padding:.45rem .2rem 1rem;
        font-weight:750; font-size:1.05rem;
    }
    .shield {
        width:31px; height:31px; border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        background:linear-gradient(135deg, rgba(56,189,248,.25), rgba(96,165,250,.06));
        border:1px solid rgba(56,189,248,.25);
        box-shadow:0 0 24px rgba(56,189,248,.12);
    }
    .side-kicker {
        color:#64748b; font-size:.68rem; text-transform:uppercase;
        letter-spacing:.12em; font-weight:750; margin:.7rem 0 .45rem;
    }
    .workflow-step {
        display:flex; gap:.6rem; align-items:flex-start;
        color:#cbd5e1; font-size:.84rem; padding:.33rem 0;
    }
    .workflow-num {
        min-width:21px; height:21px; border-radius:7px;
        display:inline-flex; align-items:center; justify-content:center;
        background:#121b2b; border:1px solid var(--line); color:#7dd3fc;
        font-size:.7rem; font-weight:750;
    }
    .governance-note {
        margin-top:1rem; padding:.9rem; border-radius:12px;
        background:linear-gradient(135deg, rgba(30,64,175,.22), rgba(14,165,233,.07));
        border:1px solid rgba(96,165,250,.18);
        color:#bfdbfe; font-size:.78rem; line-height:1.55;
    }

    /* Hero */
    .hero {
        position:relative; overflow:hidden; padding:1.35rem 1.45rem;
        border:1px solid var(--line); border-radius:18px;
        background:linear-gradient(135deg, rgba(17,24,39,.96), rgba(13,20,34,.82));
        box-shadow:0 20px 60px rgba(0,0,0,.18);
        margin-bottom:1.25rem;
        animation: rise .55s ease-out both;
    }
    .hero::after {
        content:""; position:absolute; width:280px; height:280px; right:-120px; top:-160px;
        background:radial-gradient(circle, rgba(56,189,248,.18), transparent 65%);
        pointer-events:none;
    }
    .hero-row { display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; position:relative; z-index:1; }
    .eyebrow { color:#7dd3fc; font-size:.7rem; text-transform:uppercase; letter-spacing:.16em; font-weight:800; margin-bottom:.42rem; }
    .hero-title { font-size:2rem; line-height:1.05; font-weight:800; letter-spacing:-.035em; margin:0; }
    .hero-subtitle { color:var(--muted); margin-top:.55rem; font-size:.9rem; max-width:780px; }
    .hero-badge {
        white-space:nowrap; padding:.48rem .72rem; border-radius:999px;
        color:#a7f3d0; background:rgba(16,185,129,.08); border:1px solid rgba(52,211,153,.22);
        font-size:.72rem; font-weight:750;
    }

    /* Section labels */
    .section-head { display:flex; align-items:end; justify-content:space-between; margin:1.45rem 0 .72rem; }
    .section-title { font-size:1.08rem; font-weight:800; letter-spacing:-.015em; margin:0; }
    .section-caption { color:#64748b; font-size:.75rem; margin-top:.22rem; }
    .micro-label { color:#64748b; text-transform:uppercase; letter-spacing:.1em; font-size:.65rem; font-weight:800; }

    /* Cards */
    .metric-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; }
    .metric-card {
        position:relative; overflow:hidden; min-height:108px; padding:1rem 1.05rem;
        border-radius:14px; border:1px solid var(--line);
        background:linear-gradient(145deg, rgba(17,24,39,.95), rgba(13,20,34,.9));
        transition:transform .22s ease, border-color .22s ease, box-shadow .22s ease;
        animation: rise .55s ease-out both;
    }
    .metric-card:hover { transform:translateY(-3px); border-color:rgba(56,189,248,.28); box-shadow:0 14px 35px rgba(0,0,0,.22); }
    .metric-card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:2px; background:rgba(56,189,248,.55); }
    .metric-label { color:#7f8ea3; font-size:.68rem; text-transform:uppercase; letter-spacing:.09em; font-weight:750; }
    .metric-value { font-size:1.85rem; font-weight:850; line-height:1; margin-top:.55rem; }
    .metric-help { color:#64748b; font-size:.68rem; margin-top:.45rem; }
    .green { color:var(--green); } .amber { color:var(--amber); } .blue { color:var(--blue); }

    /* Upload */
    .upload-shell { padding:1rem 1.05rem; border:1px solid var(--line); border-radius:14px; background:rgba(13,20,34,.72); }
    .file-chip { display:inline-flex; align-items:center; gap:.5rem; margin-top:.45rem; padding:.42rem .65rem; border-radius:9px; color:#cbd5e1; background:#121b2b; border:1px solid var(--line); font-size:.76rem; }

    /* Table */
    .table-shell { border:1px solid var(--line); border-radius:14px; overflow:hidden; background:#0c1320; }
    .cde-table { width:100%; border-collapse:collapse; font-size:.76rem; }
    .cde-table th { text-align:left; color:#64748b; text-transform:uppercase; letter-spacing:.08em; font-size:.62rem; font-weight:800; padding:.72rem .78rem; background:#101827; border-bottom:1px solid var(--line); }
    .cde-table td { padding:.72rem .78rem; border-bottom:1px solid rgba(148,163,184,.08); color:#cbd5e1; vertical-align:middle; }
    .cde-table tr:last-child td { border-bottom:0; }
    .cde-table tr { transition:background .18s ease; }
    .cde-table tr:hover { background:rgba(56,189,248,.035); }
    .cde-name { color:#f8fafc; font-weight:700; }
    .crit { color:#93c5fd; font-size:.7rem; font-weight:700; }
    .criteria-wrap { display:flex; flex-wrap:wrap; gap:.25rem; }
    .pill { display:inline-block; padding:.22rem .4rem; border-radius:6px; color:#bae6fd; background:rgba(14,116,144,.13); border:1px solid rgba(56,189,248,.12); font-size:.59rem; font-weight:700; }
    .status { display:inline-flex; align-items:center; gap:.32rem; padding:.25rem .45rem; border-radius:999px; font-size:.62rem; font-weight:800; }
    .status-dot { width:6px; height:6px; border-radius:50%; }
    .status-supported { color:#a7f3d0; background:rgba(16,185,129,.08); border:1px solid rgba(52,211,153,.18); }
    .status-supported .status-dot { background:#34d399; box-shadow:0 0 8px rgba(52,211,153,.6); }
    .status-review { color:#fde68a; background:rgba(245,158,11,.08); border:1px solid rgba(251,191,36,.18); }
    .status-review .status-dot { background:#fbbf24; box-shadow:0 0 8px rgba(251,191,36,.6); }

    /* Detail */
    .detail-hero { padding:1.15rem 1.25rem; border:1px solid var(--line); border-radius:16px; background:linear-gradient(135deg,#111a2b,#0d1422); margin-top:1rem; animation:fade .35s ease-out both; }
    .detail-title { font-size:1.55rem; font-weight:850; letter-spacing:-.025em; margin:.3rem 0 .6rem; }
    .badge-row { display:flex; flex-wrap:wrap; gap:.4rem; }
    .badge { display:inline-flex; align-items:center; padding:.3rem .5rem; border-radius:7px; font-size:.63rem; text-transform:uppercase; letter-spacing:.06em; font-weight:800; }
    .badge-green { color:#a7f3d0; background:rgba(16,185,129,.1); border:1px solid rgba(52,211,153,.18); }
    .badge-blue { color:#bae6fd; background:rgba(14,165,233,.09); border:1px solid rgba(56,189,248,.16); }
    .badge-amber { color:#fde68a; background:rgba(245,158,11,.09); border:1px solid rgba(251,191,36,.16); }

    .info-card { padding:1rem 1.05rem; border:1px solid var(--line); border-radius:12px; background:#0e1727; margin:.7rem 0; }
    .info-text { color:#cbd5e1; line-height:1.65; font-size:.84rem; }
    .evidence-box { padding:1rem 1.05rem; border-radius:12px; background:#0a1220; border:1px solid rgba(56,189,248,.16); border-left:3px solid var(--blue); color:#cbd5e1; line-height:1.7; font-size:.82rem; }
    .trace-line { display:flex; align-items:center; gap:.55rem; color:#64748b; font-size:.7rem; margin:.75rem 0; }
    .trace-node { padding:.35rem .52rem; border-radius:7px; background:#121b2b; border:1px solid var(--line); color:#cbd5e1; }
    .trace-arrow { color:#38bdf8; }
    .criteria-card { display:flex; flex-wrap:wrap; gap:.4rem; padding:.8rem; border-radius:10px; background:#0a1220; border:1px solid var(--line); }

    /* Governance */
    .decision-banner { padding:.9rem 1rem; border-radius:12px; border:1px solid rgba(96,165,250,.18); background:linear-gradient(135deg, rgba(30,64,175,.2), rgba(14,165,233,.05)); color:#bfdbfe; font-size:.8rem; line-height:1.55; }
    .governance-summary { display:grid; grid-template-columns:repeat(4,1fr); gap:.55rem; margin-top:.8rem; }
    .summary-item { padding:.7rem; border-radius:9px; background:#0e1727; border:1px solid var(--line); }
    .summary-value { color:#e2e8f0; font-size:.75rem; margin-top:.25rem; }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        border-radius:9px !important; font-weight:750 !important; transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { transform:translateY(-1px); box-shadow:0 8px 22px rgba(0,0,0,.18); }

    /* Inputs */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea {
        background:#101827 !important; border-color:rgba(148,163,184,.15) !important;
        border-radius:9px !important;
    }
    label { color:#94a3b8 !important; font-size:.72rem !important; font-weight:700 !important; }
    [data-testid="stFileUploader"] { border-radius:12px; }

    /* Hide some Streamlit chrome */
    #MainMenu { visibility:hidden; }
    footer { visibility:hidden; }

    @keyframes rise { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
    @keyframes fade { from { opacity:0; } to { opacity:1; } }
    @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:.55; } }

    @media (max-width: 900px) {
        .metric-grid { grid-template-columns:repeat(2,1fr); }
        .governance-summary { grid-template-columns:repeat(2,1fr); }
        .hero-title { font-size:1.55rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def esc(value):
    return html.escape(str(value or ""))


def criteria_pills(criteria):
    if not criteria:
        return '<span class="pill">NO CRITERIA</span>'
    return "".join(f'<span class="pill">{esc(c)}</span>' for c in criteria)


def status_badge(supported):
    if supported:
        return '<span class="status status-supported"><span class="status-dot"></span>Supported</span>'
    return '<span class="status status-review"><span class="status-dot"></span>Requires review</span>'


def save_governance(name, values):
    st.session_state[f"governance_{name}"] = values
    st.session_state[f"governance_saved_{name}"] = True


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand"><span class="shield">🛡️</span><span>Governance Agent</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-kicker">Workflow</div>', unsafe_allow_html=True)
    steps = [
        "Upload document", "Extract evidence", "Identify candidate CDEs",
        "Validate claims", "Review evidence", "Make human decision",
    ]
    for i, step in enumerate(steps, 1):
        st.markdown(
            f'<div class="workflow-step"><span class="workflow-num">{i}</span><span>{esc(step)}</span></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown('<div class="side-kicker">Governance principle</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="governance-note">AI discovers and validates candidate CDEs using supplied evidence. Final CDE designation, ownership and control decisions remain with human governance.</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
      <div class="hero-row">
        <div>
          <div class="eyebrow">Data Governance • Evidence Intelligence</div>
          <div class="hero-title">CDE Governance Workspace</div>
          <div class="hero-subtitle">Turn regulatory text into a review-ready Critical Data Element register — with traceable evidence, validation guardrails and a clear path to human governance decisions.</div>
        </div>
        <div class="hero-badge">● HUMAN-IN-THE-LOOP</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DOCUMENT INGESTION
# =========================================================

st.markdown(
    '<div class="section-head"><div><div class="section-title">1. Document intake</div><div class="section-caption">Provide the source material the governance review will be grounded in.</div></div></div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Upload a regulatory or business document",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX",
    )

    if uploaded_file:
        st.markdown(
            f'<div class="file-chip">📄 <b>{esc(uploaded_file.name)}</b><span>•</span>{uploaded_file.size:,} bytes</div>',
            unsafe_allow_html=True,
        )

    analyze = st.button(
        "Analyze document",
        type="primary",
        width="stretch",
        disabled=uploaded_file is None,
    )

    if analyze and uploaded_file:
        with st.status("Running governance analysis…", expanded=True) as status:
            try:
                st.write("Reading uploaded document…")
                result, validations = run_document_agent(uploaded_file.getvalue(), uploaded_file.name)
                st.write("Retrieving evidence and validating candidate claims…")
                st.session_state["analysis_result"] = result
                st.session_state["validations"] = validations
                st.session_state["filename"] = uploaded_file.name
                status.update(label="Analysis complete", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Analysis failed", state="error", expanded=True)
                st.error("The document could not be analyzed.")
                st.exception(e)


# =========================================================
# RESULTS
# =========================================================

if "analysis_result" in st.session_state and "validations" in st.session_state:
    result = st.session_state["analysis_result"]
    validations = st.session_state["validations"]
    filename = st.session_state.get("filename", "Uploaded document")

    candidates = result.candidates
    validation_list = validations.validations
    candidate_map = {c.name: c for c in candidates}
    validation_map = {v.name: v for v in validation_list}

    total = len(validation_list)
    supported = sum(1 for v in validation_list if v.supported)
    review = total - supported
    unique_criteria = sorted({c for v in validation_list for c in (v.corrected_criteria or [])})
    coverage = round((supported / total) * 100) if total else 0

    st.markdown(
        f'<div class="section-head"><div><div class="section-title">2. Analysis overview</div><div class="section-caption">{esc(filename)} • {total} candidate CDEs evaluated</div></div><div class="micro-label">Validation coverage {coverage}%</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'''
        <div class="metric-grid">
          <div class="metric-card"><div class="metric-label">Candidates</div><div class="metric-value">{total}</div><div class="metric-help">AI-identified elements</div></div>
          <div class="metric-card"><div class="metric-label">Supported</div><div class="metric-value green">{supported}</div><div class="metric-help">Evidence-backed candidates</div></div>
          <div class="metric-card"><div class="metric-label">Requires review</div><div class="metric-value amber">{review}</div><div class="metric-help">Needs governance attention</div></div>
          <div class="metric-card"><div class="metric-label">Criteria identified</div><div class="metric-value blue">{len(unique_criteria)}</div><div class="metric-help">Unique governance criteria</div></div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # =====================================================
    # CDE REGISTER
    # =====================================================

    st.markdown(
        '<div class="section-head"><div><div class="section-title">3. Candidate CDE register</div><div class="section-caption">Filter the working register, then open one element for evidence and governance review.</div></div></div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns([1.25, 1, 1])
    with f1:
        search = st.text_input("Search CDEs", placeholder="e.g. account identifier, name, address…", label_visibility="visible")
    with f2:
        status_filter = st.multiselect(
            "Status",
            ["Supported Candidate", "Requires Review"],
            default=["Supported Candidate", "Requires Review"],
        )
    with f3:
        criteria_options = ["All", "OUTPUT", "CALCULATION", "IDENTIFICATION / LINKING", "OWNERSHIP / AGGREGATION", "VALIDATION / RECONCILIATION"]
        criteria_filter = st.selectbox("Criteria", criteria_options)

    filtered = []
    for validation in validation_list:
        candidate = candidate_map.get(validation.name)
        if candidate is None:
            continue
        status = "Supported Candidate" if validation.supported else "Requires Review"
        criteria = validation.corrected_criteria or []
        if status not in status_filter:
            continue
        if search and search.lower() not in candidate.name.lower():
            continue
        if criteria_filter != "All" and criteria_filter not in criteria:
            continue
        filtered.append({
            "CDE": candidate.name,
            "Criticality": candidate.criticality,
            "Criteria": criteria,
            "Status": status,
            "Page": candidate.page,
        })

    if filtered:
        rows_html = []
        for row in filtered:
            rows_html.append(
                f'''<tr>
                    <td><span class="cde-name">{esc(row["CDE"])}</span></td>
                    <td><span class="crit">{esc(row["Criticality"])}</span></td>
                    <td><div class="criteria-wrap">{criteria_pills(row["Criteria"])}</div></td>
                    <td>{status_badge(row["Status"] == "Supported Candidate")}</td>
                    <td>{esc(row["Page"])}</td>
                </tr>'''
            )
        table = f'''
        <div class="table-shell">
          <table class="cde-table">
            <thead><tr><th style="width:21%">CDE</th><th style="width:13%">Criticality</th><th style="width:35%">Criteria</th><th style="width:18%">Status</th><th style="width:13%">Page</th></tr></thead>
            <tbody>{"".join(rows_html)}</tbody>
          </table>
        </div>'''
        st.markdown(table, unsafe_allow_html=True)
        st.caption(f"Showing {len(filtered)} of {total} candidates")
    else:
        st.warning("No CDEs match the selected filters.")

    names = [row["CDE"] for row in filtered]

    if names:
        selected_name = st.selectbox("Open CDE workspace", names, key="selected_cde")
        candidate = candidate_map[selected_name]
        validation = validation_map.get(selected_name)

        # =================================================
        # DETAIL HEADER
        # =================================================
        status_cls = "badge-green" if validation.supported else "badge-amber"
        status_label = "SUPPORTED CANDIDATE" if validation.supported else "REQUIRES REVIEW"
        crit = candidate.criticality or "Unclassified"

        st.markdown(
            f'''
            <div class="detail-hero">
              <div class="micro-label">CDE governance workspace</div>
              <div class="detail-title">{esc(candidate.name)}</div>
              <div class="badge-row"><span class="badge {status_cls}">● {status_label}</span><span class="badge badge-blue">{esc(crit)}</span></div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        overview_tab, evidence_tab, validation_tab, governance_tab = st.tabs(["Overview", "Evidence", "Validation", "Governance Review"])

        # -------------------------------------------------
        # OVERVIEW
        # -------------------------------------------------
        with overview_tab:
            st.markdown('<div class="section-head"><div><div class="section-title">AI assessment</div><div class="section-caption">The validated interpretation used to support governance review.</div></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card"><div class="info-text">{esc(validation.corrected_reason)}</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="section-head"><div><div class="section-title">Governance criteria</div></div></div>', unsafe_allow_html=True)
            if validation.corrected_criteria:
                st.markdown(f'<div class="criteria-card">{criteria_pills(validation.corrected_criteria)}</div>', unsafe_allow_html=True)
            else:
                st.warning("No criteria were directly supported by the evidence.")

            st.markdown('<div class="section-head"><div><div class="section-title">Candidate description</div></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card"><div class="info-text">{esc(candidate.description)}</div></div>', unsafe_allow_html=True)

            with st.expander("View original AI reasoning"):
                st.write(candidate.reason)

        # -------------------------------------------------
        # EVIDENCE
        # -------------------------------------------------
        with evidence_tab:
            st.markdown('<div class="section-head"><div><div class="section-title">Evidence traceability</div><div class="section-caption">Every governance decision should be traceable back to source material.</div></div></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'<div class="info-card"><div class="micro-label">Source document</div><div class="info-text">{esc(candidate.source)}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="info-card"><div class="micro-label">Page / location</div><div class="info-text">{esc(candidate.page)}</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="micro-label" style="margin:.9rem 0 .45rem">Evidence used by the AI</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="evidence-box">{esc(candidate.evidence)}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="trace-line"><span class="trace-node">Candidate</span><span class="trace-arrow">→</span><span class="trace-node">Source evidence</span><span class="trace-arrow">→</span><span class="trace-node">Validation</span><span class="trace-arrow">→</span><span class="trace-node">Governance decision</span></div>',
                unsafe_allow_html=True,
            )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------
        with validation_tab:
            st.markdown('<div class="section-head"><div><div class="section-title">Evidence guardrail validation</div><div class="section-caption">Only claims directly supported by supplied evidence should survive into the governance record.</div></div></div>', unsafe_allow_html=True)
            if validation.supported:
                st.success("Candidate claims are supported by the provided evidence.")
            else:
                st.warning("One or more candidate claims require governance review.")

            if validation.supported_claims:
                st.markdown("#### Supported claims")
                for claim in validation.supported_claims:
                    st.markdown(f'<div class="info-card" style="border-left:3px solid #34d399"><div class="info-text">✓ {esc(claim)}</div></div>', unsafe_allow_html=True)

            if validation.unsupported_claims:
                st.markdown("#### Unsupported claims")
                for claim in validation.unsupported_claims:
                    st.markdown(f'<div class="info-card" style="border-left:3px solid #fb7185"><div class="info-text">✕ {esc(claim)}</div></div>', unsafe_allow_html=True)

            st.markdown("#### Corrected governance interpretation")
            st.markdown(f'<div class="info-card"><div class="info-text">{esc(validation.corrected_reason)}</div></div>', unsafe_allow_html=True)

        # -------------------------------------------------
        # GOVERNANCE
        # -------------------------------------------------
        with governance_tab:
            st.markdown('<div class="section-head"><div><div class="section-title">Human governance review</div><div class="section-caption">Convert the evidence into an accountable governance decision and next action.</div></div></div>', unsafe_allow_html=True)
            st.markdown('<div class="decision-banner"><b>AI recommendation is advisory.</b> The governance owner is responsible for the final CDE designation, ownership assignment and control decision.</div>', unsafe_allow_html=True)

            existing = st.session_state.get(f"governance_{selected_name}", {})
            default_decision = existing.get("decision", "Not yet reviewed")
            decisions = ["Not yet reviewed", "Confirm as CDE", "Reject", "Needs Further Investigation"]

            decision = st.radio("Final CDE decision", decisions, index=decisions.index(default_decision) if default_decision in decisions else 0, horizontal=True, key=f"decision_{selected_name}")

            g1, g2 = st.columns(2)
            with g1:
                owner = st.text_input("Data Steward / Owner", value=existing.get("owner", ""), placeholder="Person or governance team", key=f"owner_{selected_name}")
            with g2:
                domain = st.text_input("Business Domain", value=existing.get("domain", ""), placeholder="e.g. Deposits, Customer, Finance", key=f"domain_{selected_name}")

            source_system = st.text_input("System / Source of Record", value=existing.get("source_system", ""), placeholder="Authoritative system or dataset", key=f"system_{selected_name}")

            g3, g4 = st.columns(2)
            with g3:
                dq_required = st.selectbox("Data quality rule", ["TBD", "Yes", "No"], index=["TBD", "Yes", "No"].index(existing.get("data_quality_rule", "TBD")) if existing.get("data_quality_rule", "TBD") in ["TBD", "Yes", "No"] else 0, key=f"dq_{selected_name}")
            with g4:
                next_action = st.text_input("Next Action", value=existing.get("next_action", ""), placeholder="e.g. Define completeness rule and assign steward", key=f"next_{selected_name}")

            proposed_rule = st.text_area("Proposed DQ Rule", value=existing.get("proposed_dq_rule", ""), placeholder="Describe the control or rule that should be implemented if this becomes a governed CDE…", height=90, key=f"rule_{selected_name}")
            notes = st.text_area("Governance Notes", value=existing.get("notes", ""), placeholder="Capture rationale, business context, exceptions or implementation notes…", height=100, key=f"notes_{selected_name}")

            if st.button("Save governance decision", type="primary", width="stretch", key=f"save_{selected_name}"):
                save_governance(selected_name, {
                    "decision": decision,
                    "owner": owner,
                    "domain": domain,
                    "source_system": source_system,
                    "data_quality_rule": dq_required,
                    "proposed_dq_rule": proposed_rule,
                    "next_action": next_action,
                    "notes": notes,
                })
                st.success("✓ Governance decision saved for this session.")

            if st.session_state.get(f"governance_saved_{selected_name}") or existing:
                saved = st.session_state.get(f"governance_{selected_name}", existing)
                st.markdown(
                    f'''
                    <div class="governance-summary">
                      <div class="summary-item"><div class="micro-label">Decision</div><div class="summary-value">{esc(saved.get("decision", "Not yet reviewed"))}</div></div>
                      <div class="summary-item"><div class="micro-label">Owner</div><div class="summary-value">{esc(saved.get("owner", "—"))}</div></div>
                      <div class="summary-item"><div class="micro-label">DQ rule</div><div class="summary-value">{esc(saved.get("data_quality_rule", "TBD"))}</div></div>
                      <div class="summary-item"><div class="micro-label">Next action</div><div class="summary-value">{esc(saved.get("next_action", "—"))}</div></div>
                    </div>
                    ''', unsafe_allow_html=True
                )

    # =====================================================
    # EXPORT
    # =====================================================

    st.markdown('<div class="section-head"><div><div class="section-title">4. Governance register</div><div class="section-caption">Export the evidence, validation and human decisions as a working governance register.</div></div></div>', unsafe_allow_html=True)

    export_rows = []
    for validation in validation_list:
        candidate = candidate_map.get(validation.name)
        if candidate is None:
            continue
        governance = st.session_state.get(f"governance_{candidate.name}", {})
        export_rows.append({
            "CDE": candidate.name,
            "Criticality": candidate.criticality,
            "Criteria": "; ".join(validation.corrected_criteria or []),
            "Validation Status": "Supported" if validation.supported else "Requires Review",
            "Source": candidate.source,
            "Page": candidate.page,
            "Evidence": candidate.evidence,
            "AI Reason": validation.corrected_reason,
            "Governance Decision": governance.get("decision", "Not yet reviewed"),
            "Data Steward": governance.get("owner", ""),
            "Business Domain": governance.get("domain", ""),
            "Source System": governance.get("source_system", ""),
            "DQ Rule Required": governance.get("data_quality_rule", "TBD"),
            "Proposed DQ Rule": governance.get("proposed_dq_rule", ""),
            "Next Action": governance.get("next_action", ""),
            "Governance Notes": governance.get("notes", ""),
        })

    if export_rows:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=export_rows[0].keys())
        writer.writeheader()
        writer.writerows(export_rows)
        st.download_button(
            "Download governance register (CSV)",
            data=csv_buffer.getvalue(),
            file_name="cde_governance_register.csv",
            mime="text/csv",
            width="stretch",
        )

    st.markdown('<div style="height:1.5rem"></div><div style="color:#475569;font-size:.7rem;text-align:center;letter-spacing:.04em">AI-assisted discovery • Evidence-based validation • Human governance accountability</div>', unsafe_allow_html=True)