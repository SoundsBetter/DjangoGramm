document.querySelectorAll('.like-btn').forEach(function (button) {
    const postId = button.getAttribute('data-id');
    button.addEventListener('click', function () {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/posts/like/${postId}/`, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.onload = function () {
            if (this.status === 200) {
                const response = JSON.parse(this.responseText);
                const likeCountElement = document.querySelector(`.like-count[data-post-id="${postId}"]`);
                if (likeCountElement) {
                    likeCountElement.innerText = response.likes_count + ' likes';
                }

                toggleHeartIcon(button, response.liked);
            } else {
                console.error('An error occurred!');
            }
        };
        xhr.send(encodeForAjax({}));
    });
});

// Функція зміни іконки серця
function toggleHeartIcon(button, isLiked) {
    const icon = button.querySelector('i');
    if (isLiked) {
        icon.classList.remove('fa-regular');
        icon.classList.add('fa-solid'); // Заповнене серце
        button.style.color = '#ff3040'; // Додатково змінюємо колір
    } else {
        icon.classList.remove('fa-solid');
        icon.classList.add('fa-regular'); // Порожнє серце
        button.style.color = ''; // Скидуємо колір
    }
}


// Функція для отримання значення cookie за назвою
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функція для кодування даних у формат, прийнятний для x-www-form-urlencoded
function encodeForAjax(data) {
    return Object.keys(data).map(function (k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(data[k])
    }).join('&');
}

function toggleBio() {
    var shortBio = document.getElementById('short_bio');
    var fullBio = document.getElementById('full_bio');
    var toggleIcon = document.getElementById('toggleIcon');

    if (fullBio.style.display === "none") {
        fullBio.style.display = "block";
        shortBio.style.display = "none";
        toggleIcon.classList.remove('fa-caret-down');
        toggleIcon.classList.add('fa-caret-up');
    } else {
        fullBio.style.display = "none";
        shortBio.style.display = "block";
        toggleIcon.classList.remove('fa-caret-up');
        toggleIcon.classList.add('fa-caret-down');
    }
}