document.addEventListener('DOMContentLoaded', function() {
    // Trouve tous les liens de la barre de navigation
    const navItems = document.querySelectorAll('.bottom-nav a');
  
    // Fonction pour mettre à jour l'élément actif
    function updateActiveNavItem() {
      // Trouve la section actuellement visible (en fonction du scroll)
      let currentSection = '';
      document.querySelectorAll('section').forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
          currentSection = section.id;
        }
      });
  
      // Met à jour la classe "active" sur les liens de navigation
      navItems.forEach(item => {
        item.classList.remove('active');
        if (item.hash === `#${currentSection}`) {
          item.classList.add('active');
        }
      });
    }
  
    // Appelle la fonction au chargement de la page et quand on scroll
    updateActiveNavItem();
    window.addEventListener('scroll', updateActiveNavItem);
  
      // Gère le clic sur les liens de navigation (pour le smooth scroll)
      navItems.forEach(item => {
      item.addEventListener('click', function(event) {
        event.preventDefault(); // Empêche le comportement par défaut du lien
  
        const targetId = this.getAttribute('href'); // Récupère l'ID de la cible
        const targetElement = document.querySelector(targetId); // Trouve l'élément cible
  
        if (targetElement) {
          // Calcule la position de l'élément cible, en tenant compte de la barre de navigation fixe
          const navHeight = document.querySelector('.bottom-nav').offsetHeight;
          const targetPosition = targetElement.offsetTop - navHeight;
  
  
          // Fait défiler la page jusqu'à l'élément cible (avec un effet "smooth")
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  });