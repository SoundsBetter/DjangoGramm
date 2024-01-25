function handleSubmit(event) {
    event.preventDefault(); // Запобігаємо стандартному відправленню форми

    var form = event.target.closest('form');
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
        if (data.status === 'success') {
            var newComment = document.createElement('div');
            newComment.innerHTML = `<strong>${data.username}:</strong><p>${data.comment}</p>`;
            var commentsContainer = form.nextElementSibling;
            commentsContainer.appendChild(newComment);
            form.reset(); // Очищуємо форму після додавання коментаря
        } else {
            // Обробка помилки
            console.error('Error:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Встановлення обробників подій для форм і кнопок
document.querySelectorAll('.comment-form').forEach(function (form) {
    form.addEventListener('submit', handleSubmit);
});

document.querySelectorAll('.submit-comment').forEach(function (button) {
    button.addEventListener('click', handleSubmit);
});
