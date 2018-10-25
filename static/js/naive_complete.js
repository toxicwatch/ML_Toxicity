var data = [{
    values: [1405, 478, 7877, 1595, 15294, 8449],
    labels: ['Identity', 'Threat', 'Insult', 'Severe', 'Toxic', 'Obscene'],
    type: 'pie'
  }];
  
var layout = {
    height: 400,
    width: 400,
    title: "Actual Class Counts",
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)'
  };
  
  Plotly.newPlot('naive_complete', data, layout);