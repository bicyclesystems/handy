function updateDisplay(id, value, isLeftZero) {
    const tens = Math.floor(value / 10);
    const ones = value % 10;
    updateDigit(`${id}-tens`, tens, isLeftZero);
    updateDigit(`${id}-ones`, ones, isLeftZero && tens === 0);
}

function updateDigit(id, value, isLeftZero) {
    const element = document.querySelector(`#${id}`);
    element.querySelector('h1').textContent = value;
    
    if (value === 0 && isLeftZero) {
        element.style.backgroundColor = '#F0F0EF';
        element.style.color = '#F4492B';
        element.style.border = '1px solid #F4492B';
    } else {
        element.style.backgroundColor = '#F4492B';
        element.style.color = '#F0F0EF';
        element.style.border = 'none';
    }
}

function startTimer(days, hours, minutes) {
    let totalMinutes = days * 1440 + hours * 60 + minutes;

    function updateTimer() {
        if (totalMinutes <= 0) {
            clearInterval(timerInterval);
            updateDisplay('days', 0, true);
            updateDisplay('hours', 0, true);
            updateDisplay('minutes', 0, true);
            return;
        }

        const d = Math.floor(totalMinutes / 1440);
        const h = Math.floor((totalMinutes % 1440) / 60);
        const m = totalMinutes % 60;

        updateDisplay('days', d, true);
        updateDisplay('hours', h, d === 0);
        updateDisplay('minutes', m, d === 0 && h === 0);

        totalMinutes--;
    }

    updateTimer();
    const timerInterval = setInterval(updateTimer, 60000);
}

let removedBrTags = [];

function handleBrTags() {
    const isMobile = window.innerWidth <= 768;

    if (isMobile && removedBrTags.length === 0) {
        // Находим все теги <br> на странице
        const allBrTags = document.getElementsByTagName('br');
        
        // Преобразуем HTMLCollection в массив и обрабатываем каждый тег
        Array.from(allBrTags).forEach(brTag => {
            // Проверяем, не находится ли тег <br> внутри элемента с data-subtitle
            if (!brTag.closest('[data-subtitle]')) {
                removedBrTags.push({
                    element: brTag,
                    parent: brTag.parentNode,
                    nextSibling: brTag.nextSibling
                });
                brTag.parentNode.removeChild(brTag);
            }
        });
    } else if (!isMobile && removedBrTags.length > 0) {
        // Восстанавливаем удаленные теги <br>
        removedBrTags.forEach(({ element, parent, nextSibling }) => {
            parent.insertBefore(element, nextSibling);
        });
        removedBrTags = [];
    }
}

document.addEventListener('DOMContentLoaded', handleBrTags);
window.addEventListener('resize', handleBrTags);

startTimer(5, 23, 45);