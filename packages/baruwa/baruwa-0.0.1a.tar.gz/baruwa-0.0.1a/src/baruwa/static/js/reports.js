
function update_counters(data){
    $("#msgcount").html(data.count);
    $("#newestmsg").html(data.newest);
    $("#oldestmsg").html(data.oldest);
}

function build_active_filters(active_filters){
    var i = active_filters.length;
    i--;
    rows = [];
    count = 0;
    $.each(active_filters,function(itr,filter){
        if(itr == i){
            var row = '<tr class="last">';
        }else{
            var row = '<tr>';
        }
        row += '<td class="first-t filters" colspan="2">[ <a href="/reports/fd/'+itr+'/">x</a> ]';
        row += ' [ <a href="/reports/fs/'+itr+'/">Save</a> ] '+filter.filter_field+' '+filter.filter_by+' '+filter.filter_value+'</td></tr>';
        rows[count++] = row;
    });
    if(rows.length){
        $("#afilters tbody").empty().append(rows.join(''));
    }else{
        $("#afilters tbody").empty().append('<tr class="last"><td class="first-t filters" colspan="2">No active filters at the moment</td></tr>');
    }
    $("#afilters tbody tr a").bind('click',ajaxify_active_filter_links);
}

function build_saved_filters(saved_filters){
    var i = saved_filters.length;
    i--;
    rows = [];
    count = 0;
    $.each(saved_filters,function(itr,filter){
        if(itr == i){
            var row = '<tr class="last">';
        }else{
            var row = '<tr>';
        }
        row += '<td class="first-t filters" colspan="2">[ <a href="/reports/sfd/'+filter.filter_id+'/">x</a> ]';
        if(!filter.is_loaded){
            row += ' [ <a href="/reports/sfl/'+filter.filter_id+'/">Load</a> ] ';
        }else{
            row += ' [ Load ] ';
        }
        row += filter.filter_name+'</td></tr>';
        rows[count++] = row;
    });
    if(rows.length){
        $("#sfilters tbody").empty().append(rows.join(''));
    }else{
        $("#sfilters tbody").empty().append('<tr class="last"><td class="first-t filters" colspan="2">No saved filters at the moment</td></tr>');
    }
    $("#sfilters tbody tr a").bind('click',ajaxify_active_filter_links);
}

function build_page(response){
    if(response.success == 'True'){
        update_counters(response.data);
        build_active_filters(response.active_filters);
        build_saved_filters(response.saved_filters);
    }else{
        $("#filter-form-errors td").addClass('filter_errors');
        $("#filter-form-errors td").html(response.errors);
        $("#filter-form-errors").fadeIn(50).delay(15000).slideToggle('fast');
        window.scroll(0,500);
    }
    $("#filter_form_submit").removeAttr('disabled').attr('value','Add');;
}

function build_elements(response){
    if(response.success == "True"){
        if(response.active_filters){
            var i = response.active_filters.length;
            i--;
            if(i > 0){
                $("#afilters tbody tr:last").removeClass('last');
                n = response.active_filters[i];
                var row = '<tr class="last whitelisted"><td class="first-t filters" colspan="2">[ <a href="/reports/fd/'+i+'/">x</a> ]';
                row += ' [ <a href="/reports/fs/'+i+'/">Save</a> ] '+n.filter_field+' '+n.filter_by+' '+n.filter_value+'</td></tr>';
                $("#afilters tbody").append(row);
                setTimeout(function(){$('#afilters tbody tr:last').removeClass('whitelisted');},15000);
                $("form")[0].reset();
            }else{
                n = response.active_filters[0];
                if(n){
                    var row = '<tr class="last"><td class="first-t filters" colspan="2">[ <a href="/reports/fd/'+i+'/">x</a> ]';
                    row += ' [ <a href="/reports/fs/'+i+'/">Save</a> ] '+n.filter_field+' '+n.filter_by+' '+n.filter_value+'</td></tr>';
                    $("#afilters tbody").empty().append(row);
                }else{
                    var row = '<tr class="last"><td class="first-t filters" colspan="2">No active filters at the moment</td></tr>';
                    $("#afilters tbody").empty().append(row);
                }
            }
            $("#afilters tbody tr a").bind('click',ajaxify_active_filter_links);
        }
        if(response.saved_filters){
            build_saved_filters(response.saved_filters);
        }
        update_counters(response.data);
        $("#filter-form-errors").hide();
    }else{
        $("#filter-form-errors td").addClass('filter_errors');
        $("#filter-form-errors td").html(response.errors);
        $("#filter-form-errors").fadeIn(50).delay(15000).slideToggle('fast');
    }
    $("#filter_form_submit").removeAttr('disabled').attr('value','Add');
}

