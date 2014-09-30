/*global d3: false  */
"use strict";

var curr_team = "New York Knicks";
var curr_team_abbr = "NYK"
var curr_stat = "FT_PCT"

//data
var nba_data;
var stadium_data;
var states_data;

//reading data file first to get values
d3.json("static/data/league_data_averaged.json", function(data){
    nba_data = data[curr_team];
});

//set up map
var w = screen.width;
var h = screen.height;

//map type & center point 
var projection = d3.geo.mercator()
    .center([-101.381836, 42.587699])
    .scale(1000);

var path = d3.geo.path().projection(projection);

//set up a quantize function to associate with colorbrew styles
var setColor = d3.scale.quantize()
    .domain([.605, .902])
    .range(colorbrewer.Greens[5]);

//set up function for radius size
var setSize = d3.scale.quantize()
    .domain([.605, .902])
    .range(d3.range(4,20).map(function(i) { return i; }));

//initialize map
var svg = d3.select("#d3_map")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

// create a container for counties
var counties = svg.append("g")
    .attr("id", "counties");

// create container for stadium points
var point_group = svg.append("g");

//reading geoJSON & CSV files
d3.json("static/data/us_states_small_size.json", function(states){
    states_data = states
    createMap(states_data);
});

//reading data file
d3.csv("static/data/stadium_geo_data.csv", function(data){
    stadium_data = data
    createPoints(stadium_data);
});

var calc_min_max = function(data) {
    var min_value = 1;
    var max_value = 0;

    for (var team in data) {
        var val = data[team][curr_stat]
        if(val > max_value){
            max_value = val
        }else if (val < min_value) {
            min_value = val
        }
    }
    return [min_value, max_value];
};

var radSize = function(place) {
    if(place == curr_team_abbr) {
        return 0
    }else {
        try {
            return setSize(nba_data[place][curr_stat]);
        }
        catch (e) {
            console.log(e);
            return setSize(0);
        }
    }
};

var radColor = function(place) {
    if(place == curr_team_abbr) {
        return setColor(0);
    }else {
        try {
            return setColor(nba_data[place][curr_stat]);
        }
        catch (e) {
            console.log(e); // pass exception object to error handler
            return setColor(0);
        }
    }
};

//draw world map
var createMap = function (states) {
    counties.append("g")
        .selectAll("path")
        .data(states.features)
        .enter()
        .append("path")
        .style("fill", "#43a2ca")
        // .attr("state", function(d) { return d.properties['NAME'] } )
        // .attr("class", function(d) { return stateColor(d.properties['NAME']) } )
        .attr("stroke", "#fff")
        .attr("d", path);
};


// place dots on screen based on cities
var createPoints = function(json){
    point_group.selectAll("circle")
        .data(json)
        .enter()
        .append("circle")
        .attr("cx", function(d){ return projection([d.lon, d.lat])[0]; })
        .attr("cy", function(d){ return projection([d.lon, d.lat])[1]; })
        .attr("place", function(d){ return d.place; })
        .attr("team", function(d){ return d.team; })
        .attr("r", function(d){ return radSize(d.place)})
        // .style("fill", "red")
        .attr("fill", function(d){ return radColor(d.place) } )

        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
};

var mouseover = function() {
    d3.select(this).style("stroke", "green");
    d3.select(this).style("stroke-width", "4px");
    var team_name = d3.select(this).attr("team");
    d3.select("#infoBox").html("Team: " + team_name);
};

var mouseout = function() {
    d3.select(this).style("stroke", "");
    d3.select(this).style("stroke-width", "");
};

//monitor dropdown menu to change map data
// d3.select("#dataSelector").on("change", function() {
//     current = dataSets[this.value]

//     setColor.domain([current.minDomain, current.maxDomain]);
//     createMap(states_data);

//     counties.attr("class", current.color);
// });
