from ready.checks.bad_response import check_bad_response_kasada, check_bad_response_cloudflare
from unittest import TestCase
from thttp import Response


class CloudflareTestCase(TestCase):
    def test_cloudflare_blocked_content(self):
        content = b"""<!DOCTYPE html>\n<html>\n<head>\n  <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport">\n  <title>Checking your Browser - GitLab</title>\n  <style>body{align-items:center;color:#666;display:flex;flex-direction:column;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;font-size:14px;justify-content:center;margin:auto;text-align:center}hr{border:0;border-bottom:1px solid #fff;border-top:1px solid #eee;margin:18px auto;max-width:800px}img{max-width:40vw}.container{margin:auto 20px}.cferror_details{list-style-type:none}.cf-error-details h1{color:#456;font-size:20px;font-weight:400;line-height:28px}</style>\n<meta http-equiv="refresh" content="35">\n</head>\n\n<body>\n  <h1>\n    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDI1IDI0IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxwYXRoIGQ9Im0yNC41MDcgOS41LS4wMzQtLjA5TDIxLjA4Mi41NjJhLjg5Ni44OTYgMCAwIDAtMS42OTQuMDkxbC0yLjI5IDcuMDFINy44MjVMNS41MzUuNjUzYS44OTguODk4IDAgMCAwLTEuNjk0LS4wOUwuNDUxIDkuNDExLjQxNiA5LjVhNi4yOTcgNi4yOTcgMCAwIDAgMi4wOSA3LjI3OGwuMDEyLjAxLjAzLjAyMiA1LjE2IDMuODY3IDIuNTYgMS45MzUgMS41NTQgMS4xNzZhMS4wNTEgMS4wNTEgMCAwIDAgMS4yNjggMGwxLjU1NS0xLjE3NiAyLjU2LTEuOTM1IDUuMTk3LTMuODkuMDE0LS4wMUE2LjI5NyA2LjI5NyAwIDAgMCAyNC41MDcgOS41WiIKICAgICAgICBmaWxsPSIjRTI0MzI5Ii8+CiAgPHBhdGggZD0ibTI0LjUwNyA5LjUtLjAzNC0uMDlhMTEuNDQgMTEuNDQgMCAwIDAtNC41NiAyLjA1MWwtNy40NDcgNS42MzIgNC43NDIgMy41ODQgNS4xOTctMy44OS4wMTQtLjAxQTYuMjk3IDYuMjk3IDAgMCAwIDI0LjUwNyA5LjVaIgogICAgICAgIGZpbGw9IiNGQzZEMjYiLz4KICA8cGF0aCBkPSJtNy43MDcgMjAuNjc3IDIuNTYgMS45MzUgMS41NTUgMS4xNzZhMS4wNTEgMS4wNTEgMCAwIDAgMS4yNjggMGwxLjU1NS0xLjE3NiAyLjU2LTEuOTM1LTQuNzQzLTMuNTg0LTQuNzU1IDMuNTg0WiIKICAgICAgICBmaWxsPSIjRkNBMzI2Ii8+CiAgPHBhdGggZD0iTTUuMDEgMTEuNDYxYTExLjQzIDExLjQzIDAgMCAwLTQuNTYtMi4wNUwuNDE2IDkuNWE2LjI5NyA2LjI5NyAwIDAgMCAyLjA5IDcuMjc4bC4wMTIuMDEuMDMuMDIyIDUuMTYgMy44NjcgNC43NDUtMy41ODQtNy40NDQtNS42MzJaIgogICAgICAgIGZpbGw9IiNGQzZEMjYiLz4KPC9zdmc+Cg==" alt="GitLab" /><br />\n  </h1>\n  <div class="container">\n    <div class="cf-browser-verification cf-im-under-attack">\n    <noscript>\n        <h1 style="color:#bd2426;">Please turn JavaScript on and reload the page.</h1>\n    </noscript>\n    <div id="cf-content">\n        <div id="cf-bubbles">\n            <div class="bubbles"></div>\n            <div class="bubbles"></div>\n            <div class="bubbles"></div>\n        </div>\n        <h1>Checking your browser before accessing gitlab.com.</h1>\n        <div id="no-cookie-warning" class="cookie-warning" style="display:none">\n            <p style="color:#bd2426;">Please enable Cookies and reload the page</p>\n        </div>\n        <p>This process is automatic. Your browser will redirect to your requested content shortly.</p>\n        <p id="cf-spinner-allow-5-secs">Please allow up to 5 seconds...</p>\n        <p id="cf-spinner-redirecting" style="display:none">Redirecting...</p>\n    </div>\n    <form id="challenge-form" class="challenge-form" action="/users/sign_in?__cf_chl_f_tk=yEH1.9z1LJpq3YZNo8N4wTDNIXgr.S8eP24Qz64n0Fo-1669515374-0-gaNycGzNB2U" method="POST" enctype="application/x-www-form-urlencoded">\n        <input type="hidden" name="md" value="r7VIAC78sS1BspamhWJ.ptPz5XGfuQ.kf35wuQdr7i0-1669515374-0-AevJOGXiyaqlAjRONHGy6FQUFORCrqkwwEJHQUmXxb16L6FFJSVdgQs7yq4EniKMPJHtE76rbTZBjDGiah6h-7IWKpbdTcEw6Wfq2ejAjI__oq8OvLInxXGV21oeW_blfrJbCbmllx7xVPI_IL1yUpL8nuyQu5EgA8DslvvR_k6PXVCyCfzuzP3VEozYHEpGh5I7ENiv1pmqtTpmnMgWxZ4sBbCQoJeZZEDMJaRfKZ9IB2Hd9VTctpRP3jRPCT867of5jJmAvS5ZBPCzWjIUcF6NebLsMNN8itXXwaPUA5UqiFJJBzL2aWTMU78e7RsxkR3iYaRF-a45qtYcAhNQJUAvbTiR3yxy9UQqAlm50Yhn1MdmQmFHV7edMBLXcNKCxMKkfBcsRY0bRSc7DN8ft5JnPVbNYFZYP0uGLdLu--YAICAtQpgxuikMYJQjulT-m0yzzJbbOzIC7zFZXhT88S-owuEvwdH3g69XV5ywu5vpE6FdcaJR5x0UvJY9UmJMsw_VAPRKNlT-0JXHVmcL30IPulUYAnRPC9eWO6wMjW_cr3meEnnMbBTFdjAYdSzBveWB5PY1C3diYwC1hweEjHUohz5cbQ_XnmhNuby7f7JUK7AulkaVpm9zfzZpIEE2xw" />\n        <input type="hidden" name="r" value="U6Wxc2B5aRslEmqihNUeE.CR2KG8tkLuEK2U4TNEuPo-1669515374-0-AafCr7zxiKFclnfzkL9ytEHYXMoVKREPoDtGgdlMII1M7z78fQ8d8hxqPy3nUOw/Sl1kwGgtAP+yi9SM89ZSSvd5P+as7LuIiELLRXPjn2Z7kxOt6oEBS/C6yIvePNMzsGsXLZKFEDZNv8Vo6sn/N9rsrYFSFQhuOSrf1TSqIsm6D0l0qxs3KcjGupmvWklSUrv01fT8vPYfDQRXlcYf39XFVfhzZn5B+FjuZcULRyHyXc3ralHTvPIOqeua09caMIadSVW6vBd5Za6BUMiHEPQ+ph06V9ZQxZPe7lYrdjQrCRWSVDqV8hla6ORM0KhOolPILY/irUPM8EkWuhx/7H2PKVG9hDlP5w2p1NedQodtBixuTy9LMeVhAVOWIf5ufH8CMBN47HBjVt0PEzuhX0wWnuBVMcMciS0zsibASDkt8dcoxUga7xaFG07Ho5kdNH4Jnp6z0mltRkwtInr9KF/R8f8CPP4T3ss3gYYqfUVGA6qqGzzFflH1wyVvYRXo611hztyYRtXNVsbwnU7FIh0AJvKVRpdkTenAJWDVvJBU0sUAcEwS3svMLYJBVRkOnmoan4bTzr0hBFCfdAvEGD8oAAoB+UftbjJqvSdH2Ydr7lgHgfg1P0fPfSLrY9WoHvm1iPEZ6AEQbKdUI6bNl+4C/ymc1rcZzwNnJUxwHGOOTCepSFsgiAKy3PvsK7rnQ7CzJ5w6DeVx8pZ3LRyqh2hFehDGwm8Z3CTTwh1z61VfefZp7v81eGNc9W51rEt/3ebRP2XK6hu0vuMOiopffFPI4t8n7E3ghIkB5TCKmC3TgQdOEVJsEbkt/U8W1ZNw4rODID5hqSSnCZ5xOms3VkLhhjOTjMj1KXrmOh7ZOAYw0YJsrq36GZt1ZrBvewsi4Y7J0UiCnTHru2TeQO6uWlbUqo6vyg4fxP+0kwQWMhNBzydUsMULhCW6hTHnwYaPrPv8NigEGEDhnJG7s3UJWx6EigC9r4N0AGXzOAH7LaXhKRTuuFyVMtZt8m+lD7NUYzoA7tCEI+nqbnr3NZtdqOFeMhfLXKYm+bGKGVq68DCoGUi+ppgItJkHcdZR42DxXnX3DiOuC6g95s2i2JddNXVGO8AZHGEyJTHCL+UV7wsEOweSUmMmMn0dAOfA+lvt5yZ+/4FZvdH3SxNs2kx5iCbqtm53dpze9s6a0XDH8PxPuQHzHGEU/QXlh6py1EH1VDcTRODKqjtyKOoMOqRgLg5uWx1VUX1HamACPoRKGMCxgS6mg8MqjLau5HiE9rhmpwR/FpFT/ufjhJesYb+61zGc4rqMFCBPEmcivV9VZ6CP15M8CqBqvupXKUhtFxw472x5ttQKuidpzor3kYLXq3WtZngL7FPUZNLe7gco9HLqTMefA2WwX5kR26JR4u7wH8l9i5Y0UBwiwGBRyfnE30u/f+7VsGqG+cm1cXA6AvgQ9tmHsHUq58HKOBwAXJDTiGA8447wopa6W/9rIgbYt2501andjddcMf3aS8cTVYSwoqkv1ajtce4kJvxinkVpDx3Y75aIijG8cbJsbIz4OcSptguA8ZhPp+wyhZFDzUZGI08SL+KQrwnPD56viXOAdSP7/mmANT56YWExSegzMLHno58nkNYcKoyleBdyvIq/SrlOWzOdaPgsq5sceKySlmVlMocO98sq5BSY4ZloUxUxdbXV1LNe2Fjm6TjNcWkgbhKuDCHG/M4gxdoT0xudvED2s7luH78og9CWUgse1pT4y4XZaHNPBsNnfHA2PdFcgs7eXN4islWlU8Vy+0BgKoAE3oWI36juj84Hf7G3j1ywg8tHrgKNGpQcIEUqUv5i" />\n    </form>\n    <div id="trk_jschal_js" style="display:none;background-image:url(\'/cdn-cgi/images/trace/jsch/nojs/transparent.gif?ray=77075c526dfea7e9\')"></div>\n    <script>\n    (function(){\n        window._cf_chl_opt={\n            cvId: \'2\',\n            cType: \'non-interactive\',\n            cNounce: \'47132\',\n            cRay: \'77075c526dfea7e9\',\n            cHash: \'748885c987b07f9\',\n            cUPMDTk: "\\/users\\/sign_in?__cf_chl_tk=yEH1.9z1LJpq3YZNo8N4wTDNIXgr.S8eP24Qz64n0Fo-1669515374-0-gaNycGzNB2U",\n            cFPWv: \'b\',\n            cTTimeMs: \'1000\',\n            cTplV: 1,\n            cTplB: \'cf\',\n            cRq: {\n                ru: \'aHR0cHM6Ly9naXRsYWIuY29tL3VzZXJzL3NpZ25faW4=\',\n                ra: \'TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTAuMTU7IHJ2OjEwNS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwNS4w\',\n                rm: \'R0VU\',\n                d: \'gBJ7mEYgJmH071oiC/h/An74LaWKe7K5bGGUOnYgpqgbicGiWDMt8ZLuhSTDkRA/ibo2IBdG9zk2Oo6pZw9BwlTewTiUVU92UgE4L+02nE7e9bIy9+n15U+yE2GQ5rZUWYPxzjflAIY7bUXy+oRHlKe88qANliPKYyl3iBVigiQf/IQIzMuv/gZH/rcL+81RM+LSVRzMtHjWlGHOODHwo85sfJJlGUK9xSa+3TaJbiCwiByYL0DNHTd99xMz0OPqe2+R0x8loOHUjXna9iXnWRQkXrZWdwtcSWypo2IK8N7Nhg/ErpBXu9rZzs4oP1LmV8yZI4BWJCI9q6G69F9qPVc8AFTZQQFjSiUkJRTjJ/V/uNjJ5EQYhQLr+kFbIuoarrWTp6/Yf3RHH1ASKLbbqyMtY1W/81HH1zLkggVs6JTvSVWWpEVmZOSaLAeKj/ilqeDnZADbGgDoHGObKeLIqavqfLUp8keBaVHwB0YNNnxK7hk0u2Qx1hpkOZeVA0OfXapG9Mc7eUeAigO/6ARxSAXWHUPTxoR9wfloBljTWcOc4YrglzzjRK7LJUGFAiyY8MhxSLMqa2l++9S1kBAFkQ==\',\n                t: \'MTY2OTUxNTM3NC40NjYwMDA=\',\n                m: \'nvVYc8gEJ1urWtHiqexBVXUxMNwsm8iGLgT6iezk6hk=\',\n                i1: \'qtCItyxgZQG7YO4Iyndl6g==\',\n                i2: \'xu6XribgPGqPlhnbw58x2A==\',\n                zh: \'UnJDyo9FrWqFHAM0dnr3Qrw4Ll86sU7CDCiveOM3u04=\',\n                uh: \'uozst7PRgePQRqvQWemQfmDZ4ySMjlf5zzU++wP5zWQ=\',\n                hh: \'lGQbzypQ55vDVgAzrKu7GNtEf1PrcZK3oqezycJ79vw=\',\n            }\n        };\n        var trkjs = document.createElement(\'img\');\n        trkjs.setAttribute(\'src\', \'/cdn-cgi/images/trace/jsch/js/transparent.gif?ray=77075c526dfea7e9\');\n        trkjs.setAttribute(\'style\', \'display: none\');\n        document.body.appendChild(trkjs);\n        var cpo = document.createElement(\'script\');\n        cpo.src = \'/cdn-cgi/challenge-platform/h/b/orchestrate/jsch/v1?ray=77075c526dfea7e9\';\n        window._cf_chl_opt.cOgUHash = location.hash === \'\' && location.href.indexOf(\'#\') !== -1 ? \'#\' : location.hash;\n        window._cf_chl_opt.cOgUQuery = location.search === \'\' && location.href.slice(0, -window._cf_chl_opt.cOgUHash.length).indexOf(\'?\') !== -1 ? \'?\' : location.search;\n        if (window.history && window.history.replaceState) {\n            var ogU = location.pathname + window._cf_chl_opt.cOgUQuery + window._cf_chl_opt.cOgUHash;\n            history.replaceState(null, null, "\\/users\\/sign_in?__cf_chl_rt_tk=yEH1.9z1LJpq3YZNo8N4wTDNIXgr.S8eP24Qz64n0Fo-1669515374-0-gaNycGzNB2U" + window._cf_chl_opt.cOgUHash);\n            cpo.onload = function() {\n                history.replaceState(null, null, ogU);\n            };\n        }\n        document.getElementsByTagName(\'head\')[0].appendChild(cpo);\n    }());\n</script>\n\n</div>\n\n    <hr />\n  </div>\n</body>\n</html>"""

        responses = {"response": Response(None, content, None, 200, None, None, None)}

        result = check_bad_response_cloudflare(responses, print_output=False)
        self.assertFalse(result.passed)


