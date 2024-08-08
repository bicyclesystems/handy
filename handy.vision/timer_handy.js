function updateDisplay(id, value) {
    const tens = Math.floor(value / 10);
    const ones = value % 10;
    document.querySelector(`#${id}-tens h1`).textContent = tens;
    document.querySelector(`#${id}-ones h1`).textContent = ones;
}

function startTimer(days, hours, minutes) {
    let totalMinutes = days * 1440 + hours * 60 + minutes;

    function updateTimer() {
        if (totalMinutes <= 0) {
            clearInterval(timerInterval);
            updateDisplay('days', 0);
            updateDisplay('hours', 0);
            updateDisplay('minutes', 0);
            return;
        }

        const d = Math.floor(totalMinutes / 1440);
        const h = Math.floor((totalMinutes % 1440) / 60);
        const m = totalMinutes % 60;

        updateDisplay('days', d);
        updateDisplay('hours', h);
        updateDisplay('minutes', m);

        totalMinutes--;
    }

    updateTimer();
    const timerInterval = setInterval(updateTimer, 60000);
}
startTimer(5, 23, 45);