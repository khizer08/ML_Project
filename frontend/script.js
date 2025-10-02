document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('weather-form');
    const resultDiv = document.getElementById('result');
    const predictBtn = document.getElementById('predict-btn');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const humidity = document.getElementById('humidity').value;
        const windSpeed = document.getElementById('wind-speed').value;

        if (humidity === '' || windSpeed === '') {
            resultDiv.textContent = 'Please fill out all fields.';
            return;
        }

        resultDiv.textContent = 'Predicting...';
        predictBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    humidity: parseFloat(humidity),
                    windSpeed: parseFloat(windSpeed)
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server responded with an error');
            }

            const data = await response.json();

            if (data.prediction) {
                resultDiv.textContent = `Predicted Temperature: ${data.prediction.toFixed(2)} °C`;
            } else {
                resultDiv.textContent = `Error: ${data.error || 'Could not retrieve prediction.'}`;
            }

        } catch (error) {
            console.error('Fetch Error:', error);
            resultDiv.textContent = `An error occurred: ${error.message}`;
        } finally {
            predictBtn.disabled = false;
        }
    });
});