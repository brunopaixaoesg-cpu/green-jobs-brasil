"""
Script para gerar apresentação PowerPoint - Green Jobs Brasil COP30
Requer: pip install python-pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def criar_apresentacao():
    # Criar apresentação
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Cores do tema
    VERDE_PRINCIPAL = RGBColor(11, 132, 87)
    VERDE_CLARO = RGBColor(24, 165, 116)
    VERDE_AGUA = RGBColor(123, 220, 181)
    AZUL_ESCURO = RGBColor(13, 92, 64)
    CINZA_TEXTO = RGBColor(44, 62, 80)
    AMARELO = RGBColor(243, 156, 18)
    
    # ==================== SLIDE 1: CAPA ====================
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Layout em branco
    
    # Fundo gradiente (simulado com retângulo)
    left = Inches(0)
    top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = VERDE_PRINCIPAL
    shape.line.color.rgb = VERDE_PRINCIPAL
    
    # Título
    left = Inches(1)
    top = Inches(2)
    width = Inches(8)
    height = Inches(1.5)
    title = slide.shapes.add_textbox(left, top, width, height)
    text_frame = title.text_frame
    text_frame.text = "🌱 Green Jobs Brasil"
    text_frame.paragraphs[0].font.size = Pt(60)
    text_frame.paragraphs[0].font.bold = True
    text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Subtítulo
    left = Inches(1)
    top = Inches(3.8)
    subtitle = slide.shapes.add_textbox(left, top, width, Inches(1))
    text_frame = subtitle.text_frame
    text_frame.text = "A Infraestrutura de Dados para a Transição Verde no Brasil"
    text_frame.paragraphs[0].font.size = Pt(24)
    text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Tagline
    top = Inches(5.2)
    tagline = slide.shapes.add_textbox(left, top, width, Inches(0.8))
    text_frame = tagline.text_frame
    text_frame.text = "Conectando pessoas, empresas e políticas públicas\npara acelerar a economia verde"
    text_frame.paragraphs[0].font.size = Pt(18)
    text_frame.paragraphs[0].font.italic = True
    text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # COP30
    top = Inches(6.5)
    cop = slide.shapes.add_textbox(left, top, width, Inches(0.5))
    text_frame = cop.text_frame
    text_frame.text = "Apresentação COP30 - Novembro 2025"
    text_frame.paragraphs[0].font.size = Pt(14)
    text_frame.paragraphs[0].font.color.rgb = VERDE_AGUA
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # ==================== SLIDE 2: O DESAFIO ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "🎯 O Desafio da Transição Verde"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "O Brasil vai criar 7 milhões de empregos verdes até 2030 (Revista Exame)"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = AMARELO
    p.space_after = Pt(20)
    
    problemas = [
        ("❌", "Não há taxonomia operacional de atividades verdes"),
        ("📊", "Dados dispersos e inacessíveis sobre empresas e vagas"),
        ("🔍", "Falta de transparência e risco de greenwashing"),
        ("🚧", "Desconexão entre mercado, educação e políticas públicas")
    ]
    
    for icon, texto in problemas:
        p = tf.add_paragraph()
        p.text = f"{icon}  {texto}"
        p.font.size = Pt(20)
        p.font.color.rgb = CINZA_TEXTO
        p.space_after = Pt(12)
        p.level = 0
    
    # ==================== SLIDE 3: A SOLUÇÃO ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "✨ Nossa Solução"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "Não somos 'só um site de emprego'"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = VERDE_PRINCIPAL
    p.space_after = Pt(20)
    
    solucoes = [
        "🧬 Taxonomia CNAE → ODS (versionada e auditável)",
        "📊 Base de dados viva (empresas + vagas + profissionais)",
        "🔌 API aberta para o ecossistema",
        "📈 Dashboards e inteligência para decisões",
        "🌳 Foco em bioeconomia e Amazônia"
    ]
    
    for texto in solucoes:
        p = tf.add_paragraph()
        p.text = texto
        p.font.size = Pt(20)
        p.font.color.rgb = CINZA_TEXTO
        p.space_after = Pt(14)
    
    # ==================== SLIDE 4: COMO FUNCIONA ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "⚙️ Como Funciona?"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    # Criar caixas de fluxo
    etapas = [
        ("1. Taxonomia\nVerde", "CNAE → ODS"),
        ("2. Base de\nDados", "Empresas + Vagas"),
        ("3. API\nAberta", "Integrações"),
        ("4. Dashboards", "Decisões")
    ]
    
    box_width = Inches(2)
    box_height = Inches(1.2)
    top = Inches(2.5)
    spacing = Inches(0.3)
    total_width = (box_width * 4) + (spacing * 3)
    left_start = (prs.slide_width - total_width) / 2
    
    for i, (titulo, subtitulo) in enumerate(etapas):
        left = left_start + (i * (box_width + spacing))
        
        # Caixa
        shape = slide.shapes.add_shape(1, left, top, box_width, box_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = VERDE_CLARO
        shape.line.color.rgb = VERDE_PRINCIPAL
        
        # Texto
        text_frame = shape.text_frame
        text_frame.clear()
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        p = text_frame.paragraphs[0]
        p.text = titulo
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        p = text_frame.add_paragraph()
        p.text = subtitulo
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        # Seta (exceto na última)
        if i < 3:
            arrow_left = left + box_width
            arrow_top = top + (box_height / 2) - Inches(0.15)
            arrow = slide.shapes.add_textbox(arrow_left, arrow_top, spacing, Inches(0.3))
            arrow_tf = arrow.text_frame
            arrow_tf.text = "→"
            arrow_tf.paragraphs[0].font.size = Pt(32)
            arrow_tf.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
            arrow_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Explicação abaixo
    left = Inches(1)
    top = Inches(4.5)
    width = Inches(8)
    height = Inches(2)
    textbox = slide.shapes.add_textbox(left, top, width, height)
    tf = textbox.text_frame
    
    items = [
        "• Classificamos CNAEs (atividades econômicas) em Core/Adjacent/Secondary",
        "• Mapeamos cada CNAE para ODS específicos (rastreável e versionado)",
        "• Integramos com Receita Federal para dados reais de empresas",
        "• API permite integração com SINE, educação, CRMs corporativos"
    ]
    
    for texto in items:
        p = tf.add_paragraph()
        p.text = texto
        p.font.size = Pt(16)
        p.font.color.rgb = CINZA_TEXTO
        p.space_after = Pt(8)
    
    # ==================== SLIDE 5: POR QUE SOMOS ÚNICOS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "🏆 Por Que Somos Únicos"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    # Criar 4 quadrantes
    diferenciais = [
        ("🇧🇷 Solução Brasileira", [
            "Baseado em CNAE",
            "Integração Receita Federal",
            "Foco Amazônia/Bioeconomia",
            "Alinhado com NDC"
        ]),
        ("🔗 API-First", [
            "Não é um silo fechado",
            "Integra SINE, educação",
            "Dados abertos",
            "Interoperável"
        ]),
        ("🛡️ Anti-Greenwashing", [
            "Critérios auditáveis",
            "Scoring transparente",
            "Rastreabilidade CNAE→ODS",
            "Versionamento"
        ]),
        ("🌳 Bioeconomia", [
            "Povos tradicionais",
            "Sociobiodiversidade",
            "Territorialização",
            "Energia descentralizada"
        ])
    ]
    
    box_width = Inches(3.5)
    box_height = Inches(2.5)
    h_spacing = Inches(0.5)
    v_spacing = Inches(0.4)
    left_start = Inches(1)
    top_start = Inches(2)
    
    for i, (titulo, items) in enumerate(diferenciais):
        col = i % 2
        row = i // 2
        left = left_start + (col * (box_width + h_spacing))
        top = top_start + (row * (box_height + v_spacing))
        
        # Caixa
        shape = slide.shapes.add_shape(1, left, top, box_width, box_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(232, 248, 245)
        shape.line.color.rgb = VERDE_PRINCIPAL
        shape.line.width = Pt(2)
        
        # Título
        title_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), box_width - Inches(0.4), Inches(0.5))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = titulo
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = VERDE_PRINCIPAL
        
        # Items
        items_box = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.7), box_width - Inches(0.6), Inches(1.6))
        tf = items_box.text_frame
        tf.clear()
        
        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(14)
            p.font.color.rgb = CINZA_TEXTO
            p.space_after = Pt(4)
    
    # ==================== SLIDE 6: IMPACTO NOS ODS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "🎯 Catalisador para os ODS"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    # Texto inicial
    left = Inches(1)
    top = Inches(1.8)
    width = Inches(8)
    textbox = slide.shapes.add_textbox(left, top, width, Inches(0.5))
    tf = textbox.text_frame
    p = tf.paragraphs[0]
    p.text = "Impactamos diretamente 12 dos 17 ODS:"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CINZA_TEXTO
    
    # Grid de ODS
    ods_list = [
        "ODS 4\nEducação", "ODS 5\nIgualdade", "ODS 6\nÁgua", "ODS 7\nEnergia",
        "ODS 8\nTrabalho", "ODS 9\nInovação", "ODS 10\nRedução", "ODS 11\nCidades",
        "ODS 12\nConsumo", "ODS 13\nClima", "ODS 15\nVida", "ODS 17\nParcerias"
    ]
    
    cols = 6
    rows = 2
    box_size = Inches(1.2)
    h_spacing = Inches(0.15)
    v_spacing = Inches(0.15)
    grid_width = (box_size * cols) + (h_spacing * (cols - 1))
    left_start = (prs.slide_width - grid_width) / 2
    top_start = Inches(2.8)
    
    for i, ods in enumerate(ods_list):
        col = i % cols
        row = i // cols
        left = left_start + (col * (box_size + h_spacing))
        top = top_start + (row * (box_size + v_spacing))
        
        shape = slide.shapes.add_shape(1, left, top, box_size, box_size)
        shape.fill.solid()
        shape.fill.fore_color.rgb = VERDE_PRINCIPAL
        shape.line.color.rgb = VERDE_PRINCIPAL
        
        text_frame = shape.text_frame
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = text_frame.paragraphs[0]
        p.text = ods
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
    
    # Como aceleramos
    top = Inches(5.3)
    textbox = slide.shapes.add_textbox(left, top, width, Inches(1.8))
    tf = textbox.text_frame
    
    p = tf.paragraphs[0]
    p.text = "Como Aceleramos as Metas:"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = VERDE_PRINCIPAL
    p.space_after = Pt(10)
    
    acoes = [
        "📍 Visibilidade territorial para direcionar recursos",
        "🎓 Requalificação guiada por demandas reais",
        "💼 Matching eficiente reduz desemprego",
        "📊 Evidências para políticas públicas e incentivos"
    ]
    
    for acao in acoes:
        p = tf.add_paragraph()
        p.text = acao
        p.font.size = Pt(14)
        p.font.color.rgb = CINZA_TEXTO
        p.space_after = Pt(6)
    
    # ==================== SLIDE 7: CASOS DE USO ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "💼 Casos de Uso"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    casos = [
        ("🏛️ Governos", [
            "Mapeamento territorial de empregos verdes",
            "Identificação de gaps de habilidades",
            "Incentivos direcionados (ex: score > 70)",
            "Dashboards públicos de accountability"
        ]),
        ("🏢 Empresas", [
            "Divulgação de vagas verdes",
            "Evidências ESG verificáveis",
            "Acesso a incentivos governamentais",
            "Marca empregadora sustentável"
        ]),
        ("👤 Profissionais", [
            "Trilhas de carreira verde",
            "Matching inteligente",
            "Capacitação direcionada",
            "Visibilidade para recrutadores"
        ]),
        ("💰 Investidores", [
            "Pipeline verificável",
            "Métricas de impacto ODS",
            "Due diligence facilitada",
            "Co-benefícios rastreáveis"
        ])
    ]
    
    box_width = Inches(4.2)
    box_height = Inches(2.3)
    h_spacing = Inches(0.3)
    v_spacing = Inches(0.3)
    left_start = Inches(0.8)
    top_start = Inches(2)
    
    for i, (titulo, items) in enumerate(casos):
        col = i % 2
        row = i // 2
        left = left_start + (col * (box_width + h_spacing))
        top = top_start + (row * (box_height + v_spacing))
        
        # Caixa
        shape = slide.shapes.add_shape(1, left, top, box_width, box_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(245, 247, 250)
        shape.line.color.rgb = VERDE_CLARO
        shape.line.width = Pt(2)
        
        # Título
        title_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.1), box_width - Inches(0.4), Inches(0.4))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = titulo
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = VERDE_PRINCIPAL
        
        # Items
        items_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.55), box_width - Inches(0.5), Inches(1.65))
        tf = items_box.text_frame
        tf.clear()
        
        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = CINZA_TEXTO
            p.space_after = Pt(3)
    
    # ==================== SLIDE 8: ROADMAP ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "🗺️ Roadmap 2025-2027"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    roadmap = [
        ("2025 - Fundação", [
            "120+ CNAEs verdes classificados",
            "Pilotos em 2-3 estados + 5 municípios",
            "Integração SINE e educação",
            "API pública documentada"
        ]),
        ("2026 - Escala Setorial", [
            "Expansão: saneamento, energia, construção",
            "Agro baixo carbono, resíduos, bioeconomia",
            "500k+ empresas com score verde",
            "Parcerias governos estaduais"
        ]),
        ("2027 - Infraestrutura Nacional", [
            "Interoperabilidade sistemas nacionais",
            "Dashboards públicos ODS × empregos",
            "Modelo de negócio sustentável",
            "Referência para políticas climáticas"
        ])
    ]
    
    box_width = Inches(9)
    box_height = Inches(1.5)
    v_spacing = Inches(0.25)
    left = Inches(0.5)
    top_start = Inches(2)
    
    for i, (fase, items) in enumerate(roadmap):
        top = top_start + (i * (box_height + v_spacing))
        
        # Caixa
        shape = slide.shapes.add_shape(1, left, top, box_width, box_height)
        
        # Cores alternadas
        if i == 0:
            cor = VERDE_AGUA
        elif i == 1:
            cor = VERDE_CLARO
        else:
            cor = VERDE_PRINCIPAL
            
        shape.fill.solid()
        shape.fill.fore_color.rgb = cor
        shape.line.color.rgb = VERDE_PRINCIPAL
        shape.line.width = Pt(2)
        
        # Título da fase
        title_box = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.15), Inches(2.5), Inches(0.4))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = fase
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Items
        items_text = "  •  ".join(items)
        items_box = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.6), box_width - Inches(0.6), Inches(0.8))
        tf = items_box.text_frame
        p = tf.paragraphs[0]
        p.text = items_text
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(255, 255, 255)
    
    # ==================== SLIDE 9: NÚMEROS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "📈 Potencial de Impacto"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    stats = [
        ("120+", "CNAEs Verdes\nClassificados"),
        ("500k+", "Empresas Mapeadas\n(meta 2026)"),
        ("7M", "Empregos Verdes\nBrasil até 2030"),
        ("12", "ODS\nImpactados")
    ]
    
    box_size = Inches(2)
    spacing = Inches(0.3)
    total_width = (box_size * 4) + (spacing * 3)
    left_start = (prs.slide_width - total_width) / 2
    top = Inches(2.5)
    
    for i, (numero, label) in enumerate(stats):
        left = left_start + (i * (box_size + spacing))
        
        # Caixa
        shape = slide.shapes.add_shape(1, left, top, box_size, box_size)
        shape.fill.gradient()
        shape.fill.gradient_angle = 45
        shape.fill.gradient_stops[0].color.rgb = VERDE_PRINCIPAL
        shape.fill.gradient_stops[1].color.rgb = AZUL_ESCURO
        shape.line.color.rgb = VERDE_PRINCIPAL
        
        # Número
        num_box = slide.shapes.add_textbox(left, top + Inches(0.4), box_size, Inches(0.6))
        tf = num_box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = numero
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        # Label
        label_box = slide.shapes.add_textbox(left, top + Inches(1.1), box_size, Inches(0.7))
        tf = label_box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.text = label
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
    
    # Texto complementar
    left = Inches(1)
    top = Inches(5.2)
    width = Inches(8)
    textbox = slide.shapes.add_textbox(left, top, width, Inches(1.5))
    tf = textbox.text_frame
    
    p = tf.paragraphs[0]
    p.text = "Operacionalizamos os ODS ao transformar metas abstratas em:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = VERDE_PRINCIPAL
    p.space_after = Pt(10)
    
    items = ["✓ Dados concretos", "✓ Trilhas práticas", "✓ Integrações sistêmicas", "✓ Dashboards acionáveis"]
    for item in items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(15)
        p.font.color.rgb = CINZA_TEXTO
        p.space_after = Pt(5)
    
    # ==================== SLIDE 10: O QUE BUSCAMOS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "🌍 O Que Buscamos na COP30"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.color.rgb = VERDE_PRINCIPAL
    
    objetivos = [
        ("🤝 Parcerias Institucionais", "Governos, ministérios, organismos internacionais"),
        ("📊 Parcerias de Dados", "Receita Federal, IBGE, SINE, plataformas educacionais"),
        ("🧪 Sandbox Regulatório", "Pilotos com flexibilidade LGPD, trabalhista, educação"),
        ("💰 Investimento/Grants", "Taxonomia, integrações, trilhas de requalificação")
    ]
    
    box_width = Inches(4.2)
    box_height = Inches(1.5)
    h_spacing = Inches(0.3)
    v_spacing = Inches(0.3)
    left_start = Inches(0.8)
    top_start = Inches(2.3)
    
    for i, (titulo, desc) in enumerate(objetivos):
        col = i % 2
        row = i // 2
        left = left_start + (col * (box_width + h_spacing))
        top = top_start + (row * (box_height + v_spacing))
        
        # Caixa
        shape = slide.shapes.add_shape(1, left, top, box_width, box_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 243, 205)
        shape.line.color.rgb = AMARELO
        shape.line.width = Pt(3)
        
        # Título
        title_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), box_width - Inches(0.4), Inches(0.5))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = titulo
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = AMARELO
        
        # Descrição
        desc_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.75), box_width - Inches(0.4), Inches(0.65))
        tf = desc_box.text_frame
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = CINZA_TEXTO
    
    # Chamada para ação
    left = Inches(1)
    top = Inches(5.8)
    width = Inches(8)
    cta_box = slide.shapes.add_textbox(left, top, width, Inches(1))
    tf = cta_box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    p = tf.paragraphs[0]
    p.text = "Green Jobs Brasil é o elo perdido entre compromissos climáticos e ação concreta"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = VERDE_PRINCIPAL
    p.alignment = PP_ALIGN.CENTER
    
    # ==================== SLIDE 11: CONTATO ====================
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Branco
    
    # Fundo
    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = VERDE_PRINCIPAL
    shape.line.color.rgb = VERDE_PRINCIPAL
    
    # Título
    left = Inches(1)
    top = Inches(2)
    width = Inches(8)
    title_box = slide.shapes.add_textbox(left, top, width, Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Vamos Conversar?"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Contatos
    top = Inches(3.5)
    contact_box = slide.shapes.add_textbox(left, top, width, Inches(2.5))
    tf = contact_box.text_frame
    
    contatos = [
        "📧 bruno@greenjobsbrasil.com.br",
        "📧 contato@greenjobsbrasil.com.br",
        "",
        "💬 WhatsApp: +55 (32) 99817-3407",
        "",
        "🔗 LinkedIn: /company/green-jobs-brasil",
        "📷 Instagram: @greenjobsbrasil"
    ]
    
    for i, contato in enumerate(contatos):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = contato
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(8)
    
    # Rodapé
    top = Inches(6.5)
    footer_box = slide.shapes.add_textbox(left, top, width, Inches(0.5))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Green Jobs Brasil • COP30 • Novembro 2025"
    p.font.size = Pt(14)
    p.font.color.rgb = VERDE_AGUA
    p.alignment = PP_ALIGN.CENTER
    
    # Salvar
    prs.save('docs/GreenJobsBrasil_COP30_Apresentacao.pptx')
    print("✅ Apresentação criada com sucesso!")
    print("📁 Arquivo: docs/GreenJobsBrasil_COP30_Apresentacao.pptx")
    print("📊 11 slides criados")

if __name__ == "__main__":
    try:
        criar_apresentacao()
    except ImportError:
        print("❌ Erro: Biblioteca python-pptx não instalada")
        print("Execute: pip install python-pptx")
        print("Depois rode novamente: python scripts/gerar_ppt_cop30.py")
