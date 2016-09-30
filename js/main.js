$(document).ready(function(){

App.RootView = Backbone.View.extend({
      template: $("#bodytemplate").html(),
      
      initialize: function(options){
					var self = this;
          this.el = options.el
        },
  
      render: function(){
          //http://coenraets.org/blog/2011/12/tutorial-html-templates-with-mustache-js/
          //$("#main-container").html(Mustache.to_html(this.template));
          this.$el.html(Mustache.to_html(this.template));
          self.$('.dropdown-button').dropdown({
									inDuration: 300,
									outDuration: 225,
									constrain_width: false, // Does not change width of dropdown to that of the activator
									hover: true, // Activate on hover
									gutter: 0, // Spacing from edge
									belowOrigin: false, // Displays dropdown below the button
									alignment: 'left' // Displays dropdown with edge aligned to the left of button
    																		});
     
          return this; 
	      },  

			events: {
          'click .textsubmit': 'textSubmit',
						},
			
      textSubmit: function(e){
            e.preventDefault();
            console.log("Jhandu balm");
						var text = $(".textProcessing").val();

						var jqhr = $.post(window.URL, {"text": text})
						jqhr.done(function(data){
									if (data.success == true){
													var subView = new App.IntermediatePerSentenceView({"model": data.result})
                                  self.$("#sentences").html(subView.render().el);
                          //var subView = new App.PerSentenceView({model: {"result": data.result, "sentence": sentence, "grams": grams, parent: self}});
													//self.$el.after(subView.render().el);
                   }
                  else {
											Materialize.toast(data.message, 4000, 'rounded')  
                      }
                })

						jqhr.fail(function(){
									Materialize.toast('Either the api or internet connection is not working, Sorry, Please try again later', 4000, 'rounded')  
                        })
        },
      
      
       
      
      


});

App.IntermediatePerSentenceView = Backbone.View.extend({
        tagName: "ul",
        className: "collection", 
        initialize: function(options){
              this.model = options.model
        
        }, 

        render: function(){
              var self = this;
              $.each(this.model, function(index, result_object){
										var subView = new App.PerSentenceView({model: result_object});
                    self.$el.append(subView.render().el)            
              })
              return this;
        },

});
App.PerSentenceView = Backbone.View.extend({
        tagName: "li",
        className: "collection-item", 
        template: $("#perSentenceTemplate").html(),
        initialize: function(options){
              this.model = options.model
              console.log(this.model.sentence); 
        
        }, 

        render: function(){
              var self = this;
              this.$el.html(Mustache.to_html(this.template, self.model));
              return this;
        },

});






});
