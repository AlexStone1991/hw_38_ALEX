// Установка минимальной даты (сегодня)
document.addEventListener('DOMContentLoaded', function() {
    const now = new Date();
    const minDate = now.toISOString().slice(0, 16);
    document.getElementById('id_appointment_date').min = minDate;
});

// Минимальная дата - текущий день
document.addEventListener('DOMContentLoaded', function() {
    const dateField = document.getElementById('{{ form.appointment_date.id_for_label }}');
    if (dateField) {
        const now = new Date();
        const minDate = now.toISOString().slice(0, 16);
        dateField.min = minDate;
        dateField.classList.add('form-control');
    }
    
    // Валидация Bootstrap
    (function() {
        'use strict'
        const forms = document.querySelectorAll('.needs-validation')
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
    })()
});