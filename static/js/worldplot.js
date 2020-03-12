
Plotly.d3.csv('images/covid16_table.csv', function(err, rows){
      function unpack(rows, key) {
          return rows.map(function(row) { return row[key]; });
      }
  
  var data = [{
        type: 'choropleth',
        locationmode: 'country names',
        locations: unpack(rows, 'Country'),
        z: unpack(rows, 'NewDeaths'),
        autocolorscale: true,
        reversescale: true,
        colorscale: 'Portland', 
        transforms: [{
          type: 'aggregate',
          groups: unpack(rows, 'Country'),
          aggregations: [
            {target: 'z', func: 'avg', enabled: true},
        ]
    }]
   }];

    var layout = {
      title: '<b>World c',
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
        buttons: [{
            method: 'restyle',
            args: ['transforms[0].aggregations[0].func', 'last'],
            label: 'Last'
        }]
  }]
    };

    Plotly.plot('graph', data, layout, {showSendToCloud: true});

});

