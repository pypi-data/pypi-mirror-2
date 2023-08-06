jq(document).ready(function() {
    jq('a.hidden-email').each(function() {
        jq.pyproxy_call('jq_reveal_email',
                        {'uid': jq(this).attr('rel')});
    });
});