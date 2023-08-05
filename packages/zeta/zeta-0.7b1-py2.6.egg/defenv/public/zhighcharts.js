// This file is subject to the terms and conditions defined in
// file 'LICENSE', which is part of this source code package.
//       Copyright (c) 2009 SKR Farms (P) LTD.

var z_hctheme = 'default';
var z_hccolors = [ '#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5',
                   '#64E572', '#FF9655', '#FFF263', '#6AF9C4' ]

function hc_setoption( charttheme ) {
    var theme = charttheme ? charttheme : z_hctheme;
    hcthemes[theme] = jQuery.extend(
                            true, null,
                            hcthemes[theme],
                            { credits: { enabled: false } }
                      );
    Highcharts.setOptions( hcthemes[theme] );
}

/*************************** Tag Charts ******************************/

function chart1_tagchart( data, id ) {
    var total = 0
    dojo.forEach( data, function(item) { total += item[1]; } )

    hc_setoption( 'minimal' );
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
        },
        title: { text: 'Tagged items by category' },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        if (this.y > 5) return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b>: '
                       + Math.round((this.y/total)*100) + ' % ';
            }
        },
        series: [{
            name: 'Count',
            data: data
        }]
    });
    return chart
}

/*************************** Attachment Charts ******************************/

function chart2_user_vs_attach( data, id ) {
    var users   = dojo.map( data, "return item[0]" );
    var files   = dojo.map( data, "return item[1]" );
    var payload = dojo.map( data, "return item[2]" );

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            zoomType: 'x',
            margin: [ 50, 50, 100, 80]
        },
        title: {
            text: 'Uploaded files and its payload, by user',
        },
        subtitle: {
            text: 'Click and drag in the plot area to zoom in',
        },
        xAxis: [{
            maxZoom: 10,
            tickInterval: 1,
            labels: {
                rotation: -45,
                align: 'right',
                formatter: function() { return data[this.value][0]; }
            }
        }],
        yAxis: [{ // Primary yAxis
            title: {
                text: 'Uploaded Payload',
                style: { color: '#89A54E' },
                margin: 100
            },
            labels: {
                formatter: function() {
                    return Math.round(this.value / 1024) + ' KB';
                },
                style: { color: '#89A54E' }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Uploaded files',
                style: { color: '#4572A7' },
                margin: 60
            },
            labels: {
                style: { color: '#4572A7' }
            },
            opposite: true
        }],
        tooltip: {
            formatter: function() {
                return '<b>'+ data[this.x][0] +'</b><br/>' +
                       (this.series.name == 'files' ? 'files : ' : 'payload : ') +
                       this.y;
            }
        },
        legend: { },
        series: [{
            name: 'payload',
            color: '#89A54E',
            type: 'column',
            data: payload
        
        }, {
            name: 'files',
            color: '#4572A7',
            type: 'spline',
            yAxis: 1,
            data: files
        }]
    });
    return chart
}

function chart3_attach_vs_download( data, id ) {
    var counts  = dojo.map( data, "return item[2]" );

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'line',
            zoomType: 'x'
        },
        title: { text: 'Files downloaded' },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            title: {
                enabled: true,
                text: 'Attachments'
            },
            maxZoom: 10
        },
        yAxis: {
            title: { text: 'Download count' }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ data[this.x][1] + '</b>,'+ this.y;
            }
        },
        plotOptions: {
            line: {
                marker: {
                    enabled: true,
                    radius: 1,
                    states: {
                        hover: { enabled: true, radius: 3 }
                    }
                },
                fillOpacity: 0.1,
                lineWidth: 1,
            }
        },
        series: [{
            data: counts,
        }]
    });
    return chart
}

function chart4_attach_vs_tags( data, id ) {
    var attach_no = dojo.map( data, "return item[1].length" );
    var tagnames  = dojo.map( data, "return item[0]" );
    var filenames = function( attachs ) {
                        return dojo.map( attachs, "return item[1]" );
                    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'column',
            zoomType: 'x'
        },
        title: { text: 'Attachments by tagname' },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            title: { text: 'Tagname' },
            tickInterval: 1,
            labels: {
                formatter: function() { return tagnames[this.value] },
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { text: 'No. of Attachments' }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ data[this.x][0] + '</b><br/>' +
                           filenames( data[this.x][1] ).join( '<br/>' )
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    formatter: function() { return this.y },
                    enabled : true,
                    style: {
                        color: '#FFFFFF'
                    }
                }
            }
        },
        series: [{
            name: 'tagged attachments',
            data: attach_no
        }]
    });
    return chart
}


