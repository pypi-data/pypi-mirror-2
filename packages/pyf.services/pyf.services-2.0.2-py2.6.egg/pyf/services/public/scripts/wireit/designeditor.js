(function(){
    var util = YAHOO.util, lang = YAHOO.lang;
    var Event = util.Event, Dom = util.Dom, Connect = util.Connect, JSON = lang.JSON, widget = YAHOO.widget;
    
    
    /**
     * Module Proxy handle the drag/dropping from the module list to the layer (in the WiringEditor)
     * @class ModuleProxy
     * @constructor
     * @param {HTMLElement} el
     * @param {WireIt.WiringEditor} WiringEditor
     */
    WireIt.ModuleProxy = function(el, WiringEditor){
    
        this._WiringEditor = WiringEditor;
        
        // Init the DDProxy
        WireIt.ModuleProxy.superclass.constructor.call(this, el, "module", {
            dragElId: "moduleProxy"
        });
        
        this.isTarget = false;
    };
    YAHOO.extend(WireIt.ModuleProxy, YAHOO.util.DDProxy, {
    
        /**
         * copy the html and apply selected classes
         * @method startDrag
         */
        startDrag: function(e){
            WireIt.ModuleProxy.superclass.startDrag.call(this, e);
            var del = this.getDragEl(), lel = this.getEl();
            del.innerHTML = lel.innerHTML;
            del.className = lel.className;
        },
        
        /**
         * Override default behavior of DDProxy
         * @method endDrag
         */
        endDrag: function(e){
        },
        
        /**
         * Add the module to the WiringEditor on drop on layer
         * @method onDragDrop
         */
        onDragDrop: function(e, ddTargets){
            // The layer is the only target :
            var layerTarget = ddTargets[0], layer = ddTargets[0]._layer, del = this.getDragEl(), pos = YAHOO.util.Dom.getXY(del), layerPos = YAHOO.util.Dom.getXY(layer.el);
            this._WiringEditor.addModule(this._module, [pos[0] - layerPos[0] + layer.el.scrollLeft, pos[1] - layerPos[1] + layer.el.scrollTop]);
        }
        
    });
    
    
    /**
     * The WiringEditor class provides a full page interface
     * @class WiringEditor
     * @constructor
     * @param {Object} options
     */
    WireIt.WiringEditor = function(options){
    
        /**
         * Hash object to reference module definitions by their name
         * @property modulesByName
         * @type {Object}
         */
        this.modulesByName = {};
        
        // set the default options
        this.setOptions(options);
        
        /**
         * Container DOM element
         * @property el
         */
        this.el = Dom.get(options.parentEl);
        
        /**
         * @property helpPanel
         * @type {YAHOO.widget.Panel}
         */
        /*this.helpPanel = new widget.Panel('helpPanel', {
            fixedcenter: true,
            draggable: true,
            visible: false,
            modal: true
        });
        this.helpPanel.render();*/
        
        
        /**
         * @property layout
         * @type {YAHOO.widget.Layout}
         */
        /*this.layout = new widget.Layout(this.el, this.options.layoutOptions);
        this.layout.render();*/
        
        // Right accordion
        /*this.renderAccordion();*/
        
        /**
         * @property layer
         * @type {WireIt.Layer}
         */
        this.layer = new WireIt.Layer(this.options.layerOptions);
        this.layer.eventChanged.subscribe(this.onLayerChanged, this, true);
		this.layer.eventAddContainer.subscribe(this.onContainerAdded, this, true);
        
        /**
         * @property leftEl
         * @type {DOMElement}
         */
        this.leftEl = Dom.get('left');
        document.getElements('#sidebar .formfields input').addEvent('change', this.markUnsaved.bind(this));
		this.saveButton = $('save');
		this.launchButton = $('launch');
		this.saveButton.addEvent('click', this.onSave.bind(this));
		this.launchButton.addEvent('click', this.onLaunch.bind(this));
		
		this.notifier= new Roar({
			position: 'upperRight',
			duration: 5000 // 5 seconds until message fades out
		});
        
        // Render module list
        this.buildModulesList();
		
		window.onbeforeunload = this.checkClose.bind(this);
        
        // Render buttons
        /*this.renderButtons();
        
        // Saved status
        this.renderSavedStatus();
        
        // Properties Form
        this.renderPropertiesForm();*/
        
        // LoadWirings
        /*if (this.adapter.init && YAHOO.lang.isFunction(this.adapter.init)) {
            this.adapter.init();
        }
        this.load();*/
    };
    
    WireIt.WiringEditor.prototype = {
    
        /**
         * @method setOptions
         * @param {Object} options
         */
        setOptions: function(options){
            /**
             * @property options
             * @type {Object}
             */
            this.options = {};
            
            // Load the modules from options
            this.modules = options.modules || [];
            for (var i = 0; i < this.modules.length; i++) {
                var m = this.modules[i];
                this.modulesByName[m.name] = m;
            }
            
            this.adapter = options.adapter || WireIt.WiringEditor.adapters.JsonRpc;
            
            this.options.languageName = options.languageName || 'anonymousLanguage';
            
            this.options.propertiesFields = options.propertiesFields ||
            [{
                "type": "string",
                inputParams: {
                    "name": "name",
                    label: "Title",
                    typeInvite: "Enter a title"
                }
            }, {
                "type": "text",
                inputParams: {
                    "name": "description",
                    label: "Description",
                    cols: 30,
                    rows: 4
                }
            }];
            
            this.options.layoutOptions = options.layoutOptions ||
            {
                units: [{
                    position: 'top',
                    height: 50,
                    body: 'top'
                }, {
                    position: 'left',
                    width: 200,
                    resize: true,
                    body: 'left',
                    gutter: '5px',
                    collapse: true,
                    collapseSize: 25,
                    header: 'Modules',
                    scroll: true,
                    animate: true
                }, {
                    position: 'center',
                    body: 'center',
                    gutter: '5px'
                }, {
                    position: 'right',
                    width: 320,
                    resize: true,
                    body: 'right',
                    gutter: '5px',
                    collapse: true,
                    collapseSize: 25,
                    animate: true
                }]
            };
            
            this.options.layerOptions = {};
            var layerOptions = options.layerOptions ||
            {};
            this.options.layerOptions.parentEl = layerOptions.parentEl ? layerOptions.parentEl : Dom.get('center');
            /*this.options.layerOptions.layerMap = YAHOO.lang.isUndefined(layerOptions.layerMap) ? true : layerOptions.layerMap;
            this.options.layerOptions.layerMapOptions = layerOptions.layerMapOptions ||
            {
                parentEl: 'layerMap',
				width: '308px'
            };*/
            
            this.options.accordionViewParams = options.accordionViewParams ||
            {
                collapsible: true,
                expandable: true, // remove this parameter to open only one panel at a time
                width: '308px',
                expandItem: 0,
                animationSpeed: '0.3',
                animate: true,
                effect: YAHOO.util.Easing.easeBothStrong
            };
			
			this.options.tube_id = tube_id;
        },
        
        
        /**
         * Render the accordion using yui-accordion
         */
        renderAccordion: function(){
            this.accordionView = new YAHOO.widget.AccordionView('accordionView', this.options.accordionViewParams);
        },
        
        /**
         * Render the properties form
         * @method renderPropertiesForm
         */
        renderPropertiesForm: function(){
            this.propertiesForm = new inputEx.Group({
                parentEl: YAHOO.util.Dom.get('propertiesForm'),
                fields: this.options.propertiesFields
            });
            
            this.propertiesForm.updatedEvt.subscribe(function(){
                this.markUnsaved();
            }, this, true);
        },
        
        /**
         * Build the left menu on the left
         * @method buildModulesList
         */
        buildModulesList: function(){
        
            var modules = this.modules;
            for (var i = 0; i < modules.length; i++) {
                this.addModuleToList(modules[i]);
            }
            
            // Make the layer a drag drop target
            if (!this.ddTarget) {
                this.ddTarget = new YAHOO.util.DDTarget(this.layer.el, "module");
                this.ddTarget._layer = this.layer;
            }
            
        },
        
        /**
         * Add a module definition to the left list
         */
        addModuleToList: function(module){
        
            var div = WireIt.cn('div', {
                className: "WiringEditor-module"
            });
            if (module.container.icon) {
                div.appendChild(WireIt.cn('img', {
                    src: module.container.icon
                }));
            }
			var display_name = module.name;
			if (module.container.display_name)
				display_name = module.container.display_name;
            div.appendChild(WireIt.cn('span', null, null, display_name));
            
            var ddProxy = new WireIt.ModuleProxy(div, this);
            ddProxy._module = module;
            
            this.leftEl.appendChild(div);
        },
        
        /**
         * add a module at the given pos
         */
        addModule: function(module, pos){
            try {
                var containerConfig = module.container;
                containerConfig.position = pos;
                containerConfig.title = module.name;
                var container = this.layer.addContainer(containerConfig);
                Dom.addClass(container.el, "WiringEditor-module-" + module.name);
				this.initializeContainer(container);
            } 
            catch (ex) {
                this.alert("Error Layer.addContainer: " + ex.message);
            }
        },
        
        /**
         * @method renderSavedStatus
         */
        renderSavedStatus: function(){
            var top = Dom.get('top');
            this.savedStatusEl = WireIt.cn('div', {
                className: 'savedStatus',
                title: 'Not saved'
            }, {
                display: 'none'
            }, "*");
            top.appendChild(this.savedStatusEl);
        },
		
		controlData: function() {
			if (this.layer.containers.some(function(container){
				return !($chk(container.getValue()['name']));
			})) {
				this.error('Please name all your nodes.');
				return false;
			}
			
			if (this.getValue().name == "") {
                this.error("Please choose a name");
                return false;
            }
			
			return true;
				
		},
		
		checkClose: function() {
			if (!this.saved) {
//				if (confirm("There are unsaved changes, are you sure you want to close ?")) {
//					return true;
//				} else {
//					return false;
//				}
				return "There are unsaved changes.";
			} else {
				return null;
			}
		},
		
		/**
		 * (re)load the current module
		 * @method loadModule
		 */
		loadModule: function() {
			if (this.options.tube_id == 0) {
				this.loadPipeContent({modules: [], wires: []});	
			} else {
				new Request.JSON({
					url: '/tubes/get_graph/' + this.options.tube_id,
					method: 'get',
					onSuccess: function(response) {
						if (response.status == 'success') {
						    this.loadPipeContent(response);
						    this.markSaved.delay(500, this);
						} else {
							this.error('Unable to load tube content: \n' + response.reason);
						};
					}.bind(this),
					onFailure: function(xhr) {
						if (xhr.responseText != "")
							this.error("Can't load tube: \n" + xhr.responseText);
						else
							this.error("Can't load tube for an unknown reason.");
					}.bind(this)
				}).send();
			}
		},
        
        /**
         * save the current module
         * @method saveModule
         */
        saveModule: function(){
        
            var value = this.getValue();
            if (!this.controlData())
				return;
				
//            
//            this.tempSavedWiring = {
//                name: value.name,
//                working: JSON.stringify(value.working),
//                language: this.options.languageName
//            };
            
//            this.adapter.saveWiring(this.tempSavedWiring, {
//                success: this.saveModuleSuccess,
//                failure: this.saveModuleFailure,
//                scope: this
//            });
			new Request.JSON({
				url: '/tubes/save_graph/',
				method: 'post',
				onSuccess: function(response) {
					if (response.status == 'success') {
					    if (this.options.tube_id == 0)
					    {
                            this.options.tube_id = response.tube_id;
                            tube_id = response.tube_id;
					    }
					    this.saveModuleSuccess();
					}
					else {
						this.saveModuleFailure(response.reason);
					};
				}.bind(this),
				onFailure: function(xhr) {
					if (xhr.responseText != "")
						this.error("Can't save: \n" + xhr.responseText);
					else
						this.error("Can't save the tube");
				}.bind(this)
			}).send($H({
				'payload': JSON.stringify(value.working),
				'tube_id': this.options.tube_id
			}).toQueryString());
            
        },
        
        /**
         * saveModule success callback
         * @method saveModuleSuccess
         */
        saveModuleSuccess: function(o){
        
            this.markSaved();
            
            this.alert("Success", "Tube successfully saved !");
            
            // TODO:
            /*var name = this.tempSavedWiring.name;	
             if(this.modulesByName.hasOwnProperty(name) ) {
             //already exists
             }
             else {
             //new one
             }*/
        },
        
        /**
         * saveModule failure callback
         * @method saveModuleFailure
         */
        saveModuleFailure: function(errorStr){
            this.alert("Error", "Unable to save the wiring : " + errorStr);
        },
        
        alert: function(title, text){
			this.notifier.alert(title, text);
        },
		
		error: function(txt) {
			new MooDialog.Error(txt, {
				title: "Error",
				height: ""
			});
		},
        
        /**
         * Create a help panel
         * @method onHelp
         */
        onHelp: function(){
            this.helpPanel.show();
        },
        
//        /**
//         * @method onNew
//         */
//        onNew: function(){
//        
//            if (!this.isSaved()) {
//                if (!confirm("Warning: Your work is not saved yet ! Press ok to continue anyway.")) {
//                    return;
//                }
//            }
//            
//            this.preventLayerChangedEvent = true;
//            
//            this.layer.clear();
//            
//            this.propertiesForm.clear(false); // false to tell inputEx to NOT send the updatedEvt
//            this.markSaved();
//            
//            this.preventLayerChangedEvent = false;
//        },
//        
//        /**
//         * @method onDelete
//         */
//        onDelete: function(){
//            if (confirm("Are you sure you want to delete this wiring ?")) {
//            
//                var value = this.getValue();
//                this.adapter.deleteWiring({
//                    name: value.name,
//                    language: this.options.languageName
//                }, {
//                    success: function(result){
//                        this.onNew();
//                        this.alert("Deleted !");
//                    },
//                    failure: function(errorStr){
//                        this.alert("Unable to delete wiring: " + errorStr);
//                    },
//                    scope: this
//                });
//                
//            }
//        },
        
        /**
         * @method onSave
         */
        onSave: function(){
			this.syncContainers();
            this.saveModule();
        },
        
		onLaunch: function() {
			window.open('/tubes/' + this.options.tube_id + '/launch');
		},
		
        /**
         * @method renderLoadPanel
         */
        renderLoadPanel: function(){
            if (!this.loadPanel) {
                this.loadPanel = new widget.Panel('WiringEditor-loadPanel', {
                    fixedcenter: true,
                    draggable: true,
                    width: '500px',
                    visible: false,
                    modal: true
                });
                this.loadPanel.setHeader("Select the wiring to load");
                this.loadPanel.setBody("Filter: <input type='text' id='loadFilter' /><div id='loadPanelBody'></div>");
                this.loadPanel.render(document.body);
                
                // Listen the keyup event to filter the module list
                Event.onAvailable('loadFilter', function(){
                    Event.addListener('loadFilter', "keyup", this.inputFilterTimer, this, true);
                }, this, true);
                
            }
        },
        
        /**
         * Method called from each keyup on the search filter in load panel.
         * The real filtering occurs only after 500ms so that the filter process isn't called too often
         */
        inputFilterTimer: function(){
            if (this.inputFilterTimeout) {
                clearTimeout(this.inputFilterTimeout);
                this.inputFilterTimeout = null;
            }
            var that = this;
            this.inputFilterTimeout = setTimeout(function(){
                that.updateLoadPanelList(Dom.get('loadFilter').value);
            }, 500);
        },
        
        
        /**
         * @method updateLoadPanelList
         */
        updateLoadPanelList: function(filter){
        
            var list = WireIt.cn("ul");
            if (lang.isArray(this.pipes)) {
                for (var i = 0; i < this.pipes.length; i++) {
                    var module = this.pipes[i];
                    this.pipesByName[module.name] = module;
                    if (!filter || filter === "" || module.name.match(new RegExp(filter, "i"))) {
                        list.appendChild(WireIt.cn('li', null, {
                            cursor: 'pointer'
                        }, module.name));
                    }
                }
            }
            var panelBody = Dom.get('loadPanelBody');
            panelBody.innerHTML = "";
            panelBody.appendChild(list);
            
            Event.addListener(list, 'click', function(e, args){
                this.loadPipe(Event.getTarget(e).innerHTML);
            }, this, true);
            
        },
        
        /**
         * @method load
         */
        load: function(){
        
//            this.adapter.listWirings({
//                language: this.options.languageName
//            }, {
//                success: function(result){
//                    this.onLoadSuccess(result);
//                },
//                failure: function(errorStr){
//                    this.alert("Unable to load the wirings: " + errorStr);
//                },
//                scope: this
//            });
			this.adapter
            
        },
        
        /**
         * @method onLoadSuccess
         */
        onLoadSuccess: function(wirings){
            this.pipes = wirings;
            this.pipesByName = {};
            
            this.renderLoadPanel();
            this.updateLoadPanelList();
            
            if (!this.afterFirstRun) {
                var p = window.location.search.substr(1).split('&');
                var oP = {};
                for (var i = 0; i < p.length; i++) {
                    var v = p[i].split('=');
                    oP[v[0]] = window.decodeURIComponent(v[1]);
                }
                this.afterFirstRun = true;
                if (oP.autoload) {
                    this.loadPipe(oP.autoload);
                    return;
                }
            }
            
            this.loadPanel.show();
	    this.markSaved();
        },
        
		loadPipeContent: function(wiring) {
		    this.layer.el.setStyle('display', 'none');
			this.layer.clear();
			// Containers
            for (i = 0; i < wiring.modules.length; i++) {
                var m = wiring.modules[i];
                if (this.modulesByName[m.name]) {
                    var baseContainerConfig = this.modulesByName[m.name].container;
                    YAHOO.lang.augmentObject(m.config, baseContainerConfig);
                    m.config.title = m.name;
                    var container = this.layer.addContainer(m.config);
                    Dom.addClass(container.el, "WiringEditor-module-" + m.name);
                    Dom.addClass(container.el, "module-type-" + m.config.type);
                    container.setValue(m.value);
					   
					this.initializeContainer(container);
                }
                else {
                    throw new Error("WiringEditor: module '" + m.name + "' not found !");
                }
            }
            this.layer.el.setStyle('display', 'block');
            
            // Wires
            if (lang.isArray(wiring.wires)) {
                for (i = 0; i < wiring.wires.length; i++) {
                    // On doit chercher dans la liste des terminaux de chacun des modules l'index des terminaux...
                    this.layer.addWire(wiring.wires[i]);
                }
            }
		},
		
        renderAlertPanel: function(){
        
            /**
             * @property alertPanel
             * @type {YAHOO.widget.Panel}
             */
            this.alertPanel = new widget.Panel('WiringEditor-alertPanel', {
                fixedcenter: true,
                draggable: true,
                width: '500px',
                visible: false,
                modal: true
            });
            this.alertPanel.setHeader("Message");
            this.alertPanel.setBody("<div id='alertPanelBody'></div><button id='alertPanelButton'>Ok</button>");
            this.alertPanel.render(document.body);
            Event.addListener('alertPanelButton', 'click', function(){
                this.alertPanel.hide();
            }, this, true);
        },
        
        onLayerChanged: function(){
            //if (!this.preventLayerChangedEvent) {
                this.markUnsaved();
            //}
        },
		
		onContainerAdded: function(event, containers) {
		},
		
		initializeContainer: function(container) {
			container.code_zones = [];
			// Ugly hack isn't it ? :)
			// Oh, oh, oh... How I hate you YUI !
//			if (container.el.hasClass("module-type-generic_plugin"))
//			{
//				var content_zone = $(container.bodyEl).getElement("textarea[name='content']");
//				var editor = CodeMirror.fromTextArea(content_zone, {
//				    height: "80%",
//					width: "100%",
//				    parserfile: "parsexml.js",
//				    stylesheet: "/css/design_xmlcolors.css",
//				    path: "/scripts/codemirror/",
//				    continuousScanning: 500,
//				    lineNumbers: true,
//				    textWrapping: false,
//					onChange: this.markUnsaved.bind(this)
//				});
//				container.code_zones.push([editor, content_zone]);
//			} else if (container.el.hasClass("module-type-code")) {
//				var content_zone = $(container.bodyEl).getElement("textarea[name='code']");
//				var editor = CodeMirror.fromTextArea(content_zone, {
//				    height: "80%",
//					width: "100%",
//				    parserfile: "parsepython.js",
//				    stylesheet: "/css/design_pythoncolors.css",
//				    path: "/scripts/codemirror/",
//				    continuousScanning: 500,
//				    lineNumbers: true,
//				    textWrapping: false,
//					indentUnit: 4,
//					onChange: this.markUnsaved.bind(this)
//				});
//				container.code_zones.push([editor, content_zone]);
//			} else {
				container.el.getElements('.xmlcode textarea').each(function(content_zone) {
					var editor = CodeMirror.fromTextArea(content_zone, {
					    width: "100%",
					    parserfile: "parsexml.js",
					    stylesheet: "/css/design_xmlcolors.css",
					    path: "/scripts/codemirror/",
					    continuousScanning: 500,
					    lineNumbers: true,
					    textWrapping: false,
						onChange: this.markUnsaved.bind(this)
					});
					container.code_zones.push([editor, content_zone]);
				}.bind(this));
				container.el.getElements('.pythoncode textarea').each(function(content_zone) {
					var editor = CodeMirror.fromTextArea(content_zone, {
					    width: "100%",
					    parserfile: "parsepython.js",
					    stylesheet: "/css/design_pythoncolors.css",
					    path: "/scripts/codemirror/",
					    continuousScanning: 500,
					    lineNumbers: true,
					    textWrapping: false,
						indentUnit: 4,
						onChange: this.markUnsaved.bind(this)
					});
					container.code_zones.push([editor, content_zone]);
				}.bind(this));
//			}
			// Code to use to resize...
//			var it = $$('div.WireIt-Container div.body > div.inputEx-Group > fieldset')[1];
//			var height = 3;
//			it.getChildren().getStyle('height').each(function(val) {height += val.toInt();});
//			it.getParent().getParent().setStyle('height', (height) + 'px');
//			it.getParent().getParent().getParent().setStyle('height', (height+35) + 'px');
            if ($chk(this.modulesByName[container.options.title].container.default_width))
                container.bodyEl.setStyle(
                    'width',
                    this.modulesByName[container.options.title].container.default_width + 'px'
                );
                       
        	container.form.updatedEvt.subscribe(this.onContainerChanged.pass(container, this), this, true);
			this.autoResizeContainer(container);
		},
		
		autoResizeContainer: function(container) {
			var fieldset = container.form.fieldset;
			var height = 10;
			fieldset.getChildren().getStyle('height').each(function(val) {height += val.toInt() + 2;});
			var width = container.bodyEl.getStyle('width').toInt();
			
			WireIt.sn(container.bodyEl, null, {width: (width)+"px", height: (height)+"px"});
			
            WireIt.sn(container.bodyEl.getParent(), null, {width: (width+10)+"px", height: (height+43)+"px"});
		},
		
		syncContainers: function() {
			this.layer.containers.each(this.syncContainer.bind(this));
		},
		
		syncContainer: function(container) {
			container.code_zones.each(function(zone_def) {
				zone_def[1].set('value', zone_def[0].getCode());
			});
		},
		
		onContainerChanged: function(container) {
			this.autoResizeContainer(container);
			this.syncContainer(container);
			this.markUnsaved();
		},
        
        markSaved: function(){
            //this.savedStatusEl.style.display = 'none';
			this.saved = true;
			this.saveButton.set('disabled', true);
			this.launchButton.set('disabled', false);
        },
		
        
        markUnsaved: function(){
            //this.savedStatusEl.style.display = '';
			this.saved = false;
			this.saveButton.set('disabled', false);
			this.launchButton.set('disabled', true);
        },
        
        isSaved: function(){
            //return (this.savedStatusEl.style.display == 'none');
			return this.saveButton.get('disabled');
        },
        
        /**
         * This method return a wiring within the given vocabulary described by the modules list
         * @method getValue
         */
        getValue: function(){
        
            var i;
            var obj = {
                modules: [],
                wires: [],
                properties: null
            };
            
            for (i = 0; i < this.layer.containers.length; i++) {
                obj.modules.push({
                    name: this.layer.containers[i].options.title,
                    value: this.layer.containers[i].getValue(),
                    config: this.layer.containers[i].getConfig()
                });
            }
            
            for (i = 0; i < this.layer.wires.length; i++) {
                var wire = this.layer.wires[i];
                
                var wireObj = {
                    src: {
                        moduleId: WireIt.indexOf(wire.terminal1.container, this.layer.containers),
                        terminal: wire.terminal1.options.name
                    },
                    tgt: {
                        moduleId: WireIt.indexOf(wire.terminal2.container, this.layer.containers),
                        terminal: wire.terminal2.options.name
                    }
                };
                obj.wires.push(wireObj);
            }
            
//            obj.properties = this.propertiesForm.getValue();
			obj.properties = {};
			document.getElements('.formfields input').each(function(el) {
			    if (el.get('type') == 'checkbox')
			        obj.properties[el.get('name')] = el.get('checked');
			    else
			        obj.properties[el.get('name')] = el.get('value');
			});
            
            return {
                name: obj.properties.name,
                working: obj
            };
        }
    };
	
    /**
     * WiringEditor Adapters
     * @static
     */
    WireIt.WiringEditor.adapters = {};
    
    
})();
