document.addEventListener('DOMContentLoaded', function() {
    // Уведомление всегда отображается
    const refreshNotice = document.getElementById('refresh-notice');
    refreshNotice.style.display = 'flex'; // Всегда отображаем
    
    // Тема
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
    
    // Язык
    const langButton = document.getElementById('lang-button');
    const langIcon = langButton.querySelector('i');
    const langSpan = langButton.querySelector('span');
    
    // Настройка начального состояния переключателя языка
    const savedLang = localStorage.getItem('lang');
    let currentLang = 'ru'; // По умолчанию русский
    
    if (savedLang) {
        currentLang = savedLang;
        document.body.setAttribute('data-lang', currentLang);
        updateLangButton(currentLang);
        updateTexts(currentLang);
    }
    
    langButton.addEventListener('click', function() {
        currentLang = currentLang === 'ru' ? 'en' : 'ru';
        
        document.body.setAttribute('data-lang', currentLang);
        updateLangButton(currentLang);
        
        localStorage.setItem('lang', currentLang);
        updateTexts(currentLang);
    });
    
    function updateLangButton(lang) {
        if (lang === 'ru') {
            langIcon.className = 'fas fa-flag-usa'; // Флаг США для перехода на английский
            langSpan.textContent = 'Русский';
            langButton.title = 'Switch to English';
        } else {
            langIcon.className = 'fas fa-flag-russia'; // Флаг России для перехода на русский
            langSpan.textContent = 'English';
            langButton.title = 'Переключить на русский';
        }
    }
    
    function updateTexts(lang) {
        document.querySelectorAll('[data-ru]').forEach(element => {
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                // Для полей ввода изменяем placeholder или value
                if (element.hasAttribute('placeholder')) {
                    element.placeholder = element.getAttribute(`data-${lang}-placeholder`);
                } else {
                    element.value = element.getAttribute(`data-${lang}`);
                }
            } else {
                // Для обычных элементов изменяем textContent
                if (lang === 'ru') {
                    element.textContent = element.getAttribute('data-ru');
                } else {
                    element.textContent = element.getAttribute('data-en');
                }
            }
        });
        
        // Обновляем title страницы
        document.title = lang === 'ru' 
            ? 'Money Patcher для Schedule I' 
            : 'Money Patcher for Schedule I';
            
        // Обновляем атрибут lang у тега html
        document.documentElement.lang = lang;
    }
    
    // Анимация кнопок скачивания
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
    
    // Плавная прокрутка
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