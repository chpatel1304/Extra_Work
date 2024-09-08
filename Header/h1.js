let currentSlide = 0;

function changeSlide(direction) {
    console.log('Change slide function called');
    
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    
    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
    console.log('Current slide index:', currentSlide);
    
    const slider = document.querySelector('.slides');
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
    changeSlide(0);
});
