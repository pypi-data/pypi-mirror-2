/***
|''Name''|TiddlySpaceSpaces|
|''Version''|0.5.2|
|''Description''|TiddlySpace spaces management|
|''Status''|@@beta@@|
|''Source''|http://github.com/TiddlySpace/tiddlyspace/raw/master/src/plugins/TiddlySpaceSpaces.js|
|''Requires''|TiddlyWebConfig TiddlySpaceInclusion TiddlySpaceUserControls|
!HTMLForm
<form action="#">
	<fieldset>
		<legend />
		<dl>
			<dt>Name:</dt>
			<dd><input type="text" name="space" /></dd>
		</dl>
		<p>
			<input type="checkbox" name="subscribe" />
			Include the current space in the new space.
		</p>
		<p class="annotation" />
		<input type="submit" />
	</fieldset>
</form>
!Code
***/
//{{{
(function($) {

var host = config.extensions.tiddlyweb.host;
var macro = config.macros.TiddlySpaceSpaces = { // TODO: rename
	formTemplate: store.getTiddlerText(tiddler.title + "##HTMLForm"),
	locale: {
		listError: "error listing spaces: %0",
		addLabel: "Create space",
		addSuccess: "created space %0",
		conflictError: "space <em>%0</em> already exists",
		charError: "error: invalid space name - must only contain lowercase " +
			"letters, digits or hyphens",
		noSpaces: "you have no spaces"
	},

	handler: function(place, macroName, params, wikifier, paramString, tiddler) {
		var container = $("<div />").appendTo(place);
		var mode = params[0] || "list";
		if(mode == "add") {
			container.append(this.generateForm());
		} else {
			this.refresh(container);
		}
	},
	refresh: function(container) {
		container = $(container);
		container.attr("refresh", "macro").attr("macroName", "TiddlySpaceSpaces").
			addClass("listTiddlySpaceSpaces").empty().append("<ul />");
		$.ajax({ // XXX: DRY; cf. TiddlySpaceInclusion
			url: host + "/spaces?mine=1",
			type: "GET",
			success: function(data, status, xhr) {
				var spaces = $.map(data, function(item, i) {
					var link = $("<a />", {
						href: item.uri,
						text: item.name
					});
					return $("<li />").append(link)[0];
				});
				var el = $("ul", container);
				if(data.length > 0) {
					el.append(spaces);
				} else { // XXX: should never occur!?
					$('<p class="annotation" />').text(macro.locale.noSpaces).
						replaceAll(el);
				}
			},
			error: function(xhr, error, exc) {
				displayMessage(macro.locale.listError.format([error]));
			}
		});
	},
	generateForm: function() {
		return $(this.formTemplate).submit(this.onSubmit).
			find("legend").text(this.locale.addLabel).end().
			find(".annotation").hide().end().
			find("[type=submit]").val(this.locale.addLabel).end();
	},
	onSubmit: function(ev) {
		var form = $(this).closest("form");
		var container = form.closest("div");
		var space = form.find("[name=space]").val();
		var subscribe = form.find("[name=subscribe]").attr("checked");
		space = new tiddlyweb.Space(space, host);
		var displayError = config.macros.TiddlySpaceLogin.displayError;
		var ns = config.extensions.tiddlyspace;
		var callback = function(resource, status, xhr) {
			if(subscribe) {
				config.macros.TiddlySpaceInclusion.inclusion(
					ns.currentSpace.name, space.name);
			}
			$(".listTiddlySpaceSpaces").each(function(i, el) {
				refreshElements(el.parentNode);
			});
		};
		var errback = function(xhr, error, exc) { // TODO: DRY (cf. TiddlySpaceLogin)
			var ctx = {
				msg: { 409: macro.locale.conflictError.format([space.name]) },
				form: form,
				selector: "[name=space]"
			};
			displayError(xhr, error, exc, ctx);
		};
		if(ns.isValidSpaceName(space.name)) {
			space.create(callback, errback);
		} else {
			xhr = { status: 409 }; // XXX: hacky
			var ctx = {
				msg: { 409: macro.locale.charError },
				form: form,
				selector: "[name=space]"
			};
			displayError(xhr, null, null, ctx);
		}
		return false;
	}
};

})(jQuery);
//}}}
