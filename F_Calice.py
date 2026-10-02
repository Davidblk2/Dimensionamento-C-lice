import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines

# Configuração da fonte global para Arial
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Configuração inicial da página
st.set_page_config(page_title="Cálices de Fundação", layout="wide")

st.title("🏗 Dimensionamento de Cálices de Fundação")
st.write("Motor de Cálculo baseado na ABNT NBR 9062 e nos modelos de bielas e tirantes (Canha, 2004 / Campos, 2010).")
st.divider()

# ==========================================
# 2. Interface de Entrada de Dados
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. Esforços Solicitantes")
    nk = st.number_input("Força Normal - Nk (kN):", value=70.61 / 1.4, step=10.0, help="Valor característico")
    mk = st.number_input("Momento Fletor - Mk (kN.m):", value=73.63 / 1.4, step=5.0, help="Valor característico")
    vk = st.number_input("Força Cortante - Vk (kN):", value=29.45 / 1.4, step=5.0, help="Valor característico")
    gamma_f = st.number_input("Coeficiente de Majoração (γf):", value=1.4, step=0.1)

with col2:
    st.header("2. Geometria (cm)")
    h_pilar = st.number_input("Dim. Pilar (Direção do Momento) - h:", value=55.0, step=5.0)
    b_pilar = st.number_input("Dim. Transversal do Pilar - b:", value=55.0, step=5.0)
    l_emb = st.number_input("Comprimento de Embutimento - Lemb:", value=100.0, step=5.0)
    h_c = st.number_input("Espessura da Parede do Colarinho - hc:", value=25.0, step=1.0)
    folga = st.number_input("Folga da Junta / Graute - f:", value=5.0, step=1.0)

with col3:
    st.header("3. Materiais e Interface")
    fck_calice = st.number_input("fck do Cálice (MPa):", value=30.0, step=5.0)
    fyk = st.number_input("fyk do Aço (MPa):", value=500.0, step=0.0)
    
    interface = st.radio(
        "Condição da Interface Pilar-Cálice:",
        ["Lisa (Concreto Simples - Padrão)", "Rugosa (Com ranhuras e graute)"]
    )
    
    # Dimensões derivadas
    h_int = h_pilar + 2 * folga
    b_int = b_pilar + 2 * folga
    h_ext = h_int + 2 * h_c
    b_ext = b_int + 2 * h_c
    h_base = max(40.0, l_emb * 0.4)

st.divider()

if h_ext <= h_int or b_ext <= b_int:
    st.error("ERRO GEOMÉTRICO: A espessura da parede (hc) deve ser suficiente para conter o pilar mais as folgas.")
    st.stop()

# ==========================================
# 3. VISUALIZAÇÃO GRÁFICA PARAMÉTRICA (CAD STYLE)
# ==========================================
st.header("📐 Esquema Geométrico Paramétrico")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4))
fig.tight_layout(pad=2.0)

cor_concreto = '#E5E7EB'
cor_pilar = '#9CA3AF'
cor_graute = '#F9FAFB'
hachura_pilar = '///'

