$('select').timezones();

var chart = AmCharts.makeChart( "chartdiv", {
  "type": "pie",
  "theme": "light",
  "dataProvider": [  {
    "stats": "Uniqueviews",
    "litres": 128.3
  }, {
    "stats": "Opened",
    "litres": 99
  }, {
    "stats": "Names",
    "litres": 60
  }, {
    "stats": "Email",
    "litres": 50
  } ],
  "valueField": "litres",
  "titleField": "stats",
   "balloon":{
   "fixedPosition":true
  },
  "export": {
    "enabled": true
  }
} );