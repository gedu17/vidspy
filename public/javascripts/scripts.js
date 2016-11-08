$(document).ready(function () {
    var currentTab = "passwordChange";
    $('#settingsTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');

        var item = this.toString();
        var hashtag = item.indexOf("#");
        var tab = item.substring(hashtag + 1);
        if (currentTab != null) {
            setHide(tab + "Success");
            setHide(tab + "Error");
        }

        currentTab = tab;
    });

    updatePopovers();
});

