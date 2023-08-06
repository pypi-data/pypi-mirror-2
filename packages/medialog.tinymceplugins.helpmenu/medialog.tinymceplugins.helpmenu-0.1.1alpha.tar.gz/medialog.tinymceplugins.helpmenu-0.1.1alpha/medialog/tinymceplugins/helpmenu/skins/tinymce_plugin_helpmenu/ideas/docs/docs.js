/**
initialize helpmenu page
**/

(function () {
	var onLoad = window.onload;
	window.onload = function () {
		if (typeof onLoad == "function")
			onLoad();

		if (window.parent && window.parent.HelpmenuDialog) {
			window.parent.HelpmenuDialog.helpmenuPage(window);
		}
	};
})();
