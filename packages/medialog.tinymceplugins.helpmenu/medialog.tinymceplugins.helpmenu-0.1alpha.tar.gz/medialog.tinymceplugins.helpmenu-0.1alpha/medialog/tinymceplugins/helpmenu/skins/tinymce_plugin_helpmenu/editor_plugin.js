/**
 * $Id: editor_plugin_src.js 201 2007-02-12 15:56:56Z Felix Riesterer $
 *
 * @author Felix Riesterer
 * @copyright Copyright © 2004-2009, Moxiecode Systems AB, All rights reserved.
 */

(function() {
	// Load plugin specific language pack
	tinymce.PluginManager.requireLangPack('help');

	tinymce.create('tinymce.plugins.HelpPlugin', {
		init : function (ed, url) {
			var t = this;
			t.url = url;
			t.editor = ed;
			t.docs = false;
			t.nonDocumentedPlugins = "compat2x,autosave,example,inlinepopups,noneditable,safari,tabfocus";

			ed.addButton('help', {
				title : 'help.desc',
				cmd : 'mceHelp'
			});

			ed.addCommand('mceHelp', function (val, page) {
				ed.windowManager.open({
					file : url + '/help.htm',
					width : (t.docs ?
						740 + parseInt(ed.getLang('help.delta_width', 0))
						:
						5400 + parseInt(ed.getLang('help.delta_width', 0))
					),
					height : (t.docs ?
						500 + parseInt(ed.getLang('help.delta_height', 0))
						:
						350 + parseInt(ed.getLang('help.delta_height', 0))
					),
					inline : 1
				}, {
					tinymce_version : tinymce.majorVersion + "." + tinymce.minorVersion,
					tinymce_releasedate : tinymce.releaseDate,
					page : page,
					pluginURL : url
				});
			});

			ed.onPostRender.add(t._setupTOC, t);
		},

		getInfo : function () {
			return {
				longname : 'Help Plugin',
				author : 'Felix Riesterer',
				authorurl : 'http://www.felix-riesterer.de/tinymce',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/help',
				version : "1.0"
			};
		},

		_setupTOC : function () {
			// load TOC from a plugin's help docs
			var n, p, t = this;

			var setup = function (plugin, lang) {
				// try editor language first and try English as fallback if necessary
				var path = t.editor.baseURI.source
					+ "/plugins/"
					+ plugin
					+ "/docs/"
					+ (lang || t.editor.settings.language)
					+ "/";

				tinymce.util.XHR.send({
					url : path + "toc.xml",

					error : function () {
						// fallback to English if language-specific docs weren't available
						if (!lang && t.editor.settings.language != "en") {
							setup (plugin, "en");
						}
					},

					success : function (text, xml) {
						// xml.responseXML now carries the TOC in XML format!
						var i, a, url, toc = [],
							p = xml.responseXML.getElementsByTagName("page");

						for (i = 0; i < p.length; i++) {
							toc[i] = {};
							for (a = 0; a < p[i].attributes.length; a++) {
								if (p[i].attributes[a].nodeValue)
									toc[i][p[i].attributes[a].nodeName] = p[i].attributes[a].nodeValue;

								if (p[i].attributes[a].nodeName.match(/file/))
									toc[i][p[i].attributes[a].nodeName] = path + p[i].attributes[a].nodeValue;

								if (p[i].attributes[a].nodeName.match(/explains/)) {
									// add plugin path to the "explains" value of the actual help page for context-sensitive help
									url = path.replace(/\/docs\/.*/, "/");
									/*
										fix context-sensitive help pages which are in the help plugin's docs
										but in fact were meant for the advanced theme's dialogs
									*/
									url = url.replace(/\/plugins\/help\//, "/themes/advanced/");
									toc[i][p[i].attributes[a].nodeName] = url + p[i].attributes[a].nodeValue;
								}

								if (p[i].attributes[a].nodeName.match(/overrides/)) {
									/*
										add theme path to the "replaces" value of the actual help page
										so a plugin's doc page overwrites the themes's original help page
										(as provided by the help plugin's doc pages)
									*/
									// url = path.replace(/\/plugins\/.*/, "/themes/advanced/");
									url = path.replace(/\/plugins\/[^\/]+/, "/plugins/help");
									toc[i][p[i].attributes[a].nodeName] = url + p[i].attributes[a].nodeValue;
								}
							}
						}

						// save TOC in this plugin's "docs" property
						if (!t.docs)
							t.docs = {};

						t.docs[plugin] = toc;
					}
				});
			};

			// get TOCs from all plugins but exclude non-documented ones!
			n = new RegExp(t.nonDocumentedPlugins.split(",").join("|"), "i");
			for (p in t.editor.plugins) {
				// exclude certain plugins since they don't need instructions for end-users
				if (!p.match(n)) {
					setup(p);
				}
			}
		},

		_addHelpIconToDialog : function (win) {
			var ed = this.editor,
				doc = win.document,
				helpPage = "",
				override = 0,
				css, div, onclick, plugin, page;

			// find out if there is a help page available for this very dialog
			for (plugin in ed.plugins.help.docs) {
				for (page in ed.plugins.help.docs[plugin]) {
					if (ed.plugins.help.docs[plugin][page].explains
						&&
						ed.plugins.help.docs[plugin][page].explains == win.location.href
					) {
						helpPage = ed.plugins.help.docs[plugin][page].file;
					}
				}
			}

			// create context-sensitive help icon
			if (helpPage) {
				// create help call command
				onclick = function () { ed.execCommand("mceHelp", false, helpPage); };

				// create icon and insert it into the dialog
				div = doc.createElement("div");
				doc.body.appendChild(div);
				div.id = "help-icon";
				div.title = ed.getLang("help.dialog_help");
				div.onclick = onclick;

				// set styles for help icon (load CSS file)
				css = doc.createElement("link");
				css.type = "text/css";
				css.rel = "stylesheet";
				css.href = this.url + "/css/help-icon.css";
				doc.getElementsByTagName("head")[0].appendChild(css);
			}
		}
	});

	tinymce.PluginManager.add('help', tinymce.plugins.HelpPlugin);
})();