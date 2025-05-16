function abrirQuiz(categoria) {
  let stringLinkDoSite = `../quiz/quiz.html?categoria=${categoria}`;

  window.location.href = stringLinkDoSite;
}

document.getElementById('btnGestaoPessoasRH').addEventListener('click', function() { abrirQuiz("gestaoPessoasRH") });
document.getElementById('btnLegalidadeRegulacao').addEventListener('click', function() { abrirQuiz("legalidadeRegulacao") });
document.getElementById('btnTecnologiaSeguranca').addEventListener('click', function() { abrirQuiz("tecnologiaSeguranca") });
document.getElementById('btnCulturaEtica').addEventListener('click', function() { abrirQuiz("culturaEtica") });
document.getElementById('btnProcessosGovernanca').addEventListener('click', function() { abrirQuiz("processosGovernanca") });
document.getElementById('btnMarketingVenda').addEventListener('click', function() { abrirQuiz("marketingVendas") });