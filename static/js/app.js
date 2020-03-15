
/// Create metadata panel
function create_metadata(sample) {

    d3.json(`/metadata/${sample}`).then(function(sample){
      var metaSample = d3.select(`#sample-metadata`).html(""); 

    metaSample.html("");

      Object.entries(sample).forEach(function([key,value]){
        var new_p = metaSample.append("p");
        new_p.text(`${key}:${value}`)
      })
    });
}


function init() {
  var selector = d3.select("#selDataset");

  d3.json("/names").then((sampleNames) => {sampleNames.forEach((sample) => {selector.append("option").text(sample).property("value", sample);});

    create_metadata(sampleNames[0]);
  
  });
}


function refresh_data(newSample) {

  create_metadata(newSample);
}

init();