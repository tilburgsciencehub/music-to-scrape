function setCookie(name, value, days) {
    var expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + '=' + value + ';expires=' + expires.toUTCString();
}

function getCookie(name) {
    var cookieArr = document.cookie.split(';');
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split('=');
        if (cookiePair[0].trim() === name) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

function addGoogleAnalyticsScript() {
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-MH61LTNGL6';
    document.head.appendChild(script);

    var analyticsScript = document.createElement('script');
    analyticsScript.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-MH61LTNGL6');
    `;
    document.head.appendChild(analyticsScript);
}

function removeGoogleAnalyticsScript() {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
        if (scripts[i].src.includes('googletagmanager.com/gtag/js')) {
            scripts[i].remove();
        }
    }
}

function acceptAllCookies() {
    // Analytics Cookie
    addGoogleAnalyticsScript()
    setCookie('analytics_accepted', 'true', 365);
}

function RejectAllCookies() {
    // Analytics Cookie
    setCookie('analytics_accepted', 'false', 365);
    removeGoogleAnalyticsScript()
}

function showCookiePreferences() {
    var popup = document.getElementById('cookie-preferences-popup');
    popup.style.display = 'block';
}

function hideCookiePreferences() {
    var popup = document.getElementById('cookie-preferences-popup');
    popup.style.display = 'none';
}

function saveCookiePreferences() {
    var analyticsCheckbox = document.getElementById('analytics-cookie');

    if (analyticsCheckbox.checked) {
        setCookie('analytics_accepted', 'true', 365);
        addGoogleAnalyticsScript();
    } else {
        setCookie('analytics_accepted', 'false', 365);
        removeGoogleAnalyticsScript();
    }

    hideCookiePreferences();
}

window.onload = function () {
    var cookieBanner = document.getElementById('cookie-banner');
    var acceptButton = document.getElementById('accept-cookies');
    var rejectButton = document.getElementById('reject-cookies');
    var analyticsCheckbox = document.getElementById('analytics-cookie');

    if (!getCookie('analytics_accepted')) {
        cookieBanner.style.display = 'block';

        acceptButton.addEventListener('click', function () {
            cookieBanner.style.display = 'none';
            acceptAllCookies();
        });

        rejectButton.addEventListener('click', function () {
            setCookie('cookie_accepted', 'false', 365);
            cookieBanner.style.display = 'none';
        });

    } else if (getCookie('analytics_accepted') === 'true') {
        addGoogleAnalyticsScript();
    }

    if (getCookie('analytics_accepted') === 'true') {
        analyticsCheckbox.checked = true;
    }
};