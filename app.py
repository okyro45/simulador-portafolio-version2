import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import *
from openpyxl import Workbook
from openpyxl.styles import Font
from modules.reports import *


# Configuración de página
st.set_page_config(
    page_title="Portafolio de Inversiones",
    page_icon="📈",
    layout="wide"
)

crear_tablas()

# Menú lateral
st.sidebar.title("Menú Principal")

opcion = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "Inicio",
        "Datos del Portafolio",
        "Acciones",
        "Bonos",
        "Fondos Inmobiliarios",
        "Fondos Bancarios",
        "Depósitos a Plazo",
        "Rentabilidad",
        "Riesgo",
        "Dashboard",
        "Rebalanceo",
        "Reportes"
    ]
)

# Página principal
st.title("📈 Simulador Profesional de Portafolios")

st.subheader("Maestría en Finanzas")

st.write("Universidad Continental")

st.divider()

if opcion == "Inicio":
    st.header("Bienvenido")
    st.write(
        """
        Sistema para la gestión y análisis de portafolios de inversión.

        Permite registrar:

        - Acciones
        - Bonos
        - Fondos Inmobiliarios
        - Fondos Bancarios
        - Depósitos a Plazo

        Además calcula:

        - Rentabilidad
        - Riesgo
        - CAPM
        - Beta
        - DDM
        - Valoración de Bonos
        """
    )
if opcion == "Datos del Portafolio":

    st.header("Datos Generales del Portafolio")

    nombre = st.text_input("Nombre del Portafolio")

    inversionista = st.text_input(
        "Nombre del Inversionista"
    )

    moneda = st.selectbox(
        "Moneda Base",
        ["PEN", "USD"]
    )

    tipo_cambio = st.number_input(
        "Tipo de Cambio PEN/USD",
        min_value=0.0,
        value=3.80
    )

    fecha = st.date_input(
        "Fecha de Creación"
    )

    observaciones = st.text_area(
        "Observaciones"
    )

    if st.button("Guardar Portafolio"):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO portfolios(
            nombre,
            inversionista,
            moneda,
            tipo_cambio,
            fecha_creacion,
            observaciones
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            nombre,
            inversionista,
            moneda,
            tipo_cambio,
            str(fecha),
            observaciones
        ))

        conn.commit()
        conn.close()

        st.success(
            "Portafolio guardado correctamente."
        )

    st.subheader("Portafolios Registrados")

    conn = conectar()

    df = pd.read_sql_query(
        "SELECT * FROM portfolios",
        conn
    )

    conn.close()

    st.dataframe(
        df,
        use_container_width=True
    )

    if not df.empty:

        st.subheader("Eliminar Portafolio")

        id_eliminar = st.selectbox(
            "Seleccione el ID a eliminar",
            df["id"].tolist()
        )

        if st.button("Eliminar Portafolio"):

            eliminar_portafolio(id_eliminar)

            st.success(
                f"Portafolio {id_eliminar} eliminado correctamente."
            )

            st.rerun()

