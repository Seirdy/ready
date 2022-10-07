import json
import sys
import os
import datetime
import urllib

from ready.checks.cookies import (
    check_cookies_should_be_httponly,
    check_cookies_should_be_samesite,
    check_cookies_should_be_secure,
)
from ready.checks.corp_coop_coep import (
    check_cross_origin_embedder_policy_should_be_require_corp,
    check_cross_origin_opener_policy_should_be_sameorigin,
    check_cross_origin_resource_policy_should_be_sameorigin,
)
from ready.checks.cors import (
    check_access_control_allow_origin_is_not_wildcard,
    check_expect_access_control_allow_origin_in_response,
)
from ready.checks.csp import (
    check_csp_must_not_include_unsafe_inline,
    check_csp_should_exist,
    check_csp_should_include_reporturi,
    check_csp_should_only_include_valid_directives,
    check_csp_should_start_with_defaultsrc_none,
    check_csp_upgrade_insecure_requests,
    check_csp_must_not_include_unsafe_eval,
)
from ready.checks.email import (
    check_dmarc_record_should_exist,
    check_spf_dns_record_does_not_exist,
    check_spf_record_should_exist,
    check_spf_txt_record_should_disallow_all,
    check_spf_uses_less_than_10_requests,
)
from ready.checks.expect_ct import (
    check_expect_ct_header_should_exist_in_response,
    check_expect_ct_header_should_include_report_uri,
)
from ready.checks.hsts import (
    check_hsts_header_should_be_included_in_response,
    check_hsts_header_should_have_a_long_max_age,
    check_hsts_header_should_have_includesubdomains,
    check_hsts_header_should_have_preload,
)
from ready.checks.html import (
    check_frame_ancestors_should_exist,
    check_html_includes_rel_icon,
    check_html_includes_title,
    check_html_meta_charset,
    check_html_script_tags_use_sri,
    check_html_should_not_use_schemeless_urls,
    check_html_starts_with_doctype,
    check_html_tag_includes_lang,
    check_permissions_policy_should_exist,
    check_referrer_policy_should_be_set,
    check_x_content_type_options_should_be_nosniff,
    check_x_xss_protection_should_be_set,
    check_x_dns_prefetch_control_is_off,
)
from ready.checks.leaky_headers import check_should_not_include_leaky_headers
from ready.checks.report_to import check_report_to_header_should_be_included_in_response
from ready.checks.ssl import (
    check_ssl_certificate_should_be_trusted,
    check_ssl_expiry_should_be_greater_than_five_days,
    check_ssl_expiry_should_be_less_than_one_year,
    check_dns_caa_record_should_exist,
    check_ssl_connection_fails_with_tls_1_1,
    check_ssl_connection_fails_with_tls_1_0,
)

from ready.checks.status import check_http_response_should_be_200
from ready.checks.redirect import check_http_to_https_redirect
from ready.checks.content import (
    check_http_cache_control_is_included,
    check_http_content_type_header_contains_charset,
    check_http_expires_header_is_not_set,
    check_http_response_should_be_gzipped,
    check_http_response_should_include_content_type,
)
from ready.checks.well_known import (
    check_favicon_is_served,
    check_robots_txt_exists,
    check_security_txt_exists,
)
from ready.checks.ns import check_at_least_two_nameservers_configured

from ready.checks.swagger import check_swagger_should_not_return_200

from ready.thttp import request, pretty


DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0",
}


def response_or_none(url, **kwargs):
    try:
        response = request(url, **kwargs)
        return response
    except urllib.error.URLError:
        return None
    except Exception as e:
        print(url, type(e))
        return None


