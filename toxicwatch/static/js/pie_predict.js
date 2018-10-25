var data = [{
    values: [38559, 1334],
    labels: ['nontoxic', 'toxic'],
    type: 'pie'
  }];
  
var layout = {
    height: 400,
    width: 400,
    title: "Prediction Toxicity Percentages",
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)'
  };
  
  Plotly.newPlot('pie_predict', data, layout);