document.addEventListener('DOMContentLoaded', () =>
requestAnimationFrame(updateTime)
)

function updateTime() {
    document.documentElement.style.setProperty('--timer-day', "'" + moment().format("ddd") + "'");
    document.documentElement.style.setProperty('--timer-hours', "'" + moment().format("h") + "'");
    document.documentElement.style.setProperty('--timer-minutes', "'" + moment().format("mm") + "'");
    document.documentElement.style.setProperty('--timer-seconds', "'" + moment().format("ss A") + "'");
    requestAnimationFrame(updateTime);
}