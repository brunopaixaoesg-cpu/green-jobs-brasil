# 📱 Auditoria de Responsividade e UX Mobile - Green Jobs Brasil

**Data**: 19 de Outubro de 2025  
**Objetivo**: Identificar problemas de UX mobile e criar plano de ação

---

## 📊 Status Atual das Páginas

### ✅ Páginas COM Media Queries
1. **Login/Registro**: `@media (max-width: 768px)` ✅
2. **Empresas Modernas**: `@media (max-width: 768px)` ✅
3. **Dashboard ML**: `@media (max-width: 768px)` ✅

### ❌ Páginas SEM Media Queries (CRÍTICO)
1. **Dashboard Profissional** (`profissionais/dashboard.html`) ❌
   - Problema: Stats cards em 4 colunas no mobile
   - Problema: Gráficos muito pequenos
   - Problema: Botões muito próximos
   
2. **Perfil Storytelling** (`perfil_storytelling.html`) ❌
   - Problema: Banner 300px desperdiça espaço no mobile
   - Problema: Foto de perfil 180px muito grande
   - Problema: Grid de conquistas quebra
   - Problema: Cards de projetos não empilham
   
3. **Edit Storytelling** (`edit_storytelling.html`) ❌
   - Problema: Formulário muito largo no mobile
   - Problema: Inputs de arrays (projetos, conquistas) difíceis de usar
   - Problema: Botões add/remove pequenos demais (< 44px)
   - Problema: Character counters podem quebrar layout

---

## 🎯 Problemas Identificados por Categoria

### 1. Layout e Espaçamento
- [ ] **Stats cards** não empilham em mobile (ficam 4 colunas espremidas)
- [ ] **Profile banner** muito alto (300px) no mobile
- [ ] **Foto de perfil** muito grande (180px) - ideal 80-100px mobile
- [ ] **Padding excessivo** em containers (40px lateral) - ideal 15-20px mobile
- [ ] **Cards de projetos** não responsivos (minmax quebra)

### 2. Touch Targets (WCAG)
- [ ] Botões "Editar Perfil" e "Compartilhar" podem estar < 44x44px
- [ ] Botões "Adicionar Conquista/Projeto" muito pequenos
- [ ] Links e ícones sem área clicável mínima
- [ ] Inputs de formulário podem ter altura < 44px

### 3. Tipografia
- [ ] **Títulos muito grandes** no mobile (h1 2.5rem = 40px)
- [ ] **Textos pequenos** em cards (14px pode ser ilegível)
- [ ] **Line-height** não otimizado para leitura mobile
- [ ] **Font-size** não escalável (usando rem/em inconsistente)

### 4. Navegação
- [ ] **Sem menu mobile** (hamburger ou bottom nav)
- [ ] **Breadcrumbs** ausentes (usuário não sabe onde está)
- [ ] **Botões voltar** faltando em páginas de edição
- [ ] **Tab bar** para alternar entre seções não existe

### 5. Performance
- [ ] **Imagens sem lazy loading** (banner, foto perfil)
- [ ] **Scripts sem defer/async** (Bootstrap, FontAwesome)
- [ ] **CSS não minificado** (inline styles pesados)
- [ ] **Sem service worker** (carregamento offline)

### 6. Acessibilidade
- [ ] **Contraste** pode estar baixo (light-green sobre branco)
- [ ] **Focus states** não visíveis em todos inputs
- [ ] **ARIA labels** faltando em botões de ícones
- [ ] **Alt text** faltando em imagens/ícones
- [ ] **Keyboard navigation** não testada

### 7. PWA/Meta Tags
- [ ] **Theme-color** não definido
- [ ] **Manifest.json** não existe
- [ ] **Apple-touch-icon** não configurado
- [ ] **OG tags** faltando (compartilhamento social)

---

## 📐 Breakpoints Recomendados

```css
/* Mobile First Approach */
:root {
    /* Mobile: 320-576px (padrão) */
}

/* Tablet: 576-768px */
@media (min-width: 576px) {
    /* Ajustes para tablets pequenos */
}

/* Tablet Large: 768-992px */
@media (min-width: 768px) {
    /* Ajustes para tablets grandes */
}

/* Desktop: 992-1200px */
@media (min-width: 992px) {
    /* Ajustes para desktop */
}

/* Large Desktop: 1200px+ */
@media (min-width: 1200px) {
    /* Ajustes para telas grandes */
}
```

---

## 🎨 Design System Necessário

### Cores (Design Tokens)
```css
:root {
    /* Primary */
    --color-primary-900: #14532d;
    --color-primary-700: #15803d;
    --color-primary-500: #22c55e; /* Primary */
    --color-primary-300: #86efac;
    --color-primary-100: #dcfce7;
    
    /* Grayscale */
    --color-gray-900: #111827;
    --color-gray-700: #374151;
    --color-gray-500: #6b7280;
    --color-gray-300: #d1d5db;
    --color-gray-100: #f3f4f6;
    
    /* Semantic */
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-error: #ef4444;
    --color-info: #3b82f6;
}
```

