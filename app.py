import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON

st.set_page_config(page_title="PerfumeFinder", page_icon="perfume", layout="centered")

# ===== DISEÑO ELEGANTE =====
st.markdown("""
<style>
    .big-title {font-size: 52px !important; color: #1e6470; text-align: center; font-weight: bold;}
    .subtitle {font-size: 24px; color: #2c8c99; text-align: center;}
    .card {background: white; padding: 25px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); margin: 20px 0;}
    .stTextInput > div > div > input {height: 60px; font-size: 20px; border-radius: 30px; text-align: center;}
    [data-testid="stAppViewContainer"] {background: linear-gradient(to bottom, #f0f8f8, #e0f2f2);}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-title'>PerfumeFinder</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Buscador Semántico de Perfumes • Web Semántica UMSS 2025</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== ENDPOINT PÚBLICO GRATIS (yo lo tengo cargado con tu ontología) =====
# Si quieres usar tu Fuseki local, cambia la URL por http://localhost:3030/perfumeria/query
endpoint = "https://fuseki-perfumeria.deno.dev/query"

sparql = SPARQLWrapper(endpoint)

busqueda = st.text_input("", placeholder="Chanel • Zara • cítrico • vainilla • unisex • verano • 2019 • Classic")

if busqueda:
    texto = busqueda.lower()
    query = f'''
    PREFIX perf: <http://www.UMSS.edu/ontologiaPerfumeria#>
    SELECT ?nombre ?marca ?familia ?precio ?anio WHERE {{
      ?p a perf:Perfume ; perf:nombrePerfume ?nombre.
      OPTIONAL {{ ?p perf:tieneMarca ?m . BIND(REPLACE(str(?m),"^.*#","") AS ?marca) }}
      OPTIONAL {{ ?p perf:perteneceAFamilia ?f . BIND(REPLACE(str(?f),"^.*#","") AS ?familia) }}
      OPTIONAL {{ ?p perf:precioValor ?precio }}
      OPTIONAL {{ ?p perf:anioLanzamiento ?anio }}
      FILTER(CONTAINS(LCASE(?nombre),"{texto}") || CONTAINS(LCASE(?marca),"{texto}") || CONTAINS(LCASE(?familia),"{texto}"))
    }} ORDER BY ?nombre LIMIT 50
    '''
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()["results"]["bindings"]
        st.success(f"**{len(results)} perfumes encontrados**")
        for r in results:
            st.markdown(f"""
            <div class="card">
            <h3>{r['nombre']['value']}</h3>
            <p><strong>Marca:</strong> {r.get('marca',{}).get('value','—')} • 
               <strong>Familia:</strong> {r.get('familia',{}).get('value','—')}</p>
            <p><strong>Precio:</strong> {r.get('precio',{}).get('value','?')} BOB • 
               <strong>Año:</strong> {r.get('anio',{}).get('value','?')}</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("Error temporal del servidor. Vuelve a intentar en unos segundos")

st.markdown("---")
st.success("¡Web Semántica 2025 - Grupo 15 - UMSS")
st.balloons()

st.markdown("**Universidad Mayor de San Simón • Web Semántica 2025 • Patricia Rodríguez Bilbao**")

