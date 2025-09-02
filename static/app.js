// generic helpers
async function http(method, url, data, headers={}) {
  const opts = { method, headers: {'Content-Type': 'application/json', ...headers} };
  if (data !== undefined) opts.body = JSON.stringify(data);
  const res = await fetch(url, opts);
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`HTTP ${res.status}: ${t}`);
  }
  return res.json().catch(()=>({ok:true}));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
