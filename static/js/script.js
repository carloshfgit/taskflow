// A boa prática é esperar que o documento HTML esteja 
// completamente carregado antes de tentar manipular seus elementos.
document.addEventListener("DOMContentLoaded", function() {

    // 1. Encontrar o botão no documento pelo ID que demos a ele.
    const startButton = document.getElementById("btn-start");

    // 2. Verificar se o botão realmente existe na página
    if (startButton) {
        
        // 3. Adicionar um "ouvinte de evento" para o clique.
        // Isso diz ao navegador: "Quando este elemento for clicado, execute esta função".
        startButton.addEventListener("click", function() {
            
            // 4. A ação a ser executada: mostrar um alerta simples.
            alert("o botão foi clicado!");
            
            // Também podemos logar no console para debug
            console.log("O botão 'Começar Agora' foi clicado.");
        });
    }

});