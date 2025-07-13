// Установка минимальной даты (сегодня)
document.addEventListener('DOMContentLoaded', function() {
    const now = new Date();
    const minDate = now.toISOString().slice(0, 16);
    document.getElementById('id_appointment_date').min = minDate;
});