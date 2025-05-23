(function() {
  'use strict';

  // Inicializa tooltips (se estiver usando Bootstrap tooltips)
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Controla a seleção dos itens do menu lateral
  document.addEventListener('DOMContentLoaded', function() {
    var menuItems = document.querySelectorAll('.itens-menu');

    menuItems.forEach(function(item) {
      item.addEventListener('click', function() {
        // Remove classe 'ativo' de todos os itens
        menuItems.forEach(function(el) {
          el.classList.remove('ativo');
        });

        // Adiciona classe 'ativo' ao item clicado
        this.classList.add('ativo');
      });
    });
  });
})();
