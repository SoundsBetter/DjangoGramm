document.querySelectorAll('.submit-comment').forEach(function (button) {
    button.addEventListener('click', function () {
        var form = this.closest('form');
        var postId = form.getAttribute('data-post-id');
        var formData = new FormData(form);

        var actionUrl = `/posts/add_comment/${postId}/`;

        fetch(actionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                // Очищення форми
                form.reset();

                // Перевірка, чи коментар був доданий успішно
                if (data.status === 'success') {
                    // Створення елементу для нового коментаря
                    var newComment = document.createElement('div');
                    newComment.innerHTML = `
                    <strong>${data.username}:</strong>
                    <p>${data.comment}</p>
                `;

                    // Додавання нового коментаря на сторінку
                    var commentsContainer = form.nextElementSibling; // або інший спосіб знайти контейнер
                    commentsContainer.appendChild(newComment);
                } else {
                    // Обробка помилки
                    console.error('Error:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

