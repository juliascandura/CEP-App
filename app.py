import streamlit as st
from scipy.stats import binom

def encontrar_plano_amostral (TAMANHO_LOTE, tamanho_amostra, quant_defeituosos, taxa_def_fornecedor, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX):
  progresso = st.progress(0)
  status_text = st.empty()
  for tamanho_amostra in range(1, TAMANHO_LOTE + 1):
    for aceitacao_maxima in range(tamanho_amostra + 1):
      risco_fornecedor = 1 - binom.cdf(aceitacao_maxima, tamanho_amostra, NQA)
      risco_consumidor = binom.cdf (aceitacao_maxima, tamanho_amostra, PTDL)
      PA_def_forn = binom.cdf(a, n, taxa_def_fornecedor)
      ITM = n + (1-PA_def_forn)*(TAMANHO_LOTE-quant_defeituosos)
      custo_inspecionados = lotes*ITM*custo_uni
      custo_deslocamento = lotes*(1-PA_def_forn)*despesa
      custo_inspecao = custo_inspecionados + custo_deslocamento    
      progresso.progress (tamanho_amostra / TAMANHO_LOTE)
      status_text.text(f' Calculando: {tamanho_amostra}/{TAMANHO_LOTE} amostras, aceitação máxima: {aceitacao_maxima}') 
      if risco_fornecedor <= RISCO_FORNECEDOR_MAX and risco_consumidor <= RISCO_CONSUMIDOR_MAX: 
        return tamanho_amostra, aceitacao_maxima, risco_fornecedor, risco_consumidor
  return None, None, None, None

st.title('Aplicativo WEB')

TAMANHO_LOTE = st.number_input('Tamanho do Lote:')
tamanho_amostra = st.number_input('Tamanho da amostra:')
quant_defeituosos = st.number_input('Quantidade máxima de defeituosos:')
taxa_def_fornecedor = st.number_input('Taxa de defeituosos do fornecedor:', format="%.3f")
NQA = st.number_input('NQA:', format="%.3f")
PTDL = st.number_input('PTDL:', format="%.3f")
RISCO_FORNECEDOR_MAX= st.number_input('Risco Fornec. Máx:', format="%.3f") 
RISCO_CONSUMIDOR_MAX= st.number_input('Risco Cons. Máx:', format="%.3f")
despesa= st.number_input('Despesa por lote reprovado:', min_value=0.0, value=200, step=1)
custo_uni= st.number_input('Custo unitário de inspeção:', min_value=0.0, value=0.75, step=1)
lotes= st.number_input('Lotes:', min_value=0.0, value=22)

if st.button('Calcular Riscos e Custos'):
  risco_fornecedor, risco_consumidor = encontrar_plano_amostral(
    TAMANHO_LOTE, tamanho_amostra, quant_defeituosos, taxa_def_fornecedor, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX
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

