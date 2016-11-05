function openMessage(id) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            openModal("System message", xhr.responseText, true);
            setHide(id + "_icon");
        }
    };

    sendQuery("/system_messages/" + id, undefined, "GET", cb);
}

function cleanMessages() {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            var cb2 = function (xhr2) {
                if (xhr2.status === 200) {
                    updateContent(xhr2.responseText);
                }
            };
            sendQuery("/template/important_system_messages", undefined, "GET", cb2);
        }
    };

    sendQuery("/system_messages/", undefined, "DELETE", cb);
}

function deleteMessage(id) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            setHide(id + "_tr");
        }
    };

    sendQuery("/system_messages/" + id, undefined, "DELETE", cb);
}

function changeSystemMessages() {
    var cb = function (xhr) {
        if (xhr.status == 200) {
            updateContent(xhr.responseText);
        }
    };
    var val = parseInt($("#listingType").val());
    var query = null;
    if (val === 0) {
        query = "/template/important_system_messages";
    }
    else if (val === 1) {
        query = "/template/all_system_messages";
    }

    sendQuery(query, undefined, "GET", cb);
}

function updateSystemMessageCount() {
    var deferred = $.Deferred();
    var cb = function (xhr) {
        if (xhr.status === 200) {

            var cb2 = function (xhr2) {
                if (xhr2.status === 200) {
                    $("#systemMessagesBadge").remove();
                    $("#messages_link").append(xhr2.responseText);
                    deferred.resolve("OK");
                }
            }
            sendQuery("/template/smbadge/" + xhr.responseText, undefined, "GET", cb2);
        }
    };

    sendQuery("/system_messages/", undefined, "COUNT", cb);
    return deferred.promise();
}