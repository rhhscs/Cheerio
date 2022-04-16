/**
 * copies a given value to the user's keyboard
 * @param {string} value the value to copy
 */
function copyToClipboard(value) {
    navigator.clipboard.writeText(value);
}


function onSignIn(googleUser) { 
    // function from Google's documentation
    var profile = googleUser.getBasicProfile();
    console.log(profile);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send("userid=" + googleUser.getAuthResponse().id_token);
}

function signOut() {
    // function from Google's documentation
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}
