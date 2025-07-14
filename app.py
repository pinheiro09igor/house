import streamlit as st
import pandas as pd
from datetime import datetime
import os
from urllib.parse import quote_plus
from st_copy_to_clipboard import st_copy_to_clipboard
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Festa em Ouro Branco!",
    page_icon="🎉",
    layout="wide"
)


def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo CSV, criando o arquivo se ele não existir."""
    if not os.path.exists(nome_arquivo):
        if 'convidados' in nome_arquivo:
            df = pd.DataFrame(columns=["Nome", "Dorme na festa?", "Data"])
        else:
            df = pd.DataFrame(columns=["Nome", "Mensagem", "Data"])
        df.to_csv(nome_arquivo, index=False)
    return pd.read_csv(nome_arquivo)


def salvar_dados(df, nome_arquivo):
    """Salva o DataFrame em um arquivo CSV."""
    df.to_csv(nome_arquivo, index=False)


ARQUIVO_CONVIDADOS = "convidados.csv"
ARQUIVO_COMENTARIOS = "comentarios.csv"
df_convidados = carregar_dados(ARQUIVO_CONVIDADOS)
df_comentarios = carregar_dados(ARQUIVO_COMENTARIOS)


def aplicar_css():
    st.markdown("""
    <style>
        /* Fundo com gradiente sutil e imagem de montanha */
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)),
                              url("https://images.unsplash.com/photo-1598141022209-226e6d3a95b3?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            color: #E0E0E0; /* Texto principal com cor mais suave */
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #FFC107; /* Cor de ouro/âmbar para títulos */
            font-family: 'Georgia', serif;
        }

        /* Botões */
        .stButton>button {
            background-color: #FFC107;
            color: #1E2A38;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FFA000;
        }
        
        /* Containers e expanders */
        .stExpander, .stForm {
            background-color: rgba(30, 42, 56, 0.9); /* Fundo semi-transparente para seções */
            border-radius: 10px;
            border: 1px solid #FFC107;
            padding: 1rem;
        }

        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #334155;
            color: #E0E0E0;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)


aplicar_css()



def secao_convite():
    st.title("⛰️ Taaa cheganu... a Festa! 🍻")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🗓️ Data e Hora:")
        st.write("**19 de Julho de 2024**")
        st.write("**A partir das 10:00**")

    with col2:
        st.subheader("📍 Destino:")
        st.write("**Ouro Branco/MG**")
        st.write("Um canto especial nas montanhas de Minas!")

    st.markdown("---")
    st.write("""
    Estão mais uma vez, todos convidados(as) para assar uma carne, 
    tomar uma cerva/suco/refri, aproveitar a vista e o frio bão de Minas!
    """)
    st.markdown("---")



def secao_rsvp():
    st.header("✅ Bora Confirmar Presença?")

    if 'form_visivel' not in st.session_state:
        st.session_state.form_visivel = False

    if st.button("Sim, eu vou!"):
        st.session_state.form_visivel = True

    if st.session_state.form_visivel:
        with st.form("form_confirmacao", clear_on_submit=True):
            nome = st.text_input(
                "Seu nome:", placeholder="Digite seu nome completo aqui")
            dormir = st.checkbox("Vou precisar de um cantinho pra dormir! 🛌")

            submitted = st.form_submit_button("Enviar Confirmação")

            if submitted:
                if not nome:
                    st.warning("Por favor, preencha seu nome!")
                else:
                    global df_convidados

                    if nome.lower() in df_convidados['Nome'].str.lower().tolist():
                        st.warning(
                            f"{nome}, você já confirmou! Se precisar alterar algo, me avise no zap.")
                    else:
                        opcao_dormir = "Sim, com certeza!" if dormir else "Não, só vou pra bagunça!"
                        novo_convidado = pd.DataFrame([{
                            "Nome": nome,
                            "Dorme na festa?": opcao_dormir,
                            "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
                        }])
                        df_convidados = pd.concat(
                            [df_convidados, novo_convidado], ignore_index=True)
                        salvar_dados(df_convidados, ARQUIVO_CONVIDADOS)

                        st.success(
                            f"Show, {nome}! Sua presença está confirmada. Nos vemos lá!")
                        st.balloons()
                        st.session_state.form_visivel = False



def secao_lista_convidados():
    st.header("😎 Galera que já confirmou:")
    if not df_convidados.empty:
        df_display = df_convidados[["Nome", "Dorme na festa?"]].copy()
        df_display.rename(columns={
                          "Nome": "Convidado(a)", "Dorme na festa?": "Vai Pernoitar?"}, inplace=True)
        st.table(df_display.style.hide(axis="index"))
    else:
        st.info("Ninguém confirmou ainda. Seja o primeiro!")




