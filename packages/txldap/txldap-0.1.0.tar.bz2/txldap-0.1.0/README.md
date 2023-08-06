txldap
======

txldap is a Twisted wrapper for [python-ldap][docs].

### Requirements

* [python-ldap](http://www.python-ldap.org/)
* [Twisted](http://twistedmatrix.com/)

### Example

    import txldap
    from twisted.internet import defer, reactor

    @defer.inlineCallbacks
    def main():
        try:
            l = txldap.Connection('ldaps://ldap.example.net')
            yield l.bind('uid=silas,ou=People,dc=example,dc=net', 'password')
            results = yield l.search('ou=People,dc=example,dc=net', txldap.SCOPE_SUBTREE, 'uid=silas')
            print results
        except txldap.LDAPError, error:
            print 'Error: %s' % error
        reactor.stop()

    if __name__ == '__main__':
        main()
        reactor.run()

### Licenses

This work is licensed under the MIT License (see the LICENSE file).

[docs]: http://www.python-ldap.org/doc/html/ldap.html "python-ldap documentation"
