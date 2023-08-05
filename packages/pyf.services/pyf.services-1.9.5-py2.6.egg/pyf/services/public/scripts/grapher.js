st = null;
  	window.addEvent('domready', function() {
		
		ST.Plot.NodeTypes.implement({
        /*'nodeline': function(node, canvas, animating) {
            if(animating === 'expand' || animating === 'contract') {
                var pos = node.pos.getc(true), nconfig = this.node, data = node.data;
                var width  = nconfig.width, height = nconfig.height;
                var algnPos = this.getAlignedPos(pos, width, height);
                var ctx = canvas.getCtx(), ort = this.config.orientation;
                ctx.beginPath();
                if(ort == 'left' || ort == 'right') {
                    ctx.moveTo(algnPos.x, algnPos.y + height / 2);
                    ctx.lineTo(algnPos.x + width, algnPos.y + height / 2);
                } else {
                    ctx.moveTo(algnPos.x + width / 2, algnPos.y);
                    ctx.lineTo(algnPos.x + width / 2, algnPos.y + height);
                }
                ctx.stroke();
            } 
        }*/
    });
		
    	var infovis = $('infovis');
	    //init canvas
	    //Create a new canvas instance.
	    var canvas = new Canvas('mycanvas', {
	        'injectInto': 'infovis',
	        'width': infovis.getSize().x,
	        'height': infovis.getSize().y
	    });
	    //end
		
	    //init st
	    //Create a new ST instance
        st = new ST(canvas, {
            Node: {
                height: 20,
	            width: 130,
	            color:'#444',
	            lineWidth: 2,
	            align:"center",
	            overridable: true
            },
            Edge: {
                type: 'bezier',
	            lineWidth: 2,
	            color:'#444',
	            overridable: true
            },
			levelsToShow: 100,
			orientation: 'top',
            //This method is called on DOM label creation.
        //Use this method to add event handlers and styles to
        //your node.
        onCreateLabel: function(label, node){
            label.id = node.id;
			if (node.data.type == 'producer' | node.data.type == 'adapter' |
				node.data.type == 'consumer')
				label.set('html', node.name + '<br /><b>'
				  + node.data.plugin_name + '</b><br />type: ' + node.data.type);
			else
				label.set('text', node.name);
			
			
			
            label.onclick = function(){
                st.onClick(node.id);
            };
            //set label styles
            var style = label.style;
            style.width = 130 + 'px';         
            style.cursor = 'pointer';
            style.color = '#fff';
            //style.backgroundColor = '#1a1a1a';
            style.fontSize = '0.8em';
            style.textAlign= 'center';
            style.paddingTop = '3px';
			
			node.data.$height = label.getSize().y;
        },
        
        //This method is called right before plotting
        //a node. It's useful for changing an individual node
        //style properties before plotting it.
        //The data properties prefixed with a dollar
        //sign will override the global node style properties.
        onBeforePlotNode: function(node){
            //add some color to the nodes in the path between the
            //root node and the selected node.
            if (node.selected) {
                node.data.$color = "#23A4FF";
            }
            else {
                delete node.data.$color;
            }
        },
        
        //This method is called right before plotting
        //an edge. It's useful for changing an individual edge
        //style properties before plotting it.
        //Edge data proprties prefixed with a dollar sign will
        //override the Edge global style properties.
        onBeforePlotLine: function(adj){
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
                adj.data.$color = "#23A4FF";
                adj.data.$lineWidth = 3;
            }
            else {
                delete adj.data.$color;
                delete adj.data.$lineWidth;
            }
			if (adj.nodeFrom.data.type == "adapter" | adj.nodeFrom.data.type == "consumer"
			    | adj.nodeFrom.data.type == "producer")
            	adj.data.$type = 'arrow';
        }
        });

	    //load json data
	    //st.loadJSON('/tubes/get_graph?id=${tube.id}');
		

		//st.loadJSON('/tubes/1/graph.json');
	    //compute node positions and layout
	    //st.compute();
		//st.onClick(st.root);
	});