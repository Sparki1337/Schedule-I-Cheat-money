// Ждем, пока документ будет полностью загружен
document.addEventListener('DOMContentLoaded', function() {
    // Получаем кнопку переключения темы и иконку
    const themeButton = document.getElementById('theme-button');
    const themeIcon = themeButton.querySelector('i');
    
    // Проверяем, была ли ранее выбрана тема в localStorage
    const savedTheme = localStorage.getItem('theme');
    
    // Если тема была сохранена, применяем её
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }
    
    // Обработчик клика по кнопке смены темы
    themeButton.addEventListener('click', function() {
        // Переключаем класс темы для body
        document.body.classList.toggle('dark-theme');
        
        // Проверяем текущую тему
        const isDarkTheme = document.body.classList.contains('dark-theme');
        
        // Изменяем иконку в зависимости от темы
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
    
    // Анимация для кнопок скачивания при наведении
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
    
    // Плавная прокрутка к якорям
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