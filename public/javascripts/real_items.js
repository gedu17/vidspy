function deleteRealItem(id, parent) {
    var cb = function (xhr) {
        if (xhr.status === 200) {
            setHide(id + "_div");
            setHide(id + "_content");
            decreaseParentCount(parent);
        }
    };
    sendQuery("/real_item/" + id, undefined, "DELETE", cb);
}