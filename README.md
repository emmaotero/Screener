# 📈 Stock Research Platform

App de análisis de acciones con scoring ponderado. NYSE, NASDAQ y BYMA.

## Deploy en Streamlit Community Cloud

1. Subí esta carpeta a un repositorio GitHub (público o privado)
2. Entrá a [share.streamlit.io](https://share.streamlit.io)
3. Conectá tu cuenta de GitHub
4. Elegí el repositorio y apuntá al archivo `app.py`
5. Click en **Deploy** — listo, tenés tu URL pública

## Estructura

```
stock_app/
├── app.py              ← App principal
├── requirements.txt    ← Dependencias
├── .streamlit/
│   └── config.toml    ← Tema dark
└── README.md
```

## Uso

- Ingresá un ticker en el sidebar (ej: AAPL, MSFT, GGAL.BA)
- Ajustá las ponderaciones a tu gusto (deben sumar 100%)
- Click en ANALIZAR

## Mercados soportados

- **USA**: NYSE y NASDAQ (ej: AAPL, TSLA, JPM)
- **Argentina BYMA**: agregar sufijo `.BA` (ej: GGAL.BA, YPFD.BA, PAMP.BA)
