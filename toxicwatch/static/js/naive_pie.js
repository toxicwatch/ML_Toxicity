var data = [{
    values: [47542, 110314, 58],
    labels: ['Positive Comments', 'Negative Comments', 'Neutral Comments'],
    type: 'pie'
  }];
  
var layout = {
    height: 475,
    width: 475,
    title: "NaiveBayes Model Breakdown",
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)'
  };
  
  Plotly.newPlot('naive_pie', data, layout);