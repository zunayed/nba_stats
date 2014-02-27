/*global d3: false  */
"use strict";

//data
var knicks_data

//set up map
var w = screen.width;
var h = screen.height;

//map type & center point 
var projection = d3.geo.mercator()
    .center([-101.381836, 42.587699])
    .scale(1000);

var path = d3.geo.path().projection(projection);

//set up a qX-9 number to associate with colorbrew.css styles
var setColor = d3.scale.quantize()
    .domain([30, 50])
    .range(d3.range(8).map(function(i) { return "q" + (i) + "-9"; }));


//initialize map
var svg = d3.select("#d3_map")
    .append("svg")
    .attr("width", w)
    .attr("height", h);


// create a container for counties
var counties = svg.append("g")
    .attr("id", "counties")
    .attr("class", "Oranges");


//reading geoJSON & CSV files
d3.json("static/data/us_states_small_size.json", function(json){
    createMap(json);
});

//reading data file
d3.json("static/data/data.json", function(data){
    knicks_data = data
    // counties.selectAll("path")
    //   .attr("class", stateColor);
});


//map number of complaint to color intensity
var stateColor = function(state) {
    if(state in knicks_data){
        return setColor(knicks_data[state]['fg %']);
    }else{
        //no data
        return "q1-9";
    }
};

//draw world map
var createMap = function (states) {
    counties.append("g")
        .selectAll("path")
        .data(states.features)
        .enter()
        .append("path")
        // .style("fill", "#43a2ca")
        .attr("state", function(d) { return d.properties['NAME'] } )
        .attr("class", function(d) { return stateColor(d.properties['NAME']) } )
        .attr("stroke", "#fff")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .attr("d", path);
};


//D3 hoverbox info way
var mouseover = function() {
    d3.select(this).style("stroke-width", "4px");
    var state_name = d3.select(this).attr("state");

    if(state_name in knicks_data){
        var fg = (knicks_data[state_name]['fg %']).toFixed(2);
    }else{
        //no data
        var fg = 'N/A'
    }

    d3.select("#infoBox").html("State: " + state_name + ' ' + 'FG %: ' + fg);
};


var mouseout = function() {
    d3.select(this).style("stroke-width", "");
    d3.select(this).style("stroke", "#fff");
};