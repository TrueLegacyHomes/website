#!/bin/bash

# Tracking code to add after <head>
HEAD_TRACKING='<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'"'"'gtm.start'"'"':
new Date().getTime(),event:'"'"'gtm.js'"'"'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='"'"'dataLayer'"'"'?'"'"'&l='"'"'+l:'"'"''"'"';j.async=true;j.src=
'"'"'https://www.googletagmanager.com/gtm.js?id='"'"'+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'"'"'script'"'"','"'"'dataLayer'"'"','"'"'GTM-T3LD72P'"'"');</script>
<!-- End Google Tag Manager -->
<!-- Facebook Domain Verification -->
<meta name="facebook-domain-verification" content="3h2v8x84iqs6m8yhoz4fnmp9w3c83y" />
<!-- Hotjar Tracking Code -->
<script>
(function(h,o,t,j,a,r){
    h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
    h._hjSettings={hjid:2420292,hjsv:6};
    a=o.getElementsByTagName('"'"'head'"'"')[0];
    r=o.createElement('"'"'script'"'"');r.async=1;
    r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
    a.appendChild(r);
})(window,document,'"'"'https://static.hotjar.com/c/hotjar-'"'"','"'"'.js?sv='"'"');
</script>'

# GTM noscript to add after <body>
BODY_TRACKING='<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T3LD72P"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->'

echo "$HEAD_TRACKING" > /tmp/head_tracking.txt
echo "$BODY_TRACKING" > /tmp/body_tracking.txt
