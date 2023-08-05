function removeRelation(rtype, seid, oeid) {
    var d = asyncRemoteExec('remove_relation', rtype, seid, oeid);
    d.addCallback(function() {
        window.location.reload();
    });
}
