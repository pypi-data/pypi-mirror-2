function updateElement(id, value) {
	/**
	 *	Manage the element with the "display" style.
	 */
	if (value == "short") {
		document.getElementById(id + "-short").style.display = 'inline';
		document.getElementById(id + "-long").style.display = 'none';
	} else {
		document.getElementById(id + "-long").style.display = 'inline';
		document.getElementById(id + "-short").style.display = 'none';
	}
}

function updatePage() {
	/**
	 * Update the page with the right display for each element.
	 */
	for (id in window.linguaface.openedFields) {
		for (lang in window.linguaface.openedFields[id]) {
			var elementId = "linguaface-" + id + "-" + lang;
			var value = window.linguaface.openedFields[id][lang];
			updateElement(elementId, value);
		}
	}
}

function initPage() {
	/**
	 * Initialize the linguaface javascript
	 */

	var languageList = document.getElementById("linguaface-langs").value;
	var langs = eval(languageList.replace(/^[/, '{').replace(/^]/, '}'));
	var idList = document.getElementById("linguaface-ids").value;
	var ids = eval(idList.replace(/^[/, '{').replace(/^]/, '}'));
	//alert(langs);
	// we are building a dictionnary of dictionnary
	// each element is a field in one language. It's value is either "short
	// or "long". At the beginning, only short fields are displayed.
	window.linguaface = {}
	window.linguaface.openedFields = {}

	for (i = 0; i < ids.length; i++) {
		window.linguaface.openedFields[ids[i]] = {};
		for (j = 0; j < langs.length; j++) {
			window.linguaface.openedFields[ids[i]][langs[j]] = "short";
		}
	}
	updatePage();
}

function switchElement(id, lang) {
	/**
	 * Switch the long or short display of an element (a field already translated)
	 */
	if (window.linguaface.openedFields[id][lang] == "short") {
		window.linguaface.openedFields[id][lang] = "long"
	} else {
		window.linguaface.openedFields[id][lang] = "short"
	}
	updatePage();
}


registerPloneFunction(initPage);