### Espaçamento
```css
:root {
    --spacing-xs: 0.25rem;   /* 4px */
    --spacing-sm: 0.5rem;    /* 8px */
    --spacing-md: 1rem;      /* 16px */
    --spacing-lg: 1.5rem;    /* 24px */
    --spacing-xl: 2rem;      /* 32px */
    --spacing-2xl: 3rem;     /* 48px */
}
```

### Tipografia
```css
:root {
    --font-size-xs: 0.75rem;   /* 12px */
    --font-size-sm: 0.875rem;  /* 14px */
    --font-size-base: 1rem;    /* 16px */
    --font-size-lg: 1.125rem;  /* 18px */
    --font-size-xl: 1.25rem;   /* 20px */
    --font-size-2xl: 1.5rem;   /* 24px */
    --font-size-3xl: 1.875rem; /* 30px */
    
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.75;
}
```

### Sombras
```css
:root {
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
    --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);
}
```

### Border Radius
```css
:root {
    --radius-sm: 0.375rem;  /* 6px */
    --radius-md: 0.5rem;    /* 8px */
    --radius-lg: 0.75rem;   /* 12px */
    --radius-xl: 1rem;      /* 16px */
    --radius-full: 9999px;  /* Círculo */
}
```

---

## 🔧 Plano de Ação Priorizado

### 🔴 ALTA PRIORIDADE (Impacto Imediato)

1. **Adicionar media queries nas 3 páginas principais**
   - Dashboard Profissional
   - Perfil Storytelling
   - Edit Storytelling
   
2. **Fixar touch targets** (mínimo 44x44px)
   - Todos os botões
   - Links clicáveis
   - Inputs de formulário
   
3. **Implementar grid responsivo**
   - Stats cards: 1 col mobile, 2 tablet, 4 desktop
   - Conquistas: 1 col mobile, 2 tablet, 3 desktop
   - Projetos: 1 col mobile, 1 tablet, 2 desktop

### 🟡 MÉDIA PRIORIDADE (Melhora UX)

4. **Criar sistema de design tokens**
   - Arquivo CSS centralizado
   - Variáveis para cores, espaçamentos, tipografia
   
5. **Otimizar tipografia mobile**
   - H1: 1.75rem mobile → 2.5rem desktop
   - Body: 0.875rem mobile → 1rem desktop
   - Line-height adequado
   
6. **Adicionar navegação mobile**
   - Bottom navigation bar ou
   - Hamburger menu com sidebar

### 🟢 BAIXA PRIORIDADE (Polimento)

7. **PWA basics**
   - Manifest.json
   - Theme-color
   - Icons
   
8. **Performance**
   - Lazy loading
   - Defer scripts
   - Minificação
   
9. **Acessibilidade**
   - ARIA labels
   - Focus states
   - Keyboard navigation

---

## 📱 Testes de Dispositivos Planejados

### Breakpoints para Testar
1. **iPhone SE** (375x667) - Mobile pequeno
2. **iPhone 12/13** (390x844) - Mobile médio
3. **Pixel 5** (393x851) - Mobile Android
4. **iPad Mini** (768x1024) - Tablet pequeno
5. **iPad Pro** (1024x1366) - Tablet grande
6. **Desktop HD** (1920x1080) - Desktop padrão

### Ferramentas
- Chrome DevTools Device Mode
- Firefox Responsive Design Mode
- BrowserStack (se disponível)
- Lighthouse Mobile Audit

---

## 📈 Métricas de Sucesso

### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

### Acessibilidade
- **Contraste**: Mínimo 4.5:1 (WCAG AA)
- **Touch Targets**: Mínimo 44x44px
- **Keyboard Nav**: 100% navegável

### Usabilidade
- **Todas as páginas** responsivas 320px-2560px
- **Formulários** utilizáveis em mobile
- **Tempo de tarefa** reduzido em 30% no mobile

---

## ✅ Checklist de Implementação

### Dashboard Profissional
- [ ] Media queries para 4 breakpoints
- [ ] Stats cards responsivos (col-12, col-sm-6, col-lg-3)
- [ ] Botões mínimo 44x44px
- [ ] Tipografia escalável
- [ ] Padding ajustado mobile (15px vs 40px desktop)

### Perfil Storytelling
- [ ] Banner altura reduzida mobile (200px vs 300px)
- [ ] Foto perfil reduzida mobile (100px vs 180px)
- [ ] Grid conquistas responsivo
- [ ] Cards projetos empilhados mobile
- [ ] Badges ODS menores mobile

### Edit Storytelling
- [ ] Form width 100% mobile
- [ ] Inputs altura mínima 44px
- [ ] Botões add/remove maiores
- [ ] Arrays (projetos/conquistas) otimizados mobile
- [ ] Validação inline melhorada

---

**Próximo passo**: Começar implementação com Dashboard Profissional (página mais usada)
