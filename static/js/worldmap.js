const height = 600,
    width = window.innerWidth

// Create a projection
const projection = d3.geoMercator().translate([width / 2, height / 2])

//  Create a path

const path = d3.geoPath().projection(projection)

const svg = d3
    .select("plottt")
    .append("svg")
    .attr("height", height)
    .attr("width", width)
    .call(
        d3
            .zoom()
            .scaleExtent([1, 20])
            .on("zoom", function() {
                svg.attr("transform", d3.event.transform)
            })
    )
    .append("g")

const tooltip = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0)

const mapURL =
    "https://d3js.org/world-50m.v1.json"

const meteoriteURL =
    "https://raw.githubusercontent.com/FreeCodeCamp/ProjectReferenceData/master/meteorite-strike-data.json"

const radiusScale = d3.scaleSqrt().range([2, 50])

const colorScale = d3.scaleOrdinal(d3.schemeCategory20)

function removeNullData(i) {
	if(i.geometry !== null && i.properties.mass !== null) return true
}

const formatYear = d3.timeFormat("%Y")

d3.json(mapURL, (error, data) => {
    const countryData = topojson.feature(data, data.objects.countries).features

    svg
        .append("g")
        .selectAll("path")
        .data(countryData)
        .enter()
        .append("path")
        .attr("class", "land")
        .attr("d", path)

    d3.json(meteoriteURL, (error, mData) => {
        mData = mData.features.filter(removeNullData)

        const meteorMass = mData.map(meteor => +meteor.properties.mass)

        radiusScale.domain(d3.extent(meteorMass))

        colorScale.domain(d3.extent(meteorMass))

        svg
            .append("g")
            .selectAll("circle")
            .data(mData)
            .enter()
            .append("circle")
            .attr("class", "circle")
            .attr("fill", d => colorScale(+d.properties.mass))
            .attr("r", d => radiusScale(+d.properties.mass))
            .attr(
                "transform",
                d =>
                    "translate(" +
                    projection([
                        d.geometry.coordinates[0],
                        d.geometry.coordinates[1]
                    ]) +
                    ")"
            )
            .on("mouseover", function(d) {
                tooltip
                    .transition()
                    .duration(100)
                    .style("opacity", 0.9)
                tooltip
                    .html(
                        "<h2>Name: " +
                            d.properties.name +
                            "</h2><h2>Year: " +
                            formatYear(new Date(d.properties.year)) +
                            "</h2><h2> Mass: " +
                            d3.format(",")(d.properties.mass) +
                            "</h2>"
                    )
                    .style("left", d3.event.pageX + 10 + "px")
                    .style("top", d3.event.pageY - 20 + "px")
            })
            .on("mouseout", function() {
                tooltip
                    .transition()
                    .duration(500)
                    .style("opacity", 0)
            })
    })
})