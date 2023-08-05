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
		 * AJAX management
		 */
		ajax: {

			check: function(checker, source, callback) {
				if (typeof(checker) == 'undefined') {
					$.getScript(source, callback);
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
		 * Forms managements
		 */
		form: {

			check: function(callback) {
				$.ZBlog.ajax.check($.fn.ajaxSubmit, '/++skin++ZBlog.FO/@@/ztfy.jquery.form/jquery-form.min.js', callback);
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
				var $img = $('<img class="loading" src="/++skin++ZBlog.FO/@@/ztfy.blog.img/loading.gif" />').appendTo($div);
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
		 * Common actions
		 */
		actions: {

			showLoginForm: function(source) {
				var $inputs = $('SPAN.inputs', source);
				$inputs.parents('LI:first').addClass('selected');
				$inputs.show();
				$('INPUT', $inputs).get(0).focus();
			},

			login: function(form) {
				if (typeof(form) == 'undefined') {
					form = $('FORM[name="login_form"]');
				}
				$.ZBlog.form.check(function() {
					$.ZBlog.actions._login(form);
				});
				return false;
			},

			_login: function(form) {
				$.ZBlog.ajax.submit(form, $(form).attr('action') + '/@@ajax/login', {}, $.ZBlog.actions._loginCallback, $.ZBlog.actions._loginError, 'text');
			},

			_loginCallback: function(result, status) {
				if (status == 'success') {
					if (result == 'OK') {
						window.location.reload();
					} else {
						jAlert($.ZBlog.I18n.BAD_LOGIN_MESSAGE, $.ZBlog.I18n.BAD_LOGIN_TITLE, null);
					}
				}
			},

			_loginError: function(request, status) {
				jAlert(status, $.ZBlog.I18n.ERROR_OCCURED, null);
			},

			logout: function() {
				$.get(window.location.href + '/@@login.html/@@ajax/logout', $.ZBlog.actions._logoutCallback);
			},

			_logoutCallback: function(result, status) {
				window.location.reload();
			}
		},

		code: {

			resizeFrame: function(frame) {
				$(frame).css('height', $('BODY', frame.contentDocument).height() + 20);
			}
		}
	}

	var lang = $('HTML').attr('lang') || $('HTML').attr('xml:lang');
	$.getScript('/++skin++ZBlog.FO/@@/ztfy.blog.front.js/i18n/' + lang + '.js');

})(jQuery);