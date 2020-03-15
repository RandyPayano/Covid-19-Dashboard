
        // The svg
        var svg = d3.select("svg"),
            width = +svg.attr("width"),
            height = +svg.attr("height");
        
        // Map and projection
        var projection = d3.geoNaturalEarth()
            .scale(width / 1.3 / Math.PI)
            .translate([width / 2, height / 2])
        
    
    
        // Create data for circles:
     
    
    
    
    
        // Load external data and boot
        d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson", function(data){
        
            // Draw the map
            svg.append("g")
                .selectAll("path")
                .data(data.features)
                .enter().append("path")
                    .attr("fill", "#778899")
                    .attr("d", d3.geoPath()
                        .projection(projection)
                    )
                    .style("stroke", "#fff")
    
    
              
                   
    
    // create a tooltip
    
    // create a tooltip 
    var Tooltip = d3.select("#my_dataviz")
          .append("div")
          .attr("class", "tooltip")
          .style("opacity", 1)
          .style("background-color", "white")
          .style("border", "solid")
          .style("border-width", "2px")
          .style("border-radius", "5px")
          .style("padding", "5px")
    
        // Three function that change the tooltip when user hover / move / leave a cell
        var mouseover = function(d) {
          Tooltip.style("opacity", 1)
        }
    
    
        var mousemove = function(d) {
          Tooltip.html(d.Country + "<br>" + "Total Cases: " + d.TotalCases + "<br>" + "Active Cases: "+  d.ActiveCases   + "<br>" + "long: " + d.long + "<br>" + "lat: " + d.lat)
            .style("left", (d3.mouse(this)[0]+10) + "px")
            .style("top", (d3.mouse(this)[1]) + "px")
        }
        var mouseleave = function(d) {
          Tooltip.style("opacity", 5)
        };
    
    
    
    
    
    
        d3.json("/latandlong", function(obj){
    
        console.log(obj);
        var obj = obj
        // Add circles:
        svg
          .selectAll("myCircles")
          .data(obj)
          .enter()
          .append("circle")
            .attr("cx", function(d){ return projection([d.long,d.lat])[0] })
            .attr("cy", function(d){ return projection([d.long,d.lat])[1] })
            .attr("r", d => d.graphing_value / 50 )
            .attr("class", "circle")
            .style("fill", "69b3a2")
            .attr("stroke", "#69b3a2")
            .attr("stroke-width", 1)
            .attr("fill-opacity", .7)
          .on("mouseover", mouseover)
          .on("mousemove", mousemove)
          .on("mouseleave", mouseleave)
    
    
    })
    })
    
    
  