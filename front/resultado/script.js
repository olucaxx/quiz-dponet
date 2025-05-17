function carregarResultados() {
    const resultadoQuiz = JSON.parse(sessionStorage.getItem('resultadoQuiz'));

    if (resultadoQuiz) {
        const acertosElement = document.getElementById('acertos');
        acertosElement.textContent = `Você acertou ${resultadoQuiz.acertos} de 15 questões`;
        
    } else {
        console.log("Nenhum resultado encontrado.");
    }
}

carregarResultados();
