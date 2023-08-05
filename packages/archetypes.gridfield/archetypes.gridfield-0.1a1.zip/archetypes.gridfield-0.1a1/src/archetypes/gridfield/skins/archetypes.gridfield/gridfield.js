jq(function(){
    jq("a.remove-record").click(function() {
        if (confirm('Do you really want to remove this record?')) {
            $self = jq(this);
            var $widget = $self.parents('.field');
            var url = $self.attr('href');
            jq.get(url, function() {
               var field_url = url.replace(/(.*?)\/(add|edit|delete).*/g, "$1");
               $widget.load(field_url + '/ajax_render');
            });
        }
       return false;
    });

    jq("a.edit-record").prepOverlay({
       subtype:'ajax',
       urlmatch:'$', urlreplace:'',
       formselector:'form',
       noform: 'close',
       closeselector:'[name=form.buttons.cancel]',
       afterpost: function(data, data_parent) {
           var $widget = data_parent.data('source').parents('.field');
           var url = data_parent.data('target');
           var field_url = url.replace(/(.*?)\/(add|edit|delete).*/g, "$1");
           $widget.load(field_url + '/ajax_render');
       }
    });
    jq("a.add-record").prepOverlay({
       subtype:'ajax',
       urlmatch:'$', urlreplace:'',
       formselector:'form',
       noform: 'close',
       closeselector:'[name=form.buttons.cancel]',
       afterpost: function(data, data_parent) {
           var $widget = data_parent.data('source').parents('.field');
           var url = data_parent.data('target');
           var field_url = url.replace(/(.*?)\/(add|edit|delete).*/g, "$1");
           $widget.empty();
           $widget.load(field_url + '/ajax_render');
       }
   });
});