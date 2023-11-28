// janela pop-up para editar

document.addEventListener("DOMContentLoaded", function () {
  var alterarForm = document.querySelectorAll(
    ".alterar-tarefa, .alterar-conceito"
  );

  alterarForm.forEach(function (form) {
    form.addEventListener("click", function () {
      var janelaPopUp = form.nextElementSibling;
      janelaPopUp.style.display = "flex";
    });
  });

  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("popup-bg")) {
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