function chart5_attach_vs_time( fromdate, data, id ) {
    var count = dojo.map( data, "return item.length" )
    var files = function( items ) {
                    return items ?
                                dojo.map( items, "return '<b>'+item[1]+'</b>' + ', ' + item[2]" )
                                : ''
                }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            zoomType: 'x'
        },
        title: {
            text: 'Attachments uploaded in timeline'
        },
        subtitle: {
            text: 'Click and drag in the plot area to zoom in'
        },
        xAxis: {
            type: 'datetime',
            maxZoom: 20 * 24 * 3600000, // Twenty days
            title: { text: null }
        },
        yAxis: {
            title: { text: 'Upload activity' },
            startOnTick: false,
            showFirstLabel: false
        },
    
        tooltip: {
            formatter: function() {
                var offset = (this.x-fromdate) / 3600 / 1000 / 24
                return files( data[offset] ).join( '<br/>' );
            }
        },
        legend: { enabled: false },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.5,
                lineWidth: 1,
                marker: {
                    enabled: true,
                    radius: 1,
                    states: {
                        hover: { enabled: true, radius: 3 }
                    }
                },
                shadow: false,
                states: {
                    hover: { lineWidth: 1 }
                }
            }
        },
        series: [{
            type: 'areaspline',
            name: 'uploadedtime',
            pointInterval: 24 * 3600 * 1000,
            pointStart: fromdate,
            data: count
        }]
    });
    return chart
}

/*************************** License Charts ******************************/

function chart6_license_projects( data, id ) {
    var piedata = dojo.map( data, "return [ item[1], item[2].length ]" );
    var lic_tot = 0
    dojo.forEach( data, function(item) { lic_tot += item[2].length; } )

    hc_setoption( 'minimal' );
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            margin: [50, 200, 60, 170]
        },
        title: { text: 'Projects under license' },
        plotArea: {
            shadow: null,
            borderWidth: null,
            backgroundColor: null
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b>: '
                       + Math.round((this.y/lic_tot)*100) +' % <br/> '
                       + data[this.point.x][2].join( '<br/>' )
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        legend: {
            layout: 'vertical',
            style: {
                left: '10px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        series: [{
            type: 'pie',
            name: 'LicenseProject',
            data: piedata,
        }]
    });
    return chart;
}


function chart7_license_vs_tags( data, id ) {
    var lic_no    = dojo.map( data, "return item[1].length" );
    var tagnames  = dojo.map( data, "return item[0]" );
    var filenames = function( fortag ) {
                        return dojo.map( fortag[1], "return item[1]" )
                    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'column',
            zoomType: 'x',
            margin: [ 50, 50, 100, 80]
        },
        title: { text: 'License by tagname' },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            title: { text: 'Tagname' },
            tickInterval: 1,
            labels: {
                formatter: function() { return tagnames[this.value] },
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { text: 'No. of License' }
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ data[this.x][0] + '</b><br/>' +
                       filenames( data[this.x] ).join( ', ' )
            }
        },
        plotOptions: {
            line: {
                marker: {
                    enabled: false
                },
                fillOpacity: 0.1,
                lineWidth: 1,
            }
        },
        series: [{
            name: 'tagged license',
            data: lic_no
        }]
    });
    return chart
}

/*************************** Users Charts ******************************/

function chart8_users_activity( data, id ) {
    var users   = dojo.map( data, 'return item[1]' );
    var weights = dojo.map( data, 'return item[2]' );

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'column',
            zoomType: 'x',
            margin: [ 50, 50, 100, 80]
        },
        title: {
            text: 'User contribution'
        },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            categories: users,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: { 
                text: 'Total activity count',
                margin: 60
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    formatter: function() { return this.y },
                    enabled : true,
                    style: {
                        color: '#FFFFFF'
                    }
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.x +'</b><br/>'+ 'Made '+ this.y + ' updates';
            }
        },
        series: [{
            name: 'Activity',
            data: weights,
        }]
    });
    return chart;
}

