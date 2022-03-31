/**
 * copies a given value to the user's keyboard
 * @param {string} value the value to copy
 */
function copyToClipboard(value) {
    navigator.clipboard.writeText(value);
}