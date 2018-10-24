
var data = [{
    values: [36069, 3824],
    labels: ['nontoxic', 'toxic'],
    type: 'pie'
  }];
  
var layout = {
    height: 400,
    width: 400,
    title: "Actual Toxicity Percentages"
  };
  
  Plotly.newPlot('pie_actual', data, layout);