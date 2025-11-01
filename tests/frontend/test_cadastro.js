// Script para testar o cadastro programaticamente
async function testarCadastro() {
    const formData = {
        cnpj: "60.331.021/0001-11",
        razao_social: "GREEN JOBS BRASIL INOVA SIMPLES (I.S.)",
        email: "contato@greenjobsbrasil.com.br",
        senha: "senha123",
        telefone: "(32) 98844-7227",
        website: "https://greenjobsbrasil.com.br",
        descricao: "Empresa focada em soluções sustentáveis e inovação",
        ods_tags: [7, 13, 15],
        score_verde: 30
    };

    try {
        const response = await fetch('/api/empresas/cadastro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        console.log('Status:', response.status);
        const result = await response.json();
        console.log('Resultado:', result);

        if (response.ok) {
            console.log('✅ Cadastro realizado com sucesso!');
        } else {
            console.error('❌ Erro no cadastro:', result.detail);
        }
    } catch (error) {
        console.error('❌ Erro na comunicação:', error);
    }
}

// Executar teste
testarCadastro();