function chart9_users_siteperm( data, id ) {
    var users       = dojo.map( data, 'return item[1]' );
    var siteperms   = dojo.map( data, 'return item[2].length' );
    var x_siteperms = dojo.map( data, 'return item[3].length' );
    var usersiteperms = function( username ) {
                            var u = null;
                            for(i = 0; i < data.length; i++ ) {
                                u = data[i];
                                if( u[1] == username ) { break; }
                            }
                            return u;
                        }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'column',
            margin: [ 50, 50, 100, 80]
        },
        title: {
            text: 'Site-wide permissions granted to each user'
        },
        xAxis: {
            categories: users,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: { text: 'Site Permissions' }
        },
        tooltip: {
            formatter: function() {
                var u = usersiteperms( this.x );
                return '<b>' + this.x + '</b><br/>' +
                       (this.series.name == 'granted permissions'
                            ? u[2].join( ', ' ) : u[3].join( ', ' ) )
            }
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled : true,
                    style: {
                        color: '#FFFFFF'
                    }
                }
            }
        },
        series: [{
                name: 'granted permissions',
                data: siteperms
            }, {
                name: 'permissions not granted',
                data: x_siteperms
        }]
    });
    return chart;
}

function chart10_project_admins( data, id ) {
    var piedata = dojo.map( data, "return [ item[1], item[2].length ]" );
    var total   = 0
    dojo.forEach( data, function(item) { total += item[2].length; } )

    hc_setoption( 'minimal' );
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
        },
        title: { text: 'Pie chart of projects administrators' },
        legend: {
            layout: 'vertical',
            style: {
                left: '100px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b> : '
                       + Math.round((this.y/total)*100) + ' % ' + '<br/>'
                       + data[this.point.x][2].join( '<br/>' )

            }
        },
        series: [{
            name: 'Project',
            data: piedata
        }]
    });
    return chart;
}

function chart11_component_owners( total, data, id ) {
    var piedata = dojo.map( data, "return [ item[1], item[2].length ]" );

    hc_setoption( 'minimal' );
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
        },
        title: { text: 'Pie chart of component owners' },
        legend: {
            layout: 'vertical',
            style: {
                left: '100px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b>: '
                       + Math.round((this.y/total)*100) + ' % ' + '<br/>'
                       + data[this.point.x][2].join( '<br/>' )
            }
        },
        series: [{
            name: 'Components',
            data: piedata
        }]
    });
    return chart;
}

/*************************** User Charts ******************************/

function chart12_userproject_activity( data, id ) {
    var piedata = data[2];
    var total   = 0;
    for(i = 0; i < data[2].length; i++ ) {
        total += data[2][i][1];
    }

    hc_setoption( 'minimal' );
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
        },
        title: { text: 'Function wise contribution by user' },
        legend: {
            layout: 'vertical',
            style: {
                left: '100px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: false,
                    color: 'white',
                    formatter: function() {
                        return this.point.name;
                    },
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function( _piedata ) {
                            return '<b>'+ this.point.name +'</b>: '
                                   + Math.round((this.y/total)*100) + ' % ' + '<br/>'
                                   + piedata[this.point.x][1]
            },
        },
        series: [{
            name: 'Project Activities',
            data: piedata
        }]
    });
    return chart;
}

/*************************** Milestone Charts ******************************/

function chart13_milestone_tickets( data, id ) {
    var types      = data[1];
    var severities = data[2];
    var statuses   = data[3];
    var owners     = data[4];

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            margin: [ 0, 0, 0, 80]
        },
        title: {
            text: 'Milestone tickets',
            style: {
                margin: '0 0 0 0'
            }
        },
        xAxis: {
        },
        tooltip: {
            formatter: function() {
                return '<b>' + this.point.name + ', </b>'
                       + this.point.y
            }
        },
        labels: {
            items: [{
                html: 'Ticket type',
                style: {
                    left: '60px',
                    top: '30px',
                    color: 'gray'				
                }
            }, {
                html: 'Ticket severity',
                style: {
                    left: '260px',
                    top: '30px',
                    color: 'gray'				
                }
            }, {
                html: 'Ticket status',
                style: {
                    left: '460px',
                    top: '30px',
                    color: 'gray'				
                }
            }, {
                html: 'Ticket owner',
                style: {
                    left: '660px',
                    top: '30px',
                    color: 'gray'				
                }
            }]
        },
        series: [{
            type: 'pie',
            name: 'bytype',
            data: types,
            center: [100, 130],
            size: 150,
            showInLegend: false
        }, {
            type: 'pie',
            name: 'byseverity',
            data: severities,
            center: [300, 130],
            size: 150,
            showInLegend: false
        }, {
            type: 'pie',
            name: 'bystatus',
            data: statuses,
            center: [500, 130],
            size: 150,
            showInLegend: false
        }, {
            type: 'pie',
            name: 'byowners',
            data: owners,
            center: [700, 130],
            size: 150,
            showInLegend: false
        }]
    });
    return chart;
}

