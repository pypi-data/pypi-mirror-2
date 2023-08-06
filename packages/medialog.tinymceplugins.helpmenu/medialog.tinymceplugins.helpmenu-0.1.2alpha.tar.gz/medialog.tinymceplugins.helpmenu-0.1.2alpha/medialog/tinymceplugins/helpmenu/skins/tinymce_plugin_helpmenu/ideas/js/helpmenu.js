tinyMCEPopup.requireLangPack();

var HelpDialog = {
	init : function () {
		var tcont, t = this, i, info, html;

		tinyMCEPopup.resizeToInnerSize();
		t.ed = tinyMCEPopup.editor;

		// Give FF some time
		window.setTimeout(function () { t.insertHelpmenuIFrame(t.ed); }, 10);

		tcont = document.getElementById('plugintablecontainer');
		document.getElementById('plugins_tab').style.display = 'none';

		html = '<table id="plugintable">';
		html += '<tr>';
		html += '<th class="plugin">' + t.ed.getLang('helpmenu.plugin') + '</th>';
		html += '<th class="author">' + t.ed.getLang('helpmenu.author') + '</th>';
		html += '<th class="version">' + t.ed.getLang('helpmenu.version') + '</th>';
		html += '</tr>';

		i = 0;

		tinymce.each(t.ed.plugins, function(p, n) {
			if (!p.getInfo)
				return;

			html += '<tr' + (Math.floor(i/2) === i/2 ? '' : ' class="even"') + '>';

			info = p.getInfo();

			html += '<td class="plugin" title="' + n + '">'
				+ (
					(info.infourl != null && info.infourl != '') ?
						'<a href="' + info.infourl + '" target="_blank">' + info.longname + '</a>'
						:
						info.longname
				)
				+ '</td>';

			html += '<td class="author" title="' + n + '">'
				+ (
					(info.authorurl != null && info.authorurl != '') ?
						'<a href="' + info.authorurl + '" target="_blank">' + info.author + '</a>'
						:
						info.author
				)
				+ '</td>';

			html += '<td class="version">' + info.version + '</td>';
			html += '</tr>';

			i++;
		});

		html += '</table>';

		tcont.innerHTML = html;

		tinyMCEPopup.dom.get('version').innerHTML = tinymce.majorVersion + "." + tinymce.minorVersion;
		tinyMCEPopup.dom.get('date').innerHTML = tinymce.releaseDate;

		// resizing
		window.onresize = HelpmenuDialog.resize;
		HelpmenuDialog.resize();

		if (i < 0) {
			document.getElementById('plugins_tab').style.display = (i > 0) ? "" : "none";
		}

		// set the TOC page as starting page for the helpmenu docs
		info = { file : "", title : "" };
		for (plugin in this.ed.plugins.helpmenu.docs) {
			for (page in this.ed.plugins.helpmenu.docs[plugin]) {
				if (this.ed.plugins.helpmenu.docs[plugin][page].file.match(/index\.htm/)) {
					info.file = this.ed.plugins.helpmenu.docs[plugin][page].file;
					info.title = this.ed.plugins.helpmenu.docs[plugin][page].title;
				}
			}
		}

		this.tocPage = info;
	},


	insertHelpmenuIFrame : function (ed) {
		if (ed.plugins.helpmenu.docs) {
			var html = '<iframe src=""></iframe>',
				page = tinyMCEPopup.getWindowArg('page'),
				anchor = "";

			document.getElementById('iframecontainer').innerHTML = html;

			if (!page || typeof page != "string") {
				page = this.tocPage.file;
			} else {
				// modify page URL
			}

			if (page.match(/#[^\/]+/)) {
				anchor = page.replace(/^.+#(.*)$/, "$1");
				page = page.replace(/^(.+)#.*$/, "$1");
			}

			html = '<iframe src="'
				+ page
				+ '?a='
				+ anchor
				+ '"></iframe>';

			document.getElementById('iframecontainer').innerHTML = html;
			mcTabs.displayTab('helpmenu_tab','helpmenu_panel')

		} else {
			document.getElementById("helpmenu_tab").style.display = "none";
			mcTabs.displayTab('general_tab','general_panel');
		}
	},


	resize : function () {
		// resize panel_wrapper
		var divs = document.getElementsByTagName("div");
		var panel_wrapper = false;
		var action_panel = false;
		for (var i = 0; i < divs.length; i++) {
			if (typeof(divs[i].className) != "undefined" && divs[i].className == "panel_wrapper")
				panel_wrapper = divs[i];
			if (typeof(divs[i].className) != "undefined" && divs[i].className == "mceActionPanel")
				action_panel = divs[i];
		}

		if (panel_wrapper && action_panel) {
			// IE needs Timeout...
			var doc = (window.document.compatMode && window.document.compatMode == "CSS1Compat") ?
				window.document.documentElement : window.document.body || null;
			var wHeight = (!tinymce.isIE) ? self.innerHeight : doc.clientHeight + 38;

			panel_wrapper.style.height = Number(wHeight - 75 - action_panel.offsetHeight) + "px";
		}
	},


	helpmenuPage : function (win) {
		this.checkTocPage(win);
		this.modifyLinkTargets(win);

		if (tinymce.isIE)
			win.document.getElementsByTagName("body")[0].style.marginRight = "15px";
	},


	modifyLinkTargets : function (win) {
		var i, url, doc = win.document;
		var a = doc.getElementsByTagName("a"),
			baseURL = win.location.pathname.replace(/[^\/]+$/, "");

		// Request with a location hash?
		if (win.location.search.match(/\?a=/i)) {
			// Yes, find element with suitable ID
			var i = win.location.search.replace(/^.*a=([^&=]+).*$/i, "$1"),
				elm = doc.getElementById(i),
				elms = doc.getElementsByName(i);

			if (!elm && elms && elms.length > 0) {
				elm = elms[0];
			}

			if (elm) {
				// scroll to element with suitable ID
				win.scrollBy(0, elm.offsetTop);
			}
		}

		// modify all link targets with a hash
		for (i = 0; i < a.length; i++) {
			url = a[i].href.replace(/^http:\/\/[^\/]+/, "");

			// URL has a hash?
			if (a[i].href && a[i].href != "" &&
				a[i].href.match(/#.+/) &&
				// In IE the href value doesn't carry the complete URL when the HTML document is loaded locally
				(!url.replace(/[^\/]+$/, "") ||
					url.replace(/[^\/]+$/, "") == baseURL)
			) {
				// modify URL so xyz#abc becomes xyz?a=abc
				a[i].href = a[i].href.replace(/^(.*)#.+$/i, "$1")
					+ "?a="
					+ a[i].href.replace(/^.*#([^#]+)$/i, "$1");
			}
		}
	},


	checkTocPage : function (win) {
		var doc = win.document;
		var body = doc.getElementsByTagName("body")[0],
			ul = doc.getElementsByTagName("ul"),
			index = this.tocPage,
			plugin,	page, p, li, a, c, h, i, found;

		// create TOC based on plugins' TOC data - but only for helpmenu plugin's index page!
		if (win.location.href.match(/\/helpmenu\/docs\/[^\/]+\/index\.htm/)) {
			if (ul.length > 0) {
				ul = ul[0];

				while (ul.firstChild) {
					ul.removeChild(ul.firstChild);
				}

			} else {
				// template file got messed up... recreate it
				while (body.firstChild) {
					body.removeChild(body.firstChild);
				}

				h = doc.createElement("h1");
				h.appendChild(
					doc.createTextNode(this.ed.getLang('helpmenu.toc'))
				);
				body.appendChild(h);

				ul = doc.createElement("ul");
				body.appendChild(ul);
			}

			// add links to TOC starting with helpmenu plugin's links
			this.addTocLinks({
				win: win,
				ul: ul,
				plugin: "helpmenu"
			});

			// add other plugins' links to TOC but exclude non-documented ones (plus helpmenu plugin itself)
			li = new RegExp(
				("helpmenu," + this.ed.plugins.helpmenu.nonDocumentedPlugins).split(",").join("|"),
				"i"
			);

			for (plugin in this.ed.plugins.helpmenu.docs) {
				if (!plugin.match(li)) {
					this.addTocLinks({
						win: win,
						ul: ul,
						plugin: plugin
					});
				}
			}

		} else {
			// modify/create links back to the helpmenu plugin's index page (TOC)
			found = 0;
			a = doc.getElementsByTagName("a");
			for (i = 0; i < a.length; i++) {
				if (decodeURIComponent(a[i].href).match(/\{\#toc_url\}/)) {
					a[i].href = index.file;
					found++;
				}

				for (c = 0; c < a[i].childNodes.length; c++) {
					if (a[i].childNodes[c].nodeType == 3) {
						a[i].childNodes[c].data = a[i].childNodes[c].data.replace(/\{\#toc\}/, index.title);
					}
				}
			}

			// make sure at least one link back to the TOC exists
			if (found < 1) {
				p = doc.createElement("p");
				p.className = "toc-link";

				a = doc.createElement("a");
				a.appendChild(doc.createTextnode(index.title));
				a.href = index.file;

				p.appendChild(a);
				body.appendChild(p);
			}
		}
	},


	addTocLinks : function (params) {
		var doc = params.win.document,
			win = params.win,
			ul = params.ul,
			plugin = params.plugin;

		var body = doc.getElementsByTagName("body")[0],
			docs = this.ed.plugins.helpmenu.docs,
			list = [],
			page, li, a, c, container, i, index;

		// create <li> elements for each page
		for (page in docs[plugin]) {
			if (!docs[plugin][page].file.match(/index\.htm/)
				// exclude TOC page of helpmenu plugin!
				|| plugin != "helpmenu"
			) {
				if (!this.overrideExists(docs[plugin][page].file)) {
					a = doc.createElement("a");
					a.href = docs[plugin][page].file;
					a.appendChild(
						doc.createTextNode(
							docs[plugin][page].title
						)
					);
					li = doc.createElement("li");
					li.appendChild(a);

					if (plugin != "helpmenu" && docs[plugin][page].index) {
						// this page is the starting page of the plugin's docs!
						container = li;
					} else {
						// regular (sub) page...
						list.push(li);
					}
				}
			}
		}

		// only links of plugins other than the helpmenu plugin need a container
		if (plugin != "helpmenu") {
			if (!container) {
				// take first page as beginning of sub TOC
				container = list.reverse().pop();
				list.reverse();
			}

			// insert sub TOC into TOC
			ul.appendChild(container);

			// create new <ul> element inside container
			ul = doc.createElement("ul");
			container.appendChild(ul);
		}

		for (i = 0; i < list.length; i++) {
			// store all <li>s in (sub) TOC
			ul.appendChild(list[i]);
		}
	},


	overrideExists : function (page) {
		var docs = this.ed.plugins.helpmenu.docs,
			p, pl, overridden = false;

		for (pl in docs) {
			for (p in docs[pl]) {
				if (docs[pl][p].overrides
					&&
					docs[pl][p].overrides == page
				) {
					return true;
				}
			}
		}

		return false;
	}
};


tinyMCEPopup.onInit.add(HelpmenuDialog.init, HelpmenuDialog);

// For modal dialogs in IE
if (tinymce.isIE) {
	document.write('<base target="_self" />');
}
