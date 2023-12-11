    let isCelsius = true;
    let temperatureData = [];

    function generateRandomTemperature() {
        temperatureData = [
            {time: '8:00', celsius: 10, fahrenheit: 58},
            {time: '10:00', celsius: 15, fahrenheit: 69},
            {time: '12:00', celsius: 20, fahrenheit: 46},
            {time: '14:00', celsius: 18, fahrenheit: 35},
            {time: '16:00', celsius: 16, fahrenheit: 50}
        ];

        temperatureData.forEach((item, index) => {
            item.celsius = Math.floor(Math.random() * 51) - 10;
            item.fahrenheit = (item.celsius * 9 / 5) + 32;
        });
    }

    function toggleTemperature() {
        const chart = document.getElementById('chart');

        //To clear graphic before usage
        chart.innerHTML = '';

        //according to the buttons type give a special list of data
        const data = isCelsius ? temperatureData.map(item => item.celsius) : temperatureData.map(item => item.fahrenheit);

        // Code for the points on the axes
        function createPoints() {
            const maxValue = Math.max(...data);
            const minValue = Math.min(...data);
            const valueRange = maxValue - minValue;
            const timeInterval = 100 / (data.length - 1);

            data.forEach((temperature, index) => {
                const x = index * timeInterval * 5; // Change the distance on the axe X
                const y = 320 - ((temperature - minValue) / valueRange) * 300 + 20; // Change the size on the axe X

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

        const dataTableBody = document.querySelector('#dataTable tbody');
        dataTableBody.innerHTML = '';

        temperatureData.forEach((item, index) => {
            const row = document.createElement('tr');
            const timeCell = document.createElement('td');
            timeCell.textContent = item.time;
            const tempCell = document.createElement('td');
            tempCell.textContent = isCelsius ? item.celsius + '°C' : item.fahrenheit + '°F';

            row.appendChild(timeCell);
            row.appendChild(tempCell);
            dataTableBody.appendChild(row);
        });
    }

    document.getElementById('toggleButton').addEventListener('click', function() {
        isCelsius = !isCelsius;
        toggleTemperature();
    });

    document.getElementById('refreshButton').addEventListener('click', function() {
            generateRandomTemperature();
            toggleTemperature();
    });

    // Create the graphic by page opening
    window.onload = function() {
            generateRandomTemperature();
            toggleTemperature();
        };