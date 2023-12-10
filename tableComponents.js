import { temperatureData} from './temperatureData.js';

export function updateTable(isCelsius) {
    const dataTableBody = document.querySelector('#dataTable tbody');
    dataTableBody.innerHTML = '';

    temperatureData.forEach((item) => {
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