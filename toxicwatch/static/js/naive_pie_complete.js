var data = [{
    values: [0, 0, 0, 119, 238, 0],
    labels: ['Identity', 'Threat', 'Insult', 'Severe', 'Toxic', 'Obscene'],
    type: 'pie'
  }];
  
var layout = {
    height: 400,
    width: 400,
    title: "NaiveBayes Classification of Toxicity",
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)'
  };
  
  Plotly.newPlot('naive_pie_complete', data, layout);