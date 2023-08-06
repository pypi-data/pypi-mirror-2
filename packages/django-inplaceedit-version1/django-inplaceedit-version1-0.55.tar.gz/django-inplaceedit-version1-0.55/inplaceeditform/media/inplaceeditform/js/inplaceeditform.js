
function inplaceeditform_ready(form_prefix, field_name, obj_id, content_type_id, form, filters){

    jQuery('#view_'+form_prefix+'-'+field_name+'').bind("mouseenter",function(){
      jQuery(this).addClass("chunk_over");
    }).bind("mouseleave",function(){
      jQuery(this).removeClass("chunk_over");
    });

    jQuery('#view_'+form_prefix+'-'+field_name+'').dblclick(function (){
        jQuery('span#view_'+form_prefix+'-'+field_name+'_save').fadeOut();
        document.getElementById('view_'+form_prefix+'-'+field_name+'').style.display = 'none';
        document.getElementById('tools_'+form_prefix+'-'+field_name+'').style.display = 'block';
        var tools_error = document.getElementById('tools_'+form_prefix+'-'+field_name+'_error');
        var child_nodes = tools_error.childNodes;
        for (i=0; i<child_nodes.length; i++)
        {
            tools_error.removeChild(child_nodes[i]);
        }
    });

    jQuery('#tools_'+form_prefix+'-'+field_name+'_cancel_id').click(function (){
        jQuery('span#view_'+form_prefix+'-'+field_name+'_save').fadeOut();
        document.getElementById('tools_'+form_prefix+'-'+field_name+'').style.display = 'none';
        document.getElementById('view_'+form_prefix+'-'+field_name+'').style.display = 'block';
    });

    jQuery('#tools_'+form_prefix+'-'+field_name+'_apply_id').click(function (){


        var value_input = jQuery('#id_'+form_prefix+'-'+field_name+'');

        var value_input = jQuery('#id_'+form_prefix+'-'+field_name+'')[0];
        var value;

        if (value_input.multiple)
        {
            var options_selected = jQuery('#id_'+form_prefix+'-'+field_name+' option:selected');
            value = [];
            for( i =0; i< options_selected.length; i++)
            {
                value[i] = options_selected[i].value;
            }
        }
        else{
            value = value_input.value;
        }
        var form_query = '';
        if (form)
        {
            form_query = '&form='+form;
        }
        var data = 'id='+obj_id+'&field='+field_name+'&value='+encodeURIComponent(jQuery.toJSON(value))+'&content_type_id='+content_type_id+form_query+'&'+'filters='+jQuery.toJSON(filters);
        jQuery.ajax({
        data: data,
        url: "/inplaceeditform/",
        type: "POST",
        async:true,
        success: function(response){

            response = eval("("+ response +")");
            if (response.errors)
            {
                var tools_error = jQuery('#tools_'+form_prefix+'-'+field_name+'_error')[0];
                var child_nodes = tools_error.childNodes;
                for (i=0; i<child_nodes.length; i++)
                {
                    tools_error.removeChild(child_nodes[i]);
                }
                var ul = document.createElement('ul');
                ul.className = "errors";
                jQuery('#tools_'+form_prefix+'-'+field_name+'_error')[0].appendChild(ul);
                for (var error in response)
                {
                    if (error != 'errors')
                    {
                        var li = document.createElement('li');
                        if ("'+field_name+'" == error)
                            li.innerHTML = response[error];
                        else
                            li.innerHTML = error+ ": " +response[error];
                        ul.appendChild(li);
                    }
                }
            }
            else
            {
                jQuery('#tools_'+form_prefix+'-'+field_name+'')[0].style.display = 'none';
                jQuery('#view_'+form_prefix+'-'+field_name+'')[0].style.display = 'block';
                jQuery('#view_'+form_prefix+'-'+field_name+'_id')[0].innerHTML = response.value;
                jQuery('div#view_'+form_prefix+'-'+field_name+'_save').fadeIn();
                window.setTimeout("jQuery('div#view_"+form_prefix+"-"+field_name+"_save').fadeOut()", 2000);
            }
        }
    });
  });
}
