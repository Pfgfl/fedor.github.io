document.addEventListener('DOMContentLoaded', () => {
    // Инициализация кода группы при загрузке страницы
    updateGroupCode();

    document.body.addEventListener('click', (event) => {
        if (event.target.id === 'lobbyButton') {
            fetch('lobby-create.html')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Сетевая ошибка: ' + response.statusText);
                    }
                    return response.text();
                })
                .then(data => {
                    document.body.innerHTML = data;

                    // Обновляем код группы после загрузки новой страницы
                    updateGroupCode();
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
        }
    });
});

// Функция для обновления текста кода группы
function updateGroupCode() {
    const groupCodeElement = document.getElementById('groupCode');
    if (groupCodeElement) {
        groupCodeElement.textContent = generateRandomCode();
    } else {
        console.error('Элемент с id "groupCode" не найден.');
    }
}

// Функция генерации случайного 6-значного числа
function generateRandomCode() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}


