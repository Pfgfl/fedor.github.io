// Открытие/закрытие бокового меню
const menuToggle = document.getElementById('menuToggle');
const closeMenu = document.getElementById('closeMenu');
const sidebarMenu = document.getElementById('sidebarMenu');
const mainContent = document.getElementById('mainContent');

// Открытие меню
menuToggle.addEventListener('click', () => {
    sidebarMenu.classList.add('active');
    mainContent.classList.add('shifted');
});

// Закрытие меню
closeMenu.addEventListener('click', () => {
    sidebarMenu.classList.remove('active');
    mainContent.classList.remove('shifted');
});

// Закрытие меню при клике на ссылку
const menuLinks = document.querySelectorAll('.menu-link');
menuLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebarMenu.classList.remove('active');
        mainContent.classList.remove('shifted');

        // Удаляем активный класс у всех ссылок
        menuLinks.forEach(l => l.classList.remove('active'));
        // Добавляем активный класс к нажатой ссылке
        link.classList.add('active');
    });
});

// Закрытие меню при клике вне меню
document.addEventListener('click', (event) => {
    const isClickInsideMenu = sidebarMenu.contains(event.target);
    const isClickOnMenuToggle = menuToggle.contains(event.target);

    if (!isClickInsideMenu && !isClickOnMenuToggle && sidebarMenu.classList.contains('active')) {
        sidebarMenu.classList.remove('active');
        mainContent.classList.remove('shifted');
    }
});

// Плавная прокрутка для якорных ссылок
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        if (this.getAttribute('href') === '#') return;

        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Анимация появления элементов при скролле
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Наблюдаем за карточками
document.querySelectorAll('.feature, .course-card, .gallery-item').forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(item);
});

// Изменение активной ссылки в меню при скролле
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            document.querySelector(`.menu-link[href="#${sectionId}"]`)?.classList.add('active');
        } else {
            document.querySelector(`.menu-link[href="#${sectionId}"]`)?.classList.remove('active');
        }
    });
});

// Простая анимация для заголовка при загрузке
window.addEventListener('load', () => {
    const mainTitle = document.querySelector('.main-title');
    mainTitle.style.opacity = '0';
    mainTitle.style.transform = 'translateY(-20px)';

    setTimeout(() => {
        mainTitle.style.transition = 'opacity 1s ease, transform 1s ease';
        mainTitle.style.opacity = '1';
        mainTitle.style.transform = 'translateY(0)';
    }, 300);
});