/*************************** Project Charts ******************************/

function chart14_project_activity( data, id ) {
    var total = 0
    dojo.forEach( data, function(item) { total += item[1]; } )

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
        },
        title: { text: 'Function wise project activity' },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        if (this.y > 1) return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b>: '
                       + Math.round((this.y/total)*100) + ' % <br/> '
                       + this.y
            }
        },
        series: [{
            name: 'Activity',
            data: data
        }]
    });
    return chart
}

function chart15_roadmap( fromdate, data, id ) {
    var mstnnames = dojo.map( data, "return item[0]" )
    var prefix    = dojo.map( data, "return item[1]" )
    var open      = dojo.map( data, "return item[2]" )
    var cancelled = dojo.map( data, "return item[3]" )
    var completed = dojo.map( data, "return item[4]" )

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'bar',
            margin: [50, 50, 100, 100]
        },
        title: {
            text: 'Milestone timeline'
        },
        xAxis: {
            gridLineWidth: 1,
            categories: mstnnames
        },
        yAxis: {
            gridLineWidth: 0,
            title: {
                text: 'Time'
            },
            tickWidth: 1,
            labels: {
                formatter: function() {
                    var thisms = fromdate + this.value * (24*3600000);
                    return Highcharts.dateFormat( "%e. %b %y", thisms );
                },
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            }
        },
        legend: {
            enabled: true
        },
        tooltip: {
            formatter: function() { return this.y + ' days'; }
        },
        plotOptions: {
            bar: {
                shadow: false,
            },
            series: {
                stacking: 'normal'
            }
        },
        series: [{
            name: 'completed',
            color: '#b7d9ba',
            data: completed,
        }, {
            name: 'cancelled',
            color: '#eb9898',
            data: cancelled
        }, {
            name: 'open',
            color: '#968ff5',
            data: open
        }, {
            name: 'prefix',
            color: '#FFFFFF',
            data: prefix
        }]
    });
    return chart
}

/*************************** Wiki Charts ******************************/

function chart16_wiki_cmtsvers( data, id ) {
    var wikipages = dojo.map( data, 'return item[0]' );
    var versions  = dojo.map( data, 'return item[1]' );
    var comments  = dojo.map( data, 'return item[2]' );

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'column',
            zoomType: 'x',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'No. of edits and comments to wikipage'
        },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            categories: wikipages,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { 
                text: 'Count',
                margin: 60
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    formatter: function() { return this.y },
                    enabled : true,
                    style: {
                        color: '#FFFFFF'
                    }
                }
            }
        },
        legend: {
            enabled: true
        },
        tooltip: {
            formatter: function() {
                return this.series.name == 'Edits' ?
                            this.y + ' edits for, <br/>' + this.x :
                            this.y + ' comments for,<br/>' + this.x
            }
        },
        series: [{
            name: 'Edits',
            data: versions
        }, {
            name: 'Comments',
            data: comments
        }]
    });
    return chart;
}