def secao_localizacao():
    st.header("🗺️ Como Chegar na Base")
    st.markdown("---")

    rua = st.secrets["rua"]
    numero = st.secrets["numero_e_comp"]
    bairro = st.secrets["bairro"]
    cidade = st.secrets["cidade_estado"]
    lat = st.secrets["latitude"]
    lon = st.secrets["longitude"]

    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(
            '<p style="font-size: 100px; text-align: center;">🏡</p>', unsafe_allow_html=True)

    with col2:
        st.subheader("Nosso Canto em Ouro Branco")

        st.markdown(f"""
        - **Endereço:** {rua}, {numero}
        - **Bairro:** {bairro}
        - **Cidade:** {cidade}
        - **Ponto de Referência:** *Adicione um aqui se quiser (ex: "Próximo à Praça de Eventos")*
        """)

        endereco_completo = f"{rua}, {numero} - {bairro}, {cidade}"
        st_copy_to_clipboard(
            "Clique aqui para copiar o endereço completo ✨", endereco_completo, key="copy_button")

    st.markdown("---")

    st.subheader("Vista Aérea do Nosso Pedaço de Chão")

    map_url = f"https://maps.google.com/maps?q={lat},{lon}&z=16&t=k&output=embed"

    map_html = f"""
        <div style="border-radius: 15px; overflow: hidden; border: 2px solid #FFC107;">
            <iframe
                src="{map_url}"
                width="100%"
                height="400"
                style="border:0;"
                allowfullscreen=""
                loading="lazy">
            </iframe>
        </div>
    """

    components.html(map_html, height=410)

    st.subheader("Trace sua Rota")
    origem = st.text_input("Digite seu endereço de partida:",
                           placeholder="Ex: Rua da Saudade, 123, Belo Horizonte")

    if 'rota_gerada' not in st.session_state:
        st.session_state.rota_gerada = False

    if st.button("Gerar Rota no Google Maps"):
        if origem:
            st.session_state.rota_gerada = True
            st.session_state.origem = origem
        else:
            st.warning("Por favor, digite um ponto de partida.")
            st.session_state.rota_gerada = False

    if st.session_state.rota_gerada and st.session_state.get('origem'):
        destino_encoded = quote_plus(endereco_completo)
        origem_encoded = quote_plus(st.session_state.origem)
        url_rota = f"https://www.google.com/maps/dir/{origem_encoded}/{destino_encoded}"
        link_html = f'<p style="text-align: center; margin-top: 20px;"><a href="{url_rota}" target="_blank" style="background-color: #FFC107; color: #1E2A38; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; border: 2px solid #FFA000;">✔️ Rota Gerada! Clique aqui para abrir no Google Maps</a></p>'
        st.markdown(link_html, unsafe_allow_html=True)



def secao_faq():
    st.header("🤔 Dúvidas Frequentes (FAQ)")

    with st.expander("O que devo levar?"):
        st.write("""
        *Resposta de um colaborador anônimo:* 
        > Uma peça de carne de sua preferência e a gelada! 🥩🍻
        """)

    with st.expander("Posso levar meu pet? 🐾"):
        st.write("""
        *Resposta de outro colaborador anônimo:* 
        > Kira e Killua estarão responsáveis pela estadia do seu pet no melhor modo 'gasto energético'. Pode trazer! 🐶
        """)

    with st.expander("E para dormir?"):
        st.write("""
        *Resposta de outro colaborador anônimo:* 
        > Se tiver colchão inflável, pode trazer. No mais, traga roupa quente para auxiliar a resistir à hipotermia... é sério, faz frio! 🥶
        """)



def secao_comentarios():
    st.header("💬 Deixe seu Recado pra Galera!")

    with st.form("form_comentario", clear_on_submit=True):
        nome_comentario = st.text_input("Seu nome:", key="nome_comentario")
        mensagem = st.text_area(
            "Sua mensagem:", placeholder="Ex: 'Não vejo a hora!' ou 'Vou levar pão de alho!'")

        submit_comentario = st.form_submit_button("Publicar Recado")

        if submit_comentario:
            if nome_comentario and mensagem:
                global df_comentarios
                novo_comentario = pd.DataFrame([{
                    "Nome": nome_comentario,
                    "Mensagem": mensagem,
                    "Data": datetime.now().strftime("%d/%m às %H:%M")
                }])
                df_comentarios = pd.concat(
                    [df_comentarios, novo_comentario], ignore_index=True)
                salvar_dados(df_comentarios, ARQUIVO_COMENTARIOS)
                st.success("Seu recado foi enviado!")
            else:
                st.warning("Preencha o nome e a mensagem, uai!")

    st.subheader("Mural de Recados")
    if not df_comentarios.empty:
        for index, row in df_comentarios.iloc[::-1].iterrows():
            st.markdown(f"**{row['Nome']}** *({row['Data']})*:")
            st.info(f"> {row['Mensagem']}")
    else:
        st.write("Ainda não há recados no mural.")



def rodape():
    st.markdown("---")
    st.write("Feito com ☕ e Python por um anfitrião animado.")
    st.write("Nos vemos na festa!")



def main():
    secao_convite()
    st.markdown("---")
    secao_rsvp()
    st.markdown("---")
    secao_lista_convidados()
    st.markdown("---")
    secao_localizacao()
    st.markdown("---")
    secao_faq()
    st.markdown("---")
    secao_comentarios()
    st.markdown("---")
    rodape()


if __name__ == "__main__":
    main()
