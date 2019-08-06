var chart = AmCharts.makeChart( "am_bar_chart", {
    "type": "serial",
    "theme": "light",
    "dataProvider": [ {
        "make": "USA",
        "visits": 2025
    }, {
        "make": "China",
        "visits": 1882
    }, {
        "make": "Japan",
        "visits": 1809
    }, {
        "make": "Germany",
        "visits": 1322
    }, {
        "make": "UK",
        "visits": 1122
    }, {
        "make": "France",
        "visits": 1114
    }, {
        "make": "India",
        "visits": 984
    }, {
        "make": "Spain",
        "visits": 711
    }, {
        "make": "Netherlands",
        "visits": 665
    }, {
        "make": "Russia",
        "visits": 580
    }, {
        "make": "South Korea",
        "visits": 443
    }, {
        "make": "Canada",
        "visits": 441
    }, {
        "make": "Brazil",
        "visits": 395
    } ],
    "valueAxes": [ {
        "gridPosition": "start",
        "gridColor": "#000000",
        "gridAlpha": 0.05,
        "dashLength": 0,
        "axisColor": "#D9E2E3",
        "color": "#717C7D",
        "guides": [{
            "value": 1300,
            "lineColor": "#E87722",
            "tickLength": 20,
            "lineAlpha": 0.75,
            "lineThickness": 2
        }]
    } ],
    "gridAboveGraphs": true,
    "startDuration": 1,
    "graphs": [ {
        "balloonText": "[[category]]: <b>[[value]]</b>",
        "fillAlphas": 0.8,
        "lineAlpha": 0,
        "fillColors": ['#00A3E0', '#00C3ED'],
        "gradientOrientation": "vertical",
        "type": "column",
        "valueField": "visits"
    } ],
    "chartCursor": {
        "categoryBalloonEnabled": false,
        "cursorAlpha": 0,
        "zoomable": false
    },
    "categoryField": "make",
    "categoryAxis": {
        "gridPosition": "start",
        "gridAlpha": 0,
        "tickPosition": "start",
        "tickLength": 20,
        "axisColor": "#D9E2E3",
        "color": "#717C7D"
    },
    "export": {
        "enabled": true
    }

} );