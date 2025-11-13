"""
Teste rápido das funcionalidades TSB.
"""
from api.data.taxonomia_tsb import (
    OBJETIVOS_TSB, 
    SETORES_TSB, 
    CRITERIOS_TSB,
    get_objetivo_by_id,
    get_objetivo_by_codigo,
    calcular_score_tsb
)
from api.utils.tsb_helpers import enriquecer_empresa_com_tsb

print("=" * 60)
print("TESTE TSB - Taxonomia Sustentável Brasileira")
print("=" * 60)

# Teste 1: Objetivos
print("\n1. OBJETIVOS TSB")
print(f"Total de objetivos: {len(OBJETIVOS_TSB)}")
print(f"Ambientais: {len([o for o in OBJETIVOS_TSB if o['tipo'] == 'ambiental'])}")
print(f"Sociais: {len([o for o in OBJETIVOS_TSB if o['tipo'] == 'social'])}")

# Teste 2: Setores
print("\n2. SETORES PRIORITÁRIOS")
print(f"Total de setores: {len(SETORES_TSB)}")
for setor in SETORES_TSB[:3]:
    print(f"  - {setor['nome']}: {len(setor['subsetores'])} subsetores")

# Teste 3: Critérios
print("\n3. CRITÉRIOS DE ELEGIBILIDADE")
for criterio, info in CRITERIOS_TSB.items():
    print(f"  - {criterio}: {info['nome']} ({info['peso']}pts)")

# Teste 4: Busca por ID
print("\n4. BUSCA POR ID")
obj = get_objetivo_by_id(1)
print(f"Objetivo 1: {obj['codigo']} - {obj['nome']}")

# Teste 5: Busca por código
print("\n5. BUSCA POR CÓDIGO")
obj = get_objetivo_by_codigo("EA")
print(f"Código EA: {obj['nome']}")

# Teste 6: Cálculo de score
print("\n6. CÁLCULO DE SCORE TSB")
criterios_exemplo = {
    "CS": True,
    "NPS": True,
    "SM": False
}
score = calcular_score_tsb(criterios_exemplo)
print(f"Critérios: {criterios_exemplo}")
print(f"Score: {score}/100")

# Teste 7: Enriquecimento de empresa
print("\n7. ENRIQUECIMENTO DE EMPRESA")
empresa_exemplo = {
    "cnpj": "12345678000199",
    "razao_social": "Energia Solar Brasil Ltda",
    "cnae_principal": "3511-5",
    "score_verde": 85
}
empresa_enriquecida = enriquecer_empresa_com_tsb(
    empresa_exemplo, 
    ["3511-5", "3513-1"]
)
print(f"Empresa: {empresa_enriquecida['razao_social']}")
print(f"TSB Elegível: {empresa_enriquecida['tsb_elegivel']}")
print(f"TSB Score: {empresa_enriquecida['tsb_score']}")
print(f"Objetivos: {empresa_enriquecida['tsb_objetivos']}")
print(f"Setores: {empresa_enriquecida['tsb_setores']}")
print(f"Badge: {empresa_enriquecida['tsb_badge']}")

print("\n" + "=" * 60)
print("TESTE CONCLUÍDO COM SUCESSO ✓")
print("=" * 60)
