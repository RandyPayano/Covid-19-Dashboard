
/// Create metadata panel
function create_metadata(sample) {

    d3.json(`/metadata/${sample}`).then(function(sample){
      var metaSample = d3.select(`#sample-metadata`).html(""); 

    metaSample.html("");
  

      Object.entries(sample).forEach(function([key,value]){   
        
      if (key === 'Country') {
        window.countryname = value
      
   
      } if (key === "A) World Population") {
        window.worldpop = value

      } if (key === "A) World Population Affected") {
        window.worldpopaff= value
        
      } if (key === "Aa) Total Cases") {
        window.totalcases = value
      

      } if (key === "D) Total Recovered") {
        window.trecovered = value

      } if (key === "E) Active Cases") {
        window.activecases= value

      } if (key === "E) Percentage Active") {
        window.pctactive = value
      
      } if (key === "G) Critical Condition") {
        window.criticalc = value

      } if (key === "G) Mortality Rate") {
        window.pctmortality= value

      } if (key === "G) Total Deaths") {
        window.totaldeaths = value
      
      } if (key === ["Tot Cases/1M pop"]) {
        window.casesperonemil = value
      
      } else {
        var somethingelse = "BLAH"


      }      
        var hi = " "
        

    

   
      






      })
 
  

      
      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.html("<br>") 

      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Country: "}  ${window.countryname} `)



      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Total Population: "} ${window.worldpop}`)


      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Total Cases: "} ${window.totalcases}`)


      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Population Affected: "} ${window.worldpopaff}`)

      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Total Cases Recovered: "} ${window.trecovered}`)


       



      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Total Active Cases: "} ${window.activecases}`)

      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Percentage Active: "} ${window.pctactive}`)


      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Total Critical Cases: "} ${window.criticalc}`)

      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Total Deaths: "} ${window.totaldeaths}`)

      var new_pp = metaSample.append("p").style("text-anchor", "left");
      new_pp.text(`${"Mortality Rate: "} ${window.pctmortality}`)
      

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