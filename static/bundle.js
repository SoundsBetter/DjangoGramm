/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/js/comment.js":
/*!******************************!*\
  !*** ./assets/js/comment.js ***!
  \******************************/
/***/ (() => {

eval("function handleSubmit(event) {\r\n    event.preventDefault(); // Запобігаємо стандартному відправленню форми\r\n\r\n    var form = event.target.closest('form');\r\n    var postId = form.getAttribute('data-post-id');\r\n    var formData = new FormData(form);\r\n\r\n    var actionUrl = `/posts/add_comment/${postId}/`;\r\n\r\n    fetch(actionUrl, {\r\n        method: 'POST',\r\n        body: formData,\r\n        headers: {\r\n            'X-CSRFToken': formData.get('csrfmiddlewaretoken')\r\n        }\r\n    })\r\n    .then(response => response.json())\r\n    .then(data => {\r\n        if (data.status === 'success') {\r\n            var newComment = document.createElement('div');\r\n            newComment.innerHTML = `<strong>${data.username}:</strong><p>${data.comment}</p>`;\r\n            var commentsContainer = form.nextElementSibling;\r\n            commentsContainer.appendChild(newComment);\r\n            form.reset(); // Очищуємо форму після додавання коментаря\r\n        } else {\r\n            // Обробка помилки\r\n            console.error('Error:', data.message);\r\n        }\r\n    })\r\n    .catch(error => {\r\n        console.error('Error:', error);\r\n    });\r\n}\r\n\r\n// Встановлення обробників подій для форм і кнопок\r\ndocument.querySelectorAll('.comment-form').forEach(function (form) {\r\n    form.addEventListener('submit', handleSubmit);\r\n});\r\n\r\ndocument.querySelectorAll('.submit-comment').forEach(function (button) {\r\n    button.addEventListener('click', handleSubmit);\r\n});\r\n\n\n//# sourceURL=webpack://djangogramm/./assets/js/comment.js?");

/***/ }),

/***/ "./assets/js/follow.js":
/*!*****************************!*\
  !*** ./assets/js/follow.js ***!
  \*****************************/
/***/ (() => {

eval("document.querySelectorAll('.follow-btn').forEach(function (button) {\r\n    const userId = button.getAttribute('data-id');\r\n\r\n    fetch(`/accounts/${userId}/check_follow/`)\r\n        .then(response => response.json())\r\n        .then(data => {\r\n            const isFollowed = data.followed;\r\n            toggleFollowIcon(button, isFollowed)\r\n        })\r\n        .catch(error => console.error(error));\r\n\r\n    button.addEventListener('click', function () {\r\n        const xhr = new XMLHttpRequest();\r\n        xhr.open('POST', `/accounts/${userId}/follow/`, true);\r\n        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');\r\n        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));\r\n        xhr.onload = function () {\r\n            if (this.status === 200) {\r\n                const response = JSON.parse(this.responseText);\r\n                const followerCountElement = document.querySelector(`.followers-count[data-post-id=\"${userId}\"]`);\r\n                if (followerCountElement) {\r\n                    followerCountElement.innerText = response.followers_count + ' likes';\r\n                }\r\n\r\n                toggleFollowIcon(button, response.followed);\r\n            } else {\r\n                console.error('An error occurred!');\r\n            }\r\n        };\r\n        xhr.send(encodeForAjax({}));\r\n    });\r\n});\r\n\r\nfunction toggleFollowIcon(button, isFollowed) {\r\n    const icon = button.querySelector('i');\r\n    if (isFollowed) {\r\n        icon.classList.remove('fa-regular', 'fa-circle-check');\r\n        icon.classList.add('fa-solid', 'fa-circle-check'); // Заповнене серце\r\n        button.style.color = '#30b7ff'; // Додатково змінюємо колір\r\n    } else {\r\n        icon.classList.remove('fa-solid', 'fa-circle-check');\r\n        icon.classList.add('fa-regular', 'fa-circle-check'); // Порожнє серце\r\n        button.style.color = ''; // Скидуємо колір\r\n    }\r\n}\r\n\r\n\n\n//# sourceURL=webpack://djangogramm/./assets/js/follow.js?");

/***/ }),

