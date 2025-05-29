function pegarTextoAviso(resultado) {
    if (resultado < 27) {
        return "<b>Resultados críticos!</b> Suas respostas indicam que sua empresa possui diversas violações graves, expondo-a a possíveis multas e danos reputacionais. Agende uma consulta urgente para evitar sanções!"
    }
    if (resultado < 47) {
        return "<b>Riscos altos!</b> Sua empresa tem diversas falhas operacionais significativas na conformidade com a LGPD! Agente uma consulta o quanto antes para evitar problemas!"
    }
    if (resultado < 67) {
        return "<b>Atenção necessária!</b> Sua empresa está parcialmente conforme, mas ainda com várias brechas. Agende uma consulta conosco para corrigir essas vulnerabilidades antes que se tornem problemas maiores!"
    }
    if (resultado < 94) {
        return "<b>Riscos detectados!</b> Sua empresa está no caminho certo, mas ainda apresenta algumas falhas. Não aguarde problemas maiores, agente uma consulta e fale conosco para corrigi-las!"
    }
    return "<b>Parabéns!</b> Sua empresa está bastante alinhada com a LGPD, mas lembre-se que ela exige atualizações constantes. Recomendamos que agende uma consulta para garantir que ela está completamente de acordo com as normas atuais!"
}

function carregarResultados() {
    const resultadoQuiz = JSON.parse(sessionStorage.getItem('resultadoQuiz'));

    if (resultadoQuiz) {
        const reguaSeta = document.getElementById("regua-seta")
        const textoAviso = document.getElementById("texto-aviso")
        const resultado = (resultadoQuiz.acertos / 15) * 100

        textoAviso.innerHTML = pegarTextoAviso(resultado)

        setTimeout(() => {
            reguaSeta.style.width = `calc(${resultado}% - 30px)`;
            reguaSeta.style.transition = "width 2s";
            reguaSeta.style.transitionTimingFunction = "ease-out";
        }, 500);

    } else {
        console.log("Nenhum resultado encontrado.");
    }
}

document.addEventListener('DOMContentLoaded', carregarResultados)
