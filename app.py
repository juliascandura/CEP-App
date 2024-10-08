import streamlit as st
from scipy.stats import binom

def encontrar_riscos(TAMANHO_LOTE, TAMANHO_AMOSTRA, QUANT_DEFEITUOSOS, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX):
  risco_fornecedor = 1 - binom.cdf(QUANT_DEFEITUOSOS, TAMANHO_AMOSTRA, NQA)
  risco_consumidor = binom.cdf (QUANT_DEFEITUOSOS, TAMANHO_AMOSTRA, PTDL)   
  return risco_fornecedor, risco_consumidor
    
def encontrar_custos(TAMANHO_LOTE, TAMANHO_AMOSTRA, QUANT_DEFEITUOSOS, TAXA_DEF_FORNECEDOR, DESPESA, CUSTO_UNI, LOTES):
  pa_def_forn = binom.cdf(QUANT_DEFEITUOSOS, TAMANHO_AMOSTRA, TAXA_DEF_FORNECEDOR)
  itm = QUANT_DEFEITUOSOS + (1-pa_def_forn)*(TAMANHO_LOTE-QUANT_DEFEITUOSOS)
  custo_inspecionados = LOTES*itm*CUSTO_UNI
  custo_deslocamento = LOTES*(1-pa_def_forn)*DESPESA
  custo_inspecao = custo_inspecionados + custo_deslocamento    
  return custo_deslocamento, custo_inspecionados, custo_inspecao


st.title('Aplicativo WEB - Inspeção por Amostragem')

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
ACEITACAO_MAXIMA = st.number_input('Aceitação máxima do lote:', min_value=1, step=1)

if st.button('Calcular Riscos'):
  risco_fornecedor, risco_consumidor = encontrar_riscos(
    TAMANHO_LOTE, TAMANHO_AMOSTRA, QUANT_DEFEITUOSOS, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX
  )
  if not risco_fornecedor is None:
    st.write(f'Risco do fornecedor: {risco_fornecedor:.3f}')
    st.write(f'Risco do consumidor: {risco_consumidor:.3f}')
    

if st.button('Calcular Custos'): 
  custo_deslocamento, custo_inspecionados, custo_inspecao = encontrar_custos(
     TAMANHO_LOTE, TAMANHO_AMOSTRA, QUANT_DEFEITUOSOS, TAXA_DEF_FORNECEDOR, DESPESA, CUSTO_UNI, LOTES
   )
  st.write(f'Custo de deslocamento: {custo_deslocamento:}')
  st.write(f'Custo de inspecionados: {custo_inspecionados:}')
  st.write(f'Custo de inspeção total: {custo_inspecao:}')
  

if st.button('Lote aceito ou não?'):
  if QUANT_DEFEITUOSOS <= ACEITACAO_MAXIMA:
    st.write('O lote foi aceito :)')
  if QUANT_DEFEITUOSOS > ACEITACAO_MAXIMA:
    st.write('O lote foi rejeitado :(')





  
