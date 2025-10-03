const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../Frontend')));

const PYTHON_API_URL = 'http://127.0.0.1:5000/predict';

app.post('/predict', async (req, res) => {
    const { humidity, windSpeed } = req.body;

    console.log('Sending data to Python API:', { humidity, windSpeed });

    try {
        const apiResponse = await fetch(PYTHON_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ humidity, windSpeed }),
        });

        if (!apiResponse.ok) {
            const errorText = await apiResponse.text();
            throw new Error(`Python API responded with status ${apiResponse.status}: ${errorText}`);
        }

        const predictionData = await apiResponse.json();
        res.json(predictionData);

    } catch (error) {
        console.error('Error calling Python API:', error);
        res.status(500).json({ error: 'Failed to communicate with the prediction service.' });
    }
});

app.listen(PORT, () => {
    console.log(`server is running on ${PORT}`);
});