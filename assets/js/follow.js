document.querySelectorAll('.follow-btn').forEach(function (button) {
    const userId = button.getAttribute('data-id');

    fetch(`/accounts/${userId}/check_follow/`)
        .then(response => response.json())
        .then(data => {
            const isFollowed = data.followed;
            toggleFollowIcon(button, isFollowed)
        })
        .catch(error => console.error(error));

    button.addEventListener('click', function () {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/accounts/${userId}/follow/`, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.onload = function () {
            if (this.status === 200) {
                const response = JSON.parse(this.responseText);
                const followerCountElement = document.querySelector(`.followers-count[data-post-id="${userId}"]`);
                if (followerCountElement) {
                    followerCountElement.innerText = response.followers_count + ' likes';
                }

                toggleFollowIcon(button, response.followed);
            } else {
                console.error('An error occurred!');
            }
        };
        xhr.send(encodeForAjax({}));
    });
});

function toggleFollowIcon(button, isFollowed) {
    const icon = button.querySelector('i');
    if (isFollowed) {
        icon.classList.remove('fa-regular', 'fa-circle-check');
        icon.classList.add('fa-solid', 'fa-circle-check'); // Заповнене серце
        button.style.color = '#30b7ff'; // Додатково змінюємо колір
    } else {
        icon.classList.remove('fa-solid', 'fa-circle-check');
        icon.classList.add('fa-regular', 'fa-circle-check'); // Порожнє серце
        button.style.color = ''; // Скидуємо колір
    }
}