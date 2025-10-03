const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../Frontend')));

const PYTHON_API_HOST = 'http://127.0.0.1:5000';

app.post('/predict-temp', async (req, res) => {
    const { humidity, windSpeed } = req.body;
    console.log('Sending data to Python API for temp:', { humidity, windSpeed });

    try {
        const apiResponse = await fetch(`${PYTHON_API_HOST}/predict-temp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ humidity, windSpeed }),
        });
        if (!apiResponse.ok) throw new Error('Python API for temp failed');
        const predictionData = await apiResponse.json();
        res.json(predictionData);
    } catch (error) {
        console.error('Error calling temp API:', error);
        res.status(500).json({ error: 'Failed to communicate with the prediction service.' });
    }
});

app.post('/predict-rain', async (req, res) => {
    const { temperature, apparentTemperature, humidity, pressure } = req.body;
    console.log('Sending data to Python API for rain:', req.body);
    
    try {
        const apiResponse = await fetch(`${PYTHON_API_HOST}/predict-rain`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req.body),
        });
        if (!apiResponse.ok) throw new Error('Python API for rain failed');
        const predictionData = await apiResponse.json();
        res.json(predictionData);
    } catch (error) {
        console.error('Error calling rain API:', error);
        res.status(500).json({ error: 'Failed to communicate with the prediction service.' });
    }
});

app.get(/^.*/, (req, res) => {
    res.sendFile(path.join(__dirname, '../Frontend/index.html'));
});

app.listen(PORT, () => {
    console.log(`server running at port:${PORT}`);
});