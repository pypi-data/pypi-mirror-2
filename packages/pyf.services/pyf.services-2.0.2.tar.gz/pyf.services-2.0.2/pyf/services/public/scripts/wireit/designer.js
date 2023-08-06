/**
 * pythonBox
 */
var joiner_def = {
    "type": "group",
    "inputParams": {
        "name" : "joiner",
        "legend" : "Joiner Info",
        "collapsible" : true,
		"collapsed": true,
        "fields" : [
            {
                "type" : "string",
                "inputParams": {
                    "label" : "Type",
                    "name" : "joiner_type",
                    "value" : "linear"
                }
            },
            {
                "type" : "text",
                "inputParams": {
                    "name": "content",
                    "label" : "Content",
                    "value" : ""/*,
                    "className": "xmlcode",
					"height": "40px"*/
                }
            }
        ]
    }
};

var advanced_def = {
    "type": "group",
    "inputParams": {
        "name" : "advanced",
        "legend" : "Advanced",
        "collapsible" : true,
		"collapsed": true,
        "fields" : [
            {
                "type" : "boolean",
                "inputParams": {
                    "label" : "Separate Process",
                    "name" : "separate_process",
                    "value" : false
                }
            }
        ]
    }
};

var configkeys_def = {
    "type" : "list",
    "inputParams": {
        "label" : "Config",
        "name" : "config_keys",
        "value" : [],
        "elementType" : {
            "type" : "combine",
            "inputParams": {
                "fields" : [
                    {
                        "type" : "string",
                        "inputParams": {
                            "typeInvite" : "key",
                            "name" : "key",
                            "value" : ""
                        }
                    },
                    {
                        "type" : "string",
                        "inputParams": {
                            "typeInvite" : "value",
                            "name" : "value",
                            "value" : ""
                        }
                    }
                ],
                "separators" : [false, " : ", false],
                "legend" : ""
            }
        }
    }
};

