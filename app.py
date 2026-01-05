# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VSM recursivo - protótipo", layout="wide")

# Lê query params para saber qual "view" mostrar
qp = st.experimental_get_query_params()
view = qp.get("view", [None])[0]  # ex: "O1" ou None

# --- Funções para gerar Mermaid ---
def mermaid_html(mermaid_code: str, height: int = 600) -> str:
    """
    Monta o HTML que carrega mermaid.js e renderiza o diagrama.
    securityLevel: 'strict' para reduzir superfície de ataque.
    """
    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
      <style>body{{margin:0;padding:8px;font-family:Inter,system-ui,Segoe UI,Roboto}}</style>
      <script>
        mermaid.initialize({{ startOnLoad: true, securityLevel: 'strict' }});
        document.addEventListener("DOMContentLoaded", function(){{
          if (typeof mermaid === 'object') {{
             mermaid.init(undefined, document.querySelectorAll('.mermaid'));
          }}
        }});
      </script>
    </head>
    <body>
      <div class="mermaid">
{mermaid_code}
      </div>
    </body>
    </html>
    """
    return html

# --- Código Mermaid principal (o que você forneceu), com click links adicionados ---
main_mermaid = r'''
flowchart TB
    %% =========================
    %% SISTEMA 1 – FAIXA OPERACIONAL
    %% =========================
    subgraph S1["Sistema 1 – Operações"]
        direction LR
        O1["Operação 1"]
        O2["Operação 2"]
        O3["Operação 3"]
        O4["Operação 4"]
        O5["Operação 5"]
        O6["Operação 6"]
    end

    %% =========================
    %% SISTEMAS DO PRESENTE
    %% =========================
    S2["Sistema 2
Coordenação"]

    S3["Sistema 3
Gestão"]

    S3S["Sistema 3*
Auditoria"]

    %% =========================
    %% SISTEMAS REFLEXIVOS
    %% =========================
    S5["Sistema 5
Política e Identidade"]

    S4["Sistema 4
Inteligência"]

    %% =========================
    %% AMBIENTE
    %% =========================
    ENV["Ambiente Externo"]

    %% =========================
    %% CONEXÕES OPERACIONAIS
    %% =========================
    ENV <--> S1

    S1 --> S2

    S2 --> S3
    S3 --> S1
    

    S3S -.-> S1

    %% =========================
    %% CONEXÕES ESTRATÉGICAS
    %% =========================
    S3 <--> S4
    S3 <--> S3S
    S4 <--> ENV

    S5 --> S3
    S5 --> S4

    %% =========================
    %% ESTILOS
    %% =========================
    classDef s1 fill:#dbeafe,stroke:#2563eb,color:#000000;
    classDef s2 fill:#fef3c7,stroke:#d97706,color:#000000;
    classDef s3 fill:#fed7aa,stroke:#c2410c,color:#000000;
    classDef s3s fill:#fecaca,stroke:#b91c1c,stroke-dasharray:4,color:#000000;
    classDef s4 fill:#dcfce7,stroke:#15803d,color:#000000;
    classDef s5 fill:#f3e8ff,stroke:#7e22ce,color:#000000;
    classDef env fill:#eeeeee,stroke:#666,color:#000000
    
    class O1,O2,O3,O4,O5,O6 s1;
    class S2 s2;
    class S3 s3;
    class S3S s3s;
    class S4 s4;
    class S5 s5;
    class ENV env;
'''

# adiciona click links (rota via query param). isso força reload da página com ?view=O1
click_lines = """
click O1 "/?view=O1" "Abrir Operação 1"
click O2 "/?view=O2" "Abrir Operação 2"
click O3 "/?view=O3" "Abrir Operação 3"
click O4 "/?view=O4" "Abrir Operação 4"
click O5 "/?view=O5" "Abrir Operação 5"
click O6 "/?view=O6" "Abrir Operação 6"
"""

# --- Sub-diagrama (modelo) quando o usuário clica em O1..O6 ---
def op_subdiagram(op_id: str) -> str:
    """
    Gera um pequeno sub-diagrama (recursão prática).
    op_id: "O1", "O2", ...
    """
    label = f"Detalhe {op_id}"
    # Exemplo simples: 3 passos e um retorno (você pode personalizar)
    sub = f'''
flowchart TB
    %% Sub-diagrama para {op_id}
    BACK(["← Voltar ao VSM"]) 
    subgraph OP["{label}"]
        direction LR
        A["Entrada / Solicitação"]
        B["Atividade principal"]
        C["Saída / Entrega"]
    end

    BACK --> ROOT["Voltar"]
    A --> B --> C

    click BACK "/" "Voltar ao diagrama principal"
'''
    return sub

# --- RENDERIZAÇÃO na interface Streamlit ---
st.title("VSM recursivo — protótipo (Streamlit + Mermaid)")

if view is None:
    st.markdown("**Visão principal (clique em uma operação para abrir o sub-diagrama)**")
    # juntamos o main_mermaid + click_lines
    full_main = main_mermaid + "\n" + click_lines
    html = mermaid_html(full_main, height=700)
    components.html(html, height=700, scrolling=True)
else:
    # exibir breadcrumb simples e o sub-diagrama correspondente
    st.markdown(f"**Visão recursiva:** `{view}`  — (protótipo: apenas 1 nível de recursão)")
    st.write("Clique em **← Voltar ao VSM** dentro do diagrama ou use o botão abaixo.")
    if st.button("Voltar ao diagrama principal"):
        # limpa query params ao recarregar
        st.experimental_set_query_params()
        st.experimental_rerun()

    sub_mermaid = op_subdiagram(view)
    html = mermaid_html(sub_mermaid, height=500)
    components.html(html, height=500, scrolling=True)

# --- Rodapé com dicas rápidas ---
st.markdown("---")
st.caption(
    "Protótipo: links via query-param (reload). Para navegação sem reload, implementar componente custom (postMessage) ou usar um component React."
)
