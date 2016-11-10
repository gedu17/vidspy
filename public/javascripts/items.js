function moveItem(id) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            openModal("Move", xhr.responseText, false);

            $("#popupSave").on('click', function () {
                var cb2 = function (xhr) {
                    if (xhr.status === 200) {
                        var defer = jQuery.Deferred();
                        var promise = defer.promise();
                        promise.then(updateVirtualView);
                        defer.resolve();
                    }
                    $("#popupSave").off('click');
                };
                var data = { parent_id: $("#parentfolder").val() };
                sendQuery("/item/move/" + id, data, "PUT", cb2);
            });
        }
    };

    sendQuery("/template/move/" + id, undefined, "GET", cb);
}

function editItem(id) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            openModal("Rename", xhr.responseText, false);

            $("#popupSave").on('click', function () {
                var cb2 = function (xhr) {
                    if (xhr.status === 200) {
                        var defer = jQuery.Deferred();
                        var promise = defer.promise();
                        promise.then(updateVirtualView);
                        defer.resolve();
                    }
                    $("#popupSave").off('click');
                };
                var data = { name: $("#newname").val() };
                sendQuery("/item/edit/" + id, data, "PUT", cb2);
            });
        }
    };

    sendQuery("/template/edit/" + id, undefined, "GET", cb);
}

function createFolder() {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            openModal("New folder", xhr.responseText, false);

            $("#popupSave").on('click', function () {
                var cb2 = function (xhr) {
                    if (xhr.status === 200) {
                        var defer = jQuery.Deferred();
                        var promise = defer.promise();
                        promise.then(updateVirtualView);
                        defer.resolve();
                    }
                    $("#popupSave").off('click');
                };
                var data = { name: $("#foldername").val(), parent: $("#parentfolder").val() };
                sendQuery("/item/create/", data, "POST", cb2);
            });
        }
    };

    sendQuery("/template/create/", undefined, "GET", cb);
}

function viewedItem(id, parent) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            removeItem(id + "_div");
            removeItem(id + "_content");
            decreaseParentCount(parent);
            checkIfEmptyList();
        }
    };
    sendQuery("/item/viewed/" + id, undefined, "PUT", cb);
}

function deleteItem(id, parent) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            removeItem(id + "_div");
            removeItem(id + "_content");
            decreaseParentCount(parent);
            checkIfEmptyList();
        }
    };
    sendQuery("/item/delete/" + id, undefined, "DELETE", cb);
}

function unviewedItem(id, parent) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            removeItem(id + "_div");
            removeItem(id + "_content");
            decreaseParentCount(parent);
            checkIfEmptyList();
        }
    };
    sendQuery("/item/unviewed/" + id, undefined, "PUT", cb);
}

function undeleteItem(id, parent) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            removeItem(id + "_div");
            removeItem(id + "_content");
            decreaseParentCount(parent);
            checkIfEmptyList();
        }
    };
    sendQuery("/item/undelete/" + id, undefined, "PUT", cb);
}

function rescan() {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            var defer = jQuery.Deferred();
            var promise = defer.promise();
            promise.then(updateVirtualView).then(updateSystemMessageCount);
            defer.resolve();
        }
    };

    $("#contentBox").empty();
    $("#contentBox").html(GetLoadingIcon(48));
    sendQuery("/items/scan/", undefined, "GET", cb);
}