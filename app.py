import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d14;
    color: #e8e8f0;
}

.main { background-color: #0d0d14; }
.block-container { padding: 2rem 2rem 2rem 2rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #12121e;
    border-right: 1px solid #1e1e32;
}
section[data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem; }

/* Header */
.app-header {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #00d4ff, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.app-sub {
    color: #4a4a6a;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
    margin-bottom: 2rem;
}

/* Ficha empresa */
.ficha-card {
    background: linear-gradient(135deg, #12121e, #1a1a2e);
    border: 1px solid #1e1e38;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.ficha-nombre {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #00d4ff;
    margin-bottom: 0.2rem;
}
.ficha-meta {
    color: #4a4a6a;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.ficha-stats {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}
.ficha-stat { display: flex; flex-direction: column; }
.ficha-stat-label { color: #4a4a6a; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.ficha-stat-value { color: #e8e8f0; font-size: 1.3rem; font-weight: 600; font-family: 'Space Mono', monospace; }
.ficha-stat-value.up { color: #00e676; }
.ficha-stat-value.down { color: #ff4444; }

/* Score card */
.score-card {
    background: #12121e;
    border: 1px solid #1e1e38;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.score-label { font-size: 0.7rem; color: #4a4a6a; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.4rem; font-family: 'Space Mono', monospace; }
.score-value { font-size: 2rem; font-weight: 700; font-family: 'Space Mono', monospace; }
.score-tag { font-size: 0.72rem; margin-top: 0.3rem; font-weight: 500; }

/* Indicator row */
.ind-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0;
    border-bottom: 1px solid #1a1a2e;
    font-size: 0.85rem;
}
.ind-row:last-child { border-bottom: none; }
.ind-name { color: #8888aa; }
.ind-value { font-family: 'Space Mono', monospace; color: #e8e8f0; }
.ind-score { font-family: 'Space Mono', monospace; font-size: 0.78rem; padding: 2px 8px; border-radius: 20px; font-weight: 700; }

/* Section title */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a4a6a;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1a1a2e;
}

/* News item */
.news-item {
    padding: 0.7rem 0;
    border-bottom: 1px solid #1a1a2e;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}
.news-title { color: #c8c8e0; font-size: 0.85rem; line-height: 1.4; }
.news-title a { color: #c8c8e0; text-decoration: none; }
.news-title a:hover { color: #00d4ff; }
.news-pub { color: #4a4a6a; font-size: 0.72rem; white-space: nowrap; font-family: 'Space Mono', monospace; }

/* Sentiment grid */
.sent-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-bottom: 1rem;
}
.sent-item {
    background: #12121e;
    border: 1px solid #1e1e38;
    border-radius: 10px;
    padding: 0.8rem 1rem;
}
.sent-item-label { color: #4a4a6a; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }
.sent-item-value { color: #e8e8f0; font-size: 0.95rem; font-weight: 600; font-family: 'Space Mono', monospace; }

/* Stметрики Streamlit override */
div[data-testid="metric-container"] {
    background: #12121e;
    border: 1px solid #1e1e38;
    border-radius: 12px;
    padding: 1rem;
}
div[data-testid="metric-container"] label { color: #4a4a6a !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.06em; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #e8e8f0 !important; font-family: 'Space Mono', monospace !important; }

/* Input */
div[data-testid="stTextInput"] input {
    background: #1a1a2e !important;
    border: 1px solid #2a2a44 !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1rem !important;
}

/* Button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #00d4ff22, #7b61ff22) !important;
    border: 1px solid #00d4ff44 !important;
    color: #00d4ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.06em !important;
    border-radius: 8px !important;
    width: 100% !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #00d4ff44, #7b61ff44) !important;
    border-color: #00d4ff88 !important;
}

/* Slider */
div[data-testid="stSlider"] { color: #4a4a6a !important; }

/* Tabs */
div[data-testid="stTabs"] button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    color: #4a4a6a !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom-color: #00d4ff !important;
}

/* Plotly charts */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PONDERACIONES
# ─────────────────────────────────────────────
PESOS_DEFAULT = {
    'fundamental':  0.35,
    'tecnico':      0.30,
    'cuantitativo': 0.20,
    'sentimiento':  0.15
}

PLOTLY_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='#0d0d14',
    plot_bgcolor='#12121e',
    font=dict(family='DM Sans', color='#8888aa'),
    margin=dict(l=10, r=10, t=40, b=10),
)


# ─────────────────────────────────────────────
# HELPERS SCORING
# ─────────────────────────────────────────────
def score_to_label(score):
    if score >= 8:   return 'COMPRA FUERTE'
    elif score >= 6: return 'COMPRA'
    elif score >= 4: return 'NEUTRAL'
    elif score >= 2: return 'VENTA'
    else:            return 'VENTA FUERTE'

def score_to_color(score):
    if score >= 8:   return '#00e676'
    elif score >= 6: return '#69f0ae'
    elif score >= 4: return '#ffd740'
    elif score >= 2: return '#ff6d00'
    else:            return '#ff1744'

def score_to_bg(score):
    if score >= 8:   return '#00e67622'
    elif score >= 6: return '#69f0ae22'
    elif score >= 4: return '#ffd74022'
    elif score >= 2: return '#ff6d0022'
    else:            return '#ff174422'


# ─────────────────────────────────────────────
# ANALISIS TECNICO
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def analisis_tecnico(ticker_str, periodo):
    hist = yf.download(ticker_str, period=periodo, progress=False)
    if hist.empty:
        return None, None, None, None
    scores = {}
    indicadores = {}
    close = hist['Close'].squeeze()
    vol   = hist['Volume'].squeeze()

    rsi_val = ta.momentum.RSIIndicator(close, window=14).rsi().iloc[-1]
    indicadores['RSI (14)'] = round(float(rsi_val), 2)
    if rsi_val < 30:        scores['RSI'] = 9
    elif rsi_val < 40:      scores['RSI'] = 7
    elif rsi_val < 50:      scores['RSI'] = 5
    elif rsi_val < 60:      scores['RSI'] = 5
    elif rsi_val < 70:      scores['RSI'] = 4
    else:                   scores['RSI'] = 2

    macd_obj  = ta.trend.MACD(close)
    macd_val  = macd_obj.macd().iloc[-1]
    macd_sig  = macd_obj.macd_signal().iloc[-1]
    macd_diff = macd_obj.macd_diff().iloc[-1]
    indicadores['MACD'] = round(float(macd_val), 4)
    indicadores['MACD Signal'] = round(float(macd_sig), 4)
    if macd_val > macd_sig and macd_diff > 0:   scores['MACD'] = 8
    elif macd_val > macd_sig:                   scores['MACD'] = 6
    elif macd_val < macd_sig and macd_diff < 0: scores['MACD'] = 2
    else:                                       scores['MACD'] = 4

    precio_actual = float(close.iloc[-1])
    sma20  = float(close.rolling(20).mean().iloc[-1])
    sma50  = float(close.rolling(50).mean().iloc[-1])
    sma200 = float(close.rolling(200).mean().iloc[-1])
    indicadores['Precio Actual'] = round(precio_actual, 2)
    indicadores['SMA 20']  = round(sma20, 2)
    indicadores['SMA 50']  = round(sma50, 2)
    indicadores['SMA 200'] = round(sma200, 2)
    ma_signals = sum([precio_actual > sma20, precio_actual > sma50,
                      precio_actual > sma200, sma20 > sma50, sma50 > sma200])
    scores['Medias Moviles'] = 2 + ma_signals * 1.5

    bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    bb_high = float(bb.bollinger_hband().iloc[-1])
    bb_low  = float(bb.bollinger_lband().iloc[-1])
    bb_pct  = (precio_actual - bb_low) / (bb_high - bb_low) * 100 if (bb_high - bb_low) != 0 else 50
    indicadores['BB %B'] = round(bb_pct, 1)
    if bb_pct < 10:    scores['Bollinger'] = 9
    elif bb_pct < 30:  scores['Bollinger'] = 7
    elif bb_pct < 70:  scores['Bollinger'] = 5
    elif bb_pct < 90:  scores['Bollinger'] = 3
    else:              scores['Bollinger'] = 1

    vol_prom   = float(vol.rolling(20).mean().iloc[-1])
    vol_actual = float(vol.iloc[-1])
    vol_ratio  = vol_actual / vol_prom if vol_prom > 0 else 1
    price_chg  = (float(close.iloc[-1]) - float(close.iloc[-2])) / float(close.iloc[-2])
    indicadores['Volumen vs Media 20d'] = str(round(vol_ratio, 2)) + 'x'
    if vol_ratio > 1.5 and price_chg > 0:   scores['Volumen'] = 8
    elif vol_ratio > 1.2 and price_chg > 0: scores['Volumen'] = 6
    elif vol_ratio < 0.7:                   scores['Volumen'] = 4
    elif vol_ratio > 1.5 and price_chg < 0: scores['Volumen'] = 2
    else:                                   scores['Volumen'] = 5

    score_total = round(float(np.mean(list(scores.values()))), 2)
    return score_total, scores, indicadores, hist


# ─────────────────────────────────────────────
# ANALISIS FUNDAMENTAL
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def analisis_fundamental(ticker_str):
    info = yf.Ticker(ticker_str).info
    scores = {}
    indicadores = {}

    pe = info.get('trailingPE', None)
    if pe and pe > 0:
        indicadores['P/E Ratio'] = round(pe, 2)
        scores['PE'] = 9 if pe < 10 else 7 if pe < 15 else 6 if pe < 20 else 5 if pe < 25 else 3 if pe < 35 else 1
    else:
        indicadores['P/E Ratio'] = 'N/D'

    pb = info.get('priceToBook', None)
    if pb and pb > 0:
        indicadores['P/B Ratio'] = round(pb, 2)
        scores['PB'] = 9 if pb < 1 else 7 if pb < 2 else 5 if pb < 3 else 3 if pb < 5 else 1
    else:
        indicadores['P/B Ratio'] = 'N/D'

    ev = info.get('enterpriseToEbitda', None)
    if ev and ev > 0:
        indicadores['EV/EBITDA'] = round(ev, 2)
        scores['EV_EBITDA'] = 9 if ev < 8 else 7 if ev < 12 else 5 if ev < 16 else 3 if ev < 22 else 1
    else:
        indicadores['EV/EBITDA'] = 'N/D'

    margen = info.get('profitMargins', None)
    if margen:
        m = margen * 100
        indicadores['Margen Neto'] = str(round(m, 1)) + '%'
        scores['Margen'] = 9 if m > 20 else 7 if m > 10 else 5 if m > 5 else 3 if m > 0 else 1
    else:
        indicadores['Margen Neto'] = 'N/D'

    de = info.get('debtToEquity', None)
    if de:
        indicadores['Deuda/Equity'] = round(de, 2)
        scores['Deuda'] = 9 if de < 30 else 7 if de < 60 else 5 if de < 100 else 3 if de < 200 else 1
    else:
        indicadores['Deuda/Equity'] = 'N/D'

    eg = info.get('earningsGrowth', None)
    if eg:
        ep = eg * 100
        indicadores['Crec. Earnings'] = str(round(ep, 1)) + '%'
        scores['EarningsGrowth'] = 9 if ep > 20 else 7 if ep > 10 else 5 if ep > 0 else 3 if ep > -10 else 1
    else:
        indicadores['Crec. Earnings'] = 'N/D'

    roe = info.get('returnOnEquity', None)
    if roe:
        rp = roe * 100
        indicadores['ROE'] = str(round(rp, 1)) + '%'
        scores['ROE'] = 9 if rp > 20 else 7 if rp > 15 else 5 if rp > 10 else 3 if rp > 0 else 1
    else:
        indicadores['ROE'] = 'N/D'

    score_total = round(float(np.mean(list(scores.values()))) if scores else 5.0, 2)
    return score_total, scores, indicadores, info


# ─────────────────────────────────────────────
# ANALISIS CUANTITATIVO
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def analisis_cuantitativo(ticker_str, periodo):
    hist = yf.download(ticker_str, period=periodo, progress=False)
    if hist.empty:
        return None, None, None
    scores = {}
    indicadores = {}
    close = hist['Close'].squeeze()
    retornos = close.pct_change().dropna()

    vol_anual = float(retornos.std() * np.sqrt(252) * 100)
    indicadores['Volatilidad Anual'] = str(round(vol_anual, 1)) + '%'
    scores['Volatilidad'] = 7 if vol_anual < 15 else 6 if vol_anual < 25 else 5 if vol_anual < 35 else 3 if vol_anual < 50 else 2

    rf = 0.045 / 252
    ret_med = float(retornos.mean())
    vol_d   = float(retornos.std())
    sharpe  = (ret_med - rf) / vol_d * np.sqrt(252) if vol_d > 0 else 0
    indicadores['Sharpe Ratio'] = round(float(sharpe), 2)
    scores['Sharpe'] = 9 if sharpe > 2 else 7 if sharpe > 1 else 5 if sharpe > 0 else 3 if sharpe > -1 else 1

    if len(close) >= 252:
        ret_1y = float((close.iloc[-1] / close.iloc[-252] - 1) * 100)
        indicadores['Retorno 1 Año'] = str(round(ret_1y, 1)) + '%'
        scores['Retorno1Y'] = 9 if ret_1y > 30 else 7 if ret_1y > 15 else 5 if ret_1y > 0 else 3 if ret_1y > -15 else 1

    ventana  = close.iloc[-252:] if len(close) >= 252 else close
    roll_max = ventana.cummax()
    dd = float(((ventana - roll_max) / roll_max).min() * 100)
    indicadores['Max Drawdown'] = str(round(dd, 1)) + '%'
    scores['Drawdown'] = 8 if dd > -10 else 6 if dd > -20 else 4 if dd > -30 else 2 if dd > -40 else 1

    try:
        spy = yf.download('SPY', period='1y', progress=False)['Close'].squeeze()
        spy_ret  = spy.pct_change().dropna()
        combined = pd.concat([retornos, spy_ret], axis=1, join='inner')
        combined.columns = ['stock', 'spy']
        if len(combined) > 20:
            cov     = float(combined.cov().iloc[0, 1])
            var_spy = float(combined['spy'].var())
            beta    = cov / var_spy if var_spy > 0 else 1
            indicadores['Beta (vs SPY)'] = round(beta, 2)
            scores['Beta'] = 6 if 0.7 <= beta <= 1.2 else 7 if beta < 0.7 else 5 if beta <= 1.5 else 4
    except:
        indicadores['Beta (vs SPY)'] = 'N/D'

    score_total = round(float(np.mean(list(scores.values()))) if scores else 5.0, 2)
    return score_total, scores, indicadores


# ─────────────────────────────────────────────
# ANALISIS SENTIMIENTO
# ─────────────────────────────────────────────
@st.cache_data(ttl=1800)
def analisis_sentimiento(ticker_str):
    ticker_obj = yf.Ticker(ticker_str)
    info = ticker_obj.info
    scores = {}
    indicadores = {}
    noticias_lista = []

    # Recomendaciones analistas
    try:
        rec      = info.get('recommendationKey', '')
        rec_mean = info.get('recommendationMean', None)
        n_anal   = info.get('numberOfAnalystOpinions', 0)
        indicadores['Recomendacion'] = rec.upper() if rec else 'N/D'
        indicadores['N Analistas'] = n_anal if n_anal else 'N/D'
        if rec_mean:
            indicadores['Score Analistas'] = str(round(rec_mean, 1)) + '/5'
            score_anl = 10 - (rec_mean - 1) * 2.25
            scores['Analistas'] = max(1, min(10, score_anl))
        target = info.get('targetMeanPrice', None)
        precio = info.get('currentPrice', info.get('regularMarketPrice', None))
        if target and precio and isinstance(precio, (int, float)):
            upside = (target - precio) / precio * 100
            indicadores['Upside Precio Obj.'] = ('+' if upside > 0 else '') + str(round(upside, 1)) + '%'
            scores['PrecioObjetivo'] = 9 if upside > 20 else 7 if upside > 10 else 5 if upside > 0 else 3 if upside > -10 else 1
    except:
        pass

    # Insiders
    try:
        insiders = ticker_obj.insider_transactions
        if insiders is not None and not insiders.empty:
            fecha_corte = datetime.now() - timedelta(days=90)
            col_fecha = next((c for c in ['Start Date', 'Date'] if c in insiders.columns), insiders.columns[0])
            try:
                insiders[col_fecha] = pd.to_datetime(insiders[col_fecha], utc=True)
                insiders = insiders[insiders[col_fecha] >= pd.Timestamp(fecha_corte, tz='UTC')]
            except:
                pass
            text_col = next((c for c in ['Text', 'Transaction', 'text'] if c in insiders.columns), None)
            compras = ventas = 0
            if text_col:
                for _, row in insiders.iterrows():
                    txt = str(row[text_col]).lower()
                    if any(w in txt for w in ['purchase', 'buy', 'acquisition']): compras += 1
                    elif any(w in txt for w in ['sale', 'sell', 'disposition']):  ventas += 1
            indicadores['Insider Compras (90d)'] = str(compras)
            indicadores['Insider Ventas (90d)']  = str(ventas)
            if compras > ventas and compras > 0:
                scores['Insiders'] = 9 if compras >= 3 else 7
            elif ventas > compras and ventas > 0:
                scores['Insiders'] = 2 if ventas >= 5 else 3
            else:
                scores['Insiders'] = 5
    except:
        indicadores['Insider Compras (90d)'] = 'N/D'
        indicadores['Insider Ventas (90d)']  = 'N/D'

    # Short interest
    try:
        spf = info.get('shortPercentOfFloat', None)
        sr  = info.get('shortRatio', None)
        if spf:
            pct = spf * 100
            indicadores['Short % Float'] = str(round(pct, 1)) + '%'
            scores['ShortInterest'] = 8 if pct < 2 else 6 if pct < 5 else 5 if pct < 10 else 3 if pct < 20 else 1
        if sr:
            indicadores['Short Ratio'] = str(round(sr, 1)) + 'd'
    except:
        indicadores['Short % Float'] = 'N/D'

    # Institucionales
    try:
        pct_inst = info.get('heldPercentInstitutions', None)
        if pct_inst:
            pct = pct_inst * 100 if pct_inst < 1 else pct_inst
            indicadores['Ownership Inst.'] = str(round(pct, 1)) + '%'
            scores['Institucionales'] = 8 if pct > 70 else 7 if pct > 50 else 5 if pct > 30 else 4
    except:
        indicadores['Ownership Inst.'] = 'N/D'

    # Earnings surprises
    try:
        earnings = ticker_obj.earnings_history
        if earnings is None or (hasattr(earnings, 'empty') and earnings.empty):
            earnings = ticker_obj.earnings_dates
        if earnings is not None and not (hasattr(earnings, 'empty') and earnings.empty):
            est_col = next((c for c in ['EPS Estimate', 'epsEstimate'] if c in earnings.columns), None)
            rep_col = next((c for c in ['Reported EPS', 'epsActual', 'EPS Actual'] if c in earnings.columns), None)
            beats = misses = 0
            if est_col and rep_col:
                for _, row in earnings.head(4).iterrows():
                    try:
                        if float(row[rep_col]) > float(row[est_col]): beats += 1
                        else: misses += 1
                    except: pass
            if beats + misses > 0:
                indicadores['Earnings Beats'] = str(beats) + '/' + str(beats + misses)
                br = beats / (beats + misses)
                scores['EarningsBeats'] = 8 if br >= 0.75 else 6 if br >= 0.5 else 4 if br >= 0.25 else 2
            else:
                indicadores['Earnings Beats'] = 'N/D'
    except:
        indicadores['Earnings Beats'] = 'N/D'

    # Noticias
    try:
        noticias = ticker_obj.news
        if noticias:
            indicadores['Noticias recientes'] = str(len(noticias))
            scores['Actividad'] = 6 if len(noticias) > 10 else 5 if len(noticias) > 5 else 4
            for item in noticias[:8]:
                noticias_lista.append({
                    'titulo':    item.get('title', 'Sin titulo'),
                    'publisher': item.get('publisher', ''),
                    'link':      item.get('link', '#')
                })
        else:
            scores['Actividad'] = 5
    except:
        scores['Actividad'] = 5

    score_total = round(float(np.mean(list(scores.values()))) if scores else 5.0, 2)
    return score_total, scores, indicadores, noticias_lista


# ─────────────────────────────────────────────
# COMPARATIVO PEERS
# ─────────────────────────────────────────────
SECTOR_PEERS = {
    'Technology':             ['AAPL', 'MSFT', 'GOOGL', 'META'],
    'Financial Services':     ['JPM', 'BAC', 'GS', 'WFC'],
    'Healthcare':             ['JNJ', 'UNH', 'PFE', 'MRK'],
    'Consumer Cyclical':      ['AMZN', 'TSLA', 'HD', 'NKE'],
    'Energy':                 ['XOM', 'CVX', 'COP', 'EOG'],
    'Industrials':            ['BA', 'CAT', 'GE', 'HON'],
    'Communication Services': ['GOOGL', 'META', 'NFLX', 'DIS'],
    'Consumer Defensive':     ['WMT', 'PG', 'KO', 'PEP'],
    'Utilities':              ['NEE', 'DUK', 'SO', 'AEP'],
    'Real Estate':            ['AMT', 'PLD', 'CCI', 'EQIX'],
    'Basic Materials':        ['LIN', 'APD', 'ECL', 'NEM'],
}

@st.cache_data(ttl=3600)
def comparativo_peers(ticker_principal, sector):
    peers = SECTOR_PEERS.get(sector, ['SPY', 'QQQ', 'IWM'])
    metricas = ['trailingPE', 'priceToBook', 'profitMargins', 'returnOnEquity', 'debtToEquity']
    nombres  = ['P/E', 'P/B', 'Margen%', 'ROE%', 'Deuda/Eq']
    resultados = {'Ticker': [ticker_principal] + peers}
    for metrica, nombre in zip(metricas, nombres):
        valores = []
        for t in [ticker_principal] + peers:
            try:
                val = yf.Ticker(t).info.get(metrica, None)
                if val and metrica in ['profitMargins', 'returnOnEquity']:
                    val = round(val * 100, 1)
                elif val:
                    val = round(val, 2)
                valores.append(val if val else 'N/D')
            except:
                valores.append('N/D')
        resultados[nombre] = valores
    return pd.DataFrame(resultados).set_index('Ticker'), peers


# ─────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────
def plot_precio(hist, ticker):
    close  = hist['Close'].squeeze()
    sma20  = close.rolling(20).mean()
    sma50  = close.rolling(50).mean()
    sma200 = close.rolling(200).mean()
    bb     = ta.volatility.BollingerBands(close)
    rsi    = ta.momentum.RSIIndicator(close, window=14).rsi()
    macd_obj  = ta.trend.MACD(close)
    macd_line = macd_obj.macd()
    macd_sig  = macd_obj.macd_signal()
    macd_hist = macd_obj.macd_diff()

    fig = make_subplots(rows=4, cols=1, row_heights=[0.5, 0.15, 0.18, 0.17],
        shared_xaxes=True, vertical_spacing=0.03,
        subplot_titles=[ticker + ' — Precio', 'Volumen', 'RSI (14)', 'MACD'])

    fig.add_trace(go.Candlestick(x=hist.index,
        open=hist['Open'].squeeze(), high=hist['High'].squeeze(),
        low=hist['Low'].squeeze(), close=close, name='Precio',
        increasing_line_color='#00e676', decreasing_line_color='#ff1744'), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=bb.bollinger_hband(), name='BB+',
        line=dict(color='#7b61ff44', dash='dot'), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=bb.bollinger_lband(), name='BB-',
        line=dict(color='#7b61ff44', dash='dot'),
        fill='tonexty', fillcolor='#7b61ff08', showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=sma20,  name='SMA 20',  line=dict(color='#ffd740', width=1.2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=sma50,  name='SMA 50',  line=dict(color='#00d4ff', width=1.2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=sma200, name='SMA 200', line=dict(color='#ff6d90', width=1.2)), row=1, col=1)

    colores_vol = ['#ff174488' if row['Close'].squeeze() < row['Open'].squeeze() else '#00e67688'
                   for _, row in hist.iterrows()]
    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'].squeeze(), name='Vol',
        marker_color=colores_vol, showlegend=False), row=2, col=1)

    fig.add_trace(go.Scatter(x=hist.index, y=rsi, name='RSI',
        line=dict(color='#b388ff', width=1.5), showlegend=False), row=3, col=1)
    fig.add_hline(y=70, line_dash='dot', line_color='#ff174466', row=3, col=1)
    fig.add_hline(y=30, line_dash='dot', line_color='#00e67666', row=3, col=1)

    colores_macd = ['#ff174488' if v < 0 else '#00e67688' for v in macd_hist]
    fig.add_trace(go.Bar(x=hist.index, y=macd_hist, name='Hist',
        marker_color=colores_macd, showlegend=False), row=4, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=macd_line, name='MACD',
        line=dict(color='#00d4ff', width=1.2), showlegend=False), row=4, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=macd_sig, name='Signal',
        line=dict(color='#ff6d90', width=1.2), showlegend=False), row=4, col=1)

    fig.update_layout(**PLOTLY_LAYOUT, height=780, xaxis_rangeslider_visible=False,
        legend=dict(orientation='h', y=1.02, bgcolor='rgba(0,0,0,0)'))
    fig.update_xaxes(gridcolor='#1a1a2e', zeroline=False)
    fig.update_yaxes(gridcolor='#1a1a2e', zeroline=False)
    return fig


def plot_gauge(score_final, scores_cat):
    fig = make_subplots(rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'bar'}]],
        column_widths=[0.4, 0.6])
    fig.add_trace(go.Indicator(
        mode='gauge+number',
        value=score_final,
        number={'font': {'size': 52, 'color': score_to_color(score_final), 'family': 'Space Mono'}},
        title={'text': score_to_label(score_final), 'font': {'size': 14, 'color': '#8888aa', 'family': 'Space Mono'}},
        gauge={
            'axis': {'range': [1, 10], 'tickcolor': '#4a4a6a', 'tickfont': {'color': '#4a4a6a', 'size': 10}},
            'bar': {'color': score_to_color(score_final), 'thickness': 0.25},
            'bgcolor': '#12121e',
            'bordercolor': '#1e1e38',
           'steps': [
                {'range': [1, 2],  'color': 'rgba(255,23,68,0.1)'},
                {'range': [2, 4],  'color': 'rgba(255,109,0,0.1)'},
                {'range': [4, 6],  'color': 'rgba(255,215,64,0.1)'},
                {'range': [6, 8],  'color': 'rgba(105,240,174,0.1)'},
                {'range': [8, 10], 'color': 'rgba(0,230,118,0.1)'},
            ]
        }
    ), row=1, col=1)

    cats   = list(scores_cat.keys())
    vals   = list(scores_cat.values())
    colors = [score_to_color(v) for v in vals]
    fig.add_trace(go.Bar(x=cats, y=vals, marker_color=colors,
        text=[str(round(v, 1)) for v in vals], textposition='outside',
        textfont=dict(family='Space Mono', size=11, color='#e8e8f0')), row=1, col=2)
    fig.update_yaxes(range=[0, 11], gridcolor='#1a1a2e', row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=10, color='#8888aa'), row=1, col=2)
    fig.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
    return fig


def plot_scores_detalle(scores_tec, scores_fun, scores_cuan, scores_sent):
    todos = {}
    for k, v in scores_fun.items():  todos['FUN · ' + k] = v
    for k, v in scores_tec.items():  todos['TEC · ' + k] = v
    for k, v in scores_cuan.items(): todos['CUA · ' + k] = v
    for k, v in scores_sent.items(): todos['SEN · ' + k] = v
    labels = list(todos.keys())
    values = list(todos.values())
    colors = [score_to_color(v) for v in values]
    bgs    = [score_to_bg(v) for v in values]

    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation='h',
        marker=dict(color=colors, line=dict(color='#0d0d14', width=0.5)),
        text=[str(int(round(v))) + '/10' for v in values],
        textposition='outside',
        textfont=dict(family='Space Mono', size=10, color='#8888aa')
    ))
    fig.add_vline(x=5, line_dash='dot', line_color='#2a2a44', opacity=0.8)
    fig.update_xaxes(range=[0, 13], gridcolor='#1a1a2e', zeroline=False)
    fig.update_yaxes(tickfont=dict(size=10, color='#6a6a8a', family='Space Mono'), gridcolor='#1a1a2e')
    fig.update_layout(**PLOTLY_LAYOUT, height=max(380, len(labels) * 28), showlegend=False)
    return fig


def plot_peers(df_peers, ticker):
    header_vals = [''] + list(df_peers.columns)
    cell_vals   = [df_peers.index.tolist()] + [df_peers[c].tolist() for c in df_peers.columns]
    row_colors  = [['#00d4ff22' if t == ticker else '#12121e' for t in df_peers.index]]
    fill_colors = row_colors * len(header_vals)

    fig = go.Figure(go.Table(
        header=dict(values=['<b>' + v + '</b>' for v in header_vals],
            fill_color='#1a1a2e', font=dict(color='#8888aa', size=11, family='Space Mono'),
            align='center', height=32, line=dict(color='#0d0d14', width=1)),
        cells=dict(values=cell_vals, fill_color=fill_colors,
            font=dict(color='#e8e8f0', size=11, family='DM Sans'),
            align='center', height=28, line=dict(color='#0d0d14', width=1))
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=220)
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-header">STOCK<br>RESEARCH</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-sub">Terminal de Análisis</div>', unsafe_allow_html=True)

    ticker_input = st.text_input('', value='AAPL', placeholder='Ticker (ej: MSFT, GGAL.BA)',
                                  label_visibility='collapsed').upper().strip()

    periodo = st.select_slider('Período histórico',
        options=['3mo', '6mo', '1y', '2y', '5y'], value='1y')

    st.markdown('---')
    st.markdown('<div class="section-title">Ponderaciones</div>', unsafe_allow_html=True)
    p_fun  = st.slider('Fundamental',  0, 100, 35, 5)
    p_tec  = st.slider('Técnico',      0, 100, 30, 5)
    p_cuan = st.slider('Cuantitativo', 0, 100, 20, 5)
    p_sent = st.slider('Sentimiento',  0, 100, 15, 5)
    total_pesos = p_fun + p_tec + p_cuan + p_sent
    if total_pesos != 100:
        st.warning(f'⚠ Suma: {total_pesos}% (debe ser 100%)')
    pesos = {'fundamental': p_fun/100, 'tecnico': p_tec/100,
             'cuantitativo': p_cuan/100, 'sentimiento': p_sent/100}

    st.markdown('---')
    analizar = st.button('▶  ANALIZAR')

    st.markdown('---')
    st.markdown('<div style="color:#2a2a44;font-size:0.7rem;font-family:Space Mono;text-align:center;">NYSE · NASDAQ · BYMA<br>Datos via Yahoo Finance</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if analizar or 'last_ticker' not in st.session_state:
    st.session_state['last_ticker'] = ticker_input
    st.session_state['run'] = True

if st.session_state.get('run'):
    ticker = st.session_state['last_ticker']

    with st.spinner(f'Cargando datos de {ticker}...'):
        score_tec,  scores_tec,  ind_tec,  hist = analisis_tecnico(ticker, periodo)
        score_fun,  scores_fun,  ind_fun,  info = analisis_fundamental(ticker)
        score_cuan, scores_cuan, ind_cuan        = analisis_cuantitativo(ticker, periodo)
        score_sent, scores_sent, ind_sent, noticias = analisis_sentimiento(ticker)

    if hist is None or hist.empty:
        st.error(f'No se encontraron datos para **{ticker}**. Verificá el ticker.')
        st.stop()

    # Score final
    if total_pesos == 100:
        score_final = round(
            score_fun  * pesos['fundamental']  +
            score_tec  * pesos['tecnico']      +
            score_cuan * pesos['cuantitativo'] +
            score_sent * pesos['sentimiento'], 2)
    else:
        score_final = round(
            score_fun  * PESOS_DEFAULT['fundamental']  +
            score_tec  * PESOS_DEFAULT['tecnico']      +
            score_cuan * PESOS_DEFAULT['cuantitativo'] +
            score_sent * PESOS_DEFAULT['sentimiento'], 2)

    # ── FICHA EMPRESA
    nombre    = info.get('longName', ticker)
    sector    = info.get('sector', 'N/D')
    industria = info.get('industry', 'N/D')
    pais      = info.get('country', 'N/D')
    mktcap    = info.get('marketCap', None)
    precio    = info.get('currentPrice', info.get('regularMarketPrice', 'N/D'))
    target    = info.get('targetMeanPrice', None)
    divyield  = info.get('dividendYield', None)

    upside_html = ''
    if target and isinstance(precio, (int, float)):
        upside = (target - precio) / precio * 100
        cls = 'up' if upside > 0 else 'down'
        upside_html = f'<span class="ficha-stat-value {cls}">${target:.1f} <span style="font-size:0.85rem">({upside:+.1f}%)</span></span>'

    st.markdown(f"""
    <div class="ficha-card">
        <div class="ficha-nombre">{nombre}</div>
        <div class="ficha-meta">{ticker} &nbsp;·&nbsp; {sector} &nbsp;·&nbsp; {industria} &nbsp;·&nbsp; {pais}</div>
        <div class="ficha-stats">
            <div class="ficha-stat">
                <span class="ficha-stat-label">Precio</span>
                <span class="ficha-stat-value">${precio}</span>
            </div>
            <div class="ficha-stat">
                <span class="ficha-stat-label">Market Cap</span>
                <span class="ficha-stat-value">{'$' + str(round(mktcap/1e9,1)) + 'B' if mktcap else 'N/D'}</span>
            </div>
            <div class="ficha-stat">
                <span class="ficha-stat-label">Precio Objetivo</span>
                {upside_html if upside_html else '<span class="ficha-stat-value">N/D</span>'}
            </div>
            <div class="ficha-stat">
                <span class="ficha-stat-label">Dividendo</span>
                <span class="ficha-stat-value">{str(round(divyield*100,2))+'%' if divyield else 'N/D'}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── GAUGE + SCORES CATEGORIA
    scores_cat = {
        f'FUN {int(pesos["fundamental"]*100)}%':  score_fun,
        f'TEC {int(pesos["tecnico"]*100)}%':      score_tec,
        f'CUA {int(pesos["cuantitativo"]*100)}%': score_cuan,
        f'SEN {int(pesos["sentimiento"]*100)}%':  score_sent,
    }
    st.plotly_chart(plot_gauge(score_final, scores_cat), use_container_width=True)

    # ── TABS
    tab1, tab2, tab3, tab4 = st.tabs(['TÉCNICO', 'FUNDAMENTAL · CUANTITATIVO', 'SENTIMIENTO', 'PEERS'])

    with tab1:
        st.plotly_chart(plot_precio(hist, ticker), use_container_width=True)
        st.markdown('<div class="section-title">Scores por Indicador</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_scores_detalle(scores_tec, scores_fun, scores_cuan, scores_sent), use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Fundamental</div>', unsafe_allow_html=True)
            for k, v in ind_fun.items():
                score_ind = scores_fun.get(k.replace('/', '_').replace(' ', ''), None)
                score_html = ''
                if score_ind:
                    score_html = f'<span class="ind-score" style="background:{score_to_bg(score_ind)};color:{score_to_color(score_ind)}">{int(round(score_ind))}</span>'
                st.markdown(f'<div class="ind-row"><span class="ind-name">{k}</span><div style="display:flex;align-items:center;gap:8px"><span class="ind-value">{v}</span>{score_html}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="section-title">Cuantitativo</div>', unsafe_allow_html=True)
            for k, v in ind_cuan.items():
                st.markdown(f'<div class="ind-row"><span class="ind-name">{k}</span><span class="ind-value">{v}</span></div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-title">Indicadores de Sentimiento</div>', unsafe_allow_html=True)
        items = list(ind_sent.items())
        cols = st.columns(3)
        for i, (k, v) in enumerate(items):
            with cols[i % 3]:
                st.markdown(f'<div class="sent-item"><div class="sent-item-label">{k}</div><div class="sent-item-value">{v}</div></div>', unsafe_allow_html=True)

        if noticias:
            st.markdown('<div class="section-title" style="margin-top:1.5rem">Últimas Noticias</div>', unsafe_allow_html=True)
            for n in noticias:
                st.markdown(f'''
                <div class="news-item">
                    <div class="news-title"><a href="{n['link']}" target="_blank">{n['titulo']}</a></div>
                    <div class="news-pub">{n['publisher']}</div>
                </div>''', unsafe_allow_html=True)

    with tab4:
        with st.spinner('Cargando comparativo...'):
            df_peers, peers_list = comparativo_peers(ticker, sector)
        st.plotly_chart(plot_peers(df_peers, ticker), use_container_width=True)
        st.markdown(f'<div style="color:#4a4a6a;font-size:0.75rem;font-family:Space Mono;">Sector: {sector} · Peers: {", ".join(peers_list)}</div>', unsafe_allow_html=True)