if opcion == "Acciones":

    st.header("Registro de Acciones")

    emisor = st.text_input("Emisor")

    ticker = st.text_input("Ticker")

    sector = st.text_input("Sector Económico")

    moneda_accion = st.selectbox(
        "Moneda",
        ["PEN", "USD"]
    )

    numero_acciones = st.number_input(
        "Número de Acciones",
        min_value=0.0
    )

    precio_accion = st.number_input(
        "Precio por Acción",
        min_value=0.0
    )

    dividendo_pagado = st.number_input(
        "Dividendo Pagado por Acción",
        min_value=0.0
    )

    dividendo_esperado = st.number_input(
        "Dividendo Esperado por Acción",
        min_value=0.0
    )

    st.subheader("Modelo DDM")

    rendimiento_requerido = st.number_input(
        "Rendimiento Requerido (%)",
        min_value=0.0,
        value=10.0
    )

    tasa_crecimiento = st.number_input(
        "Tasa de Crecimiento (%)",
        min_value=0.0,
        value=5.0
    )

    fecha_compra = st.date_input(
        "Fecha de Compra",
        key="fecha_compra_accion"
    )

    fecha_vencimiento = st.date_input(
        "Fecha Objetivo",
        key="fecha_vencimiento_accion"
    )

    importe_invertido = (
        numero_acciones *
        precio_accion
    )

    valor_mercado = (
        numero_acciones *
        precio_accion
    )

    if precio_accion > 0:

        dividend_yield = (
            dividendo_pagado /
            precio_accion
        ) * 100

    else:

        dividend_yield = 0

    k = rendimiento_requerido / 100
    g = tasa_crecimiento / 100

    if k > g:

        precio_ddm = (
            dividendo_esperado /
            (k - g)
        )

    else:

        precio_ddm = 0

    st.subheader("Resultados")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Importe Invertido",
            f"{moneda_accion} {importe_invertido:,.2f}"
        )

    with col2:

        st.metric(
            "Valor de Mercado",
            f"{moneda_accion} {valor_mercado:,.2f}"
        )

    with col3:

        st.metric(
            "Dividend Yield",
            f"{dividend_yield:.2f}%"
        )

    st.metric(
        "Precio Teórico DDM",
        f"{moneda_accion} {precio_ddm:,.2f}"
    )

    st.divider()

    if st.button("Guardar Acción"):

        guardar_accion(
            emisor,
            ticker,
            sector,
            moneda_accion,
            numero_acciones,
            precio_accion,
            importe_invertido,
            dividendo_pagado,
            dividendo_esperado,
            fecha_compra,
            fecha_vencimiento
        )

        st.success(
            "Acción guardada correctamente."
        )

    st.subheader("Acciones Registradas")

    conn = conectar()

    df_acciones = pd.read_sql_query(
        "SELECT * FROM acciones",
        conn
    )

    conn.close()

    st.dataframe(
        df_acciones,
        use_container_width=True
    )

    if not df_acciones.empty:

        st.subheader(
            "Eliminar Acción"
        )

        id_eliminar = st.selectbox(
            "Seleccione ID de la acción",
            df_acciones["id"].tolist(),
            key="eliminar_accion"
        )

        if st.button(
            "Eliminar Acción"
        ):

            eliminar_accion(
                id_eliminar
            )

            st.success(
                "Acción eliminada correctamente."
            )

            st.rerun()


# =====================================================
# BONOS
# =====================================================

if opcion == "Bonos":

    from datetime import date

    st.header("Registro de Bonos")

    emisor_bono = st.text_input(
        "Emisor"
    )

    tipo_bono = st.selectbox(
        "Tipo de Bono",
        [
            "Corporativo",
            "Soberano",
            "Municipal"
        ]
    )

    moneda_bono = st.selectbox(
        "Moneda",
        ["PEN", "USD"]
    )

    valor_nominal = st.number_input(
        "Valor Nominal",
        min_value=0.0
    )

    importe_invertido_bono = st.number_input(
        "Importe Invertido",
        min_value=0.0
    )

    cupon_anual = st.number_input(
        "Cupón Anual (%)",
        min_value=0.0
    )

    tasa_mercado = st.number_input(
        "Tasa de Mercado (%)",
        min_value=0.0
    )

    fecha_emision = st.date_input(
        "Fecha de Emisión",
        key="fecha_emision_bono"
    )

    fecha_vencimiento_bono = st.date_input(
        "Fecha de Vencimiento",
        key="fecha_vencimiento_bono"
    )

    dias_vencimiento = (
        fecha_vencimiento_bono -
        date.today()
    ).days

    r = tasa_mercado / 100

    if r > 0:

        precio_bono = (
            valor_nominal /
            ((1 + r) ** 1)
        )

    else:

        precio_bono = valor_nominal

    st.subheader("Resultados del Bono")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Precio Teórico",
            f"{moneda_bono} {precio_bono:,.2f}"
        )

    with col2:

        st.metric(
            "Valor Nominal",
            f"{moneda_bono} {valor_nominal:,.2f}"
        )

    with col3:

        st.metric(
            "Días al Vencimiento",
            dias_vencimiento
        )

    if st.button("Guardar Bono"):

        guardar_bono(
            emisor_bono,
            tipo_bono,
            moneda_bono,
            valor_nominal,
            importe_invertido_bono,
            cupon_anual,
            tasa_mercado,
            fecha_emision,
            fecha_vencimiento_bono
        )

        st.success(
            "Bono guardado correctamente."
        )

    st.subheader("Bonos Registrados")

    conn = conectar()

    df_bonos = pd.read_sql_query(
        "SELECT * FROM bonos",
        conn
    )

    conn.close()

    st.dataframe(
        df_bonos,
        use_container_width=True
    )

    if not df_bonos.empty:

        st.subheader(
            "Eliminar Bono"
        )

        id_eliminar_bono = st.selectbox(
            "Seleccione ID del bono",
            df_bonos["id"].tolist(),
            key="eliminar_bono"
        )

        if st.button(
            "Eliminar Bono"
        ):

            eliminar_bono(
                id_eliminar_bono
            )

            st.success(
                "Bono eliminado correctamente."
            )

            st.rerun()

