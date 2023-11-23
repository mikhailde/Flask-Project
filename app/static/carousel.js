let myCarousel = document.querySelector('#carouselExampleCaptions');
let carousel = new bootstrap.Carousel(myCarousel, {
    interval: 2000, // Время между слайдами (в миллисекундах)
    wrap: true, // Зацикливание слайдов
    pause: 'hover' // Пауза при наведении
});
