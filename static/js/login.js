document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const messageDiv = document.getElementById('message');
    messageDiv.innerText = 'Вход...';
    messageDiv.style.color = 'black';

    const data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            // СОХРАНЯЕМ ТОКЕН В LOCALSTORAGE!
            localStorage.setItem('userToken', result.token);

            messageDiv.style.color = 'green';
            messageDiv.innerText = 'Успешный вход! Токен сохранён.';

            window.location.href = '/catalog/';
            // Сюда позже добавим редирект на главную страницу с книгами!
        } else {
            messageDiv.style.color = 'red';
            messageDiv.innerText = 'Неверный логин или пароль!';
        }
    } catch (error) {
        messageDiv.style.color = 'red';
        messageDiv.innerText = 'Ошибка соединения с сервером!';
    }
});