function ajaxify_active_filter_links(e){
    e.preventDefault();
    $("#filter_form_submit").attr({'disabled':'disabled','value':'Loading'});
    window.scroll(0,0);
    //$.ajaxSetup({'cache':false});
    $.get($(this).attr('href'),build_page,'json');
}

function addFilter(){
    $("#filter_form_submit").attr({'disabled':'disabled','value':'Loading'});
    $("#filter-form-errors td").empty();
    $("#filter-form-errors td").removeClass('filter_errors');
    $("#filter-form-errors td").html($("<img/>").attr("src","/static/imgs/loader-orig.gif")).append('&nbsp;Processing........')
    $("#filter-form-errors").show();
    var add_filter_request = {
        filtered_field: $("#id_filtered_field").val(),
        filtered_by: $("#id_filtered_by").val(),
        filtered_value: $("#id_filtered_value").val()
    };
    $.post("/reports/",add_filter_request,build_elements,"json");
    return false;
}

$(document).ready(function(){
bool_fields = ["archive","isspam","ishighspam","issaspam","isrblspam","spamwhitelisted","spamblacklisted","virusinfected","nameinfected","otherinfected","ismcp","ishighmcp","issamcp","mcpwhitelisted","mcpblacklisted","quarantined"];
num_fields = ["size","sascore","mcpscore"];
text_fields = ["id","from_address","from_domain","to_address","to_domain","subject","clientip","spamreport","mcpreport","headers"];
time_fields = ["date","time"];
num_values = [{'value':1,'opt':'is equal to'},{'value':2,'opt':'is not equal to'},{'value':3,'opt':'is greater than'},{'value':4,'opt':'is less than'}];
text_values = [{'value':1,'opt':'is equal to'},{'value':2,'opt':'is not equal to'},{'value':9,'opt':'is null'},{'value':10,'opt':'is not null'},{'value':5,'opt':'contains'},{'value':6,'opt':'does not contain'},{'value':7,'opt':'matches regex'},{'value':8,'opt':'does not match regex'}];
time_values = [{'value':1,'opt':'is equal to'},{'value':2,'opt':'is not equal to'},{'value':3,'opt':'is greater than'},{'value':4,'opt':'is less than'}];
bool_values = [{'value':11,'opt':'is true'},{'value':12,'opt':'is false'}];
$('#id_filtered_field').prepend('<option value="0" selected="0">Please select</option>');
$('#id_filtered_value').attr({'disabled':'disabled'});
$('#id_filtered_field').bind('change',function(){
    if($.inArray($(this).val(),bool_fields) != -1){
        $('#id_filtered_by').empty();
        $.each(bool_values,function(i,n){
            $('#id_filtered_by').append($("<option/>").attr({value:n.value,innerHTML:n.opt}));
        });
        $('#id_filtered_value').attr({'disabled':'disabled'}).val("");
    }
    if($.inArray($(this).val(),num_fields) != -1){
        $('#id_filtered_by').empty();
        $.each(num_values,function(i,n){
            $('#id_filtered_by').append($("<option/>").attr({value:n.value,innerHTML:n.opt}));
        });
        $('#id_filtered_value').removeAttr("disabled").val("");
    }
    if($.inArray($(this).val(),text_fields) != -1){
        $('#id_filtered_by').empty();
        $.each(text_values,function(i,n){
            $('#id_filtered_by').append($("<option/>").attr({value:n.value,innerHTML:n.opt}));
        });
        $('#id_filtered_value').removeAttr("disabled").val("");
    }
    if($.inArray($(this).val(),time_fields) != -1){
        $('#id_filtered_by').empty();
        $.each(time_values,function(i,n){
            $('#id_filtered_by').append($("<option/>").attr({value:n.value,innerHTML:n.opt}));
        });
        $('#id_filtered_value').removeAttr("disabled").val("");
    }
});
$("#filter-form").submit(addFilter);
$("#my-spinner").ajaxStart(function(){$(this).empty().append($("<img/>").attr('src','/static/imgs/loader-orig.gif')).append('&nbsp;Processing...');})
    .ajaxError(function(event, request, settings){
        if(request.status == 200){
            location.href=settings.url;
        }else{
            $(this).empty().append($("<span/>").addClass('ajax_error')).append('&nbsp;Error occured');
        }
    }).ajaxStop(function(){$(this).empty();});
$("#afilters tbody tr a").bind('click',ajaxify_active_filter_links);
$("#sfilters tbody tr a").bind('click',ajaxify_active_filter_links);

});
