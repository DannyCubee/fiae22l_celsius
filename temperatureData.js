export const temperatureData = [
    {time: '8:00', celsius: 10, fahrenheit: 58},
    {time: '10:00', celsius: 15, fahrenheit: 69},
    {time: '12:00', celsius: 20, fahrenheit: 46},
    {time: '14:00', celsius: 18, fahrenheit: 35},
    {time: '16:00', celsius: 16, fahrenheit: 50}
];

export function generateRandomTemperature() {
    temperatureData.forEach((item, index) => {
        item.celsius = Math.floor(Math.random() * 51) - 10;
        item.fahrenheit = (item.celsius * 9 / 5) + 32;
    });

    return temperatureData;
}