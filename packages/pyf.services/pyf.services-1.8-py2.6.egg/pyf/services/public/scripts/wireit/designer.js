/**
 * pythonBox
 */
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
                }]
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
                "fields": [{
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
						"wirable": false
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
                }, {
                    "name": "in",
                    "direction": [0, -1],
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
                "fields": [{
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
						"wirable": false
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
                "fields": [{
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
						"wirable": false
					}
				}],
                "terminals": [{
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
                "fields": [{
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, {
                    "type": "text",
                    "inputParams": {
                        "label": "",
                        "name": "code",
                        "wirable": false
                    }
                }],
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
                "fields": [{
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, {
                    "type": "text",
                    "inputParams": {
                        "label": "",
                        "name": "code",
                        "wirable": false
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
                "fields": [{
                    "type": "input",
                    "inputParams": {
                        "label": "Name",
                        "name": "name",
                        "wirable": false,
                        "typeInvite": "unique name"
                    }
                }, {
                    "type": "text",
                    "inputParams": {
                        "label": "",
                        "name": "code",
                        "wirable": false
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
