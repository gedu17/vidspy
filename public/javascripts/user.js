function updateVirtualView() {
    var deferred = $.Deferred();
    var cb = function (xhr) {
        if (xhr.status == 200) {
            var txt = xhr.responseText.replace(new RegExp("&lt;", 'g'), "<").replace(new RegExp("&gt;", 'g'), ">");

            $("#contentBox").html(txt);
            updatePopovers();
            deferred.resolve("OK");
        }
    };
    sendQuery("/template/virtual_items", undefined, "GET", cb);
    return deferred.promise();
}

function changeVirtualView() {
    var cb = function (xhr) {
        if (xhr.status == 200) {
            updateContent(xhr.responseText);
            updatePopovers();
        }
    };
    var val = parseInt($("#listingType").val());
    var query = null;
    if (val === 0) {
        query = "/template/virtual_items";
    }
    else if (val === 1) {
        query = "/template/viewed_items";
    }
    else {
        query = "/template/deleted_items";
    }

    sendQuery(query, undefined, "GET", cb);
}

function logIn(id) {
    var cb = function (xhr) {
        if(xhr.status == 200) {
            location.reload();
        }
    };
    sendQuery("/account/login", {id: id}, "POST", cb);
}