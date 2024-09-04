import streamlit as st
from scipy.stats import binom

def encontrar_plano_amostral(TAMANHO_LOTE, TAMANHO_AMOSTRA, QUANT_DEFEITUOSOS, TAXA_DEF_FORNECEDOR, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX, DESPESA, CUSTO_UNI, LOTES):
  progresso = st.progress(0)
  status_text = st.empty()
  for TAMANHO_AMOSTRA in range(1, TAMANHO_LOTE + 1):
    for aceitacao_maxima in range(TAMANHO_AMOSTRA + 1):
      risco_fornecedor = 1 - binom.cdf(aceitacao_maxima, TAMANHO_AMOSTRA, NQA)
      risco_consumidor = binom.cdf (aceitacao_maxima, TAMANHO_AMOSTRA, PTDL)
      PA_def_forn = binom.cdf(QUANT_DEFEITUOSOS, TAMANHO_AMOSTRA, TAXA_DEF_FORNECEDOR)
      ITM = QUANT_DEFEITUOSOS + (1-PA_def_forn)*(TAMANHO_LOTE-QUANT_DEFEITUOSOS)
      custo_inspecionados = LOTES*ITM*CUSTO_UNI
      custo_deslocamento = LOTES*(1-PA_def_forn)*DESPESA
      custo_inspecao = custo_inspecionados + custo_deslocamento    
      progresso.progress (TAMANHO_AMOSTRA / TAMANHO_LOTE)
      status_text.text(f' Calculando: {TAMANHO_AMOSTRA}/{TAMANHO_LOTE} amostras, aceitação máxima: {aceitacao_maxima}') 
      if risco_fornecedor <= RISCO_FORNECEDOR_MAX and risco_consumidor <= RISCO_CONSUMIDOR_MAX: 
        return aceitacao_maxima, risco_fornecedor, risco_consumidor
      return custo_deslocamento, custo_inspecionados, custo_inspecao
  return None, None, None, None

st.title('Aplicativo WEB')

TAMANHO_LOTE = st.number_input('Tamanho do Lote:', min_value=1, step=1)
TAMANHO_AMOSTRA = st.number_input('Tamanho da amostra:', min_value=1, step=1)
QUANT_DEFEITUOSOS = st.number_input('Quantidade máxima de defeituosos:', min_value=1, step=1)
TAXA_DEF_FORNECEDOR = st.number_input('Taxa de defeituosos do fornecedor:', format="%.3f")
NQA = st.number_input('NQA:', min_value=0.0, step=0.01, format="%.3f")
PTDL = st.number_input('PTDL:', min_value=0.0, step=0.01,format="%.3f")
RISCO_FORNECEDOR_MAX= st.number_input('Risco Fornec. Máx:', min_value=0.0, step=0.01, format="%.3f") 
RISCO_CONSUMIDOR_MAX= st.number_input('Risco Cons. Máx:', min_value=0.0, step=0.01, format="%.3f")
DESPESA= st.number_input('Despesa por lote reprovado:', min_value=1, value=200, step=1)
CUSTO_UNI= st.number_input('Custo unitário de inspeção:', min_value=0.0, value=0.75, step=0.01)
LOTES= st.number_input('Lotes:', min_value=1, value=22, step=1)

if st.button('Calcular Riscos e Custos'):
  risco_fornecedor, risco_consumidor, aceitacao_maxima, custo_deslocamento, custo_inspecionados, custo_inspecao = encontrar_plano_amostral(
    TAMANHO_LOTE, TAMANHO_AMOSTRA, QUANT_DEFEITUOSOS, TAXA_DEF_FORNECEDOR, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX, DESPESA, CUSTO_UNI, LOTES
  )

  if tamanho_amostra is not None:
    st.write(f'Risco do fornecedor: {risco_fornecedor:.3f}')
    st.write(f'Risco do consumidor: {risco_consumidor:.3f}')
    st.write(f'Indice de aceitação maxima: {aceitacao_maxima:}')
    st.write(f'Custo de deslocamento: {custo_deslocamento:}')
    st.write(f'Custo de inspecionados: {custo_inspecionados:}')
    st.write(f'Custo de inspeção total: {custo_inspecao:}')
  else:
    st.write("Nenhum risco encontrado com os parâmetros fornecidos.")
    st.write("Nenhum custo encontrado com os parâmetros fornecidos.")