if opcion == "Rentabilidad":

    st.header(
        "Rentabilidad del Portafolio"
    )

    conn = conectar()

    df_acciones = pd.read_sql_query(
        "SELECT * FROM acciones",
        conn
    )

    df_bonos = pd.read_sql_query(
        "SELECT * FROM bonos",
        conn
    )

    df_fondos_inm = pd.read_sql_query(
        "SELECT * FROM fondos_inmobiliarios",
        conn
    )

    df_fondos_ban = pd.read_sql_query(
        "SELECT * FROM fondos_bancarios",
        conn
    )

    df_depositos = pd.read_sql_query(
        "SELECT * FROM depositos_plazo",
        conn
    )

    conn.close()

    total_acciones = (
        df_acciones["importe_invertido"].sum()
        if not df_acciones.empty
        else 0
    )

    total_bonos = (
        df_bonos["importe_invertido"].sum()
        if not df_bonos.empty
        else 0
    )

    total_inmobiliarios = (
        df_fondos_inm["importe_invertido"].sum()
        if not df_fondos_inm.empty
        else 0
    )

    total_bancarios = (
        df_fondos_ban["importe_invertido"].sum()
        if not df_fondos_ban.empty
        else 0
    )

    total_depositos = (
        df_depositos["importe"].sum()
        if not df_depositos.empty
        else 0
    )

    valor_total = (
        total_acciones +
        total_bonos +
        total_inmobiliarios +
        total_bancarios +
        total_depositos
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Valor Total del Portafolio",
            f"S/ {valor_total:,.2f}"
        )

    with col2:

        st.metric(
            "Número de Inversiones",
            len(df_acciones)
            + len(df_bonos)
            + len(df_fondos_inm)
            + len(df_fondos_ban)
            + len(df_depositos)
        )

    st.divider()

    datos = pd.DataFrame({

        "Activo": [

            "Acciones",
            "Bonos",
            "Fondos Inmobiliarios",
            "Fondos Bancarios",
            "Depósitos"

        ],

        "Monto": [

            total_acciones,
            total_bonos,
            total_inmobiliarios,
            total_bancarios,
            total_depositos

        ]

    })

    datos["Participacion_%"] = (
        datos["Monto"] /
        datos["Monto"].sum()
    ) * 100

    st.subheader(
        "Participación por Activo"
    )

    st.dataframe(
        datos,
        use_container_width=True
    )

    st.bar_chart(
        datos.set_index(
            "Activo"
        )["Monto"]
    )

