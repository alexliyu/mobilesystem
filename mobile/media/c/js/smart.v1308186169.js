var current_url=window.location.pathname+window.location.search;history.navigationMode='compatible';function to_absolute(url){url=url.split('#')[0]
if(url.match(/https?\:\/\//)){return url;}else if(url.substr(0,1)=="/"){return window.location.protocol+'//'+window.location.host+url;}else if(url.indexOf('?')!=-1){if(current_url.lastIndexOf('?')!=-1){return current_url.substring(0,current_url.lastIndexOf('?'))+url;}
return current_url+url;}else{return current_url+url;}}
function display_loading_screen(){$('body').append('<div id="loading"></div>')
$('#loading').height($('html').height())
display_spinner()}
function display_spinner(){offset=window.innerHeight/2
if(navigator.userAgent.match(/iPhone/i)||navigator.userAgent.match(/iPod/i)||navigator.userAgent.match(/iPad/i)){offset+=window.pageYOffset}
$('#loading').css('background-position','50% '+offset+'px')}
$(window).scroll(display_spinner)
function clear_loading_screen(){$('#loading').remove();}
function async_load_callback(data,textStatus,xhr){$('body').html(data.body);$('title').html(data.title);$(document).trigger('molly-page-change',[current_url])
capture_outbound();}
function ajax_failure(){$('#loading').html('<p style="position:fixed; top: 10%; width:100%; margin:0 auto; text-align:center;">Error loading page - please try again.</p>').css({'font-size':'20px','font-weight':'bold'}).fadeTo('fast',0.9,function(){setTimeout(function(){clear_loading_screen();},1200);});}
function async_load(url,query,meth){if(to_absolute(url).substr(0,base.length)!=base){return true;}
display_loading_screen()
query['format']='fragment';$.ajax({'url':to_absolute(url),'data':query,'type':meth,'dataType':'json','success':function(data,textStatus,xhr){if(data.redirect){window.location=data.redirect;return true;}
current_url=data.uri;if(!!(window.history&&history.pushState)){history.pushState(null,null,to_absolute(current_url))}else{already_doing_hash_reload=false;window.location.hash=current_url;}
return async_load_callback(data,textStatus,xhr);},'error':ajax_failure});return false;}
function capture_outbound(){$('form:not(.has-ajax-handler)').unbind('submit')
$('form:not(.has-ajax-handler)').submit(function(evt){var serial=$(this).serializeArray();var datamap={}
var i=0;for(i=0;i<serial.length;i++){datamap[serial[i].name]=serial[i].value;}
return async_load($(this).attr('action'),datamap,$(this).attr('method'));});$('form:not(.has-ajax-handler) button[type="submit"]').click(function(e){var form=$(this).parents('form');$(form).find('input[type="hidden"][name="'+$(this).attr('name')+'"]').remove()
$(form).append('<input type="hidden" name="'+$(this).attr('name')+'" value="'+$(this).attr('value')+'" />')
return true;})
$('a[href]:not(.has-ajax-handler)').unbind('click')
$('a[href]:not(.has-ajax-handler)').click(function(evt){return async_load($(this).attr('href'),{},'GET');});}
$(window).load(function(){already_doing_hash_reload=false;function check_hash_change(){var pathpart=window.location.href.split('#');if(pathpart.length==1){pathpart='';}else{pathpart=pathpart[1]}
if(!already_doing_hash_reload&&(window.location.hash&&pathpart!=current_url)){already_doing_hash_reload=true;async_load(window.location.hash.substr(1),{},"GET");}
if(!already_doing_hash_reload&&(!window.location.hash&&current_url!=window.location.pathname+window.location.search)){already_doing_hash_reload=true;async_load(window.location.pathname+window.location.search,{},"GET");}
if(!!!(window.history&&history.pushState)){setTimeout(check_hash_change,100);}}
check_hash_change();$(document).trigger('molly-page-change',[current_url])
capture_outbound();if(!!(window.history&&history.pushState)){window.addEventListener('popstate',function(e,state){if(current_url!=window.location.pathname+window.location.search){async_load(window.location.href,{},'GET');}},false)}});function capfirst(s){return s.substr(0,1).toUpperCase()+s.substr(1)}
entitydetail_ajax_refresh=null;$(document).bind('molly-page-change',function(event,url){clearTimeout(entitydetail_ajax_refresh)
if(url=='/places/'){$('.nearby a').click(function(){display_loading_screen()
$.ajax({url:$(this).attr('href'),data:{format:'json'},dataType:'json',success:function(data){parse_results(data,true);clear_loading_screen();},error:ajax_failure})
return false;})
$('.nearby a').addClass('has-ajax-handler')
$('.categories a').click(function(){display_loading_screen()
$.ajax({url:$(this).attr('href'),data:{format:'json'},dataType:'json',success:function(data){parse_results(data,false);clear_loading_screen();},error:ajax_failure})
return false;})
$('.categories a').addClass('has-ajax-handler')}
if(url.match(/^\/places\/category\/[^\/;]/)){$('li.next a').click(function(){display_loading_screen()
$.ajax({url:$(this).attr('href'),data:{format:'json'},dataType:'json',success:function(data){$('.current-page').html(data.entities.number)
if(data.entities.has_next){$('li.next a').attr('href','?page='+(data.entities.number+1).toString(10))}else{$('li.next').remove()
$('.section-content').removeClass('no-round-bottom')}
for(i in data.entities.objects){item=data.entities.objects[i]
$('#category-list').append('<li><a href="'+item._url+'">'+
item.title+'</a></li>')
if(i==0){$('#category-list li:last').addClass('page-break')}}
clear_loading_screen()},error:ajax_failure})
return false;})
$('li.next a').addClass('has-ajax-handler')}
if(url.match(/^\/places\/[a-z_\-]+:[\da-zA-Z]+\/$/)){entitydetail_ajax_refresh=setTimeout(function(){$.ajax({url:to_absolute(current_url),data:{format:'json'},dataType:'json',success:refreshRTI})},30000)
$('.nearby a').click(function(){display_loading_screen()
$.ajax({url:$(this).attr('href'),data:{format:'json'},dataType:'json',success:function(data){parse_results(data,true);clear_loading_screen();},error:ajax_failure})
return false;})
$('.nearby a').addClass('has-ajax-handler')
setupLDBButtons();}});function parse_results(data,nearby){$('.category-list').remove()
for(category in data.entity_types){$('#poi-category-selector').append('<div class="header"><h2>'+category+'</h2></div>'+'<ul class="link-list"></ul>')
for(j in data.entity_types[category]){entity_type=data.entity_types[category][j]
if(nearby){$('#poi-category-selector ul:last').append('<li><a href="'+current_url+'nearby/'+entity_type.slug+'/">'+
capfirst(entity_type.verbose_name_plural)+' <small>('+entity_type.entities_found+' within '+Math.ceil(entity_type.max_distance/10)*10+'m)</small>'+'</a></li>')}else{$('#poi-category-selector ul:last').append('<li><a href="'+current_url+'category/'+entity_type.slug+'/">'+
capfirst(entity_type.verbose_name_plural)+'</a></li>')}}}
$('#poi-category-selector ul').addClass('no-round-bottom')
$('#poi-category-selector ul:last').removeClass('no-round-bottom')
capture_outbound();}
function getTimestamp(date){function pad2(number){return(number<10?'0':'')+number}
return pad2(date.getHours())+':'+pad2(date.getMinutes())+':'+pad2(date.getSeconds())}
function refreshRTI(data){var now=new Date();$('.update-time').html(getTimestamp(now))
if(typeof(data.entity.metadata.real_time_information)!='undefined'){rebuildRTI($('#'+data.entity.identifier_scheme+'-'+data.entity.identifier_value),data.entity.metadata.real_time_information)}
if(typeof(data.entity.metadata.ldb)!='undefined'){rebuildLDB($('#'+data.entity.identifier_scheme+'-'+data.entity.identifier_value),data)}
for(var i in data.entity.associations){for(var j in data.entity.associations[i].entities){var entity=data.entity.associations[i].entities[j]
if(typeof(entity.metadata.real_time_information)!='undefined'){rebuildRTI($('#'+entity.identifier),entity.metadata.real_time_information)}}}
if(data.entity.metadata.meta_refresh){entitydetail_ajax_refresh=setTimeout(function(){$.ajax({url:to_absolute(current_url),data:{format:'json',board:board},dataType:'json',success:refreshRTI})},data.entity.metadata.meta_refresh*1000)}}
function rebuildRTI(elem,metadata){elem.empty()
if((typeof(metadata.pip_info)!='undefined'&&metadata.pip_info.length>0)||metadata.services.length==0){elem.append('<ul class="content-list no-round-bottom"></ul>')
if(metadata.pip_info.length>0){elem.find('ul').append('<li></li>')
var li=elem.find('li')
for(var i in metadata.pip_info){if(i>0){li.append('<br/>')}
li.append(metadata.pip_info[i])}}
if(metadata.services.length==0){elem.find('ul').append('<li></li>')
var li=elem.find('li')
li.append('Sorry, there is currently no real time information for this stop.')}}
if(metadata.services.length>0){elem.append('<div class="section-content no-round-bottom"><div class="pad-5"><table class="real-time-information"><tbody id="bus_times"></tbody></table></div></div>')
tbody=elem.find('tbody')
for(var i in metadata.services){var service=metadata.services[i]
tbody.append('<tr>'+'<td rowspan="2" style="font-size:200%; text-align:center;">'+service.service+'</td>'+'<td>'+service.destination+'</td>'+'<td>'+service.next+'</td>'+'</tr><tr class="notopborder"><td colspan="2"><small>Next: </small></td></tr>')
var next=tbody.find('tr:last td small')
if(service.following.length>0){for(var j in service.following){if(j>0){next.append(', ')}
next.append(service.following[j])}}else{next.append('<em>No further info</em>')}}}}
function rebuildLDB(elem,data){elem.empty()
if(data.board){board=data.board}else{board='departures'}
if(data.train_station.metadata.ldb.error){elem.append('<div class="header"><h2>'+data.train_station.title+' ('+board+')</h2></div>');}else{var generated=new Date(Date.UTC(parseInt(data.train_station.metadata.ldb.generatedAt.slice(0,4)),parseInt(data.train_station.metadata.ldb.generatedAt.slice(5,7)),parseInt(data.train_station.metadata.ldb.generatedAt.slice(8,10)),parseInt(data.train_station.metadata.ldb.generatedAt.slice(11,13)),parseInt(data.train_station.metadata.ldb.generatedAt.slice(14,16)),parseInt(data.train_station.metadata.ldb.generatedAt.slice(17,19))))
elem.append('<div class="header"><h2>'+data.train_station.title+' ('+board+') - '+getTimestamp(generated)+'</h2></div>');}
if(data.train_station.metadata.ldb.nrccMessages){elem.append('<ul class="content-list no-round-bottom"></ul>')
ul=elem.find('ul:last')
for(var i in data.train_station.metadata.ldb.nrccMessages.message){ul.append('<li>'+data.train_station.metadata.ldb.nrccMessages.message[i]+'</li>')}}
elem.append('<table class="content no-round-bottom"><thead><tr></tr></thead><tbody></tbody></table>')
tr=elem.find('.content thead tr')
if(board=='arrivals'){tr.append('<th>Origin</th>')}else{tr.append('<th>Destination</th>')}
if(data.train_station.metadata.ldb.platformAvailable){tr.append('<th>Plat.</th>')
cols='4'}else{cols='3'}
tr.append('<th>Scheduled</th><th>Expected</th>')
tbody=elem.find('.content tbody')
if(data.train_station.metadata.ldb.error){tbody.append('<tr><td colspan="'+cols+'"><p>There is currently a problem retrieving live departure information from the National Rail web site.</p>'+'<p>Departure information may still be accessed <a href="http://pda.ojp.nationalrail.co.uk/en/pj/ldbboard/dep/'+data.train_station.identifiers.crs+'"> directly from their web site</a>.</p></td></tr>')}
if(data.train_station.metadata.ldb.trainServices){for(var i in data.train_station.metadata.ldb.trainServices.service){service=data.train_station.metadata.ldb.trainServices.service[i]
tbody.append('<tr></tr>')
tr=tbody.find('tr:last')
dest=''
if(board=='arrivals'){for(var j in service.origin.location){if(j>0&&j<service.origin.location.length-1){dest+=', '}
if(j>0&&j==service.origin.location.length-1){dest+=' &amp; '}
if(j>0){dest+='<br />'}
dest+=service.origin.location[j].locationName
if(service.origin.location[j].via){dest+='<br /><small>'+service.origin.location[j].via+'</small>'
if(j<service.origin.location.length-1){dest+='<br />'}}}}else{for(var j in service.destination.location){if(j>0&&j<service.destination.location.length-1){dest+=', '}
if(j>0&&j==service.destination.location.length-1){dest+=' &amp; '}
if(j>0){dest+='<br />'}
dest+=service.destination.location[j].locationName
if(service.destination.location[j].via){dest+='<br /><small>'+service.destination.location[j].via+'</small>'
if(j<service.destination.location.length-1){dest+='<br />'}}}}
if(service.isCircularRoute){dest+='<br /><small>(Circular Route)</small>'}
tr.append('<td><a href="'+data.train_station._url+'service?id='+encodeURIComponent(service.serviceID)+'" style="color: inherit;" rel="nofollow">'+dest+'</a></td>')
if(data.train_station.metadata.ldb.platformAvailable){if(typeof(service.platform)!='undefined'){tr.append('<td>'+service.platform+'</td>')}else{tr.append('<td>&nbsp;</td>')}}
if(board=='arrivals'){tr.append('<td>'+service.sta+'</td>')
tr.append('<td>'+service.eta+'</td>')}else{tr.append('<td>'+service.std+'</td>')
tr.append('<td>'+service.etd+'</td>')}}
if(data.train_station.metadata.ldb.trainServices.service.length==0){tbody.append('<tr><td colspan="'+cols+'">There are currently no scheduled '+board+'.</td></tr>')}}else{tbody.append('<tr><td colspan="'+cols+'">There are currently no scheduled '+board+'.</td></tr>')}
elem.append('<ul class="link-list"></ul>');ul=elem.find('ul:last')
if(board=='departures'){ul.append('<li><a class="ldb-board" href="'+data.train_station._url+'?board=arrivals">View arrivals board</a></li>')}else{ul.append('<li><a class="ldb-board" href="'+data.train_station._url+'?board=departures">View departures board</a></li>')}
setupLDBButtons()
capture_outbound();}
function setupLDBButtons(){$('.ldb-board').click(function(){display_loading_screen()
$.ajax({url:$(this).attr('href'),data:{format:'json'},dataType:'json',success:function(data){rebuildLDB($('#ldb'),data);clear_loading_screen();},error:ajax_failure})
return false;})
$('.ldb-board').addClass('has-ajax-handler')}
$(function(){board=getParameterByName('board',window.location.href)
if(board==''){board='departures';}})
function submitAutomaticLocation(position,method){$('.location').html('Location found; please wait while we put a name to it.')
$('.location-accuracy').hide()
$.post(base+'geolocation/',{csrfmiddlewaretoken:$(csrfToken).find('[name=csrfmiddlewaretoken]').val(),longitude:position.coords.longitude,latitude:position.coords.latitude,accuracy:position.coords.accuracy,method:method,format:'json',return_url:$('#return_url').val(),force:'True'},locationFound,'json');}
function automaticLocation(position){submitAutomaticLocation(position,'html5')}
function automaticLocationAndSave(position){submitAutomaticLocation(position,'html5request')}
function locationFailure(d){$('.location-accuracy').hide()
if(d.code==1){$('.location').html('<i>You did not give permission for the site to know your location.</i>');$.post(base+'geolocation/',{csrfmiddlewaretoken:$(csrfToken).find('[name=csrfmiddlewaretoken]').val(),method:'denied'});}else if(d.code==2||d.code==3){$('.location').html('<i>We couldn\'t get a fix on your location right now</i>')
$.post(base+'geolocation/',{csrfmiddlewaretoken:$(csrfToken).find('[name=csrfmiddlewaretoken]').val(),method:'error'});}else{$('.location').html('<i>An error occurred: '+d.message+'</i>')}
window.setTimeout(function(){$('.location').text(locationName);$('.location-accuracy').show()},5000);}
$(document).bind('molly-page-change',function(){if(geo_position_js.init()){$('.update-location-form').append('<ul class="link-list location-automatic-list"><li><input type="submit" value="Get location automatically" class="automatic-update as-text-link" /></li></ul>');if($('.favourite-locations-list').length+$('.historic-locations-list').length){$('.location-automatic-list').addClass('no-round-bottom')}
$('.current-location-box p').prepend('<input type="submit" value="Determine location automatically" class="automatic-update automatic-update-button" />')
$('.automatic-update, .location-automatic-list').click(function(){$('.update-location-box').slideUp();$('.current-location-box').slideDown();$('.alternate-location-box').slideUp();$('.location').html('Please wait while we attempt to determine your location&hellip;')
$('.location-accuracy').hide()
geo_position_js.getCurrentPosition(automaticLocationAndSave,locationFailure,{enableHighAccuracy:true,maximumAge:30000});return false;});$('.automatic-update, .location-automatic-list').addClass('has-ajax-handler')}
$('.update-location-form').append('<input type="button" value="Cancel Update" class="cancel-update as-text-link" />');$('.current-location-box form input').click(function(){$('.current-location-box').hide();$('.cancel-update').click(function(){$('.update-location-box').slideUp();$('.alternate-location-box').slideUp();$('.current-location-box').slideDown();})
$('.cancel-update').addClass('has-ajax-handler')
$('.alternate-location-box').hide();$('.update-location-box').slideDown();$(window).scrollTop($('#location-box').offset().top)
return false;});$('.current-location-box form input').addClass('has-ajax-handler')
$('.update-location-form').submit(function(){$('.update-location-box').slideUp();$('.alternate-location-box').slideUp();$('.current-location-box').slideDown();$('.location').html('Please wait while we attempt to determine your location&hellip;')
$.post(base+'geolocation/',{csrfmiddlewaretoken:$(this).find('[name=csrfmiddlewaretoken]').val(),format:'json',method:'geocoded',name:$(this).find('.update-location-name').val()},locationFound,'json');return false;})
$('.specific-location-form').submit(specificLocationFormSubmit)
$('.favourite-location-form').submit(favouriteLocationFormSubmit)
$('.update-location-form, .specific-location-form, .favourite-location-form').addClass('has-ajax-handler')
if('placeholder'in document.createElement('input')){$('.update-location-name').attr('placeholder','e.g., OX2 6NN, kebl, St Clements')}else{$('.update-location-name').focus(function(){$(this).val('');$(this).css('color','#000000')
$(this).unbind('focus')});$('.update-location-name').val('e.g., OX2 6NN, kebl, St Clements')
$('.update-location-name').css('color','#a3a3a3')}});$(function(){if(geo_position_js.init()){if(locationRequired){geo_position_js.getCurrentPosition(automaticLocation,locationFailure,{enableHighAccuracy:true,maximumAge:30000});}
function periodic_location_update(){setTimeout(function(){geo_position_js.getCurrentPosition(automaticLocation,locationFailure,{enableHighAccuracy:true,maximumAge:30000});periodic_location_update();},600000)}
if(autoLocationUpdating){periodic_location_update();}}});function specificLocationForm(location,favourite){f='  <form class="specific-location-form" method="post" action="'+base+'geolocation/">'
+csrfToken
+'    <input type="hidden" name="method" value="manual"/>'
+'    <input type="hidden" name="accuracy" value="'+location.accuracy+'"/>'
+'    <input type="hidden" name="longitude" value="'+location.location[0]+'"/>'
+'    <input type="hidden" name="latitude" value="'+location.location[1]+'"/>'
+'    <input type="hidden" name="return_url" value="'+window.location.pathname+'"/>'
+'    <input type="hidden" name="name" value="'+location.name+'"/>'
+'    <input type="submit" class="as-text-link" value="'+location.name+'" style="font-weight: normal;" />'
+'  </form>'
if(favourite!=null)
{f+='  <form class="favourite-location-form" method="post" action="'+base+'geolocation/favourites/">'
+csrfToken
if(favourite){f+='    <input type="hidden" name="action" value="remove"/>'
+'    <input type="hidden" name="id" value="'+location.id+'"/>'
+'    <input type="hidden" name="return_url" value="'+window.location.pathname+'"/>'
+'    <input type="submit" class="unfavourite" value="(Remove from favourites)"/>'}else{f+='    <input type="hidden" name="action" value="add"/>'
+'    <input type="hidden" name="accuracy" value="'+location.accuracy+'"/>'
+'    <input type="hidden" name="longitude" value="'+location.location[0]+'"/>'
+'    <input type="hidden" name="latitude" value="'+location.location[1]+'"/>'
+'    <input type="hidden" name="return_url" value="'+window.location.pathname+'"/>'
+'    <input type="hidden" name="name" value="'+location.name+'"/>'
+'    <input type="submit" class="favourite" value="(Add as favourite)"/>'}
f+='  </form>'}
return f}
function specificLocationFormSubmit(){$('.update-location-box').slideUp();$('.alternate-location-box').slideUp();$('.current-location-box').slideDown();$.post($(this).attr('action'),{csrfmiddlewaretoken:$(this).find('[name=csrfmiddlewaretoken]').val(),longitude:$(this).find('[name=longitude]').val(),latitude:$(this).find('[name=latitude]').val(),accuracy:$(this).find('[name=accuracy]').val(),name:$(this).find('[name=name]').val(),return_url:$(this).find('[name=return_url]').val(),method:$(this).find('[name=method]').val(),id:$(this).find('[name=id]').val(),action:$(this).find('[name=action]').val(),format:'json',force:'True'},locationFound,'json');return false;}
function favouriteLocationFormSubmit(){$.post($(this).attr('action'),{csrfmiddlewaretoken:$(this).find('[name=csrfmiddlewaretoken]').val(),longitude:$(this).find('[name=longitude]').val(),latitude:$(this).find('[name=latitude]').val(),accuracy:$(this).find('[name=accuracy]').val(),name:$(this).find('[name=name]').val(),return_url:$(this).find('[name=return_url]').val(),method:$(this).find('[name=method]').val(),id:$(this).find('[name=id]').val(),action:$(this).find('[name=action]').val(),format:'json',force:'True'},locationFound,'json');return false;}
function locationFound(data){if(data.name){$('.location').html(data.name)
locationName=data.name
$('.location-accuracy').html('within approx. '+Math.round(data.accuracy)+'m')
$('.location-accuracy').show()
if(data.alternatives!=null&&data.alternatives.length>0){$('.alternate-location-box').empty()
$('.alternate-location-box').append('<div class="header">'
+'  <h2>Or did you mean&hellip;</h2>'
+'</div>'
+'<ul class="alternate-locations-list link-list">'
+'</ul>');for(i in data.alternatives){$('.alternate-locations-list').append('<li>'+specificLocationForm(data.alternatives[i],null)+'</li>')}
$('.alternate-location-box').slideDown();}else{$('.alternate-location-box').slideUp();}
$('.update-location-lists').empty()
$('.location-automatic-list').removeClass('no-round-bottom')
if(data.favourites.length>0){$('.location-automatic-list').addClass('no-round-bottom')
$('.update-location-lists').append('<div class="header">'
+'  <h2>Or select a favourite location</h2>'
+'</div>'
+'<ul class="favourite-locations-list link-list">'
+'</ul>');for(i in data.favourites){$('.favourite-locations-list').append('<li>'+specificLocationForm(data.favourites[i],true)+'</i>')}}
if(data.history.length>0){$('.location-automatic-list').addClass('no-round-bottom')
$('.favourite-locations-list').addClass('no-round-bottom')
$('.update-location-lists').append('<div class="header">'
+'  <h2>Or select from history</h2>'
+'</div>'
+'<ul class="historic-locations-list link-list">'
+'<li>'
+'    <form class="specific-location-form" method="post" action="'+base+'geolocation/clear/">'
+csrfToken
+'      <input type="submit" value="Clear history" class="as-text-link" />'
+'    </form>'
+'</li>'
+'</ul>');for(i in data.history.reverse()){$('.historic-locations-list').prepend('<li>'+specificLocationForm(data.history[i],false)+'</i>')}}
if($('.favourite-locations-list').length+$('.historic-locations-list').length){$('.location-automatic-list').addClass('no-round-bottom')}
$(document).trigger('molly-location-update')}else{locationFailure({message:data.error,code:-1})}
$('.specific-location-form').submit(specificLocationFormSubmit)
$('.favourite-location-form').submit(favouriteLocationFormSubmit)
$('.update-location-form, .update-location-form, .favourite-location-form').addClass('has-ajax-handler')}
(function(){if(window.google&&google.gears){return;}
var factory=null;if(typeof GearsFactory!='undefined'){factory=new GearsFactory();}else{try{factory=new ActiveXObject('Gears.Factory');if(factory.getBuildInfo().indexOf('ie_mobile')!=-1){factory.privateSetGlobalObject(this);}}catch(e){if((typeof navigator.mimeTypes!='undefined')&&navigator.mimeTypes["application/x-googlegears"]){factory=document.createElement("object");factory.style.display="none";factory.width=0;factory.height=0;factory.type="application/x-googlegears";document.documentElement.appendChild(factory);if(factory&&(typeof factory.create=='undefined')){factory=null;}}}}
if(!factory){return;}
if(!window.google){google={};}
if(!google.gears){google.gears={factory:factory};}})();var bb_successCallback;var bb_errorCallback;var bb_blackberryTimeout_id=-1;function handleBlackBerryLocationTimeout()
{if(bb_blackberryTimeout_id!=-1)
{bb_errorCallback({message:"Timeout error",code:3});}}
function handleBlackBerryLocation()
{clearTimeout(bb_blackberryTimeout_id);bb_blackberryTimeout_id=-1;if(bb_successCallback&&bb_errorCallback)
{if(blackberry.location.latitude==0&&blackberry.location.longitude==0)
{bb_errorCallback({message:"Position unavailable",code:2});}
else
{var timestamp=null;if(blackberry.location.timestamp)
{timestamp=new Date(blackberry.location.timestamp);}
bb_successCallback({timestamp:timestamp,coords:{latitude:blackberry.location.latitude,longitude:blackberry.location.longitude}});}
bb_successCallback=null;bb_errorCallback=null;}}
var geo_position_js=function(){var pub={};var provider=null;pub.getCurrentPosition=function(successCallback,errorCallback,options)
{provider.getCurrentPosition(successCallback,errorCallback,options);}
pub.init=function()
{try
{if(typeof(geo_position_js_simulator)!="undefined")
{provider=geo_position_js_simulator;}
else if(typeof(bondi)!="undefined"&&typeof(bondi.geolocation)!="undefined")
{provider=bondi.geolocation;}
else if(typeof(navigator.geolocation)!="undefined")
{var positionWatchId=null;provider=navigator.geolocation;pub.getCurrentPosition=function(successCallback,errorCallback,options)
{if(positionWatchId==null)
{var positionRequestCount=0;var lastPosition=null;function _successCallback(p,timeout)
{positionRequestCount+=1;clearTimeout(positionWatchTimeout);lastPosition=p;if(positionRequestCount>10||p.coords.accuracy<=150||p.coords.accuracy==18000||timeout){provider.clearWatch(positionWatchId);positionWatchId=null;if(typeof(p.latitude)!="undefined")
{successCallback({timestamp:p.timestamp,coords:{latitude:p.latitude,longitude:p.longitude}});}
else
{successCallback(p);}}else{positionWatchTimeout=setTimeout(function(){_successCallback(lastPosition,true);},5000);}}
var positionWatchId=provider.watchPosition(_successCallback,errorCallback,options);var positionWatchTimeout=setTimeout(function(){provider.getCurrentPosition(function(p,timeout){provider.clearWatch(positionWatchId);positionWatchId=null;successCallback(p);},errorCallback,$.extend(options,{timeout:5000}));},5000);}else{errorCallback({message:'There is already a location request pending',code:-1})}}}
else if(typeof(window.google)!="undefined"&&typeof(google.gears)!="undefined")
{provider=google.gears.factory.create('beta.geolocation');}
else if(typeof(Mojo)!="undefined"&&typeof(Mojo.Service.Request)!="Mojo.Service.Request")
{provider=true;pub.getCurrentPosition=function(successCallback,errorCallback,options)
{parameters={};if(options)
{if(options.enableHighAccuracy&&options.enableHighAccuracy==true)
{parameters.accuracy=1;}
if(options.maximumAge)
{parameters.maximumAge=options.maximumAge;}
if(options.responseTime)
{if(options.responseTime<5)
{parameters.responseTime=1;}
else if(options.responseTime<20)
{parameters.responseTime=2;}
else
{parameters.timeout=3;}}}
r=new Mojo.Service.Request('palm://com.palm.location',{method:"getCurrentPosition",parameters:parameters,onSuccess:function(p){successCallback({timestamp:p.timestamp,coords:{latitude:p.latitude,longitude:p.longitude,heading:p.heading}});},onFailure:function(e){if(e.errorCode==1)
{errorCallback({code:3,message:"Timeout"});}
else if(e.errorCode==2)
{errorCallback({code:2,message:"Position Unavailable"});}
else
{errorCallback({code:0,message:"Unknown Error: webOS-code"+errorCode});}}});}}
else if(typeof(device)!="undefined"&&typeof(device.getServiceObject)!="undefined")
{provider=device.getServiceObject("Service.Location","ILocation");pub.getCurrentPosition=function(successCallback,errorCallback,options)
{function callback(transId,eventCode,result){if(eventCode==4)
{errorCallback({message:"Position unavailable",code:2});}
else
{successCallback({timestamp:null,coords:{latitude:result.ReturnValue.Latitude,longitude:result.ReturnValue.Longitude,altitude:result.ReturnValue.Altitude,heading:result.ReturnValue.Heading}});}}
var criteria=new Object();criteria.LocationInformationClass="BasicLocationInformation";provider.ILocation.GetLocation(criteria,callback);}}
else if(typeof(window.blackberry)!="undefined"&&blackberry.location.GPSSupported)
{if(typeof(blackberry.location.setAidMode)=="undefined")
{return false;}
blackberry.location.setAidMode(2);pub.getCurrentPosition=function(successCallback,errorCallback,options)
{bb_successCallback=successCallback;bb_errorCallback=errorCallback;if(options['timeout'])
{bb_blackberryTimeout_id=setTimeout("handleBlackBerryLocationTimeout()",options['timeout']);}
else
{bb_blackberryTimeout_id=setTimeout("handleBlackBerryLocationTimeout()",60000);}
blackberry.location.onLocationUpdate("handleBlackBerryLocation()");blackberry.location.refreshLocation();}
provider=blackberry.location;}}
catch(e){alert("error="+e);if(typeof(console)!="undefined")
{console.log(e);}
return false;}
return provider!=null;}
return pub;}();function refreshTransport(data){$('#park_and_rides .section-content').empty()
for(var i in data.park_and_rides){var entity=data.park_and_rides[i]
var title=entity.title
if(title.slice(-13)=='Park and Ride'){title=title.slice(0,-14)}
if(title.slice(-11)=='Park & Ride'){title=title.slice(0,-12)}
$('#park_and_rides .section-content').append('<div class="park-and-ride"><h3><a href="'+entity._url+'">'+title+'</a></h3></div>')
if(entity.metadata.park_and_ride){if(entity.metadata.park_and_ride.unavailable){spaces='?'
$('.park-and-ride:last').append('<p><em>Space information currently unavailable</em></p>')}else{$('.park-and-ride:last').append('<div class="capacity-bar"><div style="width: '+entity.metadata.park_and_ride.percentage.toString()+'%; height:7px;background-color: #960300;">&nbsp;</div></div>')
spaces=entity.metadata.park_and_ride.spaces.toString()}
$('.park-and-ride:last').append('<p>Spaces: '+spaces+' / '+entity.metadata.park_and_ride.capacity+'</p>')}
if(i<(data.park_and_rides.length-1)||i%2==1){$('.park-and-ride:last').css('float','left')}
if(i%2==0){$('.park-and-ride:last').css('clear','left')}}
function pad2(number){return(number<10?'0':'')+number}
var now=new Date();now=pad2(now.getHours())+':'+pad2(now.getMinutes())+':'+pad2(now.getSeconds())
for(var type in data.nearby){$('#'+type+' h2:first').html(data.nearby[type].results_type+' '+data.nearby[type].type.verbose_name_plural+' - '+now)
tbody=$('#'+type+' .content tbody')
tbody.empty()
for(var i in data.nearby[type].entities){entity=data.nearby[type].entities[i]
tbody.append('<tr class="sub-section-divider"><th colspan="3"><a href="'+entity._url+'" style="color:inherit;">'+entity.title+'</a></th></tr>')
if(entity.distance){tbody.find('th').append('<small>(about '+Math.ceil(entity.distance/10)*10+'m '+entity.bearing+')</small>')}
if(entity.metadata.real_time_information){if(entity.metadata.real_time_information.pip_info.length>0){tbody.append('<tr><td colspan="3"></td></tr>')
var td=tbody.find('td:last')
for(var j in entity.metadata.real_time_information.pip_info){if(j>0){td.append('<br/>')}
td.append(entity.metadata.real_time_information.pip_info[i])}}
if(entity.metadata.real_time_information.services.length>0){for(var j in entity.metadata.real_time_information.services){service=entity.metadata.real_time_information.services[j]
tbody.append('<tr></tr>')
tr=tbody.find('tr:last')
tr.append('<td style="text-align: center;"><big>'+service.service+'</big></td>')
tr.append('<td>'+service.destination+'</td>')
tr.append('<td>'+service.next+'</td>')
td=tr.find('td:last')
if(service.following.length>0){td.append('<small>, '+service.following[0])
if(service.following.length>1){td.append(', &hellip;</small>')}}}}else{tbody.append('<tr><td colspan="3">There is currently no departure information from this stop</td></tr>')}}else{tbody.append('<tr><td colspan="3">There is currently no departure information from this stop</td></tr>')}}}
rebuildLDB($('#ldb'),data)
ul=$('#travel_news .content-list')
ul.empty()
for(var i in data.travel_alerts){ul.append('<li><a href="'+data.travel_alerts[i]._url+'" style="color: inherit;">'+data.travel_alerts[i].title+'</a></li>')}
capture_outbound();}
function ajaxTransportUpdate(){$.ajax({url:current_url,data:{format:'json',board:board},dataType:'json',success:refreshTransport})}
var transportTimer=null;function transportRefreshTimer(){ajaxTransportUpdate()
transportTimer=setTimeout(transportRefreshTimer,30000)}
$(document).bind('molly-page-change',function(event,url){if(url=='/transport/'){transportRefreshTimer()
$(document).bind('molly-location-update',ajaxTransportUpdate)
setupLDBButtons();}else{$(document).unbind('molly-location-update',ajaxTransportUpdate)
clearTimeout(transportTimer)}});