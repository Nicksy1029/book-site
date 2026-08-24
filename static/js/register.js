document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Отменяем перезагрузку страницы

    const messageDiv = document.getElementById('message');
    messageDiv.innerText = 'Отправка...';
    messageDiv.style.color = 'black';

    // 1. Собираем данные из формы
    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        role: document.getElementById('role').value
    };

    try {
        // 2. Отправляем POST-запрос на наш API
        const response = await fetch('/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            messageDiv.style.color = '#66bb6a';
            messageDiv.innerText = 'Регистрация прошла успешно! Перенаправляем на страницу входа...';
            // Через 1.5 секунды отправляем на страницу входа
            setTimeout(() => {
                window.location.href = '/login-page/';
            }, 1500);
        } else {
            messageDiv.style.color = '#ff5252';
            // Показываем ошибки от DRF (например, "Пользователь с таким именем уже существует")
            messageDiv.innerText = JSON.stringify(result);
        }
    } catch (error) {
        messageDiv.style.color = '#ff5252';
        messageDiv.innerText = 'Ошибка соединения с сервером!';
    }
});