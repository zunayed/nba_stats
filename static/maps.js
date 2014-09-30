/*global d3: false  */
"use strict";

//set up map and default dataset
var w = screen.width;
var h = screen.height;
var curr_team = "New York Knicks";
var curr_team_abbr = "NYK"
var curr_stat = "FT_PCT"
var nba_data;
var states_data;
var setColor;   // Quantize function
var setSize;    // Quantize function
var svg;
var counties
var point_group;

//map type & center point 
var projection = d3.geo.mercator()
    .center([-101.381836, 42.587699])
    .scale(1000);

var path = d3.geo.path().projection(projection);

//reading data file first to get values
d3.json("static/data/league_data_averaged.json", function(data){
    nba_data = data[curr_team];
});

//reading geoJSON & CSV files
d3.json("static/data/us_states_small_size.json", function(states){
    states_data = states
    initializeSVG()
    createMap(states_data);
    plotData();
});

var initializeSVG = function(domain){
    //initialize map
    svg = d3.select("#d3_map")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

    // create a container for counties & stadium points
    counties = svg.append("g")
        .attr("id", "counties");

    point_group = svg.append("g");
};



var setQuantizeFunc = function(domain){
    console.log(domain)
    //set up a quantize function to associate with colorbrew styles
    setColor = d3.scale.quantize()
        .domain(domain)
        .range(colorbrewer.Greens[8].slice(1));

    //set up function for radius size
    setSize = d3.scale.quantize()
        .domain(domain)
        .range(d3.range(6,35).map(function(i) { return i; }));
};

//draw world map
var createMap = function(states) {
    counties.append("g")
        .selectAll("path")
        .data(states.features)
        .enter()
        .append("path")
        .style("fill", "#A9BCF5")
        .attr("stroke", "#fff")
        .attr("d", path);
};

var plotData = function() {
    //reading data file
    setQuantizeFunc(calcMinMax(nba_data));

    d3.csv("static/data/stadium_geo_data.csv", function(data){
        point_group.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function(d){ return projection([d.lon, d.lat])[0]; })
            .attr("cy", function(d){ return projection([d.lon, d.lat])[1]; })
            .attr("shortname", function(d){ return d.shortname; })
            .attr("team", function(d){ return d.team; })
            .attr("r", function(d){ return radSize(d.shortname); })
            .attr("fill", function(d){ return radColor(d.shortname); })
            .on("mouseover", mouseOver)
            .on("mouseout", mouseOut)
    });
};

var mouseOver = function() {
    d3.select(this).style("stroke", "green");
    d3.select(this).style("stroke-width", "4px");
    var team_name = d3.select(this).attr("team");
    var team_abbr = d3.select(this).attr("shortname");
    var stat_value = Math.round(nba_data[team_abbr][curr_stat] * 100)/100;
    d3.select("#infoBox").html( curr_stat + " - " + team_name + " : " + stat_value);
};

var mouseOut = function() {
    d3.select(this).style("stroke", "");
    d3.select(this).style("stroke-width", "");
};

var calcMinMax = function(data) {
    var min_value = 200;
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

// determine size of circle
var radSize = function(shortname) {
    if(shortname == curr_team_abbr) {
        return 0
    }else {
        try {
            return setSize(nba_data[shortname][curr_stat]);
        }
        catch (e) {
            console.log(e);
            return setSize(0);
        }
    }
};

// determine color of circle
var radColor = function(shortname) {
    if(shortname == curr_team_abbr) {
        return setColor(0);
    }else {
        try {
            return setColor(nba_data[shortname][curr_stat]);
        }
        catch (e) {
            console.log(e); 
            return setColor(0);
        }
    }
};

//monitor dropdown menu to change map data
d3.select("#dataSelector").on("change", function() {
    curr_stat = this.value;
    console.log(curr_stat);
    // point_group.remove();
    // point_group = svg.append("g");
    // plotData()
    setQuantizeFunc(calcMinMax(nba_data))
    point_group.selectAll("circle")
        .transition()
        .duration(750)
        .attr("r", function(d){ return radSize(d.shortname); })
        .attr("fill", function(d){ return radColor(d.shortname); })
});
