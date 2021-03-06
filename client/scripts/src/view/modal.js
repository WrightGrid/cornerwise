define(["backbone", "view/alerts", "jquery", "utils", "underscore", "appState"],
       function(B, alerts, $, $u, _, appState) {
           return B.View.extend({
               initialize: function(options) {
                   if (options.url)
                       this.template = $u.templateWithUrl(options.url);
                   else if (options.template)
                       this.template = function(_, cb) {
                           cb(options.template());
                       };

                   if (!this.template)
                       throw new Error("You must initialize a modal view with a URL or template.");

                   this.showingClass = options.showingClass || "showing";
                   this.container = options.container || "#modal";
                   this.context = options.context;
                   this.shouldShow = false;
               },

               el: "#modal-contents",

               events: {
                   "submit form": "onSubmit"
               },

               getContainer: function() {
                   return this.$el.closest(this.container);
               },

               getContext: function() {
                   return _.extend({model: this.model,
                                    collection: this.collection},
                                   this.context,
                                   appState.getState());
               },

               _update: function() {
                   this.getContainer()
                       .toggleClass(this.showingClass, this.shouldShow)
                       .toggle(this.shouldShow);

                   $(document.body).toggleClass("modal", this.shouldShow);

                   if (this.shouldShow && this.wasRendered)
                       this.wasRendered();
               },

               render: function() {
                   if (this.shouldShow) {
                       var self = this;
                       this.template(
                           this.getContext(),
                           function(html) {
                               self.$el.html(html);
                               self._update();
                           });
                   }

                   return this;
               },

               show: function() {
                   this.shouldShow = true;
                   this.render();
               },

               hide: function() {
                   this.shouldShow = false;
                   this._update();
               },

               clearFormErrors: function() {
                   this.$("label").removeClass("error");
                   this.$(".form-error").remove();
               },

               showFormErrors: function(errors) {
                   var $el = this.$el;
                   this.clearFormErrors();
                   this.$(".input-group").each(function(i, el) {
                       var name = $(el).find("[name]").attr("name");
                       if (errors[name]) {
                           $(el).addClass("error");
                           $("<div class='form-error'></div>")
                               .text(errors[name].join(", "))
                               .prependTo(el);
                       }
                   });
               },

               onSubmit: function(e) {
                   var form = e.target,
                       data = $(form).serialize(),
                       self = this;

                   data += "&csrfmiddlewaretoken=" + $u.getCsrfToken();

                   $.ajax({
                       url: form.action,
                       method: form.method,
                       data: data
                   }).done(function(xhr) {
                       var result = xhr.responseJSON;
                       appState.goBack("main");
                       alerts.show({title: result.title,
                                    message: result.message});
                   }).fail(function(xhr) {
                       self.showFormErrors(xhr.responseJSON.errors);
                   });

                   e.preventDefault();
                   return false;
               }
           });
       });
