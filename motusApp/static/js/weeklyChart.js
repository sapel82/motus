// Get chart data from server
function getWeeklyData(){
    var weeklyData;
    $.ajax({
        type: 'GET',
        url: `/app/weekly_data/`,
        datatype: 'json',
        async: false,
        success: function (result){ weeklyData = $.parseJSON(result); }
    })
    return weeklyData;
}

const weeklyData = getWeeklyData();

const weekly_labels = weeklyData[0];

const weekly_data = {
    labels: weekly_labels,
    datasets: [{
        label: 'Deine Stimmung',
        backgroundColor: 'rgb(126, 206, 186)',
        borderColor: 'rgb(126, 166, 206)',
        borderWidth: 2,
        hoverBorderWidth: 3,
        pointRadius: 5,
        cubicInterpolationMode: 'monotone',
        data: weeklyData[1],
    }]
};

const weekly_plugins = {
    legend: {
        position: 'bottom'
    },
    tooltip: {
        enabled: false,
    }
}

const weekly_scales = {
    x: {
        ticks: {
            display: true
        }
    },
    y: {
        beginAtZero: true,
        min: -2,
        max: 2,
        ticks: {
            stepSize: 1,
            // font: {
            //     size: 12
            // },
            callback: function(value, index, ticks) {
                /*
                switch (value) {
                    case 0:
                        return '';

                    case 1:
                        return 'sehr traurig';
                    
                    case 2:
                        return 'traurig';

                    case 3:
                        return 'neutral';

                    case 4:
                        return 'fröhlich';

                    case 5:
                        return 'sehr fröhlich';

                    default:
                        return "Hmm";
                }
                */
                
                switch (value) {
                    case 0:
                        return 'neutral';

                    case -2:
                        return 'sehr traurig';
                    
                    case -1:
                        return 'traurig';

                    case 1:
                        return 'fröhlich';

                    case 2:
                        return 'sehr fröhlich';

                    default:
                        return "Hmm";
                }
            }
        },
    }
}

const weekly_options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: weekly_plugins,
    scales: weekly_scales,
}

const weekly_config = {
    type: 'line',
    data: weekly_data,
    options: weekly_options,
}
    
const weeklyChart = new Chart(
    document.getElementById('WeeklyChart'),
    weekly_config
);
