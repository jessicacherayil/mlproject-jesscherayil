import mpld3
import numpy as np
from mpld3 import plugins, utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins
from mentions import *

class HighlightLines(plugins.PluginBase):
    """A plugin for an interactive legend. 
    
    Inspired by http://bl.ocks.org/simzou/6439398
    
    """

    JAVASCRIPT = """
    mpld3.register_plugin("interactive_legend", InteractiveLegend);
    InteractiveLegend.prototype = Object.create(mpld3.Plugin.prototype);
    InteractiveLegend.prototype.constructor = InteractiveLegend;
    InteractiveLegend.prototype.requiredProps = ["line_ids", "labels"];
    InteractiveLegend.prototype.defaultProps = {}
    function InteractiveLegend(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    InteractiveLegend.prototype.draw = function(){
        var labels = new Array();
        for(var i=0; i<this.props.labels.length; i++){
            var obj = {}
            obj.label = this.props.labels[i]
            obj.line = mpld3.get_element(this.props.line_ids[i], this.fig)
            obj.visible = false;
            labels.push(obj);
        }
       
        var ax = this.fig.axes[0]
        var legend = this.fig.canvas.append("svg:g")
                               .attr("class", "legend");
        
        // add the rectangles
        legend.selectAll("rect")
                .data(labels)
             .enter().append("rect")
                .attr("height",10)
                .attr("width", 25)
                .attr("x",ax.width+10+ax.position[0])
                .attr("y",function(d,i) {
                                return ax.position[1]+ i * 25 - 10;})
                .attr("stroke", function(d) {
                                return d.line.props.edgecolor})
                .attr("class", "legend-box")
                .style("fill", "white")
                .on("click", click)
        
        // add the text
        legend.selectAll("text")
                console.log("text")
                .data(labels)
            .enter().append("text")
              .attr("x", function (d) {
                return ax.width+10+ax.position[0] + 25 + 15
              })
              .attr("y", function(d,i) { 
                return ax.position[1]+ i * 25
              })
              .text(function(d) { return d.label })
        
        // specify the action on click
        function click(d,i){
            d.visible = !d.visible;
            d3.select(this)
              .style("fill",function(d, i) {
                  console.log(d)
                  var color = d.line.props.edgecolor
                  return d.visible ? color : "white";
              })
            d3.select(d.line.path[0][0])
                .style("stroke-opacity", d.visible ? 1 : d.line.props.alpha);
            
        }
    };
    """

    def __init__(self, lines, labels, css):
        
        self.css_ = css or ""
        
        self.lines = lines
        self.dict_ = {"type": "interactive_legend",
                      "line_ids": [utils.get_id(line) for line in lines],
                      "labels":labels}
        print labels


css = """
.legend-box {
  cursor: pointer;  
}
"""
        
N_paths = 32
N_steps = 100

x = np.linspace(0, 32, 100)
y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
y = y.cumsum(1)

characters = ['Madame de Cleves','Dauphine', 'reine d\'Ecosse' 'Mademoiselle de Chartres', 'Princesse',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La cour', 'Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Roi', 'Henri Second', 'Nemours', 'la Reine',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'premier valet de chambre', 'Chatelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'de Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
'homme du magasin de soie']

plt.figure(figsize = (8,6))
fig, ax = plt.subplots()
labels = characters

lines = ax.plot(x, y.T, lw=4, alpha=0, label=labels)
plugins.connect(fig, HighlightLines(lines, labels, css))

mpld3.display()
mpld3.show()