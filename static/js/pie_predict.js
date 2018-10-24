var data = [{
    values: [38559, 1334],
    labels: ['nontoxic', 'toxic'],
    type: 'pie'
  }];
  
var layout = {
    height: 400,
    width: 400,
    title: "Prediction Toxicity Percentages"
  };
  
  Plotly.newPlot('pie_predict', data, layout);