document.addEventListener('DOMContentLoaded', function() {
    const themeButton = document.getElementById('theme-button');
    const themeIcon = themeButton.querySelector('i');
    
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }
    
    themeButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        
        const isDarkTheme = document.body.classList.contains('dark-theme');
        
        if (isDarkTheme) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
    
    const langButton = document.getElementById('lang-button');
    const langSpan = langButton.querySelector('span');
    
    const savedLang = localStorage.getItem('lang');
    
    if (savedLang) {
        document.body.setAttribute('data-lang', savedLang);
        langSpan.textContent = savedLang.toUpperCase();
        updateTexts(savedLang);
    }
    
    langButton.addEventListener('click', function() {
        const currentLang = document.body.getAttribute('data-lang');
        const newLang = currentLang === 'ru' ? 'en' : 'ru';
        
        document.body.setAttribute('data-lang', newLang);
        langSpan.textContent = newLang.toUpperCase();
        
        localStorage.setItem('lang', newLang);
        updateTexts(newLang);
    });
    
    function updateTexts(lang) {
        document.querySelectorAll('[data-ru]').forEach(element => {
            if (lang === 'ru') {
                element.textContent = element.getAttribute('data-ru');
            } else {
                element.textContent = element.getAttribute('data-en');
            }
        });
    }
    
    const downloadButtons = document.querySelectorAll('.download-button');
    
    downloadButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            icon.classList.add('fa-bounce');
        });
        
        button.addEventListener('mouseleave', function() {
            const icon = this.querySelector('i');
            icon.classList.remove('fa-bounce');
        });
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}); 