var pythonBox = {

    language: {
    
        languageName: "PyFTube",
        
        modules: [{
            "name": "comment",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "Comment",
                "fields": [{
                    "type": "text",
                    "inputParams": {
                        "label": "",
                        "name": "comment",
                        "wirable": false
                    }
                }],
				"type": "comment"
            },
            "value": {
                "input": {
                    "type": "url",
                    "inputParams": {}
                }
            }
        }, {
            "name": "adapter plugin",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "Adapter",
				"type": "generic_plugin",
                "fields": [joiner_def, advanced_def, {
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, {
                    "type": "input",
                    "inputParams": {
                        "label": "Plugin",
                        "name": "plugin",
                        "wirable": false,
                        "typeInvite": "plugin name"
                    }
                }, {
                    "type": "text",
                    "inputParams": {
						"label": "",
						"name": "content",
						"wirable": false,
						"className": "xmlcode"
					}
				}],
                "terminals": [{
                    "name": "out",
                    "direction": [0, 1],
                    "offsetPosition": {
                        "left": 86,
                        "bottom": -15
                    },
                    "ddConfig": {
                        "type": "output",
                        "allowedTypes": ["input"]
                    },
					"editable": true
                }, {
                    "name": "in",
                    "direction": [0, -1],
					"fakeDirection": [0, 1],
                    "offsetPosition": {
                        "left": 82,
                        "top": -15
                    },
                    "ddConfig": {
                        "type": "input",
                        "allowedTypes": ["output"]
                    }
                }]
            }
        }, {
            "name": "producer plugin",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "Producer",
				"type": "generic_plugin",
                "fields": [joiner_def, advanced_def, {
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, {
                    "type": "input",
                    "inputParams": {
                        "label": "Plugin",
                        "name": "plugin",
                        "wirable": false,
                        "typeInvite": "plugin name"
                    }
                }, {
                    "type": "text",
                    "inputParams": {
						"label": "",
						"name": "content",
						"wirable": false,
						"className": "xmlcode"
					}
				}],
                "terminals": [{
                    "name": "out",
                    "direction": [0, 1],
                    "offsetPosition": {
                        "left": 86,
                        "bottom": -15
                    },
                    "ddConfig": {
                        "type": "output",
                        "allowedTypes": ["input"]
                    }
                }]
            }
        }, {
            "name": "consumer plugin",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "consumer",
				"type": "generic_plugin",
                "fields": [joiner_def, advanced_def, {
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, {
                    "type": "input",
                    "inputParams": {
                        "label": "Plugin",
                        "name": "plugin",
                        "wirable": false,
                        "typeInvite": "plugin name"
                    }
                }, {
                    "type": "text",
                    "inputParams": {
						"label": "",
						"name": "content",
						"wirable": false,
						"className": "xmlcode"
					}
				}],
                "terminals": [{
                    "name": "out",
                    "direction": [0, 1],
                    "offsetPosition": {
                        "left": 86,
                        "bottom": -15
                    },
                    "ddConfig": {
                        "type": "output",
                        "allowedTypes": ["input"]
                    },
					"editable": true
                }, {
                    "name": "in",
                    "direction": [0, -1],
                    "offsetPosition": {
                        "left": 86,
                        "top": -15
                    },
                    "ddConfig": {
                        "type": "input",
                        "allowedTypes": ["output"]
                    }
                }]
            }
        },
		{
            "name": "producer code",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "Code Producer",
				"type": "code",
				"default_width": 500,
                "fields": [joiner_def, advanced_def, {
                        "type": "input",
                        "inputParams": {
                            "label": "Name",
                            "name": "name",
                            "wirable": false,
                            "typeInvite": "unique name"
                        }
                    }, configkeys_def,
                    {
                        "type": "text",
                        "inputParams": {
                            "label": "",
                            "name": "code",
                            "wirable": false,
    						"className": "pythoncode"
                        }
                    }
                ],
                "terminals": [{
                    "name": "out",
                    "direction": [0, 1],
                    "offsetPosition": {
                        "left": 143,
                        "bottom": -15
                    },
                    "ddConfig": {
                        "type": "output",
                        "allowedTypes": ["input"]
                    }
                }]
            },
            "value": {
                "input": {
                    "type": "url",
                    "inputParams": {}
                }
            },
        
        },
		{
            "name": "consumer code",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "Code Consumer",
				"type": "code",
                "default_width": 500,
                "fields": [joiner_def, advanced_def, {
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, configkeys_def, {
                    "type": "text",
                    "inputParams": {
                        "label": "",
                        "name": "code",
                        "wirable": false,
						"className": "pythoncode"
                    }
                }],
                "terminals": [{
                    "name": "out",
                    "direction": [0, 1],
                    "offsetPosition": {
                        "left": 86,
                        "bottom": -15
                    },
                    "ddConfig": {
                        "type": "output",
                        "allowedTypes": ["input"]
                    },
					"editable": true
                }, {
                    "name": "in",
                    "direction": [0, -1],
                    "offsetPosition": {
                        "left": 143,
                        "top": -15
                    },
                    "ddConfig": {
                        "type": "input",
                        "allowedTypes": ["output"]
                    }
                }]
            },
            "value": {
                "input": {
                    "type": "url",
                    "inputParams": {}
                }
            },
        
        }, {
            "name": "adapter code",
            "container": {
                "xtype": "WireIt.FormContainer",
                "title": "Code Adapter",
				"type": "code",
                "default_width": 500,
                "fields": [joiner_def, advanced_def, {
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, configkeys_def, {
                    "type": "text",
                    "inputParams": {
                        "label": "",
                        "name": "code",
                        "wirable": false,
						"className": "pythoncode"
                    }
                }],
                "terminals": [{
                    "name": "in",
                    "direction": [0, -1],
                    "offsetPosition": {
                        "left": 143,
                        "top": -15
                    },
                    "ddConfig": {
                        "type": "input",
                        "allowedTypes": ["output"]
                    }
                }, {
                    "name": "out",
                    "direction": [0, 1],
                    "offsetPosition": {
                        "left": 143,
                        "bottom": -15
                    },
                    "ddConfig": {
                        "type": "output",
                        "allowedTypes": ["input"]
                    }
                }]
            },
            "value": {
                "input": {
                    "type": "url",
                    "inputParams": {}
                }
            },
        
        }, ]
    },
    
    /**
     * @method init
     * @static
     */
    init: function(){
        this.editor = new pythonBox.WiringEditor(this.language);
    }
    
};

