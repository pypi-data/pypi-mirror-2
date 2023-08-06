function region_append(region, obj, modname) {
    var wrp = [];
    wrp.push('<fieldset class="module aligned order-item">');
    wrp.push('<h2><img class="item-delete" src="'+IMG_DELETELINK_PATH+'" /><span class="handle">'+modname+'</span></h2>');
    wrp.push('<div class="item-content"></div>');
    wrp.push('</fieldset>');

    $("#"+REGIONS[region]+"_body").children("div.order-machine").append(wrp.join(""))
        .children("fieldset.order-item:last").children(".item-content").append(obj);
}

function create_new_spare_form(form, modvar, last_id) {
    // create new spare form
    var new_form = form.html().replace(
        new RegExp(modvar+'-'+last_id, 'g'),
        modvar+'-'+(last_id+1));
    new_form = '<div id="'+modvar+'_set_item_'+(last_id+1)+'">'+new_form+'</div>';
    $("#"+modvar+"_set").append(new_form);
}

function set_item_field_value(item, field, value) {
    // item: DOM object created by 'region_append' function
    // field: "order-field" | "delete-field" | "region-choice-field"
    if (field=="delete-field")
        item.find("."+field).attr("checked",value);
    else if (field=="region-choice-field") {
        var old_region_id = REGION_MAP.indexOf(item.find("."+field).val());
        item.find("."+field).val(REGION_MAP[value]);

        old_region_item = $("#"+REGIONS[old_region_id]+"_body");
        if (old_region_item.children("div.order-machine").children().length == 0)
            old_region_item.children("div.empty-machine-msg").show();
        else
            old_region_item.children("div.empty-machine-msg").hide();

        new_region_item = $("#"+REGIONS[value]+"_body");
        new_region_item.children("div.empty-machine-msg").hide();
    }
    else
        item.find("."+field).val(value);
}

function move_item (region_id, item) {
    poorify_rich(item);
    $("#"+REGIONS[region_id]+"_body").children("div.order-machine").append(item);
    set_item_field_value(item, "region-choice-field", region_id);
    richify_poor(item);
}

function poorify_rich(item){
    item.children(".item-content").hide();
    if (item.find("div[id^=richtext]").length > 0) {
        var editor_id = item.find(".mceEditor").prev().attr("id");
        tinyMCE.execCommand('mceRemoveControl', false, editor_id);
    }
}
function richify_poor(item){
    item.children(".item-content").show();
    if (item.find("div[id^=richtext]").length > 0) {
        var editor_id = item.find('textarea[name*=richtext]:visible').attr("id");
        tinyMCE.execCommand('mceAddControl', false, editor_id);
    }
}

function zucht_und_ordnung(move_item) {
    for (var i=0; i<REGIONS.length;i++) {
        var container = $("#"+REGIONS[i]+"_body div.order-machine");
        for (var j=0; j<container.children().length; j++) {
            if (move_item)
                container.find("input.order-field[value="+j+"]").parents("fieldset.order-item").appendTo(container);
            else
                set_item_field_value(container.find("fieldset.order-item:eq("+j+")"), "order-field", j);
        }
    }
}

function attach_dragdrop_handlers() {
    // hide content on drag n drop
    $("#main h2.handle").mousedown(function(){
        poorify_rich($(this).parents("fieldset.order-item"));
    });
    $("#main h2.handle").mouseup(function(){
        richify_poor($(this).parents("fieldset.order-item"));
    });
}
