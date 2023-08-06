
function addtoNew() {

  var collrequest =  $.ajax({
    url: "/collection", 
    type: "POST",
    data: $("#newcoll").serialize(), //we use the data from the form 
    success: function (data){
      var newitem = $('<li class="ui-state-highlight ui-widget-header"><a href="'
        + data['local_path']
        + '"><strong>'
        + data['title']
        + '</a></strong></li>')
      if ( $('#collections > li').length != 0) { 
        $('#collections li:first').before(newitem);
        }else {
          $('#collections').append(newitem);
        }

     },
  })

};

function newCollection(){
  var formhtml = '\n<form id="newcoll">'
    + '\n<input type="text" name="title" value="Title"><br />'
    + '\n<input type="text" name="subject" value="Subject">'
    + '\n<input type="hidden" name="entries" value="<'
    + $('#uriref').text()
    + '>">'
    + '\n</form>'
  var $newcollform = $('<div id=""></div>').html(formhtml).dialog({
          autoOpen: false,
          hide: "fold",
          position: ['20','10'],
          width: 300,
          title: 'Add work to new collection',
          buttons: { "Cancel": function() { 
           $(this).dialog("close"); 
            } , 
          "Save": function () {
            addtoNew();
            $(this).dialog("close");

            }
          }
        });
  $('#newcollection').click(function () {
    $newcollform.dialog('open');
    $newcollform.find('input.text[name="title"]').focus();
    });
 
};

function updateCollection(collection, div) {
    var uri = '/collection/' + collection.id.split('/')[4].split('>')[0]
    var data =  JSON.stringify(collection);
    $.ajax({
	url: uri,
	type: "POST",
	data: data,
	contentType: "json",
	success: function (data){
	    if (data.status == 'ok') {
		div.find('a:last').remove(); // should really not use find here..
		var updated = $("<span />");
		updated.text(" updated!");
		div.append(updated);
		div.addClass('ui-state-highlight')
		    .animate({ backgroundColor: "magenta" }, 1000)
		    .animate({ backgroundColor: "white" }, 1000)
	    }
	},
    });
};

function addtoExisting() {
    account_uri = $("#account_uri").attr("href")
    $.getJSON('/collection/search?user='+account_uri, function(data) {
	if (data != null ) { 
	    var entryId = '<' + $('#uriref').text() + '>';
	    var collList = $('#collections');
            $(data.rows).each(function(idx, collection) {
		var collDivid = "#coll_" + collection.id.split('/')[4];
		var collUri = collection.id.slice(1, collection.id.length-1);
		var entryonCollection = 0;

		var collElem = $("<li />");
		collElem.attr("id", collDivid);
		var collHref = $("<a />");
		collHref.attr("href", collUri);
		collHref.text(collection.title);
		collElem.append(collHref);

		// hrmmm... hash table here? for big collections this will be brutal
		$(collection.entries).each(function () {
		    if ( entryId == this.id ) {
			entryonCollection = 1;
                    };
		});

		if ( entryonCollection == 1 ) {
		    var remove = $("<a />");
		    remove.attr("href", "#");
		    remove.attr("class", "remove");
		    remove.text(" [remove]");
		    remove.click(function () {
			var entries = $.makeArray(collection.entries);
			var indexCollection = {id: entryId};
			entries.splice(entries.indexOf(indexCollection), 1);
			collection.entries = entries;
			updateCollection(collection, collElem);
                    });
		    collElem.append(remove);
		} else {
		    var add = $("<a />");
		    add.attr("href", "#");
		    add.attr("class", "add");
		    add.text(" [add]");
		    add.click(function () {
			var newitem = Array({id : entryId });
			var entries = $.makeArray(collection.entries);
			collection.entries = entries.concat(newitem);
			updateCollection(collection, collElem);
                    });
		    collElem.append(add);
		};
		collList.append(collElem);
            }); // each data.row
	} // if data != nil
    }); // getJSON
}

$(document).ready(function() {
  newCollection();
  setTimeout("addtoExisting()",1000); // a bit later to prevent deadlocks
});
