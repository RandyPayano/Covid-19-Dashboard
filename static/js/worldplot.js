
Plotly.d3.csv('images/covid16_table.csv', function(err, rows){
      function unpack(rows, key) {
          return rows.map(function(row) { return row[key]; });
      }
  
  var data = [{
        type: 'choropleth',
        locationmode: 'country names',
        locations: unpack(rows, 'Country'),
        z: unpack(rows, 'NewDeaths'),
        autocolorscale: false,
        reversescale: true,
        colorscale: 'Portland', 
        transforms: [{
          type: 'aggregate',
          groups: unpack(rows, 'Country'),
          aggregations: [
            {target: 'z', func: 'first', enabled: true},
        ]
    }]
   }];

    var layout = {
      title: 'Recovery Rate (%)',
      geo: {
          showframe: false,
          showcoastlines: false,
          projection:{
             type: 'robinson'
          }
      },
      updatemenus: [{
        x: 0.85,
        y: 1.15,
        xref: 'paper',
        yref: 'paper',
        yanchor: 'top',
        active: 0,
        showactive: false,
        buttons: []
  }]
    };

    Plotly.plot('graph', data, layout, {showSendToCloud: true});

});