if opcion == "Riesgo":

    st.header("Análisis de Riesgo")

    conn = conectar()

    df_acciones = pd.read_sql_query(
        "SELECT * FROM acciones",
        conn
    )

    conn.close()

    if df_acciones.empty:

        st.warning(
            "No existen acciones registradas."
        )

    else:

        rendimientos = (
            df_acciones["precio_accion"]
        )

        media = rendimientos.mean()

        varianza = rendimientos.var()

        desviacion = rendimientos.std()

        if media != 0:

            cv = (
                desviacion /
                media
            ) * 100

        else:

            cv = 0

        # ==========================
        # ESTADÍSTICA DESCRIPTIVA
        # ==========================

        st.subheader(
            "Estadística Descriptiva"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Media",
                f"{media:,.2f}"
            )

            st.metric(
                "Varianza",
                f"{varianza:,.2f}"
            )

        with col2:

            st.metric(
                "Desviación Estándar",
                f"{desviacion:,.2f}"
            )

            st.metric(
                "Coeficiente de Variación",
                f"{cv:.2f}%"
            )

        st.subheader(
            "Datos Utilizados"
        )

        st.dataframe(
            df_acciones,
            use_container_width=True
        )

        # ==========================
        # CAPM
        # ==========================

        st.divider()

        st.subheader(
            "Modelo CAPM"
        )

        rf = st.number_input(
            "Tasa Libre de Riesgo (%)",
            min_value=0.0,
            value=4.0
        )

        rm = st.number_input(
            "Rendimiento Esperado del Mercado (%)",
            min_value=0.0,
            value=12.0
        )

        beta = st.number_input(
            "Beta",
            value=1.0
        )

        prima_mercado = rm - rf

        capm = rf + beta * prima_mercado

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Prima de Mercado",
                f"{prima_mercado:.2f}%"
            )

        with col2:

            st.metric(
                "CAPM",
                f"{capm:.2f}%"
            )

        # ==========================
        # RIESGO AVANZADO
        # ==========================

        st.divider()

        st.subheader(
            "Riesgo Avanzado"
        )

        beta_estimada = (
            desviacion / media
            if media > 0
            else 0
        )

        if len(df_acciones) > 1:

            correlacion = (
                df_acciones[
                    "precio_accion"
                ].corr(
                    df_acciones[
                        "importe_invertido"
                    ]
                )
            )

            covarianza = (
                df_acciones[
                    "precio_accion"
                ].cov(
                    df_acciones[
                        "importe_invertido"
                    ]
                )
            )

        else:

            correlacion = 0

            covarianza = 0

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Beta Estimada",
                f"{beta_estimada:.4f}"
            )

        with col2:

            st.metric(
                "Correlación",
                f"{correlacion:.4f}"
            )

        with col3:

            st.metric(
                "Covarianza",
                f"{covarianza:,.4f}"
            )

        # ==========================
        # VALUE AT RISK (VaR)
        # ==========================

        st.divider()

        st.subheader(
            "Value at Risk (VaR)"
        )

        valor_portafolio = (
            df_acciones[
                "importe_invertido"
            ].sum()
        )

        var_95 = (
            valor_portafolio *
            1.65 *
            (desviacion / 100)
        )

        var_99 = (
            valor_portafolio *
            2.33 *
            (desviacion / 100)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "VaR 95%",
                f"S/ {var_95:,.2f}"
            )

        with col2:

            st.metric(
                "VaR 99%",
                f"S/ {var_99:,.2f}"
            )

        st.info(
            f"""
            Con un nivel de confianza de 95%,
            la pérdida máxima esperada es:

            S/ {var_95:,.2f}

            Con un nivel de confianza de 99%,
            la pérdida máxima esperada es:

            S/ {var_99:,.2f}
            """
        )
        # ==========================
        # CONDITIONAL VAR (CVaR)
        # ==========================

        st.divider()

        st.subheader(
            "Conditional Value at Risk (CVaR)"
        )

        cvar_95 = var_95 * 1.25

        cvar_99 = var_99 * 1.25

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "CVaR 95%",
                f"S/ {cvar_95:,.2f}"
            )

        with col2:

            st.metric(
                "CVaR 99%",
                f"S/ {cvar_99:,.2f}"
            )

        st.warning(
            f"""
            Si el VaR es superado,
            la pérdida promedio esperada sería:

            CVaR 95% = S/ {cvar_95:,.2f}

            CVaR 99% = S/ {cvar_99:,.2f}
            """
        )
        # ==========================
        # SHARPE RATIO
        # ==========================

        st.divider()

        st.subheader(
            "Sharpe Ratio"
        )

        rf_sharpe = st.number_input(
            "Tasa Libre de Riesgo Sharpe (%)",
            min_value=0.0,
            value=4.0,
            key="rf_sharpe"
        )

        retorno_portafolio = st.number_input(
            "Retorno Esperado Portafolio (%)",
            min_value=0.0,
            value=12.0,
            key="retorno_portafolio"
        )

        if desviacion > 0:

            sharpe = (
                (retorno_portafolio - rf_sharpe)
                /
                desviacion
            )

        else:

            sharpe = 0

        st.metric(
            "Sharpe Ratio",
            f"{sharpe:.4f}"
        )

        # ==========================
        # ALPHA
        # ==========================

        st.divider()

        st.subheader(
            "Alpha"
        )

        retorno_real = st.number_input(
            "Retorno Real (%)",
            min_value=0.0,
            value=14.0,
            key="retorno_real"
        )

        alpha = (
            retorno_real -
            capm
        )

        st.metric(
            "Alpha",
            f"{alpha:.2f}%"
        )

        # ==========================
        # R²
        # ==========================

        st.divider()

        st.subheader(
            "Coeficiente de Determinación (R²)"
        )

        if correlacion != 0:

            r2 = correlacion ** 2

        else:

            r2 = 0

        st.metric(
            "R²",
            f"{r2:.4f}"
        )

        st.info(
            f"""
            El modelo explica aproximadamente
            {r2*100:.2f}% de la variación
            observada en los datos.
            """
        )


