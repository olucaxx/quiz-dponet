let stringLinkDoSite = "";

function abrirSelecaoDificuldade(categoria) {
  stringLinkDoSite = `quiz.html?categoria=${categoria}`;
  document.getElementById('container-dificuldade').style.display = 'block';
}

document.getElementById('btnGestaoPessoasRH').addEventListener('click', function() { abrirSelecaoDificuldade("gestaoPessoasRH") });
document.getElementById('btnLegalidadeRegulacao').addEventListener('click', function() { abrirSelecaoDificuldade("legalidadeRegulacao") });
document.getElementById('btnTecnologiaSeguranca').addEventListener('click', function() { abrirSelecaoDificuldade("tecnologiaSeguranca") });
document.getElementById('btnCulturaEtica').addEventListener('click', function() { abrirSelecaoDificuldade("culturaEtica") });
document.getElementById('btnProcessosGovernanca').addEventListener('click', function() { abrirSelecaoDificuldade("processosGovernanca") });
document.getElementById('btnMarketingVenda').addEventListener('click', function() { abrirSelecaoDificuldade("marketingVendas") });

function escolherDificuldade(dificuldade) {
  document.getElementById('container-dificuldade').style.display = 'none';

  const destino = `${stringLinkDoSite}&dificuldade=${dificuldade}`;
  window.location.href = destino;
}

window.onclick = function(event) {
  const modal = document.getElementById('container-dificuldade');
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
