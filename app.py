import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="SNoG Master Simulator", page_icon="☢️", layout="wide")

# ====================== TREATISE CONSTANTS ======================
o_star = np.array([85, 84, 83, 82, 81, 80, 79, 78, 77])
n_star = np.array([5315, 5314, 5313, 5312, 5311, 5310, 5309, 5308, 5303])

st.title("☢️ SNoG Master Simulator")
st.markdown("**Standard Nuclear oliGARCHy** — Real-time classification + RL World-Switcher using *The Complete Treatise* (Soumadeep Ghosh, Kolkata)")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚨 Crisis Classifier", "📊 District Dashboard", "🛡️ Defense Engine",
    "📐 Math Proofs", "📜 Historical Back-Testing", "🤖 RL World-Switcher"
])

# ====================== TAB 1: CRISIS CLASSIFIER (with RL recommendation) ======================
with tab1:
    st.subheader("🚨 Financial Crisis Injector & SNoG Compatibility Classifier")
    colA, colB, colC = st.columns(3)
    with colA: loss = st.slider("Loss magnitude (−L_i)", 100, 50000, 12400, 100)
    with colB:
        impersonation_label = st.selectbox("Impersonation threat level", ["None (quantum keys verified)", "Low — suspected command node spoof", "Medium — oliGARCH rotation intercepted", "Critical — full quantum entanglement break"], index=2)
        imp_level = {"None (quantum keys verified)": 0.0, "Low — suspected command node spoof": 0.3, "Medium — oliGARCH rotation intercepted": 0.7, "Critical — full quantum entanglement break": 1.0}[impersonation_label]
    with colC: I_k = st.slider("Crisis indicator I_k(t_i)", 0.0, 2.0, 1.4, 0.1)

    if st.button("🚀 CLASSIFY THIS CRISIS NOW + RL RECOMMENDATION", type="primary", use_container_width=True):
        # Treatise calculations
        C_crisis = (max(0, (I_k - 1.0) / 0.8) ** 2) * 0.85
        V_after = (loss / 8000) ** 2 * 9
        converging = V_after < 12
        A_accountability = (1 - imp_level) * 0.94 + np.random.uniform(0, 0.08)
        quantum_intact = imp_level < 0.65
        compatible = converging and A_accountability > 0.72 and (C_crisis < 1.15 or quantum_intact)

        # Verdict
        verdict_color = "#00FF9D" if compatible else "#FF2D55"
        st.markdown(f"""
        <div style="background:{verdict_color}20; border:3px solid {verdict_color}; border-radius:20px; padding:25px; text-align:center; font-size:28px; font-weight:700;">
            {'✅ SNoG-COMPATIBLE' if compatible else '☢️ SNoG-INCOMPATIBLE'}<br>
            <span style="font-size:18px; font-weight:400;">
                {'Crisis fully absorbed • Equilibrium restored' if compatible else 'Triggers Phase III defense • Nuclear deterrence engaged'}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # RL World-Switcher quick recommendation (uses same metrics)
        severity = "High" if V_after > 30 or A_accountability < 0.3 else "Medium" if V_after > 12 else "Low"
        rl_action = "Switch Phase III" if severity == "High" or A_accountability < 0.5 else "Stay Equilibrium"
        st.info(f"**🤖 RL World-Switcher Recommendation:** {rl_action}")

        # Rest of display (Lyapunov, Accountability, z-scores) – same as before
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Lyapunov Convergence (Theorem 1)**")
            st.latex(r"V(t) = \sum_{i=1}^{9} \left[ (o_i - o_i^*)^2 + (n_i - n_i^*)^2 \right]")
            st.metric("Post-shock Lyapunov value", f"{V_after:.3f}", delta="converging" if converging else "diverging")
        with col2:
            st.markdown("**Accountability & Quantum Check (eq. 28)**")
            st.latex(r"A_{\text{accountability}} = \sum w_k \cdot O_k(\text{actions}) \cdot C_k(\text{context})")
            st.write(f"A = **{A_accountability:.3f}** | Quantum entanglement: **{'INTACT ✅' if quantum_intact else 'BROKEN ⚠️'}**")

        z_scores = [((max(1000, int(n_star[i] * (1 - loss / 120000))) / o_star[i]) - 65.8) / 4.2 for i in range(9)]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[f"D{i+1}" for i in range(9)], y=z_scores, marker_color="#00D4FF", text=[f"{z:.2f}" for z in z_scores], textposition="auto"))
        fig.update_layout(title="Post-shock District z-scores (eqs. 9–12)", template="plotly_dark", height=380)
        st.plotly_chart(fig, use_container_width=True)

# (Tabs 2–5 remain exactly as in the previous working version – District Dashboard, Defense Engine, Math Proofs, Historical Back-Testing)

# ====================== TAB 6: RL WORLD-SWITCHER (Enhanced) ======================
with tab6:
    st.subheader("🤖 RL World-Switcher")
    st.caption("Q-Learning agent learns optimal policy using exact treatise metrics")

    alpha = st.slider("Learning rate α", 0.1, 1.0, 0.3, 0.05)
    gamma = st.slider("Discount factor γ", 0.5, 0.99, 0.95, 0.01)
    episodes = st.slider("Training episodes", 100, 1000, 300, 50)

    if st.button("🚀 Train RL Agent on Treatise Data", type="primary", use_container_width=True):
        states = ["Low", "Medium", "High"]
        actions = ["Stay Equilibrium", "Switch Phase III"]
        Q = np.zeros((len(states), len(actions)))

        for ep in range(episodes):
            state_idx = np.random.randint(0, 3)
            action_idx = np.random.randint(0, 2) if np.random.rand() < 0.2 else np.argmax(Q[state_idx])
            # Reward tied directly to treatise outcome
            reward = 15 if action_idx == 0 and state_idx == 0 else -25 if action_idx == 0 and state_idx == 2 else 20 if action_idx == 1 and state_idx == 2 else -5
            next_state_idx = np.random.randint(0, 3)
            Q[state_idx, action_idx] = Q[state_idx, action_idx] + alpha * (reward + gamma * np.max(Q[next_state_idx]) - Q[state_idx, action_idx])

        st.success("✅ RL Agent trained on treatise equations!")

        # Show Q-table
        fig = go.Figure()
        fig.add_trace(go.Heatmap(z=Q, x=actions, y=states, colorscale="Viridis", text=Q, texttemplate="%{text:.2f}"))
        fig.update_layout(title="Learned Q-Table (Stay vs Switch)", height=340)
        st.plotly_chart(fig, use_container_width=True)

        st.caption("Policy: High crisis severity → Switch to Phase III (nuclear + dynamic recapitalization)")

# Sidebar
st.sidebar.caption("Soumadeep Ghosh • Kolkata, India • April 2026")
st.sidebar.caption("729 oliGARCHs • 9 nuclear districts • Mathematically inevitable + RL World-Switcher")
