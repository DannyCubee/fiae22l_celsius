      let isCelsius = true;
    let temperatureData = [];

    async function callData(data) {
    try {
        const response = await fetch("172.20.174.121:8000/api/v1/all-temperatures");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const values = await response.json();

        values.forEach((value) => {
            console.log(value["temp_c"]);
            console.log("test");
            const newItem = {
                time: value.time,
                celsius: value.celsius,
                fahrenheit: value.fahrenheit
            };
            data.push(newItem);
        });

        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return [];
    }
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

            const yAxisMinLabel = document.createElement('div');
            yAxisMinLabel.className = 'axis-label';
            yAxisMinLabel.style.left = '3px';
            yAxisMinLabel.style.bottom = '20px';
            yAxisMinLabel.textContent = `${minValue}${isCelsius ? '°C' : '°F'}`;
            chart.appendChild(yAxisMinLabel);

            const yAxisMaxLabel = document.createElement('div');
            yAxisMaxLabel.className = 'axis-label';
            yAxisMaxLabel.style.left = '3px';
            yAxisMaxLabel.style.top = '20px';
            yAxisMaxLabel.textContent = `${maxValue}${isCelsius ? '°C' : '°F'}`;
            chart.appendChild(yAxisMaxLabel);

            let i = 0;
            data.forEach((temperature, index) => {

                const x = index * timeInterval * 5; // Change the distance on the axe X
                const y = 335 - ((temperature - minValue) / valueRange) * 335 ; // Change the size on the axe X

                if (index === 0 || index === data.length - 1) {
                    const timeLabel = document.createElement('div');
                    timeLabel.className = 'axis-label';
                    timeLabel.style.left = x + 40 + 'px';
                    timeLabel.style.bottom = '0';
                    timeLabel.textContent = temperatureData[index].time;
                    chart.appendChild(timeLabel);
                }

                if(i < data.length - 1) {
                    const x2 = (i + 1) * timeInterval * 5;
                    const y2 = 335 - ((data[i + 1] - minValue) / valueRange) * 335;
                    const distance = Math.sqrt(Math.pow(x2 - x, 2) + Math.pow(y2 - y, 2));

                    const line = document.createElement('div');
                    line.className = 'line';
                    line.style.left = x + 54 + 'px';
                    line.style.top = y + 27 + 'px';
                    line.style.width = Math.sqrt(Math.pow(x2 - x, 2) + Math.pow(y2 - y, 2)) + 'px';
                    line.style.transformOrigin = '0% 0%';
                    line.style.transform = `rotate(${Math.atan2(y2 - y, x2 - x)}rad)`;
                    chart.appendChild(line);
                    i++;
                }
                const newPoint = document.createElement('div');
                newPoint.className = 'point';
                newPoint.style.left = x + 50 + 'px';
                newPoint.style.top = y + 25 + 'px';

                chart.appendChild(newPoint);

                const tempLabel = document.createElement('div');
                tempLabel.className = 'axis-label';
                tempLabel.style.left = x + 40 + 'px';
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
            temperatureData = callData(temperatureData);
            toggleTemperature();
    });

    // Create the graphic by page opening
    window.onload = function() {
            temperatureData = callData(temperatureData);
            toggleTemperature();
        };