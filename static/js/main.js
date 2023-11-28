// janela pop-up para editar

document.addEventListener("DOMContentLoaded", function () {
  var alterarForm = document.querySelectorAll(
    ".alterar-tarefa, .alterar-conceito" // seleciona todos os itens com essas classes
  );

  alterarForm.forEach(function (form) {
    // forEach - para todos os forms dentro do for no html
    form.addEventListener("click", function () {
      var janelaPopUp = form.nextElementSibling;
      // nextElementSibling - pega o próximo elemento/elemento irmão (nesse caso, o pop up)
      janelaPopUp.style.display = "flex"; // e o torna visível
    });
  });

  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("popup-bg")) {
      // quando clicar no background sai do popup
      event.target.style.display = "none";
    }
  });
});

// quando clica em deletar

function confirmarExclusao() {
  var confirmacao = confirm("Tem certeza que deseja excluir?");
  document.getElementById("confirmacao").value = confirmacao ? "true" : "false";
  return confirmacao;
}
