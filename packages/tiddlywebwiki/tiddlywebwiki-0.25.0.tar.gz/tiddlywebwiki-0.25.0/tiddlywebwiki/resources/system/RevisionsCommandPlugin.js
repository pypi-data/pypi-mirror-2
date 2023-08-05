/***
|''Name''|RevisionsCommandPlugin|
|''Description''|provides access to tiddler revisions|
|''Author''|FND|
|''Contributors''|Martin Budden|
|''Version''|0.3.0|
|''Status''|@@beta@@|
|''Source''|http://svn.tiddlywiki.org/Trunk/association/plugins/RevisionsCommandPlugin.js|
|''CodeRepository''|http://svn.tiddlywiki.org/Trunk/association/plugins/|
|''License''|[[BSD|http://www.opensource.org/licenses/bsd-license.php]]|
|''CoreVersion''|2.4.2|
|''Keywords''|serverSide|
!Usage
Extend [[ToolbarCommands]] with {{{revisions}}}.
!Revision History
!!v0.1 (2009-07-23)
* initial release (renamed from experimental ServerCommandsPlugin)
!!v0.1 (2010-03-04)
* suppressing wikification in diff view
!To Do
* strip server.* fields from revision tiddlers
* resolve naming conflicts
* i18n, l10n
* code sanitizing
* documentation
!Code
***/
//{{{
(function() {

jQuery.twStylesheet(".diff { white-space: pre, font-family: monospace }",
	{ id: "diff" });

var cmd; //# alias
cmd = config.commands.revisions = {
	type: "popup",
	hideShadow: true,
	text: "revisions",
	tooltip: "display tiddler revisions",
	revTooltip: "", // TODO: populate dynamically?
	loadLabel: "loading...",
	loadTooltip: "loading revision list",
	selectLabel: "select",
	selectTooltip: "select revision for comparison",
	selectedLabel: "selected",
	compareLabel: "compare",
	revSuffix: " [rev. #%0]",
	diffSuffix: " [diff: #%0 #%1]",
	dateFormat: "YYYY-0MM-0DD 0hh:0mm",

	handlePopup: function(popup, title) {
		stripSuffix = function(type, title) {
			var str = cmd[type + "Suffix"];
			var i = str.indexOf("%0");
			i = title.indexOf(str.substr(0, i));
			if(i != -1) {
				title = title.substr(0, i);
			}
			return title;
		};
		title = stripSuffix("rev", title);
		title = stripSuffix("diff", title);
		var tiddler = store.getTiddler(title);
		var type = this._getField("server.type", tiddler);
		var adaptor = new config.adaptors[type]();
		var limit = null; // TODO: customizable
		var context = {
			host: this._getField("server.host", tiddler),
			workspace: this._getField("server.workspace", tiddler)
		};
		var loading = createTiddlyButton(popup, cmd.loadLabel, cmd.loadTooltip);
		var params = { popup: popup, loading: loading, origin: title };
		adaptor.getTiddlerRevisionList(title, limit, context, params, this.displayRevisions);
	},

	displayRevisions: function(context, userParams) {
		var callback = function(ev) {
			var e = ev || window.event;
			var revision = resolveTarget(e).getAttribute("revision");
			context.adaptor.getTiddlerRevision(tiddler.title, revision, context,
				userParams, cmd.displayTiddlerRevision);
		};
		removeNode(userParams.loading);
		var table = createTiddlyElement(userParams.popup, "table");
		for(var i = 0; i < context.revisions.length; i++) {
			var tiddler = context.revisions[i];
			var row = createTiddlyElement(table, "tr");
			var timestamp = tiddler.modified.formatString(cmd.dateFormat);
			var revision = tiddler.fields["server.page.revision"];
			var cell = createTiddlyElement(row, "td");
			createTiddlyButton(cell, timestamp, cmd.revTooltip, callback, null,
				null, null, { revision: revision });
			cell = createTiddlyElement(row, "td", null, null, tiddler.modifier);
			cell = createTiddlyElement(row, "td");
			createTiddlyButton(cell, cmd.selectLabel, cmd.selectTooltip,
				cmd.revisionSelected, null, null, null,
				{ index:i, revision: revision, col: 2 });
			cmd.context = context; // XXX: unsafe (singleton)!?
		}
	},

	revisionSelected: function(ev) {
		var e = ev || window.event;
		e.cancelBubble = true;
		if(e.stopPropagation) {
			e.stopPropagation();
		}
		var n = resolveTarget(e);
		var index = n.getAttribute("index");
		var col = n.getAttribute("col");
		while(!index || !col) {
			n = n.parentNode;
			index = n.getAttribute("index");
			col = n.getAttribute("col");
		}
		cmd.revision = n.getAttribute("revision");
		var table = n.parentNode.parentNode.parentNode;
		var rows = table.childNodes;
		for(var i = 0; i < rows.length; i++) {
			var c = rows[i].childNodes[col].firstChild;
			if(i == index) {
				if(c.textContent) {
					c.textContent = cmd.selectedLabel;
				} else {
					c.text = cmd.selectedLabel;
				}
			} else {
				if(c.textContent) {
					c.textContent = cmd.compareLabel;
				} else {
					c.text = cmd.compareLabel;
				}
				c.onclick = cmd.compareSelected;
			}
		}
	},

	compareSelected: function(ev) {
		var e = ev || window.event;
		var n = resolveTarget(e);
		var context = cmd.context;
		context.rev1 = n.getAttribute("revision");
		context.rev2 = cmd.revision;
		context.tiddler = context.revisions[n.getAttribute("index")];
		context.format = "unified";
		context.adaptor.getTiddlerDiff(context.tiddler.title, context,
			context.userParams, cmd.displayTiddlerDiffs);
	},

	displayTiddlerDiffs: function(context, userParams) {
		var tiddler = context.tiddler;
		tiddler.title += cmd.diffSuffix.format([context.rev1, context.rev2]);
		tiddler.text = '{{diff{\n{{{\n' + context.diff + '\n}}}\n}}}';
		tiddler.fields.doNotSave = "true"; // XXX: correct?
		if(!store.getTiddler(tiddler.title)) {
			store.addTiddler(tiddler);
		}
		var src = story.getTiddler(userParams.origin);
		story.displayTiddler(src, tiddler);
	},

	displayTiddlerRevision: function(context, userParams) {
		var tiddler = context.tiddler;
		tiddler.title += cmd.revSuffix.format([tiddler.fields["server.page.revision"]]);
		tiddler.fields.doNotSave = "true"; // XXX: correct?
		if(!store.getTiddler(tiddler.title)) {
			store.addTiddler(tiddler);
		}
		var src = story.getTiddler(userParams.origin);
		story.displayTiddler(src, tiddler);
	},

	_getField: function(name, tiddler) {
		return tiddler.fields[name] || config.defaultCustomFields[name];
	}
};

})();
//}}}
