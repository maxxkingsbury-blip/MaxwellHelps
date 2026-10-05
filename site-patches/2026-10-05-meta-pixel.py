"""Site patch 2026-10-05: add Meta Pixel (2256759738577487) + intake-click Lead event
to every page, and update the Privacy and Cookie policies to disclose it.
Idempotent: safe to run more than once."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PID = "2256759738577487"
SNIP = f"""<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('set', 'autoConfig', false, '{PID}');
fbq('init', '{PID}');
fbq('track', 'PageView');
document.addEventListener('click', function (e) {{
  var a = e.target.closest && e.target.closest('a[href*="healthsherpa.com/intake"]');
  if (a) fbq('track', 'Lead', {{content_name: 'Start intake form'}});
}});
</script>
<noscript><img height="1" width="1" style="display:none" alt=""
src="https://www.facebook.com/tr?id={PID}&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
"""
OPT = '<a href="https://www.facebook.com/adpreferences/ad_settings" target="_blank" rel="noopener">Facebook ad preferences</a>'


def edit(name, pairs):
    p = ROOT / name
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if new in t:
            continue
        if t.count(old) != 1:
            raise SystemExit(f"{name}: expected exactly one match for {old[:60]!r}")
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")


for page in ["index.html", "medicare-101.html", "privacy.html", "cookies.html", "terms.html"]:
    edit(page, [("</head>", SNIP + "</head>")])

edit("privacy.html", [
    ("Effective September 28, 2026", "Effective October 5, 2026"),
    ("<p>This website has no contact forms, user accounts, analytics, advertising or tracking cookies. Specifically:</p>",
     "<p>This website has no contact forms or user accounts. It uses one advertising tool, the Meta Pixel, described below. Specifically:</p>"),
    ("<li><strong>Fonts.</strong>",
     "<li><strong>Meta Pixel.</strong> We use the Meta Pixel (from Meta Platforms, which runs Facebook and Instagram) to measure our ads. When you visit a page, your browser sends Meta the page address, your IP address, browser details and a Meta cookie. When you click &ldquo;Start intake form,&rdquo; it also tells Meta that the button was clicked. We do not send Meta your plan-fit answers or anything you type into the intake form. Meta may use this information to show and measure ads, under Meta&rsquo;s own privacy policy. You can limit this in your "
     + OPT + " or by blocking third-party cookies in your browser.</li>\n<li><strong>Fonts.</strong>"),
    ("If our practices change, for example if analytics are added, we will update this page and the effective date above.",
     "If our practices change, we will update this page and the effective date above."),
])

edit("cookies.html", [
    ('content="Maxwell Helps cookie policy: this site does not use cookies."',
     'content="Maxwell Helps cookie policy: the only cookies come from the Meta Pixel used to measure our ads."'),
    ("This website does not use cookies or tracking. Here are the details.",
     "This website uses one tracking tool, the Meta Pixel, to measure our ads. Here are the details."),
    ("Effective September 28, 2026", "Effective October 5, 2026"),
    ("<p>No. This website does not set any cookies and does not store anything in your browser's local storage. It has no analytics, advertising pixels, chat widgets, social media plugins or embedded videos.</p>",
     "<p>Only one kind. The Meta Pixel sets Meta cookies (such as <code>_fbp</code>) so we can see which of our Facebook and Instagram ads bring visitors to this site and how many people click &ldquo;Start intake form.&rdquo; We do not send Meta your plan-fit answers or anything you type into the intake form. The site has no other analytics, chat widgets, social media plugins or embedded videos.</p>"),
    ("<p>No. Because the site uses no cookies and no tracking, there is nothing to accept, so no cookie banner is shown.</p>",
     "<p>No banner is shown. You can limit how Meta uses this information in your " + OPT
     + ", block third-party cookies in your browser, or use a browser extension that blocks trackers. The site works the same either way.</p>"),
    ("<li><strong>GitHub Pages:</strong>",
     "<li><strong>Meta Pixel:</strong> your browser loads Meta&rsquo;s script from connect.facebook.net and sends page visits and intake-button clicks to Meta, which receives your IP address and browser details. Meta&rsquo;s privacy policy applies.</li>\n<li><strong>GitHub Pages:</strong>"),
    ("If we ever add cookies or analytics, we will update this policy first and ask for your consent where the law requires it.",
     "If we add other cookies or analytics, we will update this policy first and ask for your consent where the law requires it."),
])
print("patch applied")