class KasadaTestCase(TestCase):
    def test_kasada_blocked_content(self):
        content = b"""<!DOCTYPE html><html><head></head><body><script>window.KPSDK={};KPSDK.now=typeof performance!=='undefined'&&performance.now?performance.now.bind(performance):Date.now.bind(Date);KPSDK.start=KPSDK.now();</script><script src="/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/ips.js?KP_UIDz=0D9xVG2Ip5eHSs6ZwGDJpAGT6uIWNHUgspsmZEfLljMmX77gXo6bBoMN20oeZuHoeDAkszo9OCe5IVNHjNjyv7ICjEyf1P3ZgWgqgN0ru799vvQbYCKbSEjpWL9efcxFtnVwGcHCoSMwk0zOO6PpJq6FD"></script></body></html>"""

        responses = {"response": Response(None, content, None, 429, None, None, None)}
        result = check_bad_response_kasada(responses, print_output=False)
        self.assertFalse(result.passed)

    def test_kasada_normal_content(self):
        content = b"""<<!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="">
            <title>Minimal base.html</title>
        </head>
        <body>

            <!-- Delete this part -->
            <h1>base.html</h1>
            <p>The absolute minimum <code>base.html</code> to get your project started.</p>
            <h3>Usage:</h3>
            <pre>
              curl https://basehtml.xyz &gt; base.html
            </pre>
            <a href="https://github.com/sesh/base.html">more info</a>
            <script src="/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/ips.js?KP_UIDz=0D9xVG2Ip5eHSs6ZwGDJpAGT6uIWNHUgspsmZEfLljMmX77gXo6bBoMN20oeZuHoeDAkszo9OCe5IVNHjNjyv7ICjEyf1P3ZgWgqgN0ru799vvQbYCKbSEjpWL9efcxFtnVwGcHCoSMwk0zOO6PpJq6FD"></script>
        </body>
        </html>"""

        responses = {"response": Response(None, content, None, 200, None, None, None)}
        result = check_bad_response_kasada(responses, print_output=False)
        self.assertTrue(result.passed)