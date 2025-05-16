//vetor de questões para colocar o enunciado, o etxo de cada opção e qual é a alternativa certa e as erradas
//Esse array vai ser do tipo objeto, pois será de vários tipos, como enunciado, questão, etc
const elementoQuestao = window.document.getElementById("enunciado")//cria uma variável para poder mudar o enunciado das questões
const botoesRespostas = window.document.getElementById("alternativas")
const botaoProximaQuestao = window.document.getElementById("botao-proxima")

const totalPerguntas = 5

let indiceQuestaoAtual = 0//para saber qual é o número da questão atual
let nomeQuiz = "";

// Função para embaralhar um array utilizando o algoritmo de Fisher-Yates
function embaralharArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Troca os elementos
    }
}

function carregarQuestoes() {
  fetch('http://localhost:8080/questions/' + categoria)  // Caminho para o arquivo JSON
    .then(response => response.json()) // Converte a resposta em JSON
    .then(data => {
      nomeQuiz = data.categoria;
      questoes = data.questoes;  // Acessa o array de questões no JSON
      embaralharArray(questoes);  // Embaralha as questões ao carregar
      questoes.forEach(q => embaralharArray(q.respostas)); // Embaralha as alternativas de cada questão
      iniciarQuiz();  // Inicia o quiz após carregar as questões
    })
    .catch(error => console.error('Erro ao carregar o arquivo JSON:', error));
}

function iniciarQuiz(){
  const elementoCategoria = document.getElementById('categoria');
  elementoCategoria.textContent = "Teste: " + nomeQuiz;

	indiceQuestaoAtual = 0
	pontuacao = 0
  botaoProximaQuestao.innerHTML = "Próxima"//muda o texto do botão para próxima
  mostrarQuestao()//chamar a Função que será usada para mostrar cada questão uma de cada vez
}

function resetarEstado(){//
	botaoProximaQuestao.style.display = "none"
  botoesRespostas.style.background = "#fff"
  while(botoesRespostas.firstChild){//serve para retirar os botões que criamos inicialmente em html para depois trocar pelo texto das próximas questões
  	//ele remove o primeiro botão que é a first child, logo o segundo vira o primeiro e é apagado e vai assim até que todos os botões sejam apagados
  	botoesRespostas.removeChild(botoesRespostas.firstChild)
  }
}

function mostrarQuestao(){//Função que será usada para mostrar cada questão uma de cada vez
	resetarEstado()
	let questaoAtual = questoes[indiceQuestaoAtual]//chama o array do tipo objeto lá em cima para colocar a questão e o índice é como vamos referenciar qual questão estamos chamando
  let numeroQuestao = indiceQuestaoAtual + 1//como todo array começa na posição 0, o número da questão apareceria 0, porém para a maioria das pessoas isso é esquisito, não existe questão 0, então pra ficar mais adequado pegamos o índice 0 e somamos 1 para que fique visualmente melhor para o usuário final que não tem conhecimento de programação
  elementoQuestao.innerHTML = numeroQuestao + "° " + questaoAtual.questao//aqui de fato eu coloco o número e coloco o texto da questão que está no vetor lá em cima 
  questaoAtual.respostas.forEach((respostas) => {//o for each serve para varrer o vetor assim posso passar por todas as opções e pegar o que preciso e jogar as informções nos botões do html
  	const botao = window.document.createElement("button")//aqui estou criando um elemento no site do tipo button de forma dinâmica que substituirá aqueles botões na parte de html que estão escritos Resposta 01 etc...
    botao.innerHTML = respostas.texto //gera dinamicamnete o texto lá do array para os botões
    botao.dataset.id= respostas.id//armazeno o id lá do array para mais para frente verificar qual resposta é a correta
    botao.classList.add("btn")//se não colocar isso os botões vão perder o estilo do css que colocamos,visto que vc está gerando novos botões diferentes do que foi colocado no html, porém com isso a formatação volta pq colocamos a classe btn dentro desses novos botões
    botao.addEventListener("click", selecionarQuestao);//Ao clicar no botão vou chamar uma função chamda selecionar questão
    botoesRespostas.appendChild(botao)//aqui ele de fato mostra os botões com os textos lá do array objeto
  })
}

