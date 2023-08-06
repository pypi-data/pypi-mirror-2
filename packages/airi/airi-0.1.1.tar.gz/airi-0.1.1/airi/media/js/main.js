var layout;
var tools;
var current;

function getBrowser(){
  	return navigator.appVersion+'-'+navigator.appName;
}

function createIconText(text, icon, id){
  return $._div({
    'class': 'ui-state-highlight ui-corner-all',
    'id': id,
    })
    ._p()
      ._span_({
        "class": "ui-icon " + icon, 
        "style":"float: left; margin-right: .3em;"
      })
      ._span_()
        .text(text)
    .p_()
  .div_()
}

function prepareMjpeg(){
  $("#video").empty()

  createIconText("You're running Chrome you will not get Audio", "ui-icon-info", "chrome-warning").appendTo("#video")

  $._div({'id': 'resizable', 'class': 'ui-widget-content'})
    .div_().appendTo("#video")

}

function prepareSWF(){
  $("#video").empty()

  $._div_({'id': 'resizable'}).appendTo("#video");
}

function prepareStream(){
  if (getBrowser().toLowerCase().indexOf("chrome")>-1)
    prepareMjpeg();
  else
    prepareSWF();
}


function enableMjpeg(address){
  $("#resizzable").empty()
  $._embed_({
    "id": "video-content", 
    "class": "wrapper",
    "width": "100%",
    "height": "100%",
    "src": "/stream/"+address.replace(/:/g, "_")
  }).appendTo("#video")
}

function enableSWF(address){
  $("#resizable").empty()
  $._p()
    ._a_({'href': 'http://www.adobe.com/go/getflashplayer'})
      ._img_({
        'src': 'http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif',
        'alt': 'Get Adobe Flash player'
      })
  .p_().appendTo("#resizable")

  $("#resizable").flash({
    swf: "/media/airi.swf",
    style: "width: 100%; height: 100%",
    flashvars : {
      browser: getBrowser(),
      target: address.replace(/:/g, "_"),
    },
	play: "true",
	id: "video-content",
	class: "wrapper"
  })

  $( "#resizable" ).resizable( {
    aspectRatio: 4/3,
    minWidth: 160,
    minHeight: 140
  });
}

function enableStream(address){
  if (getBrowser().toLowerCase().indexOf("chrome")>-1)
    enableMjpeg(address);
  else
    enableSWF(address);
}

function connect(target){
  current = target.data['address'];
  enableStream(target.data['address']);
  tools.accordion("activate", $("#o_current"));
}

function generateMenuButton(id, text){
  return $._button({
    'id': id,
    'class': 'control-button ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only',
  })._span_({'class': 'ui-button-text'})
      .text(text)
        .button_()
}

function createLoading(text){
  return $._p({
    class: 'loading control-info',
    style: 'height: 3.5em !important; border: 0px;'
  })
    .text(text)
    ._img_({'src': 'media/images/loading.gif', 'class': 'loading'})
    .p_()
}

function updateRemoteDevices(){
  $(".loading").remove()
  $(".remote_devices_dynamic").remove()

  createLoading("Scanning please wait...").appendTo("#remote_devices")
  updateControl()

  $.ajax({
    url: "/api/devices/",
    datatype: 'json',
    error: function(jqXHR, textStatus, errorThrown){
      $(".loading").remove()
      $(jqXHR.responseText).addClass("remote_devices_dynamic").appendTo("#remote_devices")

    },
    success: function(data, textStatus){
      var item;
      $(".loading").remove()
      $(".remote_devices_dynamic").remove()
      if (data.length > 0){
        $.each(data, function(key, val) {
          item = $._button_({
            id: 'connect_'+val['address'].replace(/:/g, ""),
            class: 'control-target control-button remote_devices_dynamic'
          }).text(val["address"]+"\n"+val["name"])
          item.button({icons: {primary: 'ui-icon-circle-arrow-e'}})
          item.click({'address':val["address"]}, connect);
          item.appendTo('#remote_devices')
        });
      }
      else {
        item=$._p_({class: 'control-error remote_devices_dynamic ui-state-highlight'}).text("No devices Found");
        item.appendTo("#remote_devices")
        updateControl();
      }
    }})
}

function addIcon(type, state, parent, position){
  icon="ui-icon ui-airi-icon"
  if (state)
    icon +=" ui-airi-"+type
  else
    icon +=" ui-airi-no"+type
  $._span_({'class': icon, "style": "left: "+(20+position*11)+"px;"}).prependTo("#"+parent);
}

function countConnected(success, error){
  $.ajax({
    url: "/api/connected/",
    datatype: 'json',
    error: function(jqXHR, textStatus, errorThrown){
      if (error != null)
      error(jqXHR, textStatus, errorThrown);
    },
    success: function(data, textStatus){
      var i = 0;
      var address=[];
      var name;
      for (name in data){
        address[i]=name;
        i++;
      }
      if (success != null)
        success(i, address, data);
    }})
}