function chart17_wikivotes( data, id ) {
    var wikipages = dojo.map( data, 'return item[0]' );
    var upvotes   = dojo.map( data, 'return item[1]' );
    var downvotes = dojo.map( data, 'return item[2]' );
    var totalupvotes = 0
    var totaldownvotes = 0
    dojo.forEach( data, function(x) {
                            totalupvotes += x[1];
                            totaldownvotes += x[2];
                        }
                )

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            zoomType: 'x',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Voting wikipage'
        },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            categories: wikipages,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { 
                text: 'Count',
            }
        },
        tooltip: {
            formatter: function() {
                var s;
                if (this.point.name) { // the pie chart
                    s = 'Total ' + this.point.name + ' : ' + this.y;
                } else {
                    s = this.y + ' ' + this.series.name;
                }
                return s;
            }
        },
        labels: {
            items: [{
                html: 'Total votes',
                style: {
                    left: '150px',
                    top: '8px',
                    color: 'black'				
                }
            }]
        },
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
        series: [{
            type: 'column',
            name: 'Upvotes',
            data: upvotes,
            color: '#89A54E'
        }, {
            type: 'column',
            name: 'Downvotes',
            data: downvotes,
            color: '#AA4643'
        }, {
            type: 'pie',
            name: 'Total upvotes and downvotes',
            data: [{
                name: 'Upvotes',
                y: totalupvotes,
                color: '#89A54E'
            }, {
                name: 'Downvotes',
                y: totaldownvotes,
                color: '#AA4643'
            }],
            center: [100, 50],
            size: 80,
            showInLegend: false
        }]
    });
    return chart;
}

function chart18_wikiauthors( data, id ) {
    function makedata( authors, i ) {
        var data  = [];
        var total = 0;
        for(j = 0; j < authors.length; j++) {
            data[data.length] = authors[j][i][1];
            total += authors[j][i][1]; 
        }
        return [ data, total ]
    }
    function makechart( authors ) {
        var wseries = [];
        var utotal  = [];
        for(i = 0; i < authors[0].length; i++ ) {
            var username = authors[0][i][0];
            var values   = makedata( authors, i );
            wseries[wseries.length] = {
                    type : 'column',
                    name : username,
                    data : values[0]
            }
            utotal[utotal.length] = {
                    name : username,
                    y    : values[1]
            }
        }
        return [ wseries, utotal ]
    }

    var wikipages = dojo.map( data, 'return item[0]' );
    var authors   = dojo.map( data, 'return item[1]' );
    var users     = dojo.map( authors[0], 'return item[0]' );
    var cpdata    = makechart( authors );
    var series    = cpdata[0];
    series[series.length] = { type: 'pie',
                              name: 'Total edits by authors',
                              data: cpdata[1],
                              center: [100, 50],
                              size: 100,
                              showInLegend: false
                            }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            zoomType: 'x',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Wikipage authors'
        },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            categories: wikipages,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { 
                text: 'Count',
            }
        },
        legend: {
            style: {
                left: '20px',
                bottom: '10px',
                right: 'auto',
                top: 'auto'
            }
        },
        tooltip: {
            formatter: function() {
                var s;
                if (this.point.name) { // the pie chart
                    s = '<b>' + this.point.name + '</b>,<br/>' + 'edited ' + this.y + ' times'
                } else {
                    s = '<b>' + this.series.name + '</b>,<br/>' + 'edited ' + this.y + ' times'
                }
                return s;
            }
        },
        labels: {
            items: [{
                html: 'Total edits by authors',
                style: {
                    left: '140px',
                    top: '0px',
                    color: 'black'				
                }
            }]
        },
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
        series: series
    });
    return chart;
}

function chart19_wikicommentors( data, id ) {
    function makedata( commentors, i ) {
        var data  = [];
        var total = 0;
        for(j = 0; j < commentors.length; j++) {
            data[data.length] = commentors[j][i][1];
            total += commentors[j][i][1]; 
        }
        return [ data, total ]
    }
    function makechart( commentors ) {
        var wseries = [];
        var utotal  = [];
        for(i = 0; i < commentors[0].length; i++ ) {
            var username = commentors[0][i][0];
            var values   = makedata( commentors, i );
            wseries[wseries.length] = {
                    type : 'column',
                    name : username,
                    data : values[0]
            }
            utotal[utotal.length] = {
                    name : username,
                    y    : values[1]
            }
        }
        return [ wseries, utotal ]
    }

    var wikipages = dojo.map( data, 'return item[0]' );
    var commentors= dojo.map( data, 'return item[1]' );
    var users     = dojo.map( commentors[0], 'return item[0]' );
    var cpdata    = makechart( commentors );
    var series    = cpdata[0];
    series[series.length] = { type: 'pie',
                              name: 'Total comments',
                              data: cpdata[1],
                              center: [100, 50],
                              size: 100,
                              showInLegend: false
                            }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            zoomType: 'x',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Wikipage comments'
        },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            categories: wikipages,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { 
                text: 'Count',
            }
        },
        legend: {
            style: {
                left: '20px',
                bottom: '10px',
                right: 'auto',
                top: 'auto'
            }
        },
        tooltip: {
            formatter: function() {
                var s;
                if (this.point.name) { // the pie chart
                    s = '<b>' + this.point.name + ',</b><br/>' + 'commented ' + this.y + ' times'
                } else {
                    s = '<b>' + this.series.name + ',</b><br/>' + 'commented ' + this.y + ' times'
                }
                return s;
            }
        },
        labels: {
            items: [{
                html: 'Total comments',
                style: {
                    left: '140px',
                    top: '0px',
                    color: 'black'				
                }
            }]
        },
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
        series: series
    });
    return chart;
}

