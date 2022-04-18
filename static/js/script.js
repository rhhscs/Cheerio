/**
 * copies a given value to the user's keyboard
 * @param {string} value the value to copy
 */
function copyToClipboard(value) {
    navigator.clipboard.writeText(value);
}


function onSignIn(googleUser) { 
    // function from Google's documentation, slightly modified
    var profile = googleUser.getBasicProfile();
    console.log(googleUser);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("userid=" + JSON.stringify(googleUser.getBasicProfile()));
}

function signOut() {
    // function from Google's documentation
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}
