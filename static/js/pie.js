
var data = [{
    values: [36069, 3824],
    labels: ['nontoxic', 'toxic'],
    type: 'pie'
  }];
  
var layout = {
    height: 400,
    width: 400,
    title: "Actual Toxicity Percentages",
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)'
  };
  
  Plotly.newPlot('pie_actual', data, layout);