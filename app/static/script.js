document.addEventListener("DOMContentLoaded", function () {
    const cookieBanner = document.getElementById("cookie-banner");
    const acceptCookiesBtn = document.getElementById("accept-cookies");
    const rejectCookiesBtn = document.getElementById("reject-cookies");

    // Функция для установки куки согласия
    function setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    }

    // Функция для получения значения куки по имени
    function getCookie(name) {
        const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
        return cookieValue ? cookieValue.pop() : "";
    }

    // Функция для скрытия плашки и установки куки при согласии
    function acceptCookies() {
        setCookie("cookies_accepted", "true", 365);
        cookieBanner.classList.add("hidden");
    }

    // Функция для скрытия плашки и установки куки при отказе
    function rejectCookies() {
        setCookie("cookies_accepted", "false", 365);
        cookieBanner.classList.add("hidden");
    }

    // Проверка, показывать ли плашку (проверяем, установлено ли куки согласия)
    if (getCookie("cookies_accepted") !== "true") {
        cookieBanner.classList.remove("hidden");
    }

    // Обработчики событий для кнопок согласия и отказа
    acceptCookiesBtn.addEventListener("click", acceptCookies);
    rejectCookiesBtn.addEventListener("click", rejectCookies);
});