function updateConnectedDevices(){
  $(".loading").remove()
  $(".connected_devices_dynamic").remove()

  createLoading("Loading please wait...").appendTo("#connected_devices")
  updateControl()

  $.ajax({
    url: "/api/connected/",
    datatype: 'json',
    error: function(jqXHR, textStatus, errorThrown){
      $(".loading").remove()
      $(jqXHR.responseText).addClass("connected_device_dynamic").appendTo("#connected_devices")

    },
    success: function(data, textStatus){
      var item;
      var icons;
      var i = 0;
      $(".loading").remove()
      var data_=$(data);
      while (data_[i]!=null)
        i++;
      if (i > 0){
        $.each(data, function(key, val) {
          id='switch_'+key.replace(/:/g, "")
          item = $._button_({
            id: id,
            class: 'control-target control-button connected_devices_dynamic'
          }).text(key+"\n"+val["name"])
          item.button({icons:{"primary": "ui-icon-signal-diag"}})
          item.click({'address':key}, connect);
          item.appendTo('#connected_devices')

          addIcon("pan", val['capabilities']['pan'], id, 0);
          addIcon("zoom", val['capabilities']['zoom'], id, 1);
          addIcon("flash", val['capabilities']['flash'], id, 2);
          addIcon("sco", val['capabilities']['voice'], id, 3);
        });
      } else {
        createIconText("No devices connected", "ui-icon-circle-close", "not-connected").appendTo("#connected_devices")
      }
    }})
}

function automaticSelectConnected(count, address, data){
  if (count == 0)
    return tools.accordion("activate", $("#o_devices"));
  current=(address[count-1]);
  enableStream(current);
  tools.accordion("activate", $("#o_current"));
}

function updateCurrentDevice(){
  if (current == null){
    return countConnected(automaticSelectConnected);
  }

  $(".loading").remove()
  $("#current_device_").hide()

  createLoading("Loading please wait...").appendTo("#current_device")
  updateControl()

  $.ajax({
    url: "/api/connected/"+current.replace(/:/g, "_"),
    datatype: 'json',
    error: function(jqXHR, textStatus, errorThrown){
      $(".loading").remove()
      $(jqXHR.responseText).addClass("current_device_dynamic").appendTo("#current_device")

    },
    success: function(data, textStatus){
        $(".loading").remove()
        $.each(['address', 'name', 'transport'], function(index, value) 
          {
            $("#current_device_"+value).text(data[value])
          }
        )

        $("#current_device_").show()
        $("#current_device_ .information").show()
      }
    }
  )
}

function tool_choosen(event, ui){
  var clicked = $(this).find('.ui-state-active').attr('id');

  if (clicked == 'o_remote'){
    if ($(".remote_devices_dynamic").length==0)
      updateRemoteDevices();
  } else if (clicked == 'o_connected'){
    updateConnectedDevices();
  } else if (clicked == 'o_current'){
    updateCurrentDevice();
  }
}

function updateControl(){
  $(".control-info").button({
    icons: { primary: "ui-icon-info" },
  }).unbind();
  $(".control-info-disabled").button({
    disabled:true,
    icons: { primary: "ui-icon-info" },
  }).unbind();

  $(".control-error").button({
    icons: { primary: "ui-icon-circle-close" },
  }).unbind();
}


function init(){
  prepareStream();
  layout = $('body').layout({
    north__spacing_open: 0,
    center__spacing_open: 0,
    east: {
      resizable: false,
      size: "30% important",
      paneClass: "pane",
      resizerClass: "resizer",
      togglerClass: "toggler",
      buttonClass: "button",
      contentSelector: ".ui-widget-content",
      contentIgnoreSelector: "span",
      spacing_open: "30% !important",
      spacing_closed: 22,
      togglerLength_closed: 21,
      togglerLength_open: 21,
      hideTogglerOnSlide: true,
      togglerAlign_closed: "top",
      tooglerTip_open: "Hide Controls",
      tooglerTip_closed: "Show Controls",
      slideTrigger_open: "click",
      initClosed: true,
      fxName: "slide",
      fxSpeed: "normal",
      fxSpeed_open: 750,
      fxSpeed_close: 1500,
      fxSettings_open: { easing: "easeInQuint" },
      fxSettings_close: { easing: "easeOutQuint" },
      onopen_start: function() {
        $("#controls").css({"width":screen.width*.3});
      },
    },
    south__spacing_open: 0,
  });
  
  var eastSelector = ".ui-layout-east";
  $("<span></span>").attr("id", "east-closer").prependTo(eastSelector);
  layout.addCloseBtn("#east-closer", "east");
  
  tools = $('#tools').accordion({
    active: false,
    event: "click",
    fillSpace: true,
    clearStyle: false,
    autoHeight: false,
    collapsible: true,
    header: 'h3',
    animated: "easeslide",
    change: tool_choosen,
  });

  updateControl()
  $("#do_scan").button({
    icons: { primary: "ui-icon-search" },
    disabled: false
  })
  $("#do_scan").click(updateRemoteDevices);
  updateCurrentDevice();
}

$(document).ready(init);
