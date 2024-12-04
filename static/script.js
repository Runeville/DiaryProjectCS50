document.addEventListener('DOMContentLoaded', () => {
    // Находим все <label> с классом emotion-label
    const labels = document.querySelectorAll('.emotion-label');

    labels.forEach(label => {
        label.addEventListener('click', () => {
            // Найдем связанный checkbox через атрибут for
            const checkboxId = label.getAttribute('for');
            const checkbox = document.getElementById(checkboxId);

            if (checkbox) {
                // Переключаем состояние checkbox
                // checkbox.checked = !checkbox.checked;

                // Изменяем цвет текста label в зависимости от состояния checkbox
                if (!checkbox.checked) {
                    const labelText = label.textContent.trim();
                    if (labelText === 'Angry') {
                        label.style.color = 'red';
                    } else if (labelText === 'Happy') {
                        label.style.color = 'green';
                    }
                } else {
                    // Сбрасываем цвет текста на черный
                    label.style.color = 'rgba(0, 0, 0, 0.5)';
                }
            }
        });
    });
});