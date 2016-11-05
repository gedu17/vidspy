function createUser() {
    var name = $("#name").val();
    var password = $("#password").val();
    var password2 = $("#passwordRepeat").val();
    var level = $("#level").val();
    if(name.length < 3) {
        setError("createUserError", "createUserSuccess", "Name is too short. Should be at least 3 digits.");
    }
    else if($("#password").val() !== $("#passwordRepeat").val()) {
        setError("createUserError","createUserSuccess", "Passwords do not match.");
    }
    else {
        var cb = function(xhr) {
            if(xhr.status == 200) {
                updateManageUsers("createUserError", "createUserSuccess");
                setTimeout(function() {
                    setSuccess("createUserError","createUserSuccess", "User created.");
                    clearForm("createUserForm");
                }, 500);
                
            }
            else {
                setError("createUserError","createUserSuccess", "Username already exists.");
            }
        };

        var data = {name: name, password: password, level: level};
        setHide("createUserError");
        setHide("createUserSuccess");
        sendQuery("/account/create", data, "POST", cb);
    }
    scrollToTop();
}

function deleteUser(id, name) {
    $("#popupTitle").text("Confirmation");
    $("#popupBody").html("Are you sure you want to remove user " + name + "?");
    $("#popupSave").html("Remove");
    var cb = function(xhr) {
        if(xhr.status == 200) {
            updateManageUsers("manageUsersError", "manageUsersSuccess");
            setTimeout(function() {setSuccess("manageUsersError", "manageUsersSuccess", "User " + name + " successfully removed.")}, 500);
        }
        else {
            setError("manageUsersError", "manageUsersSuccess", "Failed to remove " + name + ". Bad permissions.")
        }
        $("#popupSave").off('click');
    };
    $("#popupSave").on('click', function() {
        sendQuery("/account/delete/" + id, null, "DELETE", cb);
    });
}

function updateManageUsers(errid, succid) {
    var cb = function(xhr) {
        if(xhr.status == 200) {
            $("#manageUsers").html(xhr.responseText);
        }
        else {
            setError(errid, succid, "Failed to update manage users tab. Please reload manually.");
        }
    };
    sendQuery("/account/users", undefined, "GET", cb);
}

function setAdmin(id, value) {
    var cb = function(xhr) {
        if(xhr.status === 200) {
            if(parseInt(value) === 0) {
                $("#" + id + "_admin").addClass("hide");
                $("#" + id + "_notadmin").removeClass("hide");
            }
            else {
                $("#" + id + "_notadmin").addClass("hide");
                $("#" + id + "_admin").removeClass("hide");
            }
        }
    };
    sendQuery("/account/admin/" + id, {value: value}, "PUT", cb);
}

function setActive(id, value) {
    var cb = function(xhr) {
        if(xhr.status === 200) {
            if(parseInt(value) === 0) {
                $("#" + id + "_active").addClass("hide");
                $("#" + id + "_inactive").removeClass("hide");
            }
            else {
                $("#" + id + "_inactive").addClass("hide");
                $("#" + id + "_active").removeClass("hide");
            }
        }
    };
    sendQuery("/account/active/" + id, {value: value}, "PUT", cb);
}

function updateAdminSettings() {
    var inputs = $("#adminSettings :input").not(":button");
    var data = [];
    for(var i = 0; i < inputs.length; i++) {
        data.push({ id:  inputs[i].id,
                    value: inputs[i].value
        });
    }
    var cb = function(xhr) {
        if(xhr.status === 200) {
            setSuccess("adminSettingsError", "adminSettingsSuccess", "Admin settings updated.");
        }
        else {
            setError("adminSettingsError", "adminSettingsSuccess", "Error updating admin settings.");
        }
    };
    setHide("adminSettingsError");
    setHide("adminSettingsSuccess");
    sendQuery("/account/adminsettings", data, "POST", cb);
    scrollToTop();
}

function updateUserPaths() {
    var inputs = $("#userPathsForm :checked").not(":button");
    var data = [];
    for(var i = 0; i < inputs.length; i++) {
        data.push({ id:  inputs[i].id,
                    value: inputs[i].value
        });
    }

    var cb = function(xhr) {
        if(xhr.status === 200) {
            setSuccess("userPathsError", "userPathsSuccess", "User paths updated.");
        }
        else {
            setError("userPathsError", "userPathsSuccess", "Failed to update user paths.");
        }
    }
    setHide("userPathsError");
    setHide("userPathsSuccess");
    sendQuery("/settings/user_paths", data, "POST", cb);
    scrollToTop();
}

function changePassword() {
    if($("#newPassword").val() === $("#newPasswordConfirmation").val()) {
        var cb = function(xhr) {
            if(xhr.status === 200) {
                setSuccess("passwordChangeError", "passwordChangeSuccess", "Password successfully changed.");
                clearForm("passwordChangeForm");
            }
            else {
                setError("passwordChangeError", "passwordChangeSuccess", "Old password is incorrect.");
            }
        };
        var data = {old_password: $("#oldPassword").val(), new_password: $("#newPassword").val()};
        setHide("passwordChangeError");
        setHide("passwordChangeSuccess");
        sendQuery("/account/password", data, "POST", cb);
    }
    else {
        setError("passwordChangeError", "passwordChangeSuccess", "Passwords do not match.");
    }
    scrollToTop();
}