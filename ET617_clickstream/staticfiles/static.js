// clickstream/static/clickstream/clickstream.js
(function(){
    function postJSON(url, data){
        return fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        }).then(r => r.json().catch(()=>({}))).catch(()=>({}));
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    window.recordEvent = function(eventType, meta){
        const payload = {
            event_type: eventType,
            path: window.location.pathname + window.location.search,
            meta: meta || {},
            user_id: window.USER_ID || null
        };
        postJSON('/api/click/', payload);
    };

    window.recordClick = function(name){
        window.recordEvent('click:'+name, {});
    };

    // capture global clicks (optional)
    document.addEventListener('click', function(e){
        const target = e.target;
        if (target.tagName === 'A' || target.tagName === 'BUTTON' || target.dataset.track === 'true'){
            const meta = {
                tag: target.tagName,
                id: target.id || null,
                classes: target.className || null,
                text: target.innerText ? target.innerText.slice(0,100) : null
            };
            window.recordEvent('click', meta);
        }
    }, true);

    // expose helper to check login and set USER_ID
    fetch('/api/whoami/').then(resp => resp.json()).then(data => {
        if (data && data.id) window.USER_ID = data.id;
    }).catch(()=>{});
})();
