document.addEventListener('DOMContentLoaded', () => {
    // 1. БЕРЕМ ТОКЕН ИЗ LOCALSTORAGE
    const token = localStorage.getItem('userToken');

    // Если токена нет — сразу редиректим на логин
    if (!token) {
        window.location.href = '/login-page/';
        return;
    }

    // Вспомогательная функция для заголовков с токеном
    function getAuthHeaders() {
        return {
            'Authorization': `Token ${token}`,
            'Accept': 'application/json'
        };
    }

    // ЭЛЕМЕНТЫ DOM
    const usernameDisplay = document.getElementById('username-display');
    const userRoleBadge = document.getElementById('user-role-badge');
    const addBookBtn = document.getElementById('add-book-btn');
    const logoutBtn = document.getElementById('logout-btn');

    const searchInput = document.getElementById('search-input');
    const genreSelect = document.getElementById('genre-select');
    const booksContainer = document.getElementById('books-container');

    const uploadModal = document.getElementById('upload-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const uploadBookForm = document.getElementById('upload-book-form');
    const bookGenreSelect = document.getElementById('book-genre');

    // Элементы профиля
    const profileBtn = document.getElementById('profile-btn');
    const profileModal = document.getElementById('profile-modal');
    const closeProfileModalBtn = document.getElementById('close-profile-modal');

    let currentUser = null;

    // Заполнение данных профиля при клике
    profileBtn.addEventListener('click', () => {
        if (currentUser) {
            document.getElementById('profile-username').textContent = currentUser.username;
            document.getElementById('profile-email').textContent = currentUser.email || 'Не указан';
            document.getElementById('profile-role').textContent = currentUser.role === 'AUTHOR' ? 'Автор' : 'Читатель';
            profileModal.classList.remove('hidden');
        }
    });

    // Закрытие модалки профиля
    closeProfileModalBtn.addEventListener('click', () => profileModal.classList.add('hidden'));

    window.addEventListener('click', (e) => {
        if (e.target === profileModal) profileModal.classList.add('hidden');
    });

    // 2. ИНИЦИАЛИЗАЦИЯ И ПРО ВЕРКА АВТОРИЗАЦИИ
    async function init() {
        try {
            const response = await fetch('/api/users/me/', {
                headers: getAuthHeaders()
            });

            if (!response.ok) {
                // Если токен невалиден или просрочен
                localStorage.removeItem('userToken');
                window.location.href = '/login-page/';
                return;
            }

            currentUser = await response.json();
            setupUserUI(currentUser);

            await loadGenres();
            await loadBooks();

        } catch (error) {
            console.error('Ошибка авторизации:', error);
            window.location.href = '/login-page/';
        }
    }

    // 3. НАСТРОЙКА ИНТЕРФЕЙСА ПОД РОЛЬ ЮЗЕРА
    function setupUserUI(user) {
        usernameDisplay.textContent = user.username;
        userRoleBadge.textContent = user.role === 'AUTHOR' ? 'Автор' : 'Читатель';

        if (user.role === 'AUTHOR') {
            addBookBtn.classList.remove('hidden');
        }
    }

    // 4. ЗАГРУЗКА ЖАНРОВ
    async function loadGenres() {
        try {
            const res = await fetch('/api/genres/', {
                headers: getAuthHeaders()
            });
            const genres = await res.json();

            genres.forEach(genre => {
                const optionFilter = new Option(genre.name, genre.id);
                genreSelect.add(optionFilter);

                const optionModal = new Option(genre.name, genre.id);
                bookGenreSelect.add(optionModal);
            });
        } catch (err) {
            console.error('Ошибка загрузки жанров:', err);
        }
    }

    // 5. ЗАГРУЗКА И ОТРИСОВКА КНИГ
    async function loadBooks(searchQuery = '') {
        try {
            let url = '/api/books/';
            if (searchQuery) {
                url += `?search=${encodeURIComponent(searchQuery)}`;
            }

            const res = await fetch(url, {
                headers: getAuthHeaders()
            });
            let books = await res.json();

            const selectedGenreId = genreSelect.value;
            if (selectedGenreId) {
                books = books.filter(book =>
                    book.genres.some(g => g.id == selectedGenreId)
                );
            }

            renderBooks(books);
        } catch (err) {
            console.error('Ошибка загрузки книг:', err);
            booksContainer.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #888;">Не удалось загрузить книги.</p>';
        }
    }

    // Отрисовка HTML-карточек
    function renderBooks(books) {
        booksContainer.innerHTML = '';

        if (!Array.isArray(books) || books.length === 0) {
            booksContainer.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #888;">Книг пока нет или ничего не найдено.</p>';
            return;
        }

        books.forEach(book => {
            const defaultCover = 'https://placehold.co/200x260/2a2a2a/ffffff?text=No+Cover';
            const coverUrl = book.cover ? book.cover : defaultCover;

            const genresBadges = book.genres ? book.genres.map(g => `<span class="genre-tag">${g.name}</span>`).join('') : '';

            const card = document.createElement('div');
            card.className = 'book-card';
            card.innerHTML = `
                <img src="${coverUrl}" alt="${book.title}" class="book-cover">
                <div class="book-info">
                    <div class="book-title">${book.title}</div>
                    <div class="book-author">Автор: ${book.author}</div>
                    <div class="book-genres">${genresBadges}</div>
                    <button class="btn btn-primary download-btn" style="margin-top: 12px; width: 100%;" data-id="${book.id}">
                        Скачать (${book.downloads_count || 0})
                    </button>
                </div>
            `;

            card.querySelector('.download-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                downloadBook(book.id);
            });

            booksContainer.appendChild(card);
        });
    }

    // 6. СКАЧИВАНИЕ КНИГИ
    async function downloadBook(bookId) {
        try {
            const res = await fetch(`/api/books/${bookId}/download/`, {
                method: 'POST',
                headers: getAuthHeaders()
            });
            const data = await res.json();
            if (data.file_url) {
                window.open(data.file_url, '_blank');
                loadBooks(searchInput.value);
            }
        } catch (err) {
            alert('Ошибка при скачивании файла');
        }
    }

    // 7. ОБРАБОТЧИКИ СОБЫТИЙ ФИЛЬТРОВ
    searchInput.addEventListener('input', () => loadBooks(searchInput.value));
    genreSelect.addEventListener('change', () => loadBooks(searchInput.value));

    // 8. МОДАЛЬНОЕ ОКНО
    addBookBtn.addEventListener('click', () => uploadModal.classList.remove('hidden'));
    closeModalBtn.addEventListener('click', () => uploadModal.classList.add('hidden'));

    window.addEventListener('click', (e) => {
        if (e.target === uploadModal) uploadModal.classList.add('hidden');
    });

    // Отправка новой книги (FormData + Authorization header)
    uploadBookForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('title', document.getElementById('book-title').value);
        formData.append('description', document.getElementById('book-description').value);
        formData.append('file', document.getElementById('book-file').files[0]);
        formData.append('genres', bookGenreSelect.value);

        const coverFile = document.getElementById('book-cover').files[0];
        if (coverFile) {
            formData.append('cover', coverFile);
        }
        try {
            const res = await fetch('/api/books/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`
                },
                body: formData
            });

            if (res.ok) {
                alert('Книга отправлена на модерацию!');
                uploadBookForm.reset();
                uploadModal.classList.add('hidden');
                loadBooks(searchInput.value);
            } else {
                const errData = await res.json();
                alert('Ошибка при загрузке книги: ' + JSON.stringify(errData));
            }
        } catch (err) {
            console.error('Ошибка сети:', err);
            alert('Ошибка сервера при отправке файла');
        }
    });

    // Выход (Логаут)
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('userToken');
        window.location.href = '/login-page/';
    });

    // Старт
    init();
});