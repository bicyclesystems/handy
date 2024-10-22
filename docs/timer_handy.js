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
    let startTime = localStorage.getItem('timerStartTime');
    let totalMinutesInitial = days * 1440 + hours * 60 + minutes;
    
    if (!startTime) {
        startTime = Date.now();
        localStorage.setItem('timerStartTime', startTime);
        localStorage.setItem('totalMinutesInitial', totalMinutesInitial);
    } else {
        totalMinutesInitial = parseInt(localStorage.getItem('totalMinutesInitial'));
    }

    function updateTimer() {
        const elapsedMinutes = Math.floor((Date.now() - startTime) / 60000);
        let totalMinutes = totalMinutesInitial - elapsedMinutes;

        if (totalMinutes <= 0) {
            clearInterval(timerInterval);
            localStorage.removeItem('timerStartTime');
            localStorage.removeItem('totalMinutesInitial');
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
    }

    updateTimer();
    const timerInterval = setInterval(updateTimer, 60000);
}

startTimer(5, 23, 45);