def ready(domain, print_headers=False, print_content=False, json_output=False, hide_output=False, fuzz=False, extra_args={}):
    responses = {
        "http_response": response_or_none(f"http://{domain}", verify=False, headers=DEFAULT_HEADERS, timeout=3),
        "response": response_or_none(f"https://{domain}", verify=False, headers=DEFAULT_HEADERS, timeout=3),
    }

    if not responses["response"]:
        print(f"No response from https://{domain}")
        return None

    responses["security_txt_response"] = response_or_none(
        f"https://{domain}/.well-known/security.txt",
        headers=DEFAULT_HEADERS,
        timeout=3,
    )

    responses["robots_txt_response"] = response_or_none(f"https://{domain}/robots.txt", headers=DEFAULT_HEADERS, timeout=3)

    responses["favicon_response"] = response_or_none(
        f"https://{domain}/favicon.ico",
        verify=False,
        headers=DEFAULT_HEADERS,
        timeout=3,
    )

    responses["dns_ns_response"] = response_or_none(f"https://dns.google/resolve?name={domain}&type=NS")
    responses["dns_mx_response"] = response_or_none(f"https://dns.google/resolve?name={domain}&type=MX")
    responses["dns_txt_response"] = response_or_none(f"https://dns.google/resolve?name={domain}&type=TXT")
    responses["dns_spf_response"] = response_or_none(f"https://dns.google/resolve?name={domain}&type=SPF")
    responses["dns_caa_response"] = response_or_none(f"https://dns.google/resolve?name={domain}&type=CAA")
    responses["dns_dmarc_response"] = response_or_none(f"https://dns.google/resolve?name=_dmarc.{domain}&type=TXT")

    if responses["dns_mx_response"] and responses["dns_mx_response"].status == 429:
        print("DNS Queries have been rate limited")
        print(responses["dns_mx_response"])
        sys.exit(1)

    checks = []
    is_html = "html" in responses["response"].headers.get("content-type", "")

    # TODO: accept argument to _not_ print to stdout
    if print_headers:
        pretty(responses["response"], content=False)
        print()

    if print_content:
        print(responses["response"].content)

    checks = [
        check_http_to_https_redirect,
        check_http_response_should_be_200,
        check_http_response_should_include_content_type,
        check_hsts_header_should_be_included_in_response,
        check_hsts_header_should_have_a_long_max_age,
        check_hsts_header_should_have_includesubdomains,
        check_hsts_header_should_have_preload,
        check_csp_should_exist,
        check_csp_should_start_with_defaultsrc_none,
        check_csp_must_not_include_unsafe_inline,
        check_csp_must_not_include_unsafe_eval,
        check_csp_upgrade_insecure_requests,
        check_csp_should_include_reporturi,
        check_csp_should_only_include_valid_directives,
        check_report_to_header_should_be_included_in_response,
        check_robots_txt_exists,
        check_security_txt_exists,
        check_favicon_is_served,
        check_http_response_should_be_gzipped,
        check_http_content_type_header_contains_charset,
        check_http_expires_header_is_not_set,
        check_http_cache_control_is_included,
        check_referrer_policy_should_be_set,
        check_cross_origin_resource_policy_should_be_sameorigin,
        check_cross_origin_opener_policy_should_be_sameorigin,
        check_cross_origin_embedder_policy_should_be_require_corp,
        check_expect_ct_header_should_exist_in_response,
        check_expect_ct_header_should_include_report_uri,
        check_should_not_include_leaky_headers,
        check_ssl_expiry_should_be_less_than_one_year,
        check_ssl_expiry_should_be_greater_than_five_days,
        check_ssl_certificate_should_be_trusted,
        check_ssl_connection_fails_with_tls_1_1,
        check_ssl_connection_fails_with_tls_1_0,
        check_dns_caa_record_should_exist,
        check_at_least_two_nameservers_configured,
        check_cookies_should_be_samesite,
        check_cookies_should_be_secure,
        check_cookies_should_be_httponly,
    ]

    if is_html:
        checks.extend(
            [
                check_permissions_policy_should_exist,
                check_frame_ancestors_should_exist,
                check_x_content_type_options_should_be_nosniff,
                check_x_xss_protection_should_be_set,
                check_html_starts_with_doctype,
                check_html_tag_includes_lang,
                check_html_meta_charset,
                check_html_includes_title,
                check_html_includes_rel_icon,
                check_html_should_not_use_schemeless_urls,
                check_html_script_tags_use_sri,
                check_x_dns_prefetch_control_is_off,
            ]
        )

    if not is_html:
        # checks for API endpoints
        checks.extend(
            [
                check_expect_access_control_allow_origin_in_response,
                check_access_control_allow_origin_is_not_wildcard,
            ]
        )

    if responses["dns_mx_response"] and "Answer" in responses["dns_mx_response"].json:
        checks.extend(
            [
                check_spf_record_should_exist,
                check_spf_dns_record_does_not_exist,
                check_spf_txt_record_should_disallow_all,
                check_dmarc_record_should_exist,
                check_spf_uses_less_than_10_requests,
            ]
        )

    if fuzz:
        checks.append(check_swagger_should_not_return_200)

    extra_args["print_output"] = not hide_output

    results = []
    for c in checks:
        result = c(responses, domain=domain, **extra_args)
        if result:
            results.append(result)

    if json_output:
        print(
            json.dumps(
                {
                    "checks": {
                        r.check: {
                            "passed": r.passed,
                            "message": r.message,
                        }
                        for r in results
                    },
                    "when": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                indent=2,
            )
        )

    return results


def parse_args(args):
    result = {
        a.split("=")[0]: int(a.split("=")[1])
        if "=" in a and a.split("=")[1].isnumeric()
        else a.split("=")[1]
        if "=" in a
        else True
        for a in args
        if "--" in a
    }
    result["[]"] = [a for a in args if not a.startswith("--")]
    return result


def usage():
    print("ready")
    print("")
    print("Usage: ready.py [--headers] [--content] [--json] [--quiet] [--score] [--fuzz] <domain>")
    print("")
    print("  --headers     Output the headers from the HTTPS request made to the domain")
    print("  --content     Output the content from the HTTPS request made to the domain")
    print("  --fuzz        Include checks that fuzz urls (only run this on your own domain)")
    print("  --json        Provide JSON output")
    print("  --quiet       No text output")
    print("  --score       Print a score out of 100 for this domain")
    print("  --doc         Print the list of check names")


def cli():
    args = parse_args(sys.argv[1:])

    if "--doc" in args:
        for filename in os.listdir("./ready/checks"):
            if filename.endswith(".py"):
                for line in open("./ready/checks/" + filename).readlines():
                    if line.strip().startswith("# Check: "):
                        print(line.strip().replace("# Check: ", "- "))
        sys.exit()

    if "--help" in args or not args["[]"]:
        usage()
        sys.exit()

    results = ready(
        args["[]"][0],
        print_headers=args.get("--headers", False),
        print_content=args.get("--content", False),
        json_output=args.get("--json", False),
        hide_output=args.get("--quiet", False),
        fuzz=args.get("--fuzz", False)
    )

    if "--score" in args:
        print(f"Score: {100 - 3 * len([x for x in results if not x.passed and not x.warn_on_fail])}/100")


if __name__ == "__main__":
    cli()
