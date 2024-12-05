document.addEventListener('DOMContentLoaded', () => {
    const labels = document.querySelectorAll('.emotion-label');

    labels.forEach(label => {
        label.addEventListener('click', () => {
            const checkboxId = label.getAttribute('for');
            const checkbox = document.getElementById(checkboxId);

            if (checkbox) {
                if (!checkbox.checked) {
                    const labelText = label.textContent.trim();
                    if (labelText === 'Angry') {
                        label.style.color = 'red';
                    } else if (labelText === 'Happy') {
                        label.style.color = 'green';
                    }
                } else {
                    label.style.color = 'rgba(0, 0, 0, 0.5)';
                }
            }
        });
    });
});