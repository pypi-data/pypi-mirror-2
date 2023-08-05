(function($) {

	/**
	 * String prototype extensions
	 */
	String.prototype.startsWith = function(str) {
		var slen = this.length;
		var dlen = str.length;
		if (slen < dlen) {
			return false;
		}
		return (this.substr(0,dlen) == str);
	}

	String.prototype.endsWith = function(str) {
		var slen = this.length;
		var dlen = str.length;
		if (slen < dlen) {
			return false;
		}
		return (this.substr(slen-dlen) == str);
	}

	/**
	 * Main $.ZBlog JavaScript package
	 */
	$.ZBlog = {

		/**
		 * JSON management
		 */
		json: {

			getAddr: function() {
				var href = window.location.href;
				return href.substr(0, href.lastIndexOf("/")+1);
			},

			post: function(method, params, onsuccess, onerror, base) {
				var addr = $.ZBlog.json.getAddr();
				if (base) {
					addr += '/' + base;
				}
				var options = {
					url: addr,
					type: 'POST',
					method: method,
					params: params,
					success: onsuccess,
					error: onerror
				};
				$.jsonRpc(options);
			}

		},  /** $.ZBlog.json */

		/**
		 * AJAX management
		 */
		ajax: {

			check: function(checker, source, callback) {
				if (typeof(checker) == 'undefined') {
					$.getScript(source, callback)
				} else {
					callback();
				}
			},

			getAddr: function() {
				var href = window.location.href;
				return href.substr(0, href.lastIndexOf("/")+1);
			},
	
			post: function(url, data, onsuccess, onerror, datatype) {
				if (url.startsWith('http://')) {
					var addr = url;
				} else {
					var addr = $.ZBlog.ajax.getAddr() + url;
				}
				var options = {
					url: addr,
					type: 'POST',
					data: data,
					dataType: datatype,
					success: onsuccess,
					error: onerror
				};
				$.ajax(options);
			},

			submit: function(form, url, data, onsuccess, onerror, datatype) {
				if (url.startsWith('http://')) {
					var addr = url;
				} else {
					var addr = $.ZBlog.ajax.getAddr() + url;
				}
				var options = {
					url: addr,
					type: 'POST',
					data: data,
					dataType: datatype,
					success: onsuccess,
					error: onerror
				};
				$(form).ajaxSubmit(options);
			}

		},

		/**
		 * Loading management
		 */
		loader: {

			div: null,

			start: function(parent) {
				parent.empty();
				var $div = $('<div class="loader"></div>').appendTo(parent);
				var $img = $('<img class="loading" src="/++skin++ZBlog.BO/@@/ztfy.blog.img/loading.gif" />').appendTo($div);
				$.ZBlog.loader.div = $div;
			},

			stop: function() {
				if ($.ZBlog.loader.div != null) {
					$.ZBlog.loader.div.replaceWith('');
					$.ZBlog.loader.div = null;
				}
			}

		}, /** $.ZBlog.loader */

		/**
		 * Dialogs management
		 */
		dialog: {

			src: null,

			options: {
				expose: {
					maskId: 'mask',
					color: '#ccc',
					opacity: 0.6,
					zIndex: 9998
				},
				api: true,
				oneInstance: false,
				closeOnClick: false,
				onBeforeLoad: function() {
					$.ZBlog.loader.start(this.getContent());
					this.getContent().load($.ZBlog.dialog.src);
					if ($.browser.msie && ($.browser.version < '7')) {
						$('select').css('visibility', 'hidden');
					}
				},
				onClose: function() {
					$.ZBlog.dialog.onClose();
					if ($.browser.msie && ($.browser.version < '7')) {
						$('select').css('visibility', 'hidden');
					}
				}
			},

			count: 0,

			getCurrent: function() {
				return $('#dialog_' + $.ZBlog.dialog.count);
			},

			open: function(src) {
				if (!$.ZBlog.dialog.dialogs) {
					$.ZBlog.dialog.dialogs = new Array();
					$.ZBlog.dialog.count = 0;
				}
				$.ZBlog.dialog.count += 1;
				var id = 'dialog_' + $.ZBlog.dialog.count;
				var options = {}
				var expose_options = {
					maskId: 'mask',
					color: '#ccc',
					opacity: 0.6,
					zIndex: $.ZBlog.dialog.options.expose.zIndex + $.ZBlog.dialog.count
				};
				$.extend(options, $.ZBlog.dialog.options, { expose: expose_options });
				$.ZBlog.dialog.dialogs[$.ZBlog.dialog.count] = $('<div class="overlay"></div>').attr('id', id)
																							   .appendTo($('body'));
				$.ZBlog.dialog.src = src;
				$('#' + id).empty()
						   .overlay(options)
						   .load();
			},

			close: function() {
				var id = 'dialog_' + $.ZBlog.dialog.count;
				$('#' + id).overlay().close();
			},

			onClose: function() {
				if (typeof(tinyMCE) != 'undefined') {
					if (tinyMCE.activeEditor) {
						tinyMCE.execCommand('mceRemoveControl', false, tinyMCE.activeEditor.id);
					}
				}
				$('BODY DIV:last').remove();
				$.ZBlog.dialog.dialogs[$.ZBlog.dialog.count].remove();
				$.ZBlog.dialog.dialogs[$.ZBlog.dialog.count] = null;
				$.ZBlog.dialog.count -= 1;
			},

		}, /** $.ZBlog.dialog */

		/**
		 * Forms managements
		 */
		form: {

			check: function(callback) {
				$.ZBlog.ajax.check($.fn.ajaxSubmit, '/++skin++ZBlog.BO/@@/ztfy.jquery.form/jquery-form.min.js', callback);
			},

			hideStatus: function() {
				$('FORM DIV.status').animate({
					'opacity': 0,
					'height': 0
				}, 2000, function() {
					$(this).remove();
				});
			},

			reset: function(form) {
				form.reset();
				$('input:first', form).focus();
			},

			add: function(form, parent) {
				$.ZBlog.form.check(function() {
					$.ZBlog.form._add(form, parent);
				});
				return false;
			},

			_add: function(form, parent) {
				if (typeof(tinyMCE) != 'undefined') {
					tinyMCE.triggerSave();
				}
				var data = {}
				if (parent) {
					data.parent = parent;
				}
				$.ZBlog.form.add_action = $(form).attr('action');
				$.ZBlog.ajax.submit(form, $(form).attr('action') + '/@@ajax/ajaxCreate', data, $.ZBlog.form._addCallback, null, 'json');
			},

			_addCallback: function(result, status) {
				if (status == 'success') {
					output = result.output;
					if (output.startsWith('<!-- OK -->')) {
						$.ZBlog.dialog.close();
						$('DIV.form').replaceWith(output);
					} else {
						var dialog = $.ZBlog.dialog.getCurrent();
						$('DIV.dialog', dialog).replaceWith(output);
						$('FORM', dialog).attr('action', $.ZBlog.form.add_action);
						$('#form-buttons-add', dialog).bind('click', function(event) {
							$.ZBlog.form.add(this.form, result.parent);
						});
						$('#form-buttons-cancel', dialog).bind('click', function(event) {
							$.ZBlog.dialog.close();
						});
						$('.hint', dialog).tooltip({
							tip: '#tooltip',
							position: 'bottom left',
							opacity: 0.8,
							offset: [ -5, 0 ]
						});
					}
				}
			},

			edit: function(form, base) {
				$.ZBlog.form.check(function() {
					$.ZBlog.form._edit(form, base);
				});
				return false;
			},

			_edit: function(form, base) {
				if (typeof(tinyMCE) != 'undefined') {
					tinyMCE.triggerSave();
				}
				$.ZBlog.form.edit_action = $(form).attr('action');
				$.ZBlog.ajax.submit(form, $(form).attr('action') + '/@@ajax/ajaxEdit', {}, $.ZBlog.form._editCallback, null, 'json');
			},

			_editCallback: function(result, status) {
				if (status == 'success') {
					var output = result.output;
					if (output == 'OK') {
						$.ZBlog.dialog.close();
						$('DIV.status').remove();
						$('DIV.required-info').after('<div class="status"><div class="summary">' + $.ZBlog.I18n.DATA_UPDATED + '</div></div>');
					} else if (output == 'NONE') {
						$.ZBlog.dialog.close();
						$('DIV.status').remove();
						$('DIV.required-info').after('<div class="status"><div class="summary">' + $.ZBlog.I18n.NO_UPDATE + '</div></div>');
					} else if (output.startsWith('<!-- OK -->')) {
						$.ZBlog.dialog.close();
						$('DIV.form').replaceWith(output);
					} else {
						var dialog = $.ZBlog.dialog.getCurrent();
						$('DIV.dialog', dialog).replaceWith(output);
						$('FORM', dialog).attr('action', $.ZBlog.form.edit_action);
						$('#form-buttons-dialog_submit', dialog).bind('click', function(event) {
							$.ZBlog.form.edit(this.form);
						});
						$('#form-buttons-dialog_cancel', dialog).bind('click', function(event) {
							$.ZBlog.dialog.close();
						});
						$('.hint', dialog).tooltip({
							tip: '#tooltip',
							position: 'bottom left',
							opacity: 0.8,
							offset: [ -5, 0 ]
						});
					}
				}
			},

			remove: function(oid, source) {
				jConfirm($.ZBlog.I18n.CONFIRM_REMOVE, $.ZBlog.I18n.CONFIRM, function(confirmed) {
					if (confirmed) {
						var data = {
							id: oid
						}
						$.ZBlog.form.ajax_source = source;
						$.ZBlog.ajax.post(window.location.href + '/@@ajax/ajaxRemove', data, $.ZBlog.form._removeCallback, null, 'text');
					}
				});
			},

			_removeCallback: function(result, status) {
				if ((status == 'success') && (result == 'OK')) {
					$($.ZBlog.form.ajax_source).parents('TR').remove();
				}
			},

			update: function(form) {
				$.ZBlog.form.check(function() {
					$.ZBlog.form._update(form);
				});
				return false;
			},

			_update: function(form) {
				if (typeof(tinyMCE) != 'undefined') {
					tinyMCE.triggerSave();
				}
				var data = $(form).formToArray(true);
				$.ZBlog.ajax.post($(form).attr('action') + '/@@ajax/ajaxUpdate', data, $.ZBlog.form._updateCallback, null, 'text');
			},

			_updateCallback: function(result, status) {
				if ((status == 'success') && (result == 'OK')) {
					$('DIV.status').remove();
					$('LEGEND').after('<div class="status"><div class="summary">Data successfully updated.</div></div>');
				}
			}

		}, /** $.ZBlog.form */

		/**
		 * Container management
		 */
		container: {

			remove: function(oid, source) {
				var options = {
					_source: source,
					url: $.ZBlog.json.getAddr(),
					type: 'POST',
					method: 'remove',
					params: {
						id: oid
					},
					success: function(data, status) {
						$(this._source).parents('TR').remove();
					},
					error: function(request, status, error) {
						jAlert(request.responseText, $.ZBlog.I18n.ERROR_OCCURED, window.location.reload);
					}
				}
				jConfirm($.ZBlog.I18n.CONFIRM_REMOVE, $.ZBlog.I18n.CONFIRM, function(confirmed) {
					if (confirmed) {
						$.jsonRpc(options);
					}
				});
			}

		},  /** $.ZBlog.container */

		/**
		 * Sortables management
		 */
		sortable: {

			options: {
				handle: 'IMG.handler',
				axis: 'y',
				containment: 'parent',
				placeholder: 'sorting-holder',
				stop: function(event, ui) {
					var ids = new Array();
					$('TABLE.orderable TD.id').each(function (i) {
						ids[ids.length] = $(this).text();
					});
					var data = {
						ids: ids
					}
					$.ZBlog.ajax.post(window.location.href + '/@@ajax/ajaxUpdateOrder', data, null, function(request, status, error) {
						jAlert(request.responseText, $.ZBlog.I18n.ERROR_OCCURED, window.location.reload);
					});
				}
			}

		},  /** $.ZBlog.sortable */

		/**
		 * Treeviews management
		 */
		treeview: {

			changeParent: function(event,ui) {
				var $dragged = $(ui.draggable.parents('TR'));
				if ($dragged.appendBranchTo(this)) {
					var source = $dragged.attr('id').substr('node-'.length);
					var target = $(this).attr('id').substr('node-'.length);
					var options = {
						url: $.ZBlog.json.getAddr(),
						type: 'POST',
						method: 'changeParent',
						params: {
							source: parseInt(source),
							target: parseInt(target)
						},
						error: function(request, status, error) {
							jAlert(request.responseText, $.ZBlog.I18n.ERROR_OCCURED, window.location.reload);
						}
					}
					$.jsonRpc(options);
				}
			}

		},  /** $.ZBlog.treeview */

		/**
		 * Internal references management
		 */
		reference: {

			activate: function(selector) {
				$('INPUT[name='+selector+']').attr('readonly','')
											 .val('')
											 .focus();
				$('INPUT[name='+selector+']').prev().val('');
			},

			keyPressed: function(event) {
				if (event.which == 13) {
					$.ZBlog.reference.search(this);
					return false;
				}
			},

			search: function(source) {
				$.ZBlog.reference.source = source;
				var $form = $(source).parents('FORM');
				$.ZBlog.ajax.post($form.attr('action') + '/@@ajax/ajaxSearch', { 'title': $(source).val() }, $.ZBlog.reference._searchCallback, null, 'json');
			},

			_searchCallback: function(result, status) {
				if (status == 'success') {
					if (result.length == 1) {
						$.ZBlog.reference.select(result[0].oid, result[0].title);
					} else if (result.length > 1) {
						var $selectbox = $('#selector');
						if ($selectbox.length == 0) {
							$selectbox = $('<div id="selector"></div>');
						}
						$selectbox.empty();
						for (var i=0; i<result.length; i++) {
							var oid = result[i].oid;
							var title = result[i].title;
							$('<div onclick="return $.ZBlog.reference.select(\'' + oid + '\',\'' + title + '\');"></div>').addClass('reference')
																														  .text(title)
																														  .appendTo($selectbox);
						}
						var $source = $($.ZBlog.reference.source);
						var position = $source.position();
						$selectbox.css('width', $source.width()-10)
								  .appendTo($source.parents('DIV.overlay'))
								  .overlay({
							expose: 'transparent',
							api: true,
							oneInstance: false,
							closeOnClick: false,
							closeOnEsc: false,
							top: position.top + $source.height(),
							left: position.left + 30,
							absolute: true,
							onBeforeLoad: function() {
								if ($.browser.msie && ($.browser.version < 7)) {
									$('select').css('visibility', 'hidden');
								}
							},
							onClose: function() {
								if ($.browser.msie && ($.browser.version < 7)) {
									$('select').css('visibility', 'visible');
								}
							}
						}).load();
					}
				}
			},

			select: function(oid, title) {
				var source = $.ZBlog.reference.source;
				$(source).prev().val(oid);
				$(source).val(title + ' (OID: ' + oid + ')')
						 .attr('readonly', 'readonly');
				$('#selector').overlay().close();
				$('#selector').remove();
				return false;
			}

		},  /** $.ZBlog.reference */

		/**
		 * Topics management
		 */
		topic: {

			remove: function(form) {
				$.ZBlog.ajax.post($(form).attr('action') + '/@@ajax/ajaxDelete', {}, $.ZBlog.topic.removeCallback, null, 'json');
				return false;
			},

			removeCallback: function(result, status) {
				if (status == 'success') {
					window.location = result.url;
				}
			}

		},  /** $.ZBlog.topic */

		/**
		 * Properties viewlet management
		 */
		properties: {

			switcher: function(div) {
				$('DIV.properties DIV.switch').toggle();
			}

		}  /** $.ZBlog.properties */

	}  /** $.ZBlog */

	var lang = $('HTML').attr('lang') || $('HTML').attr('xml:lang');
	$.getScript('/++skin++ZBlog.BO/@@/ztfy.blog.back.js/i18n/' + lang + '.js');

	/**
	 * Override Chromium opacity bug on Linux !
	 */
	if ($.browser.safari) {
		$.support.opacity = true;
	}

	/**
	 * Automatically handle images properties download links
	 */
	if ($.fn.fancybox) {
		$(document).ready(function() {
			$('DIV.download-link IMG').parents('A').fancybox({
				type: 'image',
				titleShow: false,
				hideOnContentClick: true
			});
		});
	}

})(jQuery);