function chart20_wiki_vs_tags( data, id ) {
    var wiki_no = dojo.map( data, "return item[1].length" );
    var tagnames  = dojo.map( data, "return item[0]" );
    var filenames = function( wikis ) {
                        return dojo.map( wikis, "return item[1]" );
                    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'column',
            zoomType: 'x',
            margin: [ 50, 50, 100, 80]
        },
        title: { text: 'Wikipages by tagname' },
        subtitle: { text: 'Click and drag in the plot area to zoom in'},
        xAxis: {
            title: { text: 'Tagname' },
            tickInterval: 1,
            labels: {
                formatter: function() { return tagnames[this.value] },
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { text: 'No. of wikipages' }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ data[this.x][0] + '</b><br/>' +
                           filenames( data[this.x][1] ).join( '<br/>' )
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    formatter: function() { return this.y },
                    enabled : true,
                    style: {
                        color: '#FFFFFF'
                    }
                }
            }
        },
        series: [{
            name: 'tagged wikipages',
            data: wiki_no
        }]
    });
    return chart;
}

/*************************** Ticket Charts ******************************/

function chart21_projtickets( data, id ) {
    var piedata = [{ name : 'type',
                     data : data[0],
                     center: [200, 200],
                     size: 250,
                     showInLegend: false
                  }, {
                     name : 'status',
                     data : data[1],
                     center: [550, 200],
                     size: 250,
                     showInLegend: false
                  }, {
                     name : 'severity',
                     data : data[2],
                     center: [900, 200],
                     size: 250,
                     showInLegend: false
                  }]

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
            margin: [ 50, 50, 100, 80]
        },
        title: {
            text: 'Pie chart of tickets by type, severity and status'
        },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        labels: {
            items: [{
                html: '<b>Tickets by type</b>',
                style: {
                    left: '140px',
                    top: '20px',
                    color: 'black'				
                }
            }, {
                html: '<b>Tickets by severity</b>',
                style: {
                    left: '500px',
                    top: '20px',
                    color: 'black'				
                }
            }, {
                html: '<b>Tickets by status</b>',
                style: {
                    left: '850px',
                    top: '20px',
                    color: 'black'				
                }
            }]
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return'<b>' + this.point.name + ',<b><br/>' + this.y;
            }
        },
        series: piedata
    });
    return chart;
}

