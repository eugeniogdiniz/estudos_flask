/* global bootstrap: false */
(function() {
  'use strict'
  
  // Inicializa tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // Controla a seleção dos itens do menu
  document.addEventListener('DOMContentLoaded', function() {
    var navLinks = document.querySelectorAll('.nav-link')
    
    navLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
        // Se for um link vazio, previne o comportamento padrão
        if (this.getAttribute('href') === '#') {
          e.preventDefault()
        }
        
        // Remove a classe active de todos os itens
        navLinks.forEach(function(item) {
          item.classList.remove('active')
          item.removeAttribute('aria-current')
        })
        
        // Adiciona ao item clicado
        this.classList.add('active')
        this.setAttribute('aria-current', 'page')
      })
    })
  })
})()