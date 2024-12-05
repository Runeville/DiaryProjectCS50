document.addEventListener('DOMContentLoaded', () => {
    const labels = document.querySelectorAll('.emotion-label');

    labels.forEach(label => {
        label.addEventListener('click', () => {
            const checkboxId = label.getAttribute('for');
            const checkbox = document.getElementById(checkboxId);
            const color = label.dataset.color;

            if (checkbox) {
                if (!checkbox.checked) {
                    label.style.color = color;
                } else {
                    label.style.color = 'rgba(0, 0, 0, 0.5)';
                }
            }
        });
    });
});