function chart22_ticketowners( data, id ) {
    var piecharts = [];
    var items     = []
    yoffset = 0;
    for(i = 0; i < data.length; i++ ) {
        piecharts[piecharts.length] = { name : 'type',
                                        data : data[i][1],
                                        center: [100, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      }
        piecharts[piecharts.length] = { name : 'severity',
                                        data : data[i][2],
                                        center: [375, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      }
        piecharts[piecharts.length] = { name : 'status',
                                        data : data[i][3],
                                        center: [650, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      }
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by type',
                    style: {
                        left: '25px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        }
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by severity',
                    style: {
                        left: '300px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        }
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by status',
                    style: {
                        left: '575px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        }
        yoffset += 300;
    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
            margin: [ 50, 50, 100, 80]
        },
        title: {
            text: 'Pie chart of tickets by type, severity and status, for each user'
        },
        labels: {
            items : items
        },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return'<b>' + this.point.name + ',<b><br/>' + this.y;
            }
        },
        series: piecharts
    });
    return chart;
}

function chart23_ticketcomponents( data, id ) {
    var piecharts = [];
    var items     = [];
    yoffset = 0;
    for(i = 0; i < data.length; i++ ) {
        piecharts[piecharts.length] = { name : 'type',
                                        data : data[i][1],
                                        center: [100, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        piecharts[piecharts.length] = { name : 'severity',
                                        data : data[i][2],
                                        center: [375, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        piecharts[piecharts.length] = { name : 'status',
                                        data : data[i][3],
                                        center: [650, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by type',
                    style: {
                        left: '25px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by severity',
                    style: {
                        left: '300px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by status',
                    style: {
                        left: '575px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        yoffset += 300;
    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Pie chart of tickets by type, severity and status, for each components'
        },
        labels: {
            items : items
        },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return'<b>' + this.point.name + ',<b><br/>' + this.y;
            }
        },
        series: piecharts
    });
    return chart;
}

function chart24_ticketmilestones( data, id ) {
    var piecharts = []
    var items     = []
    yoffset = 0;
    for(i = 0; i < data.length; i++ ) {
        piecharts[piecharts.length] = { name : 'type',
                                        data : data[i][1],
                                        center: [100, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        piecharts[piecharts.length] = { name : 'severity',
                                        data : data[i][2],
                                        center: [375, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        piecharts[piecharts.length] = { name : 'status',
                                        data : data[i][3],
                                        center: [650, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by type',
                    style: {
                        left: '25px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by severity',
                    style: {
                        left: '300px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by status',
                    style: {
                        left: '575px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        yoffset += 300;
    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Pie chart of tickets by type, severity and status, for each milestone'
        },
        labels: {
            items : items
        },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return'<b>' + this.point.name + ',<b><br/>' + this.y;
            }
        },
        series: piecharts
    });
    return chart;
}

function chart25_ticketversions( data, id ) {
    var piecharts = []
    var items     = []
    yoffset = 0;
    for(i = 0; i < data.length; i++ ) {
        piecharts[piecharts.length] = { name : 'type',
                                        data : data[i][1],
                                        center: [100, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        piecharts[piecharts.length] = { name : 'severity',
                                        data : data[i][2],
                                        center: [375, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        piecharts[piecharts.length] = { name : 'status',
                                        data : data[i][3],
                                        center: [650, 150+yoffset],
                                        size: 200,
                                        showInLegend: false
                                      };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by type',
                    style: {
                        left: '25px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by severity',
                    style: {
                        left: '300px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        items[items.length]         = {
                    html: 'for <span class="fgcrimson">'+data[i][0]+'</span>, by status',
                    style: {
                        left: '575px',
                        top: (20+yoffset)+'px',
                        color: 'black'				
                    }
        };
        yoffset += 300;
    }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Pie chart of tickets by type, severity and status, for each version'
        },
        labels: {
            items : items
        },
        legend: {
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return'<b>' + this.point.name + ',<b><br/>' + this.y;
            }
        },
        series: piecharts
    });
    return chart;
}

function chart26_ticketcommentors( data, id ) {
    function makedata( commentors, i ) {
        var data  = [];
        var total = 0;
        for(j = 0; j < commentors.length; j++) {
            data[data.length] = commentors[j][i][1];
            total += commentors[j][i][1]; 
        }
        return [ data, total ]
    }
    function makechart( commentors ) {
        var wseries = [];
        var utotal  = [];
        for(i = 0; i < commentors[0].length; i++ ) {
            var username = commentors[0][i][0];
            var values   = makedata( commentors, i );
            wseries[wseries.length] = {
                    type : 'column',
                    name : username,
                    data : values[0]
            }
            utotal[utotal.length] = {
                    name : username,
                    y    : values[1]
            }
        }
        return [ wseries, utotal ]
    }

    var tickets   = dojo.map( data, 'return item[0]' );
    var commentors= dojo.map( data, 'return item[1]' );
    var users     = dojo.map( commentors[0], 'return item[0]' );
    var cpdata    = makechart( commentors );
    var series    = cpdata[0];
    series[series.length] = { type: 'pie',
                              name: 'Total comments',
                              data: cpdata[1],
                              center: [100, 50],
                              size: 100,
                              showInLegend: false
                            }

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            zoomType: 'x',
            margin: [ 50, 50, 200, 80]
        },
        title: {
            text: 'Ticket comments'
        },
        xAxis: {
            categories: tickets,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                     font: 'normal 13px Verdana, sans-serif'
                }
            },
            maxZoom: 10
        },
        yAxis: {
            title: { 
                text: 'Count',
            }
        },
        legend: {
            style: {
                left: '20px',
                bottom: '10px',
                right: 'auto',
                top: 'auto'
            }
        },
        tooltip: {
            formatter: function() {
                var s;
                if (this.point.name) { // the pie chart
                    s = '<b>' + this.point.name + ',</b><br/>' + 'commented ' + this.y + ' times'
                } else {
                    s = '<b>' + this.series.name + ',</b><br/>' + 'commented ' + this.y + ' times'
                }
                return s;
            }
        },
        labels: {
            items: [{
                html: 'Total comments',
                style: {
                    left: '140px',
                    top: '0px',
                    color: 'black'				
                }
            }]
        },
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
        series: series
    });
    return chart;
}

/*************************** Review Charts ******************************/

function chart27_reviewusers( data, id ) {
    dojo.setObject( 'data', data )
    var piedata = [{ name : 'author',
                     data : data[0],
                     center: [150, 150],
                     size: 200,
                     showInLegend: false
                  }, {
                     name : 'moderator',
                     data : data[1],
                     center: [450, 150],
                     size: 200,
                     showInLegend: false
                  }, {
                     name : 'participant',
                     data : data[2],
                     center: [750, 150],
                     size: 200,
                     showInLegend: false
                  }]

    hc_setoption();
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'pie',
            margin: [ 50, 50, 100, 0]
        },
        title: {
            text: 'Users associated with project reviews'
        },
        labels: {
            items: [{
                html: '<b>Authors</b>',
                style: {
                    left: '100px',
                    top: '20px',
                    color: 'black'				
                }
            }, {
                html: '<b>Moderators</b>',
                style: {
                    left: '400px',
                    top: '20px',
                    color: 'black'				
                }
            }, {
                html: '<b>Participants</b>',
                style: {
                    left: '700px',
                    top: '20px',
                    color: 'black'				
                }
            }]
        },
        legend: {
            enabled: false,
            layout: 'vertical',
            style: {
                left: '50px',
                bottom: 'auto',
                right: 'auto',
                top: '100px'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                dataLabels: {
                    enabled: false,
                    formatter: function() {
                        return this.point.name;
                    },
                    color: 'white',
                    style: {
                        font: '13px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        tooltip: {
            formatter: function() {
                return'<b>' + this.point.name + ',<b><br/>' + this.y;
            }
        },
        series: piedata
    });
    return chart;
}

/*************************** Timeline Charts ******************************/

function timelinechart( datatline, fromdate, id, title ) {
    var counttline = dojo.map( datatline, "return item.length" );
    var itemlogs   = function ( logs ) {
                        return dojo.map( logs, "return item[2]" ) };

    hc_setoption('dark-green');
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: 'areaspline',
            zoomType: 'x'
        },
        title: {
            text: title
        },
        subtitle: {
            text: 'Click and drag in the plot area to zoom in'
        },
        xAxis: {
            type: 'datetime',
            maxZoom: 10*24*3600000, // Ten days
        },
        yAxis: {
            title: { text: 'Acitivity' },
            startOnTick: false,
            showFirstLable: false,
        },
        tooltip: {
            formatter: function() {
                    var offset = (this.x-fromdate) / 3600 / 1000 / 24;
                    return '<b>'+ this.series.name +'</b><br/>' +
                           itemlogs( datatline[offset] ).join(', ');
            }
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.5,
                lineWidth: 1,
                marker: {
                    enabled: true,
                    radius: 1,
                    states: {
                        hover: { enabled: true, radius: 3 }
                    }
                },
                shadow: false,
                states: {
                    hover: { lineWidth: 1 }
                }
            }
        },
        series: [{
            name: title,
            pointInterval: 24 * 3600 * 1000,
            pointStart: fromdate,
            data: counttline
        }]
    });
    return chart
}