if opcion == "Fondos Inmobiliarios":

    from datetime import date

    st.header(
        "Fondos de Inversión Inmobiliarios"
    )

    emisor = st.text_input(
        "Emisor del Fondo"
    )

    unidades = st.number_input(
        "Número de Unidades",
        min_value=0.0
    )

    moneda = st.selectbox(
        "Moneda",
        ["PEN", "USD"]
    )

    importe = st.number_input(
        "Importe Invertido",
        min_value=0.0
    )

    tasa = st.number_input(
        "Tasa Anual Esperada (%)",
        min_value=0.0,
        value=8.0
    )

    fecha_inversion = st.date_input(
        "Fecha de Inversión",
        key="fi_fecha_inv"
    )

    fecha_vencimiento = st.date_input(
        "Fecha de Vencimiento",
        key="fi_fecha_venc"
    )

    dias = (
        fecha_vencimiento -
        date.today()
    ).days

    años = dias / 365

    valor_futuro = (
        importe *
        (
            1 +
            (tasa / 100)
        ) ** años
    )

    rentabilidad = (
        valor_futuro -
        importe
    )

    st.subheader(
        "Resultados"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Valor Futuro",
            f"{moneda} {valor_futuro:,.2f}"
        )

    with col2:

        st.metric(
            "Rentabilidad Esperada",
            f"{moneda} {rentabilidad:,.2f}"
        )

    with col3:

        st.metric(
            "Días al Vencimiento",
            dias
        )

    if st.button(
        "Guardar Fondo Inmobiliario"
    ):

        guardar_fondo_inmobiliario(
            emisor,
            unidades,
            moneda,
            importe,
            tasa,
            fecha_inversion,
            fecha_vencimiento
        )

        st.success(
            "Fondo Inmobiliario guardado correctamente."
        )

    conn = conectar()

    df_fondos = pd.read_sql_query(
        "SELECT * FROM fondos_inmobiliarios",
        conn
    )

    conn.close()

    st.subheader(
        "Fondos Inmobiliarios Registrados"
    )

    st.dataframe(
        df_fondos,
        use_container_width=True
    )

    if not df_fondos.empty:

        st.subheader(
            "Eliminar Fondo Inmobiliario"
        )

        id_eliminar = st.selectbox(
            "Seleccione ID",
            df_fondos["id"].tolist(),
            key="eliminar_fi"
        )

        if st.button(
            "Eliminar Fondo Inmobiliario"
        ):

            eliminar_fondo_inmobiliario(
                id_eliminar
            )

            st.success(
                "Fondo eliminado correctamente."
            )

            st.rerun()

