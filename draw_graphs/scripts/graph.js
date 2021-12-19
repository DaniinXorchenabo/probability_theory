const _d1 = {18.055: 8, 20.165: 7, 22.275: 12, 24.385: 14, 26.495: 15, 28.605: 14, 30.715: 12, 32.825: 8, 34.94: 10}

const _d2 = {
    0: 0,
    16.99: 0,
    17.01: 0.08,
    19.10: 0.08,
    19.11: 0.15,
    21.21: 0.15,
    21.22: 0.27,
    23.32: 0.27,
    23.33: 0.41,
    25.43: 0.41,
    25.44: 0.56,
    27.54: 0.56,
    27.55: 0.7,
    29.65: 0.7,
    29.66: 0.82,
    31.76: 0.82,
    31.77: 0.9,
    33.87: 0.9,
    33.88: 1.0,
    35.98: 1.0,
    100.01: 1.0
}

var trace1 = {
    type: 'bar',
    x: [...Object.keys(_d1)],
    y: [...Object.values(_d1)],
    marker: {
        color: '#C8A2C8',
        line: {
            width: 2.5
        }
    }
};
var trace2 = {
    mode: 'lines',
    x: [...Object.keys(_d1)],
    y: [...Object.values(_d1)],
    line: {
        color: '#ffa706',
        width: 5.5,
    }
};
var trace3 = {
    mode: 'lines',
    x: [...Object.keys(_d2)],
    y: [...Object.values(_d2)],
    line: {
        color: '#ffa706',
        width: 5.5,
    }
};


const data = [
    trace1, // Отрисовка гистограммы
    trace2, // Отрисовка многоугольника распределения
    trace3  // Отрисовка функции распределения
];

const layout = {
    font: {size: 18}
};

const config = {responsive: true}

Plotly.newPlot('my_graph', data, layout, config);