inputEx.Group.prototype.toggleCollapse = function(){
    var Dom = YAHOO.util.Dom;
    if (Dom.hasClass(this.fieldset, 'inputEx-Expanded')) {
        Dom.replaceClass(this.fieldset, 'inputEx-Expanded', 'inputEx-Collapsed');
    }
    else {
        Dom.replaceClass(this.fieldset, 'inputEx-Collapsed', 'inputEx-Expanded');
    }
    this.fireUpdatedEvt();
};

// Functions executed with the scope of a wire
var wireRed = function() {
	this.options.color = 'rgb(255, 0, 0)';
	this.redraw();
};
var wireBlue = function() {
	this.options.color = 'rgb(173, 216, 230)';
	this.redraw();
};
var wireClick = function(wire) {
	this.removeWire(wire);
};

WireIt.Terminal.prototype.addWire = function(wire) {
  // Adds this wire to the list of connected wires :
  this.wires.push(wire);

  // Set class indicating that the wire is connected
  this.el.addClass(this.options.connectedClassName);

  // Fire the event
  this.eventAddWire.fire(wire);
  
  wire.eventMouseIn.subscribe(wireRed, wire, true);
  wire.eventMouseOut.subscribe(wireBlue, wire, true);
  wire.eventMouseClick.subscribe(wireClick.pass(wire, this), wire, true);

};

/**
 * The wiring editor is overriden to add a button "RUN" to the control bar
 */
pythonBox.WiringEditor = function(options){
    pythonBox.WiringEditor.superclass.constructor.call(this, options);
};

YAHOO.lang.extend(pythonBox.WiringEditor, WireIt.WiringEditor, {


    /**
     * Add the "run" button
     */
    /*renderButtons: function(){
        pythonBox.WiringEditor.superclass.renderButtons.call(this);
        
        // Add the run button
        var toolbar = YAHOO.util.Dom.get('toolbar');
        var runButton = new YAHOO.widget.Button({
            label: "Run",
            id: "WiringEditor-runButton",
            container: toolbar
        });
        runButton.on("click", pythonBox.run, pythonBox, true);
    },*/
    
    /**
     * Customize the load success handler for the composed module list
     */
    onLoadSuccess: function(wirings){
        pythonBox.WiringEditor.superclass.onLoadSuccess.call(this, wirings);
        
        //  Customize to display composed module in the left list
        this.updateComposedModuleList();
    },
    
    /**
     * All the saved wirings are reusable modules :
     */
    updateComposedModuleList: function(){
    
        // to optimize:
        
        // Remove all previous module with the ComposedModule class
        var l = YAHOO.util.Dom.getElementsByClassName("ComposedModule", "div", this.leftEl);
        for (var i = 0; i < l.length; i++) {
            this.leftEl.removeChild(l[i]);
        }
        
        if (YAHOO.lang.isArray(this.pipes)) {
            for (i = 0; i < this.pipes.length; i++) {
                var module = this.pipes[i];
                this.pipesByName[module.name] = module;
                
                // Add the module to the list
                var div = WireIt.cn('div', {
                    className: "WiringEditor-module ComposedModule"
                });
                div.appendChild(WireIt.cn('span', null, null, module.name));
                var ddProxy = new WireIt.ModuleProxy(div, this);
                ddProxy._module = {
                    name: module.name,
                    container: {
                        "xtype": "pythonBox.ComposedContainer",
                        "title": module.name
                    }
                };
                this.leftEl.appendChild(div);
            }
        }
    }
});
