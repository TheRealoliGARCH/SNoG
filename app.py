import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="SNoG Master Simulator", page_icon="☢️", layout="wide")

# ====================== TREATISE CONSTANTS ======================
o_star = np.array([85, 84, 83, 82, 81, 80, 79, 78, 77])
n_star = np.array([5315, 5314, 5313, 5312, 5311, 5310, 5309, 5308, 5303])
total_oligarchs = 729
total_population = 48524
non_oligarchs = 47795

st.title("☢️ SNoG Master Simulator")
st.markdown("**Standard Nuclear oliGARCHy** • Real-time crisis classification using *The Complete Treatise* (Soumadeep Ghosh, Kolkata)")

tab1, tab2, tab3, tab4 = st.tabs(["🚨 Crisis Classifier", "📊 District Dashboard", "🛡️ Defense Engine", "📐 Math Proofs"])

# ====================== TAB 1: CRISIS CLASSIFIER ======================
with tab1:
    st.subheader("🚨 Financial Crisis Injector & SNoG Compatibility Classifier")
    colA, colB, colC = st.columns(3)
    
    with colA:
        loss = st.slider("Loss magnitude (−L_i)", min_value=100, max_value=50000, value=12400, step=100)
    with colB:
        impersonation = st.selectbox("Impersonation threat level", 
            ["None (quantum keys verified)", "Low — suspected command node spoof", "Medium — oliGARCH rotation intercepted", "Critical — full quantum entanglement break"],
            index=2)
        imp_level = {"None (quantum keys verified)": 0.0, "Low — suspected command node spoof": 0.3,
                     "Medium — oliGARCH rotation intercepted": 0.7, "Critical — full quantum entanglement break": 1.0}[impersonation]
    with colC:
        I_k = st.slider("Crisis indicator I_k(t_i)", min_value=0.0, max_value=2.0, value=1.4, step=0.1)

    if st.button("🚀 CLASSIFY THIS CRISIS NOW", type="primary", use_container_width=True):
        # Crisis detection (Treatise eq. 25)
        C_crisis = (max(0, (I_k - 1.0) / 0.8) ** 2) * 0.85
        
        # Lyapunov V(t) post-shock (Treatise eqs. 29-30)
        V_after = (loss / 8000) ** 2 * 9
        converging = V_after < 12
        
        # Accountability + Quantum check (eq. 28)
        A_accountability = (1 - imp_level) * 0.94 + np.random.uniform(0, 0.08)
        quantum_intact = imp_level < 0.65
        
        # Final verdict
        compatible = converging and A_accountability > 0.72 and (C_crisis < 1.15 or quantum_intact)
        
        verdict_color = "#00FF9D" if compatible else "#FF2D55"
        st.markdown(f"""
        

            {'✅ SNoG-COMPATIBLE' if compatible else '☢️ SNoG-INCOMPATIBLE'}

            
                {'Crisis fully absorbed • Returns to equilibrium in finite time' if compatible else 'Triggers Phase III defense • Nuclear deterrence engaged'}
            
        

        """, unsafe_allow_html=True)
        
        # Results columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Lyapunov Convergence (Theorem 1)**")
            st.latex(r"V(t) = \sum_{i=1}^{9} \left[ (o_i - o_i^*)^2 + (n_i - n_i^*)^2 \right]")
            st.write(f"dV/dt ≈ **{'NEGATIVE → converging' if converging else 'POSITIVE → diverging'}**")
            st.metric("Post-shock Lyapunov value", f"{V_after:.3f}")
        
        with col2:
            st.markdown("**Accountability & Quantum Check (eq. 28)**")
            st.latex(r"A_{\text{accountability}} = \sum w_k \cdot O_k(\text{actions}) \cdot C_k(\text{context})")
            st.write(f"A = **{A_accountability:.3f}** | Quantum entanglement: **{'INTACT ✅' if quantum_intact else 'BROKEN ⚠️'}**")
        
        # District z-scores chart
        st.subheader("Post-shock District Responsibility z-scores (eqs. 9–12)")
        z_scores = []
        for i in range(9):
            ni_post = max(1000, int(n_star[i] * (1 - loss / 120000)))
            r_i = ni_post / o_star[i]
            mu_r = 65.8
            sigma_r = 4.2
            z = (r_i - mu_r) / sigma_r
            z_scores.append(z)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[f"D{i+1}" for i in range(9)], y=z_scores, marker_color="#00D4FF", text=[f"{z:.2f}" for z in z_scores], textposition="auto"))
        fig.update_layout(title="District z-scores after −L_i shock", template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Export CSV
        results_df = pd.DataFrame({
            "timestamp": [datetime.now()],
            "loss_Li": [loss],
            "impersonation_level": [imp_level],
            "I_k": [I_k],
            "C_crisis": [C_crisis],
            "V_after": [V_after],
            "A_accountability": [A_accountability],
            "compatible": [compatible]
        })
        st.download_button("📥 Export this simulation as CSV", results_df.to_csv(index=False), f"snog_crisis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

# ====================== TAB 2: DISTRICT DASHBOARD ======================
with tab2:
    st.subheader("📊 Live 9-District Dashboard (Treatise pp. 4 & 7)")
    st.caption("Exact distribution: 729 oliGARCHs • 47,795 non-oliGARCHs across 9 nuclear-capable districts")
    
    df = pd.DataFrame({
        "District": [f"D{i+1}" for i in range(9)],
        "oliGARCHs": o_star,
        "non_oliGARCHs": n_star,
        "responsibility_r_i": n_star / o_star
    })
    st.dataframe(df.style.format({"responsibility_r_i": "{:.2f}"}), use_container_width=True, hide_index=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["District"], y=df["oliGARCHs"], name="oliGARCHs", marker_color="#FF2D55"))
    fig.add_trace(go.Bar(x=df["District"], y=df["non_oliGARCHs"], name="non-oliGARCHs", marker_color="#00D4FF"))
    fig.update_layout(title="Nuclear-Capable District Populations", barmode="group", template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

# ====================== TAB 3: DEFENSE ENGINE ======================
with tab3:
    st.subheader("🛡️ Augmented Defense Framework (Defensive Rating 9.95/10)")
    st.markdown("**Multi-Tier Redundancy • Quantum-Secured Communications • Dynamic Recapitalization** (Sections 6 & 11)")
    
    rating = 9.95
    st.metric("Current Defensive Rating", f"{rating}/10", "Maximum possible under treatise")
    
    st.progress(rating / 10)
    
    st.write("All enhancements active:")
    cols = st.columns(3)
    cols[0].success("✅ Quantum key distribution (eq. 20)")
    cols[1].success("✅ oliGARCH rotation protocol (eq. 19)")
    cols[2].success("✅ Dynamic recapitalization (eq. 22-23)")

# ====================== TAB 4: MATH PROOFS ======================
with tab4:
    st.subheader("📐 Mathematical Proofs of Inevitability (Section 10)")
    st.latex(r"""
    V(t) = \sum_{i=1}^{9} \left[ (o_i - o_i^*)^2 + (n_i - n_i^*)^2 \right] \quad \text{(Lyapunov function)}
    """)
    st.latex(r"\frac{dV}{dt} < 0 \quad \text{whenever } V > 0 \quad \Rightarrow \text{ convergence to Standard Nuclear oliGARCHy}")
    st.markdown("**Theorem 1**: Any system under the oliGARCH differential equation converges to exactly **9 districts, 729 oliGARCHs, 48,524 total population**.")
    st.caption("Source: *The Complete Treatise on the Standard Nuclear oliGARCHy*, Soumadeep Ghosh, Kolkata, 2025")

st.sidebar.markdown("---")
st.sidebar.caption("729 oliGARCHs • 9 nuclear districts • Mathematically inevitable")
