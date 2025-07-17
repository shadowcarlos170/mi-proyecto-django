function toggleTheme() {
    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    htmlElement.setAttribute('data-theme', newTheme);
    
    // Guardar preferencia en localStorage
    localStorage.setItem('theme', newTheme);
    
    // Actualizar texto del botón
    const themeButton = document.querySelector('.theme-toggle-button button');
    if (newTheme === 'dark') {
        themeButton.innerHTML = '☀️ Modo Claro';
    } else {
        themeButton.innerHTML = '🌙 Modo Oscuro';
    }
}

// Al cargar la página, verificar el tema guardado
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Actualizar texto del botón según el tema guardado
    const themeButton = document.querySelector('.theme-toggle-button button');
    if (savedTheme === 'dark') {
        themeButton.innerHTML = '☀️ Modo Claro';
    } else {
        themeButton.innerHTML = '🌙 Modo Oscuro';
    }
});