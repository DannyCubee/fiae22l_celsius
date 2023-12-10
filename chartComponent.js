import {generateRandomTemperature } from 'temperatureData.js';
export function updateChart(isCelsius) {
    const chart = document.getElementById('chart');
    const temperatureData = generateRandomTemperature();

    chart.innerHTML = '';

    const data = isCelsius ? temperatureData.map(item => item.celsius) : temperatureData.map(item => item.fahrenheit);

    function createPoints() {
        const maxValue = Math.max(...data);
        const minValue = Math.min(...data);
        const valueRange = maxValue - minValue;
        const timeInterval = 100 / (data.length - 1);

        data.forEach((temperature, index) => {
            const x = index * timeInterval * 5;
            const y = 320 - ((temperature - minValue) / valueRange) * 300 + 20;

            const newPoint = document.createElement('div');
            newPoint.className = 'point';
            newPoint.style.left = x + 35 + 'px';
            newPoint.style.top = y + 25 + 'px';
            chart.appendChild(newPoint);

            const timeLabel = document.createElement('div');
            timeLabel.className = 'axis-label';
            timeLabel.style.left = x + 30 + 'px';
            timeLabel.style.bottom = '0';
            timeLabel.textContent = temperatureData[index].time;
            chart.appendChild(timeLabel);

            const tempLabel = document.createElement('div');
            tempLabel.className = 'axis-label';
            tempLabel.style.left = x + 25 + 'px';
            tempLabel.style.top = y + 10 + 'px';
            tempLabel.textContent = isCelsius ? temperature + '°C' : temperature + '°F';
            chart.appendChild(tempLabel);
        });
    }

    createPoints();
}