def desenhar_cota_tecnica(ax, x1, y1, x2, y2, simbolo, offset_texto=(0, 0), rotacao=0):
    ax.annotate('', xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', color='black', lw=0.8, shrinkA=0, shrinkB=0))
    xm = (x1 + x2) / 2 + offset_texto[0]
    ym = (y1 + y2) / 2 + offset_texto[1]
    ax.text(xm, ym, simbolo, ha='center', va='center', color='black',
            fontsize=8, fontweight='bold', rotation=rotacao,
            bbox=dict(facecolor='white', edgecolor='none', pad=1.0))

# PLANTA BAIXA
ax1.add_patch(patches.Rectangle((-h_ext/2, -b_ext/2), h_ext, b_ext, facecolor=cor_concreto, edgecolor='black', lw=1.0))
ax1.add_patch(patches.Rectangle((-h_int/2, -b_int/2), h_int, b_int, facecolor=cor_graute, edgecolor='black', lw=0.8, linestyle=':'))
ax1.add_patch(patches.Rectangle((-h_pilar/2, -b_pilar/2), h_pilar, b_pilar, facecolor=cor_pilar, edgecolor='black', hatch=hachura_pilar, lw=1.0))

desenhar_cota_tecnica(ax1, -h_ext/2, b_ext/2 + 14, h_ext/2, b_ext/2 + 14, "A")
desenhar_cota_tecnica(ax1, -h_ext/2, -b_ext/2 - 14, -h_int/2, -b_ext/2 - 14, "hc")
desenhar_cota_tecnica(ax1, -h_pilar/2, -b_ext/2 - 14, h_pilar/2, -b_ext/2 - 14, "h")
desenhar_cota_tecnica(ax1, h_int/2, -b_ext/2 - 14, h_ext/2, -b_ext/2 - 14, "hc")

rotulo_vert_pilar = "h" if h_pilar == b_pilar else "b"
desenhar_cota_tecnica(ax1, h_ext/2 + 14, -b_ext/2, h_ext/2 + 14, b_ext/2, "B", rotacao=-90)
desenhar_cota_tecnica(ax1, -h_ext/2 - 14, -b_ext/2, -h_ext/2 - 14, -b_int/2, "hc", rotacao=90)
desenhar_cota_tecnica(ax1, -h_ext/2 - 14, -b_pilar/2, -h_ext/2 - 14, b_pilar/2, rotulo_vert_pilar, rotacao=90)
desenhar_cota_tecnica(ax1, -h_ext/2 - 14, b_int/2, -h_ext/2 - 14, b_ext/2, "hc", rotacao=90)

ax1.set_xlim(-h_ext/2 - 30, h_ext/2 + 30)
ax1.set_ylim(-b_ext/2 - 26, b_ext/2 + 25)
ax1.set_aspect('equal')
ax1.set_title("PLANTA BAIXA", fontsize=9, fontweight='bold', pad=6)
ax1.axis('off')

# CORTE TRANSVERSAL
ax2.add_patch(patches.Rectangle((-h_ext/2, -h_base), h_ext, h_base, facecolor=cor_concreto, edgecolor='black', lw=1.0))
ax2.add_patch(patches.Rectangle((-h_ext/2, 0), h_c, l_emb + folga, facecolor=cor_concreto, edgecolor='black', lw=1.0))
ax2.add_patch(patches.Rectangle((h_int/2, 0), h_c, l_emb + folga, facecolor=cor_concreto, edgecolor='black', lw=1.0))

ax2.add_patch(patches.Rectangle((-h_int/2, 0), h_int, folga, facecolor=cor_graute, edgecolor='black', lw=0.6))
ax2.add_patch(patches.Rectangle((-h_int/2, folga), folga, l_emb, facecolor=cor_graute, edgecolor='black', lw=0.6))
ax2.add_patch(patches.Rectangle((h_pilar/2, folga), folga, l_emb, facecolor=cor_graute, edgecolor='black', lw=0.6))

altura_ext_topo = 35.0
ax2.add_patch(patches.Rectangle((-h_pilar/2, folga), h_pilar, l_emb + altura_ext_topo, facecolor=cor_pilar, edgecolor='black', hatch=hachura_pilar, lw=1.0))

desenhar_cota_tecnica(ax2, -h_ext/2 - 16, folga, -h_ext/2 - 16, folga + l_emb, "Lemb", rotacao=90)
desenhar_cota_tecnica(ax2, -h_ext/2 - 16, 0, -h_ext/2 - 16, folga, "f", rotacao=90)
desenhar_cota_tecnica(ax2, h_ext/2 + 16, -h_base, h_ext/2 + 16, 0, "Hbase", rotacao=-90)

desenhar_cota_tecnica(ax2, -h_ext/2, folga + l_emb + 12, -h_int/2, folga + l_emb + 12, "hc")
desenhar_cota_tecnica(ax2, -h_pilar/2, folga + l_emb + 12, h_pilar/2, folga + l_emb + 12, "h")
desenhar_cota_tecnica(ax2, h_int/2, folga + l_emb + 12, h_ext/2, folga + l_emb + 12, "hc")

ax2.set_xlim(-h_ext/2 - 35, h_ext/2 + 35)
ax2.set_ylim(-h_base - 10, folga + l_emb + altura_ext_topo + 10)
ax2.set_aspect('equal')
ax2.set_title("CORTE TRANSVERSAL", fontsize=9, fontweight='bold', pad=6)
ax2.axis('off')

st.pyplot(fig, use_container_width=False)
plt.close(fig)

st.divider()

# ==========================================
# 4. Parâmetros Avançados e Execução
# ==========================================
st.header("⚙️ Parâmetros Avançados do Modelo")
editar_parametros = st.checkbox("Habilitar edição manual dos parâmetros de cálculo (y, y', enb)")

y_padrao = l_emb / 6.0
y_linha_padrao = l_emb / 10.0
enb_padrao = h_pilar / 4.0

if editar_parametros:
    col_a, col_b, col_c = st.columns(3)
    y_calc = col_a.number_input("Distância pressão superior - y (cm):", value=float(y_padrao))
    y_linha_calc = col_b.number_input("Distância pressão inferior - y' (cm):", value=float(y_linha_padrao))
    enb_calc = col_c.number_input("Excentricidade na base - enb (cm):", value=float(enb_padrao))
else:
    y_calc = y_padrao
    y_linha_calc = y_linha_padrao
    enb_calc = enb_padrao
    st.info(f"Modo Automático Ativo: y = {y_calc:.2f} cm | y' = {y_linha_calc:.2f} cm | enb = {enb_calc:.2f} cm")

st.divider()

if 'calculado' not in st.session_state:
    st.session_state.calculado = False

if st.button("Calcular Esforços e Armaduras", type="primary"):
    st.session_state.calculado = True

# ==========================================
# 5. MOTOR DE CÁLCULO
# ==========================================
if st.session_state.calculado:
    
    nd = nk * gamma_f
    md = (mk * gamma_f) * 100.0
    vd = vk * gamma_f
    fcd = (fck_calice / 10.0) / 1.4      
    fyd = (fyk / 10.0) / 1.15             
    mu = 0.3 if "Lisa" in interface else 0.6
    
    termo_2_val = enb_calc + ((mu * y_linha_calc - (mu**2) * (0.5 * h_pilar + enb_calc)) / (1 + mu**2))
    termo_3_val = l_emb - ((y_linha_calc - mu * (0.5 * h_pilar + enb_calc)) / (1 + mu**2))
    numerador = md - (nd * termo_2_val) + (vd * termo_3_val)
    denominador = l_emb - y_calc - y_linha_calc + (mu * h_pilar)
    
    h_sup_d = numerador / denominador
    termo_inf = (mu * nd + vd) / (1 + mu**2)
    h_inf_d = h_sup_d - termo_inf
    
    denominador_beta = 0.85 * h_ext - (h_c / 2.0)
    tan_beta = (l_emb - y_calc) / denominador_beta
    
    if tan_beta > 0.93: tipo_consolo = "Consolo Longo (Flexão Pura)"
    elif tan_beta > 0.5: tipo_consolo = "Consolo Curto (Modelo de Biela e Tirante)"
    else: tipo_consolo = "Consolo Muito Curto (Atrito-Cisalhamento)"
        
    l_dist_sup_cm = l_emb / 3.0
    l_dist_inf_cm = 2.0 * l_emb / 3.0
    l_dist_sup_m = l_dist_sup_cm / 100.0
    l_dist_inf_m = l_dist_inf_cm / 100.0
    
    as_hp_calc = h_sup_d / (2 * fyd)
    as_h_min_sup = 0.0015 * (h_c * l_dist_sup_cm)
    as_hp_adot = max(as_hp_calc, as_h_min_sup)
    as_hp_m = as_hp_adot / l_dist_sup_m
    
    as_hsec_calc = 0.5 * as_hp_adot
    as_h_min_inf = 0.0015 * (h_c * l_dist_inf_cm)
    as_hsec_adot = max(as_hsec_calc, as_h_min_inf)
    as_hsec_m = as_hsec_adot / l_dist_inf_m
    
    c_c = h_sup_d / 2.0
    p_a = l_emb / 10.0
    m_d_canto = c_c * (l_emb - p_a) 
    d_util = b_ext - 4.0
    k_flex = m_d_canto / (h_c * (d_util**2) * fcd)
    
    if tipo_consolo.startswith("Consolo Longo"):
        z_braco = d_util * (1 - 0.4 * (1 - np.sqrt(1 - 2 * k_flex))) if 1 - 2 * k_flex > 0 else 0.8 * d_util
        as_vp_calc = m_d_canto / (z_braco * fyd)
    elif tipo_consolo.startswith("Consolo Curto"):
        as_vp_calc = (c_c / tan_beta) / fyd
    else:
        as_vp_calc = c_c / (1.4 * fyd * mu)
        
    as_vp_min = 0.0015 * (h_c * b_ext)
    as_vp_final = max(as_vp_calc, as_vp_min)
    
    as_vs_calc = 0.40 * as_vp_final
    as_vs_min = 0.0010 * (h_c * b_ext)
    as_vs_final = max(as_vs_calc, as_vs_min)
    dim_min_int = min(h_int, b_int)
    as_vs_m = as_vs_final / (dim_min_int / 100.0)

    # ==========================================
    # 6. SELEÇÃO INTERATIVA DE ARMADURAS 
    # ==========================================
    st.markdown("### 📋 Resumo Executivo e Escolha de Armaduras")
    
    def gerar_opcoes_distribuida(as_req):
        bitolas = [5.0, 6.3, 8.0, 10.0, 12.5, 16.0]
        opcoes = []
        for phi in bitolas:
            area_barra = (np.pi * (phi/10)**2) / 4
            s_calc = 100 * area_barra / as_req
            s_pratico = int(np.floor(s_calc))
            if s_pratico > 20: s_pratico = 20
            if s_pratico >= 5:
                as_disp = 100 * area_barra / s_pratico
                opcoes.append(f"Ø {phi:.1f} mm c/ {s_pratico} cm (As disp. = {as_disp:.2f} cm²/m)")
        if not opcoes: return ["Nenhuma bitola atende os limites. Aumente a seção."]
        return opcoes

    def gerar_opcoes_concentrada(as_req):
        bitolas = [10.0, 12.5, 16.0, 20.0, 25.0]
        opcoes = []
        for n_barras in [4, 6, 8, 10, 12]:
            for phi in bitolas:
                area_barra = (np.pi * (phi/10)**2) / 4
                as_disp = n_barras * area_barra
                if as_disp >= as_req:
                    opcoes.append(f"{n_barras} barras Ø {phi:.1f} mm (As disp. = {as_disp:.2f} cm²)")
        opcoes.sort(key=lambda x: float(x.split("= ")[1].split(" cm²")[0]))
        return opcoes[:8]

    with st.container(border=True):
        st.markdown("#### 🟦 1. Estribos Horizontais Principais ($A_{s,hp}$)")
        c1, c2 = st.columns([1, 2])
        c1.metric("As Calculado (Projeto)", f"{as_hp_m:.2f} cm²/m")
        adotado_hp = c2.selectbox("As Adotado:", gerar_opcoes_distribuida(as_hp_m), key="hp")

    with st.container(border=True):
        st.markdown("#### 🟦 2. Estribos Horizontais Secundários ($A_{s,h,sec}$)")
        c1, c2 = st.columns([1, 2])
        c1.metric("As Calculado (Projeto)", f"{as_hsec_m:.2f} cm²/m")
        adotado_hsec = c2.selectbox("As Adotado:", gerar_opcoes_distribuida(as_hsec_m), key="hsec")

    with st.container(border=True):
        st.markdown("#### 🟥 3. Armadura Vertical Principal ($A_{s,vp}$)")
        c1, c2 = st.columns([1, 2])
        c1.metric("As Calculado (Projeto)", f"{as_vp_final:.2f} cm² / canto")
        adotado_vp = c2.selectbox("As Adotado (Por Canto):", gerar_opcoes_concentrada(as_vp_final), key="vp")

    with st.container(border=True):
        st.markdown("#### 🟧 4. Armadura Vertical Secundária ($A_{s,vs}$)")
        c1, c2 = st.columns([1, 2])
        c1.metric("As Calculado (Por Face)", f"{as_vs_m:.2f} cm²/m")
        adotado_vs = c2.selectbox("As Adotado:", gerar_opcoes_distribuida(as_vs_m), key="vs")
        
    st.caption(f"*Classificação estrutural do cálice: **{tipo_consolo}***")

    # ==========================================
    # PARSING DOS VALORES ESCOLHIDOS PARA O GRÁFICO
    # ==========================================
    try: espac_vs_real = float(adotado_vs.split("c/ ")[1].split(" ")[0])
    except: espac_vs_real = 10.0
    
    try: phi_vs_real = adotado_vs.split("Ø ")[1].split(" ")[0]
    except: phi_vs_real = "8.0"

    try: 
        n_vp_real = adotado_vp.split(" ")[0]
        phi_vp_real = adotado_vp.split("Ø ")[1].split(" ")[0]
    except: 
        n_vp_real, phi_vp_real = "4", "10.0"
        
    try: phi_hp_real = adotado_hp.split("Ø ")[1].split(" ")[0]
    except: phi_hp_real = "8.0"

    # ==========================================
    # 7. APRESENTAÇÃO COM ABAS: GRÁFICOS DINÂMICOS E MEMÓRIA DE CÁLCULO
    # ==========================================
    st.header("📊 Detalhamento e Memória de Cálculo")
    
    aba_resumo, aba_formulas = st.tabs(["📊 Planta de Armaduras (CAD)", "📝 Memória de Cálculo Passo-a-Passo"])
    
    with aba_resumo:
        fig_res, (ax_esf, ax_arm) = plt.subplots(1, 2, figsize=(9.5, 4.5))
        fig_res.tight_layout(pad=2.0)

        c_estribo = '#2563EB'
        c_vp = '#DC2626'
        c_vs = '#D97706'

        # --- 1. GRÁFICO DE ESFORÇOS (CORTE) ---
        ax_esf.add_patch(patches.Rectangle((-h_ext/2, folga), h_c, l_emb, facecolor=cor_concreto, edgecolor='black', lw=1.0))
        ax_esf.add_patch(patches.Rectangle((h_int/2, folga), h_c, l_emb, facecolor=cor_concreto, edgecolor='black', lw=1.0))
        
        # Pilar reto no topo, saindo 20cm acima da folga
        altura_pilar_esf = 20.0 
        y_top_esf = folga - altura_pilar_esf
        ax_esf.add_patch(patches.Rectangle((-h_pilar/2, y_top_esf), h_pilar, l_emb + altura_pilar_esf, facecolor=cor_pilar, edgecolor='black', hatch=hachura_pilar))
        
        ax_esf.invert_yaxis()

        # Nd (Seta vertical descendo até o topo reto do pilar, texto acima)
        ax_esf.annotate('', xy=(0, y_top_esf), xytext=(0, y_top_esf - 25), arrowprops=dict(facecolor='black', shrink=0, width=1.5, headwidth=5))
        ax_esf.text(0, y_top_esf - 30, f"Nd={nd:.0f}kN", fontweight='bold', fontsize=8, ha='center', va='bottom')
        
        # Vd (Seta horizontal apontando para a face esquerda do pilar, logo acima do cálice)
        y_lat = folga - 10.0
        ax_esf.annotate('', xy=(-h_pilar/2, y_lat), xytext=(-h_pilar/2 - 30, y_lat), arrowprops=dict(facecolor='black', shrink=0, width=1.5, headwidth=5))
        ax_esf.text(-h_pilar/2 - 35, y_lat, f"Vd={vd:.0f}kN", fontweight='bold', fontsize=8, ha='right', va='center')
        
        # Md (Seta em arco rotacionando ao lado da face direita do pilar)
        ax_esf.annotate('', xy=(h_pilar/2, y_lat), xytext=(h_pilar/2 + 30, y_lat), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.5", color='black', lw=1.5))
        ax_esf.text(h_pilar/2 + 35, y_lat, f"Md={md/100:.0f}kNm", fontweight='bold', fontsize=8, ha='left', va='center')

        # Pressões Horizontais
        cota_y_sup = folga + y_calc
        cota_y_inf = folga + l_emb - y_linha_calc
        ax_esf.annotate('', xy=(-h_int/2, cota_y_sup), xytext=(-h_ext/2 - 30, cota_y_sup), arrowprops=dict(facecolor='red', edgecolor='red', shrink=0, width=2.0))
        ax_esf.text(-h_ext/2 - 35, cota_y_sup - 5, f"Hsup,d\n{h_sup_d:.1f} kN", color='red', fontweight='bold', ha='right', va='center', fontsize=8)
        ax_esf.annotate('', xy=(h_int/2, cota_y_inf), xytext=(h_ext/2 + 30, cota_y_inf), arrowprops=dict(facecolor='blue', edgecolor='blue', shrink=0, width=2.0))
        ax_esf.text(h_ext/2 + 35, cota_y_inf - 5, f"Hinf,d\n{h_inf_d:.1f} kN", color='blue', fontweight='bold', ha='left', va='center', fontsize=8)

        desenhar_cota_tecnica(ax_esf, -h_ext/2 - 10, folga, -h_ext/2 - 10, folga + l_dist_sup_cm, f"1/3 Lemb", rotacao=90)
        desenhar_cota_tecnica(ax_esf, -h_ext/2 - 10, folga + l_dist_sup_cm, -h_ext/2 - 10, folga + l_emb, f"2/3 Lemb", rotacao=90)

        # Limite Y ajustado
        ax_esf.set_xlim(-h_ext/2 - 80, h_ext/2 + 80)
        ax_esf.set_ylim(folga + l_emb + 20, y_top_esf - 40)
        ax_esf.axis('off')
        ax_esf.set_title("ESFORÇOS E DISTRIBUIÇÃO", fontweight='bold', pad=10, fontsize=9)

        # --- 2. PLANTA DE ARMADURAS DETALHADA COM COTAS (CAD) ---
        ax_arm.add_patch(patches.Rectangle((-h_ext/2, -b_ext/2), h_ext, b_ext, facecolor=cor_concreto, edgecolor='black', lw=1.0))
        ax_arm.add_patch(patches.Rectangle((-h_int/2, -b_int/2), h_int, b_int, facecolor=cor_graute, edgecolor='black', lw=1.0, linestyle=':'))
        
        cobrimento = 4.0
        w_est_ext = h_ext - 2 * cobrimento
        h_est_ext = b_ext - 2 * cobrimento
        w_est_int = h_int + 2 * cobrimento
        h_est_int = b_int + 2 * cobrimento
        
        ax_arm.add_patch(patches.Rectangle((-w_est_ext/2, -h_est_ext/2), w_est_ext, h_est_ext, fill=False, edgecolor=c_estribo, lw=2.0, linestyle='-'))
        ax_arm.add_patch(patches.Rectangle((-w_est_int/2, -h_est_int/2), w_est_int, h_est_int, fill=False, edgecolor=c_estribo, lw=2.0, linestyle='-'))

        raio_bar = 1.1
        cobr_bar = raio_bar + 0.5
        
        # A. Armadura Vertical Principal (As,vp)
        for cx, cy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            p1_x, p1_y = cx * (w_est_ext/2 - cobr_bar), cy * (h_est_ext/2 - cobr_bar)
            p2_x, p2_y = cx * (w_est_int/2 + cobr_bar), p1_y
            p3_x, p3_y = p1_x, cy * (h_est_int/2 + cobr_bar)
            p4_x, p4_y = p2_x, p3_y
            for px, py in [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y), (p4_x, p4_y)]:
                ax_arm.add_patch(patches.Circle((px, py), raio_bar*1.2, facecolor=c_vp, edgecolor='black', lw=0.6, zorder=5))

        # B. Armadura Vertical Secundária (As,vs) usando o espaçamento real selecionado
        margem_x, margem_y = raio_bar + 4.0, raio_bar + 4.0
        comp_util_x = w_est_int - 2 * margem_x
        comp_util_y = h_est_int - 2 * margem_y
        
        x_sec = []
        if comp_util_x > 0:
            n_barras_x = max(2, int(comp_util_x / espac_vs_real) + 1)
            x_sec = np.linspace(-comp_util_x/2, comp_util_x/2, n_barras_x)
            for xs in x_sec:
                ax_arm.add_patch(patches.Circle((xs, h_est_ext/2 - cobr_bar), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))
                ax_arm.add_patch(patches.Circle((xs, -h_est_ext/2 + cobr_bar), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))
                ax_arm.add_patch(patches.Circle((xs, h_est_int/2 + cobr_bar), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))
                ax_arm.add_patch(patches.Circle((xs, -h_est_int/2 - cobr_bar), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))

        y_sec = []
        if comp_util_y > 0:
            n_barras_y = max(2, int(comp_util_y / espac_vs_real) + 1)
            y_sec = np.linspace(-comp_util_y/2, comp_util_y/2, n_barras_y)
            for ys in y_sec:
                ax_arm.add_patch(patches.Circle((-w_est_ext/2 + cobr_bar, ys), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))
                ax_arm.add_patch(patches.Circle((w_est_ext/2 - cobr_bar, ys), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))
                ax_arm.add_patch(patches.Circle((-w_est_int/2 - cobr_bar, ys), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))
                ax_arm.add_patch(patches.Circle((w_est_int/2 + cobr_bar, ys), raio_bar, facecolor=c_vs, edgecolor='black', zorder=4))

        # --- 3. INSERÇÃO DAS CHAMADAS DE PROJETO ---
        style_box = dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=0.5)
            
        ax_arm.annotate(f"VP: {n_vp_real} Nº Ø{phi_vp_real} mm\n(por canto)", 
                        xy=(w_est_ext/2 - cobr_bar, h_est_ext/2 - cobr_bar),
                        xytext=(w_est_ext/2 + 25, h_est_ext/2 + 25),
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=-90", color='black', lw=0.8),
                        fontsize=8, fontweight='bold', bbox=style_box, zorder=10)

        if len(y_sec) > 0:
            y_centro = y_sec[len(y_sec)//2]
            ax_arm.annotate(f"VS: Ø{phi_vs_real} mm c/{int(espac_vs_real)}", 
                            xy=(w_est_ext/2 - cobr_bar, y_centro),
                            xytext=(w_est_ext/2 + 35, y_centro),
                            arrowprops=dict(arrowstyle="->", color='black', lw=0.8),
                            fontsize=8, fontweight='bold', bbox=style_box, zorder=10)

        ax_arm.annotate(f"Estribo: Ø{phi_hp_real} mm", 
                        xy=(0, h_est_ext/2),
                        xytext=(0, h_est_ext/2 + 25),
                        arrowprops=dict(arrowstyle="->", color='black', lw=0.8),
                        fontsize=8, fontweight='bold', ha='center', bbox=style_box, zorder=10)

        # --- 4. LEGENDA TÉCNICA ABAIXO DA PLANTA ---
        leg_vp = mlines.Line2D([], [], color=c_vp, marker='o', linestyle='None', markersize=6, label='Armad. Principal (Canto)')
        leg_vs = mlines.Line2D([], [], color=c_vs, marker='o', linestyle='None', markersize=6, label='Armad. Secundária (Face)')
        leg_est = mlines.Line2D([], [], color=c_estribo, linewidth=1.5, label='Estribos')
        
        ax_arm.legend(handles=[leg_vp, leg_vs, leg_est], loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=7.5, frameon=False)

        ax_arm.set_xlim(-h_ext/2 - 50, h_ext/2 + 65)
        ax_arm.set_ylim(-b_ext/2 - 15, b_ext/2 + 45)
        ax_arm.set_aspect('equal')
        ax_arm.axis('off')
        ax_arm.set_title("PLANTA EXECUTIVA DE ARMADURAS", fontweight='bold', pad=10, fontsize=9)

        st.pyplot(fig_res, use_container_width=False)
        plt.close(fig_res)

    with aba_formulas:
        st.subheader("1. Majoração dos Esforços e Parâmetros")
        st.markdown(f"""
        * **Força Normal:** $N_d = N_k \\cdot \\gamma_f = {nk:.2f} \\times {gamma_f:.2f} = \\mathbf{{{nd:.2f}\\text{{ kN}}}}$
        * **Momento Fletor:** $M_d = M_k \\cdot \\gamma_f = {mk:.2f} \\times {gamma_f:.2f} = \\mathbf{{{md/100:.2f}\\text{{ kN}}\\cdot\\text{{m}}}} = \\mathbf{{{md:.1f}\\text{{ kN}}\\cdot\\text{{cm}}}}$
        * **Força Cortante:** $V_d = V_k \\cdot \\gamma_f = {vk:.2f} \\times {gamma_f:.2f} = \\mathbf{{{vd:.2f}\\text{{ kN}}}}$
        """)

        st.subheader("2. Esforços Horizontais de Contato")
        st.markdown(f"**Interface adotada:** {interface.split(' (')[0]} $\\rightarrow$ Coeficiente de atrito $\\mu = \\mathbf{{{mu}}}$")
        
        st.write("**A. Pressão Superior no Colarinho ($H_{sup,d}$):**")
        st.latex(r"H_{sup,d} = \frac{M_d - N_d \left[ e_{nb} + \frac{\mu\,y' - \mu^2(0{,}5h + e_{nb})}{1 + \mu^2} \right] + V_d \left[ L_{emb} - \frac{y' - \mu(0{,}5h + e_{nb})}{1 + \mu^2} \right]}{L_{emb} - y - y' + \mu\,h}")
        st.latex(rf"""H_{{sup,d}} = \frac{{{md:.1f} - {nd:.2f} \cdot {termo_2_val:.2f} + {vd:.2f} \cdot {termo_3_val:.2f}}}{{{denominador:.2f}}} = \mathbf{{{h_sup_d:.2f}\text{{ kN}}}}""")
        
        st.write("**B. Pressão Inferior no Fundo do Cálice ($H_{inf,d}$):**")
        st.latex(r"H_{inf,d} = H_{sup,d} - \frac{\mu\,N_d + V_d}{1 + \mu^2}")
        st.latex(rf"""H_{{inf,d}} = {h_sup_d:.2f} - {termo_inf:.2f} = \mathbf{{{h_inf_d:.2f}\text{{ kN}}}}""")

        st.subheader("3. Classificação Estrutural")
        st.latex(r"\tan\beta = \frac{L_{emb} - y}{0{,}85 \cdot h_{ext} - \frac{h_c}{2}}")
        st.latex(rf"""\tan\beta = \frac{{{l_emb:.1f} - {y_calc:.2f}}}{{0{{,}}85 \cdot {h_ext:.1f} - \frac{{{h_c:.1f}}}{{2}}}} = \mathbf{{{tan_beta:.3f}}} \rightarrow \text{{{tipo_consolo}}}""")

        st.subheader("4. Armaduras Horizontais")
        st.markdown(f"**Comprimentos de Distribuição:**")
        st.markdown(f"* Terço superior ($L_{{dist,sup}}$): $L_{{emb}} / 3 = {l_emb:.1f} / 3 = \\mathbf{{{l_dist_sup_cm:.1f}\\text{{ cm}}}}$")
        st.markdown(f"* Dois terços inferiores ($L_{{dist,inf}}$): $2 \\cdot L_{{emb}} / 3 = 2 \\cdot {l_emb:.1f} / 3 = \\mathbf{{{l_dist_inf_cm:.1f}\\text{{ cm}}}}$")
        
        st.write("---")
        st.write("**A. Estribos Horizontais Principais ($A_{s,hp}$):**")
        st.latex(r"A_{s,hp,calc} = \frac{H_{sup,d}}{2 \cdot f_{yd}} \quad \text{e} \quad A_{s,hp,min} = 0{,}0015 \cdot h_c \cdot L_{dist,sup}")
        st.latex(rf"""A_{{s,hp}} = \max\left( \frac{{{h_sup_d:.2f}}}{{2 \cdot {fyd:.2f}}} \, ; \ 0{{,}}0015 \cdot {h_c:.1f} \cdot {l_dist_sup_cm:.1f} \right)""")
        st.latex(rf"""A_{{s,hp}} = \max\left( {as_hp_calc:.2f} \, ; \ {as_h_min_sup:.2f} \right) = \mathbf{{{as_hp_adot:.2f}\text{{ cm}}^2}}""")
        st.markdown("**Taxa de armadura por metro (para detalhamento):**")
        st.latex(rf"""A_{{s,hp}} \ (\text{{Projeto}}) = \frac{{{as_hp_adot:.2f}}}{{{l_dist_sup_m:.2f}\text{{ m}}}} = \mathbf{{{as_hp_m:.2f}\text{{ cm}}^2/\text{{m}}}}""")

        st.write("---")
        st.write("**B. Estribos Horizontais Secundários ($A_{s,h,sec}$):**")
        st.latex(r"A_{s,hsec,calc} = 0{,}5 \cdot A_{s,hp} \quad \text{e} \quad A_{s,hsec,min} = 0{,}0015 \cdot h_c \cdot L_{dist,inf}")
        st.latex(rf"""A_{{s,h,sec}} = \max\left( 0{{,}}5 \cdot {as_hp_adot:.2f} \, ; \ 0{{,}}0015 \cdot {h_c:.1f} \cdot {l_dist_inf_cm:.1f} \right)""")
        st.latex(rf"""A_{{s,h,sec}} = \max\left( {as_hsec_calc:.2f} \, ; \ {as_h_min_inf:.2f} \right) = \mathbf{{{as_hsec_adot:.2f}\text{{ cm}}^2}}""")
        st.markdown("**Taxa de armadura por metro (para detalhamento):**")
        st.latex(rf"""A_{{s,h,sec}} \ (\text{{Projeto}}) = \frac{{{as_hsec_adot:.2f}}}{{{l_dist_inf_m:.2f}\text{{ m}}}} = \mathbf{{{as_hsec_m:.2f}\text{{ cm}}^2/\text{{m}}}}""")

        st.subheader("5. Armaduras Verticais")
        st.markdown("**Solicitações por Canto:**")
        st.latex(rf"""C_c = \frac{{H_{{sup,d}}}}{{2}} = \frac{{{h_sup_d:.2f}}}{{2}} = \mathbf{{{c_c:.2f}\text{{ kN}}}}""")
        st.latex(rf"""M_d \text{{ (canto)}} = C_c \cdot \left( L_{{emb}} - \frac{{L_{{emb}}}}{{10}} \right) = {c_c:.2f} \cdot \left( {l_emb:.1f} - {p_a:.1f} \right) = \mathbf{{{m_d_canto:.2f}\text{{ kN}}\cdot\text{{cm}}}}""")

        st.write("---")
        st.write("**A. Armadura Vertical Principal nos Cantos ($A_{s,vp}$):**")
        if tipo_consolo.startswith("Consolo Longo"):
            st.markdown(f"*Dimensionamento para Consolo Longo (Cálculo de Flexão com $z = {z_braco:.2f}$ cm):*")
            st.latex(rf"""A_{{s,vp,calc}} = \frac{{M_d}}{{z \cdot f_{{yd}}}} = \frac{{{m_d_canto:.2f}}}{{{z_braco:.2f} \cdot {fyd:.2f}}} = \mathbf{{{as_vp_calc:.2f}\text{{ cm}}^2}}""")
        elif tipo_consolo.startswith("Consolo Curto"):
            st.markdown(f"*Dimensionamento para Consolo Curto (Modelo de Bielas e Tirantes):*")
            st.latex(rf"""A_{{s,vp,calc}} = \frac{{\frac{{C_c}}{{\tan\beta}}}}{{f_{{yd}}}} = \frac{{\frac{{{c_c:.2f}}}{{{tan_beta:.3f}}}}}{{{fyd:.2f}}} = \mathbf{{{as_vp_calc:.2f}\text{{ cm}}^2}}""")
        else:
            st.markdown(f"*Dimensionamento para Consolo Muito Curto (Atrito-Cisalhamento):*")
            st.latex(rf"""A_{{s,vp,calc}} = \frac{{C_c}}{{1{{,}}4 \cdot f_{{yd}} \cdot \mu}} = \frac{{{c_c:.2f}}}{{1{{,}}4 \cdot {fyd:.2f} \cdot {mu}}} = \mathbf{{{as_vp_calc:.2f}\text{{ cm}}^2}}""")
            
        st.latex(rf"""A_{{s,vp,min}} = 0{{,}}0015 \cdot h_c \cdot B_{{ext}} = 0{{,}}0015 \cdot {h_c:.1f} \cdot {b_ext:.1f} = \mathbf{{{as_vp_min:.2f}\text{{ cm}}^2}}""")
        
        # Correção aqui: Deixei apenas uma barra na frente do comando \text
        st.latex(rf"""A_{{s,vp}} \ (\text{{Adotado por Canto}}) = \max({as_vp_calc:.2f}, {as_vp_min:.2f}) = \mathbf{{{as_vp_final:.2f}\text{{ cm}}^2 / \text{{canto}}}}""")

        st.write("---")
        st.write("**B. Armadura Vertical Secundária de Face ($A_{s,vs}$):**")
        st.latex(r"A_{s,vs} = \max\left( 0{,}40 \cdot A_{s,vp} \, ; \ 0{,}0010 \cdot h_c \cdot B_{ext} \right)")
        st.latex(rf"""A_{{s,vs}} = \max\left( 0{{,}}40 \cdot {as_vp_final:.2f} \, ; \ 0{{,}}0010 \cdot {h_c:.1f} \cdot {b_ext:.1f} \right)""")
        st.latex(rf"""A_{{s,vs}} = \max({as_vs_calc:.2f} \, ; \ {as_vs_min:.2f}) = \mathbf{{{as_vs_final:.2f} \text{{ cm}}^2 / \text{{face}}}}""")
        st.markdown(f"**Taxa de armadura por metro (distribuída na menor face - $L_{{menor}} = {dim_min_int:.1f}$ cm):**")
        st.latex(rf"""A_{{s,vs}} \ (\text{{Projeto}}) = \frac{{{as_vs_final:.2f}}}{{{dim_min_int/100:.2f}\text{{ m}}}} = \mathbf{{{as_vs_m:.2f} \text{{ cm}}^2/\text{{m}}}}""")