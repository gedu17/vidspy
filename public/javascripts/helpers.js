function setError(errid, succid, msg) {
    if (!$("#" + succid).hasClass("hide")) {
        $("#" + succid).addClass("hide");
    }
    $("#" + errid).removeClass("hide");
    $("#" + errid).html(msg);
}

function setSuccess(errid, succid, msg) {
    if (!$("#" + errid).hasClass("hide")) {
        $("#" + errid).addClass("hide");
    }
    $("#" + succid).removeClass("hide");
    $("#" + succid).html(msg);
}

function setHide(id) {
    if (!$("#" + id).hasClass("hide")) {
        $("#" + id).addClass("hide");
    }
}

function setShow(id) {
    $("#" + id).removeClass("hide");
}

function removeItem(id) {
    $("#" + id).remove();
}

function sendQuery(url, data, method, callback) {
    $.ajax({
        url: url,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        method: method
    }).complete(function (xhr, textStatus) {
        callback(xhr);
    });
}

function clearForm(id) {
    document.getElementById(id).reset();
}

function openModal(title, text, hideSave) {
    $("#popupTitle").text(title);
    $("#popupBody").html(text);
    if (hideSave === true) {
        setHide("popupSave");
    }
    else {
        setShow("popupSave");
    }
    $("#popup").modal();
}

function updatePopovers() {
    $("button[id^='viewItem'").popover({
        trigger: 'focus',
        html: true
    });
}

function decreaseParentCount(parent) {
    if (parseInt(parent) === 0) {
        var count = parseInt($("#parentCount").text());
        $("#parentCount").text(count - 1);
    }
    else {
        var count = parseInt($("#" + parent + "_count").text());
        $("#" + parent + "_count").text(count - 1);
    }
}

function scrollToTop() {
    $("html, body").animate({ scrollTop: 0 }, "slow");
}

function updateContent(content) {
    var txt = content.replace(new RegExp("&lt;", 'g'), "<").replace(new RegExp("&gt;", 'g'), ">");
    $("#contentBox").html(txt);
}

function GetLoadingIcon(size) {
    //Size in pixels - 30
    var spinnerSize = size;
    if (typeof (size) === "undefined") {
        spinnerSize = 48;
    }

    return "<div class=\"loadingCenter\" style=\"font-size: " + size + "px;\"><span class=\"glyphicon glyphicon-refresh glyphicon-refresh-animate\"></span></div>";

}

function checkIfEmptyList() {
    if($("#itemList").children().length === 2) {
        changeVirtualView();
    }
}