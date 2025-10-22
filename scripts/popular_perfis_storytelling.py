"""
Script para popular 3 perfis storytelling completos
Profissionais: João (Energia), Ana (Resíduos), Carlos (Água)
"""

import sqlite3
import json

def popular_perfis():
    conn = sqlite3.connect('gjb_dev.db')
    cursor = conn.cursor()
    
    # Profissional 2: João Pedro Costa - Especialista em Energia Renovável
    joao_historia = """Comecei minha jornada na área de energia há 8 anos, quando percebi o potencial transformador das 
energias renováveis no Brasil. Trabalhei em projetos de energia solar e eólica em 6 estados, sempre focado em tornar 
a energia limpa acessível e economicamente viável. Acredito que a transição energética não é só uma necessidade ambiental, 
mas também uma oportunidade econômica gigantesca para o país."""

    joao_motivacao = """Sou movido pela possibilidade de contribuir para um Brasil 100% renovável. Ver uma comunidade rural 
ganhando acesso à energia solar, reduzindo custos e impacto ambiental, é o que me faz acordar todos os dias com propósito."""

    joao_conquistas = [
        {
            "titulo": "Liderança em Projeto Solar de 50MW",
            "descricao": "Coordenei a implementação de usina solar que abastece 30 mil residências",
            "data": "2024",
            "icone": "☀️"
        },
        {
            "titulo": "Certificação Internacional PV",
            "descricao": "Photovoltaic Systems Professional Certificate - NABCEP",
            "data": "2023",
            "icone": "🎓"
        },
        {
            "titulo": "Prêmio Inovação Energética",
            "descricao": "Reconhecimento pela implementação de storage híbrido mais eficiente do setor",
            "data": "2022",
            "icone": "🏆"
        }
    ]

    joao_projetos = [
        {
            "titulo": "Usina Solar Fotovoltaica 50MW",
            "empresa": "Energy Solutions BR",
            "descricao": "Implementação completa de usina solar com capacidade de 50MW, incluindo estudos de viabilidade, engenharia, instalação e comissionamento.",
            "periodo": "Jan 2023 - Dez 2024",
            "resultados": ["50MW gerados", "30 mil casas abastecidas", "42 mil ton CO2 evitadas/ano", "ROI em 7 anos"],
            "ods": [7, 9, 13],
            "tecnologias": ["PVSyst", "AutoCAD", "PVSOL", "Módulos Bifaciais", "Inversores Centralizados"]
        },
        {
            "titulo": "Sistema de Armazenamento Híbrido",
            "empresa": "Renova Energia",
            "descricao": "Desenvolvimento e implementação de sistema híbrido solar + eólica com armazenamento em baterias de lítio para indústria.",
            "periodo": "Mar 2022 - Out 2022",
            "resultados": ["95% disponibilidade", "60% redução custo energia", "Sistema 100% autônomo"],
            "ods": [7, 12, 13],
            "tecnologias": ["Tesla Powerpack", "SCADA", "Gestão Energética AI"]
        }
    ]

    joao_idiomas = [
        {"idioma": "Português", "nivel": "Nativo"},
        {"idioma": "Inglês", "nivel": "Fluente"},
        {"idioma": "Espanhol", "nivel": "Intermediário"}
    ]

    cursor.execute("""
        UPDATE profissionais_esg 
        SET 
            historia_verde = ?,
            motivacao = ?,
            valores_pessoais = ?,
            objetivos_carreira = ?,
            conquistas_json = ?,
            portfolio_projetos_json = ?,
            idiomas_json = ?
        WHERE id = 2
    """, (
        joao_historia,
        joao_motivacao,
        "Inovação, Eficiência, Impacto Mensurável, Sustentabilidade Econômica",
        "Liderar a transição energética de grandes corporações para 100% renovável e desenvolver soluções de storage escaláveis.",
        json.dumps(joao_conquistas, ensure_ascii=False),
        json.dumps(joao_projetos, ensure_ascii=False),
        json.dumps(joao_idiomas, ensure_ascii=False)
    ))

    print("✅ João Pedro Costa atualizado (Energia Renovável)")

    # Profissional 3: Ana Beatriz Santos - Gestora de Resíduos Sólidos
    ana_historia = """Minha paixão pela economia circular começou há 6 anos, quando vi de perto o impacto dos resíduos mal 
gerenciados no meio ambiente. Desde então, trabalho para transformar resíduos em recursos, implementando programas de 
reciclagem e compostagem que já desviaram mais de 10 mil toneladas de materiais de aterros sanitários."""

    ana_motivacao = """Acredito que não existe 'lixo', apenas recursos no lugar errado. Meu objetivo é provar que economia 
circular é viável, lucrativa e essencial para um futuro sustentável."""

    ana_conquistas = [
        {
            "titulo": "Zero Waste em Indústria Alimentícia",
            "descricao": "Implementei programa que atingiu 98% de desvio de resíduos em 2 anos",
            "data": "2024",
            "icone": "♻️"
        },
        {
            "titulo": "Certificação ISO 14001",
            "descricao": "Auditora líder em Sistema de Gestão Ambiental",
            "data": "2023",
            "icone": "📋"
        },
        {
            "titulo": "10 mil Toneladas Desviadas",
            "descricao": "Total de resíduos desviados de aterros em projetos liderados",
            "data": "2019-2024",
            "icone": "🌍"
        }
    ]

    ana_projetos = [
        {
            "titulo": "Programa Zero Waste Industrial",
            "empresa": "EcoFood Brasil",
            "descricao": "Implementação completa de programa zero waste em fábrica de alimentos com 500 colaboradores, incluindo segregação, compostagem, reciclagem e valorização de resíduos.",
            "periodo": "Jan 2022 - Dez 2024",
            "resultados": ["98% desvio aterro", "3.200 ton/ano recicladas", "R$450k economia", "Zero resíduos perigosos"],
            "ods": [12, 13, 15],
            "tecnologias": ["Gestão de Resíduos", "Compostagem Industrial", "MRF", "Power BI"]
        },
        {
            "titulo": "Logística Reversa de Embalagens",
            "empresa": "RetornaPack",
            "descricao": "Estruturação de sistema de logística reversa para rede varejista com 120 lojas, atingindo meta de 25% de retorno de embalagens.",
            "periodo": "Mai 2021 - Dez 2021",
            "resultados": ["27% taxa retorno", "840 ton recuperadas", "Compliance PNRS", "150 pontos coleta"],
            "ods": [12, 17],
            "tecnologias": ["Sistema de Rastreamento", "Gestão de Stakeholders", "Educação Ambiental"]
        }
    ]

    ana_idiomas = [
        {"idioma": "Português", "nivel": "Nativo"},
        {"idioma": "Inglês", "nivel": "Avançado"},
        {"idioma": "Italiano", "nivel": "Básico"}
    ]

    cursor.execute("""
        UPDATE profissionais_esg 
        SET 
            historia_verde = ?,
            motivacao = ?,
            valores_pessoais = ?,
            objetivos_carreira = ?,
            conquistas_json = ?,
            portfolio_projetos_json = ?,
            idiomas_json = ?
        WHERE id = 3
    """, (
        ana_historia,
        ana_motivacao,
        "Circularidade, Pragmatismo, Colaboração, Educação Ambiental",
        "Expandir soluções de economia circular para PMEs e desenvolver tecnologias de valorização de resíduos orgânicos.",
        json.dumps(ana_conquistas, ensure_ascii=False),
        json.dumps(ana_projetos, ensure_ascii=False),
        json.dumps(ana_idiomas, ensure_ascii=False)
    ))

    print("✅ Ana Beatriz Santos atualizada (Gestão de Resíduos)")

    # Profissional 4: Carlos Eduardo Lima - Especialista em Recursos Hídricos
    carlos_historia = """Engenheiro ambiental com 10 anos de experiência em gestão de recursos hídricos. Iniciei minha carreira 
em consultorias ambientais e evoluí para liderar projetos de saneamento e reúso de água em indústrias. Já implementei sistemas 
que economizaram mais de 500 milhões de litros de água/ano, provando que eficiência hídrica é estratégica e lucrativa."""

    carlos_motivacao = """A água é o recurso mais precioso do planeta e o Brasil tem privilégio de abundância, mas precisamos 
usar com inteligência. Trabalho para que cada gota conte e seja reutilizada sempre que possível."""

    carlos_conquistas = [
        {
            "titulo": "500 Milhões de Litros Economizados",
            "descricao": "Total de água economizada em projetos de eficiência hídrica implementados",
            "data": "2015-2024",
            "icone": "💧"
        },
        {
            "titulo": "Sistema de Reúso Premiado",
            "descricao": "Projeto de reúso que serve como case internacional de eficiência",
            "data": "2023",
            "icone": "🏆"
        },
        {
            "titulo": "Certificação Alliance for Water Stewardship",
            "descricao": "Implementador certificado AWS para gestão sustentável da água",
            "data": "2022",
            "icone": "🎓"
        }
    ]

    carlos_projetos = [
        {
            "titulo": "Sistema de Reúso Industrial Completo",
            "empresa": "TechChem Indústria",
            "descricao": "Projeto e implementação de estação de tratamento e reúso de efluentes industriais com capacidade de 200m³/dia, permitindo reúso de 85% da água utilizada no processo.",
            "periodo": "Mar 2023 - Nov 2024",
            "resultados": ["85% reúso", "146 milhões L/ano economizados", "R$730k economia", "Outorga reduzida 60%"],
            "ods": [6, 9, 12],
            "tecnologias": ["ETE Compacta", "Ultrafiltração", "Osmose Reversa", "Monitoramento Online", "AutoCAD"]
        },
        {
            "titulo": "Gestão Hídrica em Condomínio Industrial",
            "empresa": "EcoLogistics Park",
            "descricao": "Implementação de sistema centralizado de captação, tratamento e distribuição de água para 18 empresas, com aproveitamento de água de chuva e tratamento de efluentes.",
            "periodo": "Jan 2021 - Ago 2022",
            "resultados": ["40% redução consumo", "Sistema de chuva 12 milhões L/ano", "18 empresas atendidas", "Certificação LEED Water"],
            "ods": [6, 11, 12],
            "tecnologias": ["Cisternas Modulares", "Sistema de Filtração", "Gestão Remota IoT", "Modelagem Hidráulica"]
        }
    ]

    carlos_idiomas = [
        {"idioma": "Português", "nivel": "Nativo"},
        {"idioma": "Inglês", "nivel": "Fluente"},
        {"idioma": "Francês", "nivel": "Intermediário"}
    ]

    cursor.execute("""
        UPDATE profissionais_esg 
        SET 
            historia_verde = ?,
            motivacao = ?,
            valores_pessoais = ?,
            objetivos_carreira = ?,
            conquistas_json = ?,
            portfolio_projetos_json = ?,
            idiomas_json = ?
        WHERE id = 4
    """, (
        carlos_historia,
        carlos_motivacao,
        "Eficiência, Sustentabilidade Hídrica, Inovação Tecnológica, Responsabilidade",
        "Desenvolver soluções de reúso em escala para saneamento básico e liderar consultoria especializada em segurança hídrica.",
        json.dumps(carlos_conquistas, ensure_ascii=False),
        json.dumps(carlos_projetos, ensure_ascii=False),
        json.dumps(carlos_idiomas, ensure_ascii=False)
    ))

    print("✅ Carlos Eduardo Lima atualizado (Recursos Hídricos)")

    conn.commit()
    conn.close()

    print("\n🎉 3 perfis storytelling completos populados!")
    print("\n📊 Resumo:")
    print("  - João (ID 2): Energia Renovável - 2 projetos, 3 conquistas")
    print("  - Ana (ID 3): Gestão de Resíduos - 2 projetos, 3 conquistas")
    print("  - Carlos (ID 4): Recursos Hídricos - 2 projetos, 3 conquistas")
    print("\n✅ Acesse:")
    print("  - João: http://127.0.0.1:8002/api/profissionais/perfil/2")
    print("  - Ana: http://127.0.0.1:8002/api/profissionais/perfil/3")
    print("  - Carlos: http://127.0.0.1:8002/api/profissionais/perfil/4")

if __name__ == "__main__":
    popular_perfis()
