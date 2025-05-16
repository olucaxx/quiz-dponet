function carregarResultados() {
    const resultadoQuiz = JSON.parse(sessionStorage.getItem('resultadoQuiz'));

    if (resultadoQuiz) {
        const acertosElement = document.getElementById('acertos');
        acertosElement.textContent = `Você acertou ${resultadoQuiz.acertos} de ${resultadoQuiz.total} questões`;
        
        if (resultadoQuiz.observacoes.length > 0) { 
            const observacoesContainer = document.getElementById('container-observacoes');
            resultadoQuiz.observacoes.forEach((observacao) => {
                const observacaoElement = document.createElement('p');
                observacaoElement.textContent = `${observacao.numQuestao} - ${observacao.observacao}`;
                observacoesContainer.appendChild(observacaoElement);
            });
        } else {
            const observacaoElement = document.createElement('p');
            observacaoElement.textContent = "Todas as questões foram respondidas corretamente, parabéns!";
            const observacoesContainer = document.getElementById('container-observacoes');
            observacoesContainer.appendChild(observacaoElement); // Adiciona o elemento no DOM
        }
    } else {
        console.log("Nenhum resultado encontrado.");
    }
}

carregarResultados();