if opcion == "Fondos Bancarios":

    from datetime import date

    st.header(
        "Fondos de Inversión Bancarios"
    )

    entidad = st.text_input(
        "Entidad Financiera"
    )

    fondo = st.text_input(
        "Nombre del Fondo"
    )

    tipo_fondo = st.selectbox(
        "Tipo de Fondo",
        [
            "Conservador",
            "Moderado",
            "Agresivo"
        ]
    )

    moneda = st.selectbox(
        "Moneda",
        ["PEN", "USD"],
        key="fb_moneda"
    )

    importe = st.number_input(
        "Importe Invertido",
        min_value=0.0,
        key="fb_importe"
    )

    rendimiento = st.number_input(
        "Rendimiento Esperado (%)",
        min_value=0.0,
        value=7.0
    )

    fecha_inversion = st.date_input(
        "Fecha de Inversión",
        key="fb_fecha_inv"
    )

    fecha_vencimiento = st.date_input(
        "Fecha de Vencimiento",
        key="fb_fecha_venc"
    )

    dias = (
        fecha_vencimiento -
        date.today()
    ).days

    años = dias / 365

    valor_futuro = (
        importe *
        (
            1 +
            (rendimiento / 100)
        ) ** años
    )

    rentabilidad = (
        valor_futuro -
        importe
    )

    st.subheader("Resultados")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Valor Futuro",
            f"{moneda} {valor_futuro:,.2f}"
        )

    with col2:
        st.metric(
            "Rentabilidad Esperada",
            f"{moneda} {rentabilidad:,.2f}"
        )

    with col3:
        st.metric(
            "Días al Vencimiento",
            dias
        )

    if st.button(
        "Guardar Fondo Bancario"
    ):

        guardar_fondo_bancario(
            entidad,
            fondo,
            tipo_fondo,
            moneda,
            importe,
            rendimiento,
            fecha_inversion,
            fecha_vencimiento
        )

        st.success(
            "Fondo Bancario guardado correctamente."
        )

    conn = conectar()

    df_fondos_bancarios = pd.read_sql_query(
        "SELECT * FROM fondos_bancarios",
        conn
    )

    conn.close()

    st.subheader(
        "Fondos Bancarios Registrados"
    )

    st.dataframe(
        df_fondos_bancarios,
        use_container_width=True
    )

    if not df_fondos_bancarios.empty:

        st.subheader(
            "Eliminar Fondo Bancario"
        )

        id_eliminar = st.selectbox(
            "Seleccione ID",
            df_fondos_bancarios["id"].tolist(),
            key="eliminar_fb"
        )

        if st.button(
            "Eliminar Fondo Bancario"
        ):

            eliminar_fondo_bancario(
                id_eliminar
            )

            st.success(
                "Fondo bancario eliminado correctamente."
            )

            st.rerun()

if opcion == "Depósitos a Plazo":

    from datetime import date

    st.header(
        "Depósitos a Plazo"
    )

    entidad = st.text_input(
        "Entidad Financiera"
    )

    moneda = st.selectbox(
        "Moneda",
        ["PEN", "USD"],
        key="dp_moneda"
    )

    importe = st.number_input(
        "Importe Invertido",
        min_value=0.0,
        key="dp_importe"
    )

    tasa = st.number_input(
        "Tasa Anual (%)",
        min_value=0.0,
        value=6.0
    )

    fecha_constitucion = st.date_input(
        "Fecha de Constitución"
    )

    fecha_vencimiento = st.date_input(
        "Fecha de Vencimiento",
        key="dp_venc"
    )

    dias = (
        fecha_vencimiento -
        date.today()
    ).days

    años = dias / 365

    interes = (
        importe *
        (tasa / 100) *
        años
    )

    valor_futuro = (
        importe +
        interes
    )

    st.subheader("Resultados")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Interés Generado",
            f"{moneda} {interes:,.2f}"
        )

    with col2:

        st.metric(
            "Valor Futuro",
            f"{moneda} {valor_futuro:,.2f}"
        )

    with col3:

        st.metric(
            "Días al Vencimiento",
            dias
        )

    if st.button(
        "Guardar Depósito"
    ):

        guardar_deposito(
            entidad,
            moneda,
            importe,
            tasa,
            fecha_constitucion,
            fecha_vencimiento
        )

        st.success(
            "Depósito guardado correctamente."
        )

    conn = conectar()

    df_depositos = pd.read_sql_query(
        "SELECT * FROM depositos_plazo",
        conn
    )

    conn.close()

    st.subheader(
        "Depósitos Registrados"
    )

    st.dataframe(
        df_depositos,
        use_container_width=True
    )

    st.info(
        f"""
        Rentabilidad calculada considerando
        vencimiento al
        {fecha_vencimiento.strftime('%d/%m/%Y')}
        """
    )

    if not df_depositos.empty:

        st.subheader(
            "Eliminar Depósito"
        )

        id_eliminar = st.selectbox(
            "Seleccione ID",
            df_depositos["id"].tolist(),
            key="eliminar_deposito"
        )

        if st.button(
            "Eliminar Depósito"
        ):

            eliminar_deposito(
                id_eliminar
            )

            st.success(
                "Depósito eliminado correctamente."
            )

            st.rerun()


