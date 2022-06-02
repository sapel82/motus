// Get chart data from server
function getAllTimeData(){
    var allTimeData;
    $.ajax({
        type: 'GET',
        url: `/app/alltime_data/`,
        datatype: 'json',
        async: false,
        success: function (result){ allTimeData = $.parseJSON(result); }
    })
    return allTimeData;
}

const alltime_labels = [
    'sehr traurig',
    'traurig',
    'neutral',
    'fröhlich',
    'sehr fröhlich'
];

const alltime_data = {
    labels: alltime_labels,
    datasets: [{
        label: '---',
        backgroundColor: [
            'rgb(206, 126, 126)',
            'rgb(206, 166, 126)',
            'rgb(206, 206, 126)',
            'rgb(166, 206, 126)',
            'rgb(126, 206, 126)'
        ],
        data: getAllTimeData()
    }]
};

const alltime_plugins = {
    legend: {
        position: 'bottom'
    },
}

const alltime_scales  = {
}

const alltime_options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: alltime_plugins,
    scales: alltime_scales,
}

const alltime_config = {
    type: 'doughnut',
    data: alltime_data,
    options: alltime_options,
}
    
const allTimeChart = new Chart(
    document.getElementById('allTimeChart'),
    alltime_config
);