/***/ "./assets/js/index.js":
/*!****************************!*\
  !*** ./assets/js/index.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _like__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./like */ \"./assets/js/like.js\");\n/* harmony import */ var _like__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_like__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _follow__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./follow */ \"./assets/js/follow.js\");\n/* harmony import */ var _follow__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_follow__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _comment__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./comment */ \"./assets/js/comment.js\");\n/* harmony import */ var _comment__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_comment__WEBPACK_IMPORTED_MODULE_2__);\n\r\n\r\n\r\n\r\nfunction getCookie(name) {\r\n    let cookieValue = null;\r\n    if (document.cookie && document.cookie !== '') {\r\n        const cookies = document.cookie.split(';');\r\n        for (let i = 0; i < cookies.length; i++) {\r\n            const cookie = cookies[i].trim();\r\n            // Does this cookie string begin with the name we want?\r\n            if (cookie.substring(0, name.length + 1) === (name + '=')) {\r\n                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));\r\n                break;\r\n            }\r\n        }\r\n    }\r\n    return cookieValue;\r\n}\r\n// Функція для кодування даних у формат, прийнятний для x-www-form-urlencoded\r\n\r\nfunction encodeForAjax(data) {\r\n    return Object.keys(data).map(function (k) {\r\n        return encodeURIComponent(k) + '=' + encodeURIComponent(data[k])\r\n    }).join('&');\r\n}\r\n\r\nwindow.getCookie = getCookie;\r\nwindow.encodeForAjax = encodeForAjax;\n\n//# sourceURL=webpack://djangogramm/./assets/js/index.js?");

/***/ }),

/***/ "./assets/js/like.js":
/*!***************************!*\
  !*** ./assets/js/like.js ***!
  \***************************/
/***/ (() => {

eval("document.querySelectorAll('.like-btn').forEach(function (button) {\r\n    const postId = button.getAttribute('data-id');\r\n    button.addEventListener('click', function () {\r\n        const xhr = new XMLHttpRequest();\r\n        xhr.open('POST', `/posts/like/${postId}/`, true);\r\n        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');\r\n        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));\r\n        xhr.onload = function () {\r\n            if (this.status === 200) {\r\n                const response = JSON.parse(this.responseText);\r\n                const likeCountElement = document.querySelector(`.like-count[data-post-id=\"${postId}\"]`);\r\n                if (likeCountElement) {\r\n                    likeCountElement.innerText = response.likes_count + ' likes';\r\n                }\r\n\r\n                toggleHeartIcon(button, response.liked);\r\n            } else {\r\n                console.error('An error occurred!');\r\n            }\r\n        };\r\n        xhr.send(encodeForAjax({}));\r\n    });\r\n});\r\n\r\n// Функція зміни іконки серця\r\nfunction toggleHeartIcon(button, isLiked) {\r\n    const icon = button.querySelector('i');\r\n    if (isLiked) {\r\n        icon.classList.remove('fa-regular');\r\n        icon.classList.add('fa-solid'); // Заповнене серце\r\n        button.style.color = '#ff3040'; // Додатково змінюємо колір\r\n    } else {\r\n        icon.classList.remove('fa-solid');\r\n        icon.classList.add('fa-regular'); // Порожнє серце\r\n        button.style.color = ''; // Скидуємо колір\r\n    }\r\n}\r\n\r\n\r\n// Функція для отримання значення cookie за назвою\r\nfunction toggleBio() {\r\n    var shortBio = document.getElementById('short_bio');\r\n    var fullBio = document.getElementById('full_bio');\r\n    var toggleIcon = document.getElementById('toggleIcon');\r\n\r\n    if (fullBio.style.display === \"none\") {\r\n        fullBio.style.display = \"block\";\r\n        shortBio.style.display = \"none\";\r\n        toggleIcon.classList.remove('fa-caret-down');\r\n        toggleIcon.classList.add('fa-caret-up');\r\n    } else {\r\n        fullBio.style.display = \"none\";\r\n        shortBio.style.display = \"block\";\r\n        toggleIcon.classList.remove('fa-caret-up');\r\n        toggleIcon.classList.add('fa-caret-down');\r\n    }\r\n}\r\n\r\nwindow.toggleBio = toggleBio;\r\n\n\n//# sourceURL=webpack://djangogramm/./assets/js/like.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/js/index.js");
/******/ 	
/******/ })()
;