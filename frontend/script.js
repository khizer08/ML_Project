document.addEventListener('DOMContentLoaded', () => {
    const tempForm = document.getElementById('weather-form');
    const tempResultDiv = document.getElementById('result');
    const tempPredictBtn = document.getElementById('predict-btn');

    tempForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const humidity = document.getElementById('humidity').value;
        const windSpeed = document.getElementById('wind-speed').value;

        if (humidity === '' || windSpeed === '') {
            tempResultDiv.textContent = 'Please fill out all fields.';
            return;
        }

        tempResultDiv.textContent = 'Predicting...';
        tempPredictBtn.disabled = true;

        try {
            const response = await fetch('/predict-temp', {
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
                const errorData = await response.json().catch(() => {
                    return response.text().then(text => { throw new Error(text) });
                });
                throw new Error(errorData.error || 'Server responded with an error');
            }

            const data = await response.json();

            if (data.prediction) {
                tempResultDiv.textContent = `Predicted Temperature: ${data.prediction.toFixed(2)} °C`;
            } else {
                tempResultDiv.textContent = `Error: ${data.error || 'Could not retrieve prediction.'}`;
            }

        } catch (error) {
            console.error('Fetch Error:', error);
            tempResultDiv.textContent = `An error occurred: ${error.message}`;
        } finally {
            tempPredictBtn.disabled = false;
        }
    });

    const rainForm = document.getElementById('rain-form');
    const rainResultDiv = document.getElementById('rain-result');
    const rainPredictBtn = document.getElementById('rain-predict-btn');

    if (rainForm) {
        rainForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const temperature = document.getElementById('temperature').value;
            const apparentTemperature = document.getElementById('apparent-temp').value;
            const humidity = document.getElementById('rain-humidity').value;
            const pressure = document.getElementById('pressure').value;
            
            if (temperature === '' || apparentTemperature === '' || humidity === '' || pressure === '') {
                rainResultDiv.textContent = 'Please fill out all fields.';
                return;
            }

            rainResultDiv.textContent = 'Predicting...';
            rainPredictBtn.disabled = true;

            try {
                const response = await fetch('/predict-rain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        temperature: parseFloat(temperature),
                        apparentTemperature: parseFloat(apparentTemperature),
                        humidity: parseFloat(humidity),
                        pressure: parseFloat(pressure)
                    }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Server responded with an error');
                }

                const data = await response.json();
                rainResultDiv.textContent = `Prediction: ${data.prediction}`;

            } catch (error) {
                console.error('Fetch Error:', error);
                rainResultDiv.textContent = `An error occurred: ${error.message}`;
            } finally {
                rainPredictBtn.disabled = false;
            }
        });
    }
});