if opcion == "Dashboard":

    st.header("Dashboard del Portafolio")

    conn = conectar()

    df_acciones = pd.read_sql_query(
        "SELECT * FROM acciones",
        conn
    )

    df_bonos = pd.read_sql_query(
        "SELECT * FROM bonos",
        conn
    )

    df_fondos_inm = pd.read_sql_query(
        "SELECT * FROM fondos_inmobiliarios",
        conn
    )

    df_fondos_ban = pd.read_sql_query(
        "SELECT * FROM fondos_bancarios",
        conn
    )

    df_depositos = pd.read_sql_query(
        "SELECT * FROM depositos_plazo",
        conn
    )

    conn.close()

    total_acciones = (
        df_acciones["importe_invertido"].sum()
        if not df_acciones.empty
        else 0
    )

    total_bonos = (
        df_bonos["importe_invertido"].sum()
        if not df_bonos.empty
        else 0
    )

    total_inmobiliarios = (
        df_fondos_inm["importe_invertido"].sum()
        if not df_fondos_inm.empty
        else 0
    )

    total_bancarios = (
        df_fondos_ban["importe_invertido"].sum()
        if not df_fondos_ban.empty
        else 0
    )

    total_depositos = (
        df_depositos["importe"].sum()
        if not df_depositos.empty
        else 0
    )

    valor_total = (
        total_acciones +
        total_bonos +
        total_inmobiliarios +
        total_bancarios +
        total_depositos
    )

    numero_inversiones = (
        len(df_acciones)
        + len(df_bonos)
        + len(df_fondos_inm)
        + len(df_fondos_ban)
        + len(df_depositos)
    )

    # ==========================
    # KPIs PRINCIPALES
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Valor Total",
            f"S/ {valor_total:,.2f}"
        )

    with col2:

        st.metric(
            "Acciones",
            f"S/ {total_acciones:,.2f}"
        )

    with col3:

        st.metric(
            "Bonos",
            f"S/ {total_bonos:,.2f}"
        )

    with col4:

        st.metric(
            "Fondos",
            f"S/ {total_inmobiliarios + total_bancarios:,.2f}"
        )

    st.divider()

    # ==========================
    # INDICADORES EJECUTIVOS
    # ==========================

    st.subheader(
        "Indicadores Ejecutivos"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Número de Inversiones",
            numero_inversiones
        )

    with col2:

        st.metric(
            "Tipos de Activos",
            5
        )

    # ==========================
    # DATAFRAME BASE
    # ==========================

    grafico = pd.DataFrame({

        "Activo": [
            "Acciones",
            "Bonos",
            "Fondos Inmobiliarios",
            "Fondos Bancarios",
            "Depósitos a Plazo"
        ],

        "Monto": [
            total_acciones,
            total_bonos,
            total_inmobiliarios,
            total_bancarios,
            total_depositos
        ]

    })

    # ==========================
    # GRAFICO PIE
    # ==========================

    st.subheader(
        "Distribución por Tipo de Activo"
    )

    fig = px.pie(
        grafico,
        names="Activo",
        values="Monto",
        title="Distribución del Portafolio"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # GRAFICO BARRAS
    # ==========================

    st.subheader(
        "Comparación de Inversiones"
    )

    st.bar_chart(
        grafico.set_index("Activo")
    )

    # ==========================
    # RESUMEN EJECUTIVO
    # ==========================

    st.subheader(
        "Resumen Ejecutivo"
    )

    st.dataframe(
        grafico,
        use_container_width=True
    )

    # ==========================
    # PARTICIPACION
    # ==========================

    if grafico["Monto"].sum() > 0:

        grafico["Participacion_%"] = (
            grafico["Monto"]
            /
            grafico["Monto"].sum()
        ) * 100

    else:

        grafico["Participacion_%"] = 0

    st.subheader(
        "Participación Porcentual"
    )

    st.dataframe(
        grafico,
        use_container_width=True
    )

    # ==========================
    # RANKING
    # ==========================

    st.subheader(
        "Ranking por Monto Invertido"
    )

    ranking = grafico.sort_values(
        by="Monto",
        ascending=False
    )

    st.dataframe(
        ranking,
        use_container_width=True
    )

    # ==========================
    # PRINCIPAL INVERSION
    # ==========================

    if not ranking.empty:

        activo_principal = ranking.iloc[0]

        st.success(
            f"""
            Principal inversión: {activo_principal['Activo']}

            Monto invertido:
            S/ {activo_principal['Monto']:,.2f}
            """
        )

    # ==========================
    # CONCENTRACION
    # ==========================

    mayor_participacion = (
        grafico["Participacion_%"].max()
    )

    st.metric(
        "Mayor Participación",
        f"{mayor_participacion:.2f}%"
    )

if opcion == "Rebalanceo":

    st.header(
        "Rebalanceo del Portafolio"
    )

    conn = conectar()

    df_acciones = pd.read_sql_query(
        "SELECT * FROM acciones",
        conn
    )

    df_bonos = pd.read_sql_query(
        "SELECT * FROM bonos",
        conn
    )

    df_fondos_inm = pd.read_sql_query(
        "SELECT * FROM fondos_inmobiliarios",
        conn
    )

    df_fondos_ban = pd.read_sql_query(
        "SELECT * FROM fondos_bancarios",
        conn
    )

    df_depositos = pd.read_sql_query(
        "SELECT * FROM depositos_plazo",
        conn
    )

    conn.close()

    total_acciones = (
        df_acciones["importe_invertido"].sum()
        if not df_acciones.empty
        else 0
    )

    total_bonos = (
        df_bonos["importe_invertido"].sum()
        if not df_bonos.empty
        else 0
    )

    total_inmobiliarios = (
        df_fondos_inm["importe_invertido"].sum()
        if not df_fondos_inm.empty
        else 0
    )

    total_bancarios = (
        df_fondos_ban["importe_invertido"].sum()
        if not df_fondos_ban.empty
        else 0
    )

    total_depositos = (
        df_depositos["importe"].sum()
        if not df_depositos.empty
        else 0
    )

    valor_total = (
        total_acciones +
        total_bonos +
        total_inmobiliarios +
        total_bancarios +
        total_depositos
    )

    st.subheader(
        "Distribución Objetivo (%)"
    )

    objetivo_acciones = st.number_input(
        "Acciones %",
        value=40.0
    )

    objetivo_bonos = st.number_input(
        "Bonos %",
        value=20.0
    )

    objetivo_fondos = st.number_input(
        "Fondos %",
        value=20.0
    )

    objetivo_depositos = st.number_input(
        "Depósitos %",
        value=20.0
    )

    actual_acciones = (
        total_acciones / valor_total * 100
        if valor_total > 0
        else 0
    )

    actual_bonos = (
        total_bonos / valor_total * 100
        if valor_total > 0
        else 0
    )

    actual_fondos = (
        (total_inmobiliarios + total_bancarios)
        / valor_total * 100
        if valor_total > 0
        else 0
    )

    actual_depositos = (
        total_depositos / valor_total * 100
        if valor_total > 0
        else 0
    )

    rebalanceo = pd.DataFrame({

        "Activo": [
            "Acciones",
            "Bonos",
            "Fondos",
            "Depósitos"
        ],

        "Actual (%)": [
            actual_acciones,
            actual_bonos,
            actual_fondos,
            actual_depositos
        ],

        "Objetivo (%)": [
            objetivo_acciones,
            objetivo_bonos,
            objetivo_fondos,
            objetivo_depositos
        ]

    })

    rebalanceo["Diferencia"] = (
        rebalanceo["Objetivo (%)"]
        -
        rebalanceo["Actual (%)"]
    )

    st.dataframe(
        rebalanceo,
        use_container_width=True
    )


if opcion == "Reportes":

    st.header(
        "Reportes"
    )

    if st.button(
        "Generar Reporte Excel"
    ):

        archivo = (
            generar_excel_completo()
        )

        st.success(
            "Reporte generado correctamente."
        )

        with open(
            archivo,
            "rb"
        ) as f:

            st.download_button(
                "Descargar Excel",
                f,
                file_name="Reporte_Ejecutivo.xlsx"
            )

    st.divider()

    if st.button(
        "Generar Reporte PDF"
    ):

        archivo_pdf = (
            generar_pdf_ejecutivo()
        )

        with open(
            archivo_pdf,
            "rb"
        ) as f:

            st.download_button(
                "Descargar PDF",
                f,
                file_name="Reporte_Ejecutivo.pdf"
            )