function selecionarQuestao(e){//esse "e" dentro dos parenteses é o evento passado pelo javascript que no nosso caso é o click
	respostas = questoes[indiceQuestaoAtual].respostas
  const respostaCerta = respostas.filter((respostas) => respostas.acertou == true)[0]//aqui eu armazeno a alternativa correta em uma variável depois de filtrar pelas respostas qual possui o atributo correct igual à true
  const botaoClicado = e.target//para saber qual botão foi clicado
  
  respostas.forEach(resposta => {
    const botaoResposta = document.querySelector(`[data-id='${resposta.id}']`);
    if (resposta.acertou) {
      botaoResposta.style.backgroundColor = "#9aeabc"; 
    }
  });

  if(botaoClicado.dataset.id == respostaCerta.id){
    pontuacao++
  }else{
  	botaoClicado.style.backgroundColor = "#ed665c"; 
    const questaoAtual = questoes[indiceQuestaoAtual]
    observacoes.push({
      numQuestao: indiceQuestaoAtual + 1,
      observacao: questaoAtual.observacao
    })
  }
  
  Array.from(botoesRespostas.children).forEach((botao) => {
  	botao.disabled = true
  })

  botaoProximaQuestao.style.display = "block"

  registrarResposta();
}

function registrarResposta() {
  sessionStorage.setItem('resultadoQuiz', JSON.stringify({
    acertos: pontuacao,
    total: totalPerguntas,
  }));
}


function mostrarSituacao(){
  //essa função mostra a situção dos acertos
  //se for maior que tanots é bom, ou ruim, ou regular, ou péssimo, por exemplo
  let situacao
  if(pontuacao == 5){
  	situacao = "Parabéns sua empresa está 100% segura"
    botoesRespostas.style.background = "#4bf22e"
    //botoesRespostas.style.backgroundImage = "url('https://img.freepik.com/fotos-gratis/fundo-texturizado-abstrato_1258-30484.jpg')";
    //botoesRespostas.classList.add("cor-situacao-otimo")//Não consegui fazer funcionar
  }else if(pontuacao >= 4){
  	situacao = "Sua empresa está bem segura, mas precisa melhorar em certos pontos"
    botoesRespostas.style.background = "#ecf23d"
  }else if(pontuacao >= 2){
  	situacao = "Sinto muito, sua empresa corre sérios riscos de segurança, entre em contato conosco o mais rápido possível"
    botoesRespostas.style.background = "#f2a13d"
  }else{
  	situacao = "Você está totalmente desprotegido, entre em contato urgentemente"
    botoesRespostas.style.background = "#fc2d26"
  }
	return situacao
}

function mostrarPontuacao(){
  let situacaoEmpresa = mostrarSituacao()//recebe o texto retornado pela função para dizer como está a situação
  window.open("resultado.html", "_self")
}

function lidarProximoBotao(){
	indiceQuestaoAtual++//incrementa o indce da questão pra passar pra proxima pergunta
  if(indiceQuestaoAtual < questoes.length){
  	mostrarQuestao()//mostra a próxima questão
  }else{
    registrarResposta();
  	mostrarPontuacao()//mostra a pontuação se chegou no final
  }
}

botaoProximaQuestao.addEventListener("click", () => {
	if(indiceQuestaoAtual < questoes.length){//ver se chegou no fim do quiz comparando o indice da questão atual com o tamanho do array
  	lidarProximoBotao()
    return
  }else{
  	iniciarQuiz(categoria)
  }
})

function getParametroUrl(nome) {
  const params = new URLSearchParams(window.location.search);
  return params.get(nome);
}

const categoria = getParametroUrl('categoria');

if (categoria) {
  carregarQuestoes();
}
