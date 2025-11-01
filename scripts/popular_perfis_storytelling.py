"""
Script para popular 3 perfis storytelling (simplificado)
Esta versão é uma migração conservadora: atualiza 3 perfis com JSON resumido
e usa o `scripts.db_wrapper.get_connection()` para acessar o banco canônico.
"""

from scripts.db_wrapper import get_connection
import json

def popular_perfis():
    sample_profiles = [
        {
            'id': 2,
            'historia_verde': 'Profissional com foco em Energia Renovável e projetos solares.',
            'motivacao': 'Contribuir para a transição energética.',
            'conquistas': [{'titulo': 'Projeto Solar 50MW', 'data': '2024'}],
            'projetos': [{'titulo': 'Usina Solar 50MW', 'periodo': '2023-2024'}],
            'idiomas': [{'idioma': 'Português', 'nivel': 'Nativo'}]
        },
        {
            'id': 3,
            'historia_verde': 'Especialista em Gestão de Resíduos com experiência em programas de circularidade.',
            'motivacao': 'Implementar soluções de economia circular em escala.',
            'conquistas': [{'titulo': 'Programa Zero Waste', 'data': '2024'}],
            'projetos': [{'titulo': 'Programa Zero Waste Industrial', 'periodo': '2022-2024'}],
            'idiomas': [{'idioma': 'Inglês', 'nivel': 'Avançado'}]
        },
        {
            'id': 4,
            'historia_verde': 'Engenheiro hídrico com atuação em reúso e eficiência hídrica.',
            'motivacao': 'Aumentar a eficiência hídrica em processos industriais.',
            'conquistas': [{'titulo': 'Sistema de Reúso', 'data': '2023'}],
            'projetos': [{'titulo': 'Reúso Industrial', 'periodo': '2023'}],
            'idiomas': [{'idioma': 'Inglês', 'nivel': 'Fluente'}]
        }
    ]

    with get_connection() as conn:
        cursor = conn.cursor()
        for p in sample_profiles:
            cursor.execute(
                """
                UPDATE profissionais_esg
                SET historia_verde = ?, motivacao = ?, conquistas_json = ?, portfolio_projetos_json = ?, idiomas_json = ?
                WHERE id = ?
                """,
                (
                    p['historia_verde'],
                    p['motivacao'],
                    json.dumps(p['conquistas'], ensure_ascii=False),
                    json.dumps(p['projetos'], ensure_ascii=False),
                    json.dumps(p['idiomas'], ensure_ascii=False),
                    p['id']
                )
            )
        conn.commit()

    print("\n🎉 3 perfis storytelling completos populados (versão simplificada)!")


if __name__ == "__main__":
    popular_perfis()
