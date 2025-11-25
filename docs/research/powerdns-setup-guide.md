# Research: PowerDNS authoritative server configuration best practices

## Metadata

- **Query:** PowerDNS authoritative server configuration best practices
- **Generated:** 2025-11-25 01:48:29
- **Script:** firecrawl_sdk_research.py
- **Search Results:** 10
- **Scraped Pages:** 8

## Summary

Found 10 search results, successfully scraped 8 pages.

- **High Quality Sources:** 0/8

## Sources

1. [Authoritative Server Settings — PowerDNS Authoritative Server  documentation](https://doc.powerdns.com/authoritative/settings.html) ✓
   - Domain: `doc.powerdns.com`
   - Quality Score: 5
2. [Setting up a self-hosted authoritative DNS server with PowerDNS - Tarneo's blog
](https://tarneo.fr/posts/powerdns/) ✓
   - Domain: `tarneo.fr`
   - Quality Score: 5
3. [PowerDNS Configuration Requirements](https://docs.cloudblue.com/cbc/21.0/DNS-Hosting-Services/PowerDNS-Configuration-Requirements.htm) ✓
   - Domain: `docs.cloudblue.com`
   - Quality Score: 5
4. [
Hosting your own authoritative DNS servers using PowerDNS | Bluemedia

  ](https://bluemedia.dev/blog/authorative-dns-server-using-powerdns/)
   - Domain: `bluemedia.dev`
   - Quality Score: 3
5. [Guides and How Tos — PowerDNS Authoritative Server  documentation](https://doc.powerdns.com/authoritative/guides/index.html)
   - Domain: `doc.powerdns.com`
   - Quality Score: 3
6. [Performance and Tuning — PowerDNS Authoritative Server  documentation](https://doc.powerdns.com/authoritative/performance.html)
   - Domain: `doc.powerdns.com`
   - Quality Score: 3
7. [PowerDNS Authoritative Nameserver — PowerDNS Authoritative Server  documentation](https://doc.powerdns.com/authoritative/index.html)
   - Domain: `doc.powerdns.com`
   - Quality Score: 3
8. [Local DNS configuration and best practices - Super User](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices)
   - Domain: `superuser.com`
   - Quality Score: 3

## Content

### 1. Authoritative Server Settings — PowerDNS Authoritative Server  documentation

**Source:** [https://doc.powerdns.com/authoritative/settings.html](https://doc.powerdns.com/authoritative/settings.html)
**Domain:** `doc.powerdns.com`
**Quality Score:** 5

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/security-advisories/index.html "Security Advisories") \|
- [previous](https://doc.powerdns.com/authoritative/manpages/ixfrdist.yml.5.html "ixfrdist.yml") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

[PowerDNS Authoritative Server](https://doc.powerdns.com/authoritative/indexTOC.html)

#### Previous topic

[ixfrdist.yml](https://doc.powerdns.com/authoritative/manpages/ixfrdist.yml.5.html "previous chapter")

#### Next topic

[Security Advisories](https://doc.powerdns.com/authoritative/security-advisories/index.html "next chapter")

## Contents

- [PowerDNS Authoritative Nameserver](https://doc.powerdns.com/authoritative/index.html)
- [Installing PowerDNS](https://doc.powerdns.com/authoritative/installation.html)
- [Upgrade Notes](https://doc.powerdns.com/authoritative/upgrading.html)
- [DNS Modes of Operation](https://doc.powerdns.com/authoritative/modes-of-operation.html)
- [Migrating to PowerDNS](https://doc.powerdns.com/authoritative/migration.html)
- [Running and Operating](https://doc.powerdns.com/authoritative/running.html)
- [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html)
- [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html)
- [DNSSEC](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [Per zone settings: Domain Metadata](https://doc.powerdns.com/authoritative/domainmetadata.html)
- [Dynamic DNS Update (RFC 2136)](https://doc.powerdns.com/authoritative/dnsupdate.html)
- [Catalog Zones (RFC 9432)](https://doc.powerdns.com/authoritative/catalog.html)
- [TSIG](https://doc.powerdns.com/authoritative/tsig.html)
- [Views](https://doc.powerdns.com/authoritative/views.html)
- [Lua Records](https://doc.powerdns.com/authoritative/lua-records/index.html)
- [Guides and How Tos](https://doc.powerdns.com/authoritative/guides/index.html)
- [Backends](https://doc.powerdns.com/authoritative/backends/index.html)
- [Built-in Webserver and HTTP API](https://doc.powerdns.com/authoritative/http-api/index.html)
- [Manual Pages](https://doc.powerdns.com/authoritative/manpages/index.html)
- [Authoritative Server Settings](https://doc.powerdns.com/authoritative/settings.html#)
  - [`8bit-dns`](https://doc.powerdns.com/authoritative/settings.html#bit-dns)
  - [`allow-axfr-ips`](https://doc.powerdns.com/authoritative/settings.html#allow-axfr-ips)
  - [`allow-dnsupdate-from`](https://doc.powerdns.com/authoritative/settings.html#allow-dnsupdate-from)
  - [`allow-notify-from`](https://doc.powerdns.com/authoritative/settings.html#allow-notify-from)
  - [`allow-unsigned-autoprimary`](https://doc.powerdns.com/authoritative/settings.html#allow-unsigned-autoprimary)
  - [`allow-unsigned-notify`](https://doc.powerdns.com/authoritative/settings.html#allow-unsigned-notify)
  - [`allow-unsigned-supermaster`](https://doc.powerdns.com/authoritative/settings.html#allow-unsigned-supermaster)
  - [`also-notify`](https://doc.powerdns.com/authoritative/settings.html#also-notify)
  - [`any-to-tcp`](https://doc.powerdns.com/authoritative/settings.html#any-to-tcp)
  - [`api`](https://doc.powerdns.com/authoritative/settings.html#api)
  - [`api-key`](https://doc.powerdns.com/authoritative/settings.html#api-key)
  - [`autosecondary`](https://doc.powerdns.com/authoritative/settings.html#autosecondary)
  - [`axfr-fetch-timeout`](https://doc.powerdns.com/authoritative/settings.html#axfr-fetch-timeout)
  - [`axfr-lower-serial`](https://doc.powerdns.com/authoritative/settings.html#axfr-lower-serial)
  - [`cache-ttl`](https://doc.powerdns.com/authoritative/settings.html#cache-ttl)
  - [`carbon-instance`](https://doc.powerdns.com/authoritative/settings.html#carbon-instance)
  - [`carbon-interval`](https://doc.powerdns.com/authoritative/settings.html#carbon-interval)
  - [`carbon-namespace`](https://doc.powerdns.com/authoritative/settings.html#carbon-namespace)
  - [`carbon-ourname`](https://doc.powerdns.com/authoritative/settings.html#carbon-ourname)
  - [`carbon-server`](https://doc.powerdns.com/authoritative/settings.html#carbon-server)
  - [`chroot`](https://doc.powerdns.com/authoritative/settings.html#chroot)
  - [`secondary-check-signature-freshness`](https://doc.powerdns.com/authoritative/settings.html#secondary-check-signature-freshness)
  - [`config-dir`](https://doc.powerdns.com/authoritative/settings.html#config-dir)
  - [`config-name`](https://doc.powerdns.com/authoritative/settings.html#config-name)
  - [`consistent-backends`](https://doc.powerdns.com/authoritative/settings.html#consistent-backends)
  - [`control-console`](https://doc.powerdns.com/authoritative/settings.html#control-console)
  - [`daemon`](https://doc.powerdns.com/authoritative/settings.html#daemon)
  - [`default-api-rectify`](https://doc.powerdns.com/authoritative/settings.html#default-api-rectify)
  - [`default-catalog-zone`](https://doc.powerdns.com/authoritative/settings.html#default-catalog-zone)
  - [`default-ksk-algorithm`](https://doc.powerdns.com/authoritative/settings.html#default-ksk-algorithm)
  - [`default-ksk-size`](https://doc.powerdns.com/authoritative/settings.html#default-ksk-size)
  - [`default-publish-cdnskey`](https://doc.powerdns.com/authoritative/settings.html#default-publish-cdnskey)
  - [`default-publish-cds`](https://doc.powerdns.com/authoritative/settings.html#default-publish-cds)
  - [`default-soa-content`](https://doc.powerdns.com/authoritative/settings.html#default-soa-content)
  - [`default-soa-edit`](https://doc.powerdns.com/authoritative/settings.html#default-soa-edit)
  - [`default-soa-edit-signed`](https://doc.powerdns.com/authoritative/settings.html#default-soa-edit-signed)
  - [`default-soa-mail`](https://doc.powerdns.com/authoritative/settings.html#default-soa-mail)
  - [`default-soa-name`](https://doc.powerdns.com/authoritative/settings.html#default-soa-name)
  - [`default-ttl`](https://doc.powerdns.com/authoritative/settings.html#default-ttl)
  - [`default-zsk-algorithm`](https://doc.powerdns.com/authoritative/settings.html#default-zsk-algorithm)
  - [`default-zsk-size`](https://doc.powerdns.com/authoritative/settings.html#default-zsk-size)
  - [`delay-notifications`](https://doc.powerdns.com/authoritative/settings.html#delay-notifications)
  - [`direct-dnskey`](https://doc.powerdns.com/authoritative/settings.html#direct-dnskey)
  - [`direct-dnskey-signature`](https://doc.powerdns.com/authoritative/settings.html#direct-dnskey-signature)
  - [`disable-axfr`](https://doc.powerdns.com/authoritative/settings.html#disable-axfr)
  - [`disable-axfr-rectify`](https://doc.powerdns.com/authoritative/settings.html#disable-axfr-rectify)
  - [`disable-syslog`](https://doc.powerdns.com/authoritative/settings.html#disable-syslog)
  - [`distributor-threads`](https://doc.powerdns.com/authoritative/settings.html#distributor-threads)
  - [`dname-processing`](https://doc.powerdns.com/authoritative/settings.html#dname-processing)
  - [`dnsproxy-udp-port-range`](https://doc.powerdns.com/authoritative/settings.html#dnsproxy-udp-port-range)
  - [`dnssec-key-cache-ttl`](https://doc.powerdns.com/authoritative/settings.html#dnssec-key-cache-ttl)
  - [`dnsupdate`](https://doc.powerdns.com/authoritative/settings.html#dnsupdate)
  - [`dnsupdate-require-tsig`](https://doc.powerdns.com/authoritative/settings.html#dnsupdate-require-tsig)
  - [`do-ipv6-additional-processing`](https://doc.powerdns.com/authoritative/settings.html#do-ipv6-additional-processing)
  - [`domain-metadata-cache-ttl`](https://doc.powerdns.com/authoritative/settings.html#domain-metadata-cache-ttl)
  - [`edns-cookie-secret`](https://doc.powerdns.com/authoritative/settings.html#edns-cookie-secret)
  - [`edns-subnet-processing`](https://doc.powerdns.com/authoritative/settings.html#edns-subnet-processing)
  - [`enable-gss-tsig`](https://doc.powerdns.com/authoritative/settings.html#enable-gss-tsig)
  - [`enable-lua-records`](https://doc.powerdns.com/authoritative/settings.html#enable-lua-records)
  - [`entropy-source`](https://doc.powerdns.com/authoritative/settings.html#entropy-source)
  - [`expand-alias`](https://doc.powerdns.com/authoritative/settings.html#expand-alias)
  - [`resolve-across-zones`](https://doc.powerdns.com/authoritative/settings.html#resolve-across-zones)
  - [`forward-dnsupdate`](https://doc.powerdns.com/authoritative/settings.html#forward-dnsupdate)
  - [`forward-notify`](https://doc.powerdns.com/authoritative/settings.html#forward-notify)
  - [`guardian`](https://doc.powerdns.com/authoritative/settings.html#guardian)
  - [`ignore-unknown-settings`](https://doc.powerdns.com/authoritative/settings.html#ignore-unknown-settings)
  - [`include-dir`](https://doc.powerdns.com/authoritative/settings.html#include-dir)
  - [`launch`](https://doc.powerdns.com/authoritative/settings.html#launch)
  - [`load-modules`](https://doc.powerdns.com/authoritative/settings.html#load-modules)
  - [`local-address`](https://doc.powerdns.com/authoritative/settings.html#local-address)
  - [`local-address-nonexist-fail`](https://doc.powerdns.com/authoritative/settings.html#local-address-nonexist-fail)
  - [`local-ipv6`](https://doc.powerdns.com/authoritative/settings.html#local-ipv6)
  - [`local-ipv6-nonexist-fail`](https://doc.powerdns.com/authoritative/settings.html#local-ipv6-nonexist-fail)
  - [`local-port`](https://doc.powerdns.com/authoritative/settings.html#local-port)
  - [`log-dns-details`](https://doc.powerdns.com/authoritative/settings.html#log-dns-details)
  - [`log-dns-queries`](https://doc.powerdns.com/authoritative/settings.html#log-dns-queries)
  - [`log-timestamp`](https://doc.powerdns.com/authoritative/settings.html#log-timestamp)
  - [`logging-facility`](https://doc.powerdns.com/authoritative/settings.html#logging-facility)
  - [`loglevel`](https://doc.powerdns.com/authoritative/settings.html#loglevel)
  - [`loglevel-show`](https://doc.powerdns.com/authoritative/settings.html#loglevel-show)
  - [`lua-axfr-script`](https://doc.powerdns.com/authoritative/settings.html#lua-axfr-script)
  - [`lua-consistent-hashes-cleanup-interval`](https://doc.powerdns.com/authoritative/settings.html#lua-consistent-hashes-cleanup-interval)
  - [`lua-consistent-hashes-expire-delay`](https://doc.powerdns.com/authoritative/settings.html#lua-consistent-hashes-expire-delay)
  - [`lua-global-include-dir`](https://doc.powerdns.com/authoritative/settings.html#lua-global-include-dir)
  - [`lua-health-checks-expire-delay`](https://doc.powerdns.com/authoritative/settings.html#lua-health-checks-expire-delay)
  - [`lua-health-checks-interval`](https://doc.powerdns.com/authoritative/settings.html#lua-health-checks-interval)
  - [`lua-prequery-script`](https://doc.powerdns.com/authoritative/settings.html#lua-prequery-script)
  - [`lua-records-exec-limit`](https://doc.powerdns.com/authoritative/settings.html#lua-records-exec-limit)
  - [`lua-records-insert-whitespace`](https://doc.powerdns.com/authoritative/settings.html#lua-records-insert-whitespace)
  - [`master`](https://doc.powerdns.com/authoritative/settings.html#master)
  - [`max-cache-entries`](https://doc.powerdns.com/authoritative/settings.html#max-cache-entries)
  - [`max-ent-entries`](https://doc.powerdns.com/authoritative/settings.html#max-ent-entries)
  - [`max-include-depth`](https://doc.powerdns.com/authoritative/settings.html#max-include-depth)
  - [`max-generate-steps`](https://doc.powerdns.com/authoritative/settings.html#max-generate-steps)
  - [`max-nsec3-iterations`](https://doc.powerdns.com/authoritative/settings.html#max-nsec3-iterations)
  - [`max-packet-cache-entries`](https://doc.powerdns.com/authoritative/settings.html#max-packet-cache-entries)
  - [`max-queue-length`](https://doc.powerdns.com/authoritative/settings.html#max-queue-length)
  - [`max-signature-cache-entries`](https://doc.powerdns.com/authoritative/settings.html#max-signature-cache-entries)
  - [`max-tcp-connection-duration`](https://doc.powerdns.com/authoritative/settings.html#max-tcp-connection-duration)
  - [`max-tcp-connections`](https://doc.powerdns.com/authoritative/settings.html#max-tcp-connections)
  - [`max-tcp-connections-per-client`](https://doc.powerdns.com/authoritative/settings.html#max-tcp-connections-per-client)
  - [`max-tcp-transactions-per-conn`](https://doc.powerdns.com/authoritative/settings.html#max-tcp-transactions-per-conn)
  - [`module-dir`](https://doc.powerdns.com/authoritative/settings.html#module-dir)
  - [`negquery-cache-ttl`](https://doc.powerdns.com/authoritative/settings.html#negquery-cache-ttl)
  - [`no-config`](https://doc.powerdns.com/authoritative/settings.html#no-config)
  - [`no-shuffle`](https://doc.powerdns.com/authoritative/settings.html#no-shuffle)
  - [`non-local-bind`](https://doc.powerdns.com/authoritative/settings.html#non-local-bind)
  - [`only-notify`](https://doc.powerdns.com/authoritative/settings.html#only-notify)
  - [`outgoing-axfr-expand-alias`](https://doc.powerdns.com/authoritative/settings.html#outgoing-axfr-expand-alias)
  - [`overload-queue-length`](https://doc.powerdns.com/authoritative/settings.html#overload-queue-length)
  - [`prevent-self-notification`](https://doc.powerdns.com/authoritative/settings.html#prevent-self-notification)
  - [`primary`](https://doc.powerdns.com/authoritative/settings.html#primary)
  - [`proxy-protocol-from`](https://doc.powerdns.com/authoritative/settings.html#proxy-protocol-from)
  - [`proxy-protocol-maximum-size`](https://doc.powerdns.com/authoritative/settings.html#proxy-protocol-maximum-size)
  - [`query-cache-ttl`](https://doc.powerdns.com/authoritative/settings.html#query-cache-ttl)
  - [`query-local-address`](https://doc.powerdns.com/authoritative/settings.html#query-local-address)
  - [`query-local-address6`](https://doc.powerdns.com/authoritative/settings.html#query-local-address6)
  - [`query-logging`](https://doc.powerdns.com/authoritative/settings.html#query-logging)
  - [`queue-limit`](https://doc.powerdns.com/authoritative/settings.html#queue-limit)
  - [`receiver-threads`](https://doc.powerdns.com/authoritative/settings.html#receiver-threads)
  - [`resolver`](https://doc.powerdns.com/authoritative/settings.html#resolver)
  - [`retrieval-threads`](https://doc.powerdns.com/authoritative/settings.html#retrieval-threads)
  - [`reuseport`](https://doc.powerdns.com/authoritative/settings.html#reuseport)
  - [`rng`](https://doc.powerdns.com/authoritative/settings.html#rng)
  - [`secondary`](https://doc.powerdns.com/authoritative/settings.html#secondary)
  - [`secondary-do-renotify`](https://doc.powerdns.com/authoritative/settings.html#secondary-do-renotify)
  - [`security-poll-suffix`](https://doc.powerdns.com/authoritative/settings.html#security-poll-suffix)
  - [`send-signed-notify`](https://doc.powerdns.com/authoritative/settings.html#send-signed-notify)
  - [`server-id`](https://doc.powerdns.com/authoritative/settings.html#server-id)
  - [`setgid`](https://doc.powerdns.com/authoritative/settings.html#setgid)
  - [`setuid`](https://doc.powerdns.com/authoritative/settings.html#setuid)
  - [`signing-threads`](https://doc.powerdns.com/authoritative/settings.html#signing-threads)
  - [`slave`](https://doc.powerdns.com/authoritative/settings.html#slave)
  - [`slave-cycle-interval`](https://doc.powerdns.com/authoritative/settings.html#slave-cycle-interval)
  - [`slave-renotify`](https://doc.powerdns.com/authoritative/settings.html#slave-renotify)
  - [`soa-expire-default`](https://doc.powerdns.com/authoritative/settings.html#soa-expire-default)
  - [`soa-minimum-ttl`](https://doc.powerdns.com/authoritative/settings.html#soa-minimum-ttl)
  - [`soa-refresh-default`](https://doc.powerdns.com/authoritative/settings.html#soa-refresh-default)
  - [`soa-retry-default`](https://doc.powerdns.com/authoritative/settings.html#soa-retry-default)
  - [`socket-dir`](https://doc.powerdns.com/authoritative/settings.html#socket-dir)
  - [`superslave`](https://doc.powerdns.com/authoritative/settings.html#superslave)
  - [`svc-autohints`](https://doc.powerdns.com/authoritative/settings.html#svc-autohints)
  - [`tcp-control-address`](https://doc.powerdns.com/authoritative/settings.html#tcp-control-address)
  - [`tcp-control-port`](https://doc.powerdns.com/authoritative/settings.html#tcp-control-port)
  - [`tcp-control-range`](https://doc.powerdns.com/authoritative/settings.html#tcp-control-range)
  - [`tcp-control-secret`](https://doc.powerdns.com/authoritative/settings.html#tcp-control-secret)
  - [`tcp-fast-open`](https://doc.powerdns.com/authoritative/settings.html#tcp-fast-open)
  - [`tcp-idle-timeout`](https://doc.powerdns.com/authoritative/settings.html#tcp-idle-timeout)
  - [`traceback-handler`](https://doc.powerdns.com/authoritative/settings.html#traceback-handler)
  - [`trusted-notification-proxy`](https://doc.powerdns.com/authoritative/settings.html#trusted-notification-proxy)
  - [`udp-truncation-threshold`](https://doc.powerdns.com/authoritative/settings.html#udp-truncation-threshold)
  - [`upgrade-unknown-types`](https://doc.powerdns.com/authoritative/settings.html#upgrade-unknown-types)
  - [`version-string`](https://doc.powerdns.com/authoritative/settings.html#version-string)
  - [`views`](https://doc.powerdns.com/authoritative/settings.html#views)
  - [`webserver`](https://doc.powerdns.com/authoritative/settings.html#webserver)
  - [`webserver-address`](https://doc.powerdns.com/authoritative/settings.html#webserver-address)
  - [`webserver-allow-from`](https://doc.powerdns.com/authoritative/settings.html#webserver-allow-from)
  - [`webserver-hash-plaintext-credentials`](https://doc.powerdns.com/authoritative/settings.html#webserver-hash-plaintext-credentials)
  - [`webserver-loglevel`](https://doc.powerdns.com/authoritative/settings.html#webserver-loglevel)
  - [`webserver-max-bodysize`](https://doc.powerdns.com/authoritative/settings.html#webserver-max-bodysize)
  - [`webserver-connection-timeout`](https://doc.powerdns.com/authoritative/settings.html#webserver-connection-timeout)
  - [`webserver-password`](https://doc.powerdns.com/authoritative/settings.html#webserver-password)
  - [`webserver-port`](https://doc.powerdns.com/authoritative/settings.html#webserver-port)
  - [`webserver-print-arguments`](https://doc.powerdns.com/authoritative/settings.html#webserver-print-arguments)
  - [`write-pid`](https://doc.powerdns.com/authoritative/settings.html#write-pid)
  - [`workaround-11804`](https://doc.powerdns.com/authoritative/settings.html#workaround-11804)
  - [`xfr-cycle-interval`](https://doc.powerdns.com/authoritative/settings.html#xfr-cycle-interval)
  - [`xfr-max-received-mbytes`](https://doc.powerdns.com/authoritative/settings.html#xfr-max-received-mbytes)
  - [`zone-cache-refresh-interval`](https://doc.powerdns.com/authoritative/settings.html#zone-cache-refresh-interval)
  - [`zone-metadata-cache-ttl`](https://doc.powerdns.com/authoritative/settings.html#zone-metadata-cache-ttl)
- [Security Advisories](https://doc.powerdns.com/authoritative/security-advisories/index.html)
- [Changelogs](https://doc.powerdns.com/authoritative/changelog/index.html)
- [End of life statements](https://doc.powerdns.com/authoritative/appendices/EOL.html)
- [Frequently Asked Questions](https://doc.powerdns.com/authoritative/appendices/FAQ.html)
- [Backend writers’ guide](https://doc.powerdns.com/authoritative/appendices/backend-writers-guide.html)
- [Compiling PowerDNS](https://doc.powerdns.com/authoritative/appendices/compiling.html)
- [Cryptographic software and export control](https://doc.powerdns.com/authoritative/appendices/crypto-export.html)
- [Internals](https://doc.powerdns.com/authoritative/appendices/internals.html)
- [Supported Record Types](https://doc.powerdns.com/authoritative/appendices/types.html)
- [PowerDNS/dnsdist license](https://doc.powerdns.com/authoritative/common/license.html)

### This Page

- [Show Source](https://doc.powerdns.com/authoritative/_sources/settings.rst.txt)

1. [Docs](https://doc.powerdns.com/authoritative/indexTOC.html)
2. Authoritative Server Settings

# Authoritative Server Settings [¶](https://doc.powerdns.com/authoritative/settings.html\#authoritative-server-settings "Permalink to this headline")

All PowerDNS Authoritative Server settings are listed here, excluding
those that originate from backends, which are documented in the relevant
chapters. These settings can be set inside `pdns.conf` or on the
commandline when invoking the `pdns` binary.

You can use `+=` syntax to set some variables incrementally, but this
requires you to have at least one non-incremental setting for the
variable to act as base setting. This is mostly useful for
[include-dir](https://doc.powerdns.com/authoritative/settings.html#setting-include-dir) directive.

For boolean settings, specifying the name of the setting without a value
means `yes`.

## `8bit-dns` [¶](https://doc.powerdns.com/authoritative/settings.html\#bit-dns "Permalink to this headline")

- Boolean
- Default: no

Allow 8 bit DNS queries.

## `allow-axfr-ips` [¶](https://doc.powerdns.com/authoritative/settings.html\#allow-axfr-ips "Permalink to this headline")

- IP ranges, separated by commas
- Default: 127.0.0.0/8,::1

If set, only these IP addresses or netmasks will be able to perform
AXFR without TSIG.

Warning

This setting only applies to AXFR without TSIG keys. If you allow a TSIG key to perform an AXFR,
this setting will not be checked for that transfer, and the client will be able to perform the AXFR
from everywhere.

## `allow-dnsupdate-from` [¶](https://doc.powerdns.com/authoritative/settings.html\#allow-dnsupdate-from "Permalink to this headline")

- IP ranges, separated by commas
- Default: 127.0.0.0/8,::1

Allow DNS updates from these IP ranges. Set to empty string to honour `ALLOW-DNSUPDATE-FROM` in [ALLOW-DNSUPDATE-FROM](https://doc.powerdns.com/authoritative/dnsupdate.html#metadata-allow-dnsupdate-from).

## `allow-notify-from` [¶](https://doc.powerdns.com/authoritative/settings.html\#allow-notify-from "Permalink to this headline")

- IP ranges, separated by commas
- Default: 0.0.0.0/0,::/0

Allow AXFR NOTIFY from these IP ranges. Setting this to an empty string
will drop all incoming notifies.

Note

IPs allowed by this setting, still go through the normal NOTIFY processing as described in [Secondary operation](https://doc.powerdns.com/authoritative/modes-of-operation.html#secondary-operation)
The IP the NOTIFY is received from, still needs to be a nameserver for the secondary domain. Explicitly setting this parameter will not bypass those checks.

## `allow-unsigned-autoprimary` [¶](https://doc.powerdns.com/authoritative/settings.html\#allow-unsigned-autoprimary "Permalink to this headline")

Changed in version 4.5.0: This was called [allow-unsigned-supermaster](https://doc.powerdns.com/authoritative/settings.html#setting-allow-unsigned-supermaster) before 4.5.0.

- Boolean
- Default: yes

Turning this off requires all autoprimary notifications to be signed by
valid TSIG signature. It will accept any existing key on secondaries.

## `allow-unsigned-notify` [¶](https://doc.powerdns.com/authoritative/settings.html\#allow-unsigned-notify "Permalink to this headline")

- Boolean
- Default: yes

Turning this off requires all notifications that are received to be
signed by valid TSIG signature for the zone.

## `allow-unsigned-supermaster` [¶](https://doc.powerdns.com/authoritative/settings.html\#allow-unsigned-supermaster "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [allow-unsigned-autoprimary](https://doc.powerdns.com/authoritative/settings.html#setting-allow-unsigned-autoprimary).
Removed in 4.9.0

## `also-notify` [¶](https://doc.powerdns.com/authoritative/settings.html\#also-notify "Permalink to this headline")

- IP addresses, separated by commas

When notifying a zone, also notify these nameservers. Example:
`also-notify=192.0.2.1, 203.0.113.167`. The IP addresses listed in
`also-notify` always receive a notification. Even if they do not match
the list in [only-notify](https://doc.powerdns.com/authoritative/settings.html#setting-only-notify).

You may specify an alternate port by appending :port. Example:
`also-notify=192.0.2.1:5300`. If no port is specified, port 53
is used.

## `any-to-tcp` [¶](https://doc.powerdns.com/authoritative/settings.html\#any-to-tcp "Permalink to this headline")

- Boolean
- Default: yes

Answer questions for the ANY on UDP with a truncated packet that refers
the remote server to TCP. Useful for mitigating reflection attacks.

## `api` [¶](https://doc.powerdns.com/authoritative/settings.html\#api "Permalink to this headline")

- Boolean
- Default: no

Enable/disable the [Built-in Webserver and HTTP API](https://doc.powerdns.com/authoritative/http-api/index.html).

## `api-key` [¶](https://doc.powerdns.com/authoritative/settings.html\#api-key "Permalink to this headline")

- String

Changed in version 4.6.0: This setting now accepts a hashed and salted version.

Static pre-shared authentication key for access to the REST API. Since 4.6.0 the key can be hashed and salted using `pdnsutil hash-password` instead of being stored in the configuration in plaintext, but the plaintext version is still supported.

## `autosecondary` [¶](https://doc.powerdns.com/authoritative/settings.html\#autosecondary "Permalink to this headline")

Changed in version 4.5.0: This was called [superslave](https://doc.powerdns.com/authoritative/settings.html#setting-superslave) before 4.5.0.

- Boolean
- Default: no

Turn on autosecondary support. See [Autoprimary: automatic provisioning of secondaries](https://doc.powerdns.com/authoritative/modes-of-operation.html#autoprimary-operation).

## `axfr-fetch-timeout` [¶](https://doc.powerdns.com/authoritative/settings.html\#axfr-fetch-timeout "Permalink to this headline")

- Integer
- Default: 10

New in version 4.3.0.

Maximum time in seconds for inbound AXFR to start or be idle after starting.

## `axfr-lower-serial` [¶](https://doc.powerdns.com/authoritative/settings.html\#axfr-lower-serial "Permalink to this headline")

- Boolean
- Default: no

Also AXFR a zone from a primary with a lower serial.

## `cache-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#cache-ttl "Permalink to this headline")

- Integer
- Default: 20

Seconds to store packets in the [Packet Cache](https://doc.powerdns.com/authoritative/performance.html#packet-cache). A value of 0 will disable the cache.

## `carbon-instance` [¶](https://doc.powerdns.com/authoritative/settings.html\#carbon-instance "Permalink to this headline")

- String
- Default: auth

Set the instance or third string of the metric key. Be careful not to include
any dots in this setting, unless you know what you are doing.
See [Sending metrics to Graphite/Metronome over Carbon](https://doc.powerdns.com/authoritative/performance.html#metricscarbon)

## `carbon-interval` [¶](https://doc.powerdns.com/authoritative/settings.html\#carbon-interval "Permalink to this headline")

- Integer
- Default: 30

If sending carbon updates, this is the interval between them in seconds.
See [Sending metrics to Graphite/Metronome over Carbon](https://doc.powerdns.com/authoritative/performance.html#metricscarbon).

## `carbon-namespace` [¶](https://doc.powerdns.com/authoritative/settings.html\#carbon-namespace "Permalink to this headline")

- String
- Default: pdns

Set the namespace or first string of the metric key. Be careful not to include
any dots in this setting, unless you know what you are doing.
See [Sending metrics to Graphite/Metronome over Carbon](https://doc.powerdns.com/authoritative/performance.html#metricscarbon)

## `carbon-ourname` [¶](https://doc.powerdns.com/authoritative/settings.html\#carbon-ourname "Permalink to this headline")

- String
- Default: the hostname of the server

If sending carbon updates, if set, this will override our hostname. Be
careful not to include any dots in this setting, unless you know what
you are doing. See [Sending metrics to Graphite/Metronome over Carbon](https://doc.powerdns.com/authoritative/performance.html#metricscarbon)

## `carbon-server` [¶](https://doc.powerdns.com/authoritative/settings.html\#carbon-server "Permalink to this headline")

- IP Address

Send all available metrics to this server via the carbon protocol, which
is used by graphite and metronome. It has to be an address (no
hostnames). Moreover you can specify more than one server using a comma delimited list, ex:
carbon-server=10.10.10.10,10.10.10.20.
You may specify an alternate port by appending :port, ex:
127.0.0.1:2004. See [Sending metrics to Graphite/Metronome over Carbon](https://doc.powerdns.com/authoritative/performance.html#metricscarbon).

## `chroot` [¶](https://doc.powerdns.com/authoritative/settings.html\#chroot "Permalink to this headline")

- Path

If set, chroot to this directory for more security. See [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html).
This is not recommended; instead, we recommend containing PowerDNS using operating system features.
We ship systemd unit files with our packages to make this easy.

Make sure that `/dev/log` is available from within the chroot. Logging
will silently fail over time otherwise (on logrotate).

When setting `chroot`, all other paths in the config (except for
[config-dir](https://doc.powerdns.com/authoritative/settings.html#setting-config-dir) and [module-dir](https://doc.powerdns.com/authoritative/settings.html#setting-module-dir))
set in the configuration are relative to the new root.

When running on a system where systemd manages services, `chroot` does
not work out of the box, as PowerDNS cannot use the `NOTIFY_SOCKET`.
Either don’t `chroot` on these systems or set the ‘Type’ of the
service to ‘simple’ instead of ‘notify’ (refer to the systemd
documentation on how to modify unit-files).

## `secondary-check-signature-freshness` [¶](https://doc.powerdns.com/authoritative/settings.html\#secondary-check-signature-freshness "Permalink to this headline")

New in version 4.7.0.

- Boolean
- Default: yes

Enabled by default, freshness checks for secondary zones will set the DO flag on SOA queries. PowerDNS
can detect (signature) changes on the primary server without serial number bumps using the DNSSEC
signatures in the SOA response.

In some problematic scenarios, primary servers send truncated SOA responses. As a workaround, this setting
can be turned off, and the DO flag as well as the signature checking will be disabled. To avoid additional
drift, primary servers must then always increase the zone serial when it updates signatures.

It is strongly recommended to keep this setting enabled (yes).

## `config-dir` [¶](https://doc.powerdns.com/authoritative/settings.html\#config-dir "Permalink to this headline")

- Path

Location of configuration directory (the directory containing `pdns.conf`). Usually
`/etc/powerdns`, but this depends on `SYSCONFDIR` during
compile-time.

## `config-name` [¶](https://doc.powerdns.com/authoritative/settings.html\#config-name "Permalink to this headline")

- String

Name of this virtual configuration - will rename the binary image. See
[Running Virtual Instances](https://doc.powerdns.com/authoritative/guides/virtual-instances.html).

## `consistent-backends` [¶](https://doc.powerdns.com/authoritative/settings.html\#consistent-backends "Permalink to this headline")

- Boolean
- Default: yes

New in version 4.4.0.

When this is set, PowerDNS assumes that any single zone lives in only one backend.
This allows PowerDNS to send `ANY` lookups to its backends, instead of sometimes requesting the exact needed type.
This reduces the load on backends by retrieving all the types for a given name at once, adding all of them to the cache.
It improves performance significantly for latency-sensitive backends, like SQL ones, where a round-trip takes serious time.

Warning

This behaviour is only a meaningful optimization if the returned response to the `ANY` query can actually be cached,
which is not the case if it contains at least one record with a non-zero scope. For this reason `consistent-backends`
should be disabled when at least one of the backends in use returns location-based records, like the GeoIP backend.

Note

Pre 4.5.0 the default was no.

## `control-console` [¶](https://doc.powerdns.com/authoritative/settings.html\#control-console "Permalink to this headline")

Debugging switch - don’t use.

## `daemon` [¶](https://doc.powerdns.com/authoritative/settings.html\#daemon "Permalink to this headline")

- Boolean
- Default: no

Operate as a daemon.

## `default-api-rectify` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-api-rectify "Permalink to this headline")

- Boolean
- Default: yes

The value of [ALLOW-DNSUPDATE-FROM, FORWARD-DNSUPDATE, NOTIFY-DNSUPDATE, SOA-EDIT-DNSUPDATE](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-api-rectify) if it is not set on the zone.

Note

Pre 4.2.0 the default was always no.

## `default-catalog-zone` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-catalog-zone "Permalink to this headline")

- String:
- Default: empty

New in version 4.8.3.

When a primary zone is created via the API, and the request does not specify a catalog zone, the name given here will be used.

## `default-ksk-algorithm` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-ksk-algorithm "Permalink to this headline")

- String
- Default: ecdsa256

The default algorithm for creating zone keys when running
[pdnsutil zone add-key](https://doc.powerdns.com/authoritative/manpages/pdnsutil.1.html) if no algorithm is specified,
and also the algorithm that should be used for the KSK when running
[pdnsutil zone secure](https://doc.powerdns.com/authoritative/manpages/pdnsutil.1.html) or using the [Zone API endpoint](https://doc.powerdns.com/authoritative/http-api/cryptokey.html)
to enable DNSSEC. Must be one of:

- rsasha1
- rsasha256
- rsasha512
- ecdsa256 (ECDSA P-256 with SHA256)
- ecdsa384 (ECDSA P-384 with SHA384)
- ed25519
- ed448

Note

Actual supported algorithms depend on the crypto-libraries
PowerDNS was compiled against. To check the supported DNSSEC algorithms
in your build of PowerDNS, run `pdnsutil list-algorithms`.

## `default-ksk-size` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-ksk-size "Permalink to this headline")

- Integer
- Default: whichever is default for [default-ksk-algorithm](https://doc.powerdns.com/authoritative/settings.html#default-ksk-algorithm)

The default keysize for the KSK generated with [pdnsutil zone secure](https://doc.powerdns.com/authoritative/dnssec/pdnsutil.html).
Only relevant for algorithms with non-fixed keysizes (like RSA).

## `default-publish-cdnskey` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-publish-cdnskey "Permalink to this headline")

- Integer
- Default: empty

New in version 4.3.0.

The default PUBLISH-CDNSKEY value for zones that do not have one individually specified.
See the [PUBLISH-CDNSKEY, PUBLISH-CDS](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-publish-cdnskey-publish-cds) docs for more information.

## `default-publish-cds` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-publish-cds "Permalink to this headline")

- Comma-separated integers
- Default: empty

New in version 4.3.0.

The default PUBLISH-CDS value for zones that do not have one individually specified.
See the [PUBLISH-CDNSKEY, PUBLISH-CDS](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-publish-cdnskey-publish-cds) docs for more information.

## `default-soa-content` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-soa-content "Permalink to this headline")

- String
- Default: a.misconfigured.dns.server.invalid hostmaster.@ 0 10800 3600 604800 3600

New in version 4.4.0.

This value is used when a zone is created without providing a SOA record. @ is replaced by the zone name.

## `default-soa-edit` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-soa-edit "Permalink to this headline")

- String
- Default: empty

Use this soa-edit value for all zones if no
[SOA-EDIT](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-soa-edit) metadata value is set.
This is used by [pdnsutil zone increase-serial](https://doc.powerdns.com/authoritative/manpages/pdnsutil.1.html).

## `default-soa-edit-signed` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-soa-edit-signed "Permalink to this headline")

- String
- Default: empty

Use this soa-edit value for all signed zones if no
[SOA-EDIT](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-soa-edit) metadata value is set.
Overrides [default-soa-edit](https://doc.powerdns.com/authoritative/settings.html#setting-default-soa-edit)

## `default-soa-mail` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-soa-mail "Permalink to this headline")

- String

Deprecated since version 4.2.0: This setting was removed in 4.4.0

Mail address to insert in the SOA record if none set in the backend.

## `default-soa-name` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-soa-name "Permalink to this headline")

- String
- Default: a.misconfigured.dns.server.invalid

Deprecated since version 4.2.0: This setting was removed in 4.4.0

Name to insert in the SOA record if none set in the backend.

## `default-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-ttl "Permalink to this headline")

- Integer
- Default: 3600

TTL to use when none is provided.

## `default-zsk-algorithm` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-zsk-algorithm "Permalink to this headline")

- String
- Default: (empty)

The default algorithm for creating zone keys when running
[pdnsutil zone add-key](https://doc.powerdns.com/authoritative/manpages/pdnsutil.1.html) if no algorithm is specified,
and also the algorithm that should be used for the ZSK when running
[pdnsutil zone secure](https://doc.powerdns.com/authoritative/manpages/pdnsutil.1.html) or using the [Zone API endpoint](https://doc.powerdns.com/authoritative/http-api/cryptokey.html)
to enable DNSSEC. Must be one of:

- rsasha1
- rsasha256
- rsasha512
- ecdsa256 (ECDSA P-256 with SHA256)
- ecdsa384 (ECDSA P-384 with SHA384)
- ed25519
- ed448

Note

Actual supported algorithms depend on the crypto-libraries
PowerDNS was compiled against. To check the supported DNSSEC algorithms
in your build of PowerDNS, run `pdnsutil list-algorithms`.

## `default-zsk-size` [¶](https://doc.powerdns.com/authoritative/settings.html\#default-zsk-size "Permalink to this headline")

- Integer
- Default: 0 (automatic default for [default-zsk-algorithm](https://doc.powerdns.com/authoritative/settings.html#default-zsk-algorithm))

The default keysize for the ZSK generated with [pdnsutil zone secure](https://doc.powerdns.com/authoritative/dnssec/pdnsutil.html).
Only relevant for algorithms with non-fixed keysizes (like RSA).

## `delay-notifications` [¶](https://doc.powerdns.com/authoritative/settings.html\#delay-notifications "Permalink to this headline")

- Integer
- Default: 0 (no delay, send them directly)

Configure a delay to send out notifications, no delay by default.

## `direct-dnskey` [¶](https://doc.powerdns.com/authoritative/settings.html\#direct-dnskey "Permalink to this headline")

- Boolean
- Default: no

Read additional DNSKEY records from the records table/your BIND zonefile and use both when
preparing responses. If not set, such records in the zonefiles are ignored.

When automatic CDS and CDNSKEY publication (see [PUBLISH-CDNSKEY, PUBLISH-CDS](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-publish-cdnskey-publish-cds))
is enabled, this also applies to those types. If not set, such records are only considered
when automatic publication is turned off.

## `direct-dnskey-signature` [¶](https://doc.powerdns.com/authoritative/settings.html\#direct-dnskey-signature "Permalink to this headline")

- Boolean
- Default: no

New in version 5.0.0.

Read signatures of DNSKEY records directly from the backend.
If not set and the record is not presigned, DNSKEY records will be signed directly by PDNS Authoritative.
Please only use this if you are sure that you need it.

## `disable-axfr` [¶](https://doc.powerdns.com/authoritative/settings.html\#disable-axfr "Permalink to this headline")

- Boolean
- Default: no

Do not allow zone transfers.

## `disable-axfr-rectify` [¶](https://doc.powerdns.com/authoritative/settings.html\#disable-axfr-rectify "Permalink to this headline")

- Boolean
- Default: no

Disable the rectify step during an outgoing AXFR. Only required for
regression testing.

## `disable-syslog` [¶](https://doc.powerdns.com/authoritative/settings.html\#disable-syslog "Permalink to this headline")

- Boolean
- Default: no

Do not log to syslog, only to stderr. Use this setting when running
inside a supervisor that handles logging (like systemd).

Warning

Do not use this setting in combination with [daemon](https://doc.powerdns.com/authoritative/settings.html#setting-daemon) as all
logging will disappear.

## `distributor-threads` [¶](https://doc.powerdns.com/authoritative/settings.html\#distributor-threads "Permalink to this headline")

- Integer
- Default: 3

Number of Distributor (backend) threads to start per receiver thread.
See [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html).

## `dname-processing` [¶](https://doc.powerdns.com/authoritative/settings.html\#dname-processing "Permalink to this headline")

- Boolean
- Default: no

Turn on DNAME processing (DNAME substitution, CNAME synthesis). This
approximately doubles query load.

If this is turned off, DNAME records are treated as any other and served
only when queried explicitly.

## `dnsproxy-udp-port-range` [¶](https://doc.powerdns.com/authoritative/settings.html\#dnsproxy-udp-port-range "Permalink to this headline")

- String
- Default: 10000 60000

If [resolver](https://doc.powerdns.com/authoritative/settings.html#setting-resolver) enables the DNS Proxy, this setting limits the
port range the DNS Proxy’s UDP port is chosen from.

Default should be fine on most installs, but if you have conflicting local
services, you may choose to limit the range.

## `dnssec-key-cache-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#dnssec-key-cache-ttl "Permalink to this headline")

- Integer
- Default: 30

Seconds to cache DNSSEC keys from the database. A value of 0 disables
caching.

## `dnsupdate` [¶](https://doc.powerdns.com/authoritative/settings.html\#dnsupdate "Permalink to this headline")

- Boolean
- Default: no

Enable/Disable DNS update (RFC2136) support. See [Dynamic DNS Update (RFC 2136)](https://doc.powerdns.com/authoritative/dnsupdate.html) for more.

## `dnsupdate-require-tsig` [¶](https://doc.powerdns.com/authoritative/settings.html\#dnsupdate-require-tsig "Permalink to this headline")

New in version 5.0.0.

- Boolean
- Default: no

Requires DNS updates to be signed by a valid TSIG signature even if the zone has no associated keys.

## `do-ipv6-additional-processing` [¶](https://doc.powerdns.com/authoritative/settings.html\#do-ipv6-additional-processing "Permalink to this headline")

- Boolean
- Default: yes

Changed in version 4.4.0: This setting has been removed

Perform AAAA additional processing. This sends AAAA records in the
ADDITIONAL section when sending a referral.

## `domain-metadata-cache-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#domain-metadata-cache-ttl "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [zone-metadata-cache-ttl](https://doc.powerdns.com/authoritative/settings.html#setting-zone-metadata-cache-ttl).

Seconds to cache zone metadata from the database. A value of 0
disables caching.

## `edns-cookie-secret` [¶](https://doc.powerdns.com/authoritative/settings.html\#edns-cookie-secret "Permalink to this headline")

New in version 4.6.0.

- String
- Default: (empty)

When set, PowerDNS will respond with [**RFC 9018**](https://tools.ietf.org/html/rfc9018.html) EDNS Cookies to queries that have the EDNS0 Cookie option.
PowerDNS will also respond with BADCOOKIE to clients that have sent only a client cookie, or a bad server cookie (section 5.2.3 and 5.2.4 of [**RFC 7873**](https://tools.ietf.org/html/rfc7873.html)).

This setting MUST be 32 hexadecimal characters, as the siphash algorithm’s key used to create the cookie requires a 128-bit key.

Alternatively, starting with version 5.0.0, this parameter can be set to
random, in which case a random cookie value will be generated upon startup.

## `edns-subnet-processing` [¶](https://doc.powerdns.com/authoritative/settings.html\#edns-subnet-processing "Permalink to this headline")

- Boolean
- Default: no

Enables EDNS subnet processing, for backends that support it.

## `enable-gss-tsig` [¶](https://doc.powerdns.com/authoritative/settings.html\#enable-gss-tsig "Permalink to this headline")

- Boolean
- Default: no

Enable accepting GSS-TSIG signed messages.
In addition to this setting, see [TSIG](https://doc.powerdns.com/authoritative/tsig.html).

## `enable-lua-records` [¶](https://doc.powerdns.com/authoritative/settings.html\#enable-lua-records "Permalink to this headline")

- One of `no`, `yes` (or empty), or `shared`, String
- Default: no

Globally enable the [LUA records](https://doc.powerdns.com/authoritative/lua-records/index.html) feature.

To use shared LUA states, set this to `shared`, see [Shared Lua state model](https://doc.powerdns.com/authoritative/lua-records/index.html#lua-records-shared-state).

## `entropy-source` [¶](https://doc.powerdns.com/authoritative/settings.html\#entropy-source "Permalink to this headline")

- Path
- Default: /dev/urandom

Entropy source file to use.

## `expand-alias` [¶](https://doc.powerdns.com/authoritative/settings.html\#expand-alias "Permalink to this headline")

- Boolean
- Default: no

If this is enabled, ALIAS records are expanded (synthesized to their
A/AAAA).

If this is disabled (the default), ALIAS records will not be expanded and
the server will return NODATA for A/AAAA queries for such names.

Note

[resolver](https://doc.powerdns.com/authoritative/settings.html#setting-resolver) must also be set for ALIAS expansion to work!

Note

In PowerDNS Authoritative Server 4.0.x, this setting did not exist and
ALIAS was always expanded.

## `resolve-across-zones` [¶](https://doc.powerdns.com/authoritative/settings.html\#resolve-across-zones "Permalink to this headline")

New in version 5.0.0.

- Boolean
- Default: yes

If this is enabled, CNAME records and other referrals will be resolved as long as their targets exist in any local backend.
Can be disabled to allow for different authorities managing zones in the same server instance.

Referrals not available in local backends are never resolved.
SVCB referrals are never resolved across zones.
ALIAS is not impacted by this setting.

## `forward-dnsupdate` [¶](https://doc.powerdns.com/authoritative/settings.html\#forward-dnsupdate "Permalink to this headline")

- Boolean
- Default: no

Forward DNS updates sent to a secondary to the primary.

## `forward-notify` [¶](https://doc.powerdns.com/authoritative/settings.html\#forward-notify "Permalink to this headline")

- IP addresses, separated by commas
- Default: empty

IP addresses to forward received notifications to regardless of primary
or secondary settings.

Note

The intended use is in anycast environments where it might be
necessary for a proxy server to perform the AXFR. The usual checks are
performed before any received notification is forwarded.

## `guardian` [¶](https://doc.powerdns.com/authoritative/settings.html\#guardian "Permalink to this headline")

- Boolean
- Default: no

Run within a guardian process. See [Guardian](https://doc.powerdns.com/authoritative/running.html#running-guardian).

## `ignore-unknown-settings` [¶](https://doc.powerdns.com/authoritative/settings.html\#ignore-unknown-settings "Permalink to this headline")

New in version 4.5.0.

- Setting names, separated by commas
- Default: empty

Names of settings to be ignored while parsing configuration files, if the setting
name is unknown to PowerDNS.

Useful during upgrade testing.

## `include-dir` [¶](https://doc.powerdns.com/authoritative/settings.html\#include-dir "Permalink to this headline")

- Path

Directory to scan for additional config files. All files that end with
.conf are loaded in order using `POSIX` as locale.

## `launch` [¶](https://doc.powerdns.com/authoritative/settings.html\#launch "Permalink to this headline")

- Backend names, separated by commas

Which backends to launch and order to query them in. Launches backends.
In its most simple form, supply all backends that need to be launched.
e.g.

```
launch=bind,gmysql,remote
```

If you find that you need to query a backend multiple times with
different configuration, you can specify a name for later
instantiations. e.g.:

```
launch=gmysql,gmysql:server2
```

In this case, there are 2 instances of the gmysql backend, one by the
normal name and the second one is called ‘server2’. The backend
configuration item names change: e.g. `gmysql-host` is available to
configure the `host` setting of the first or main instance, and
`gmysql-server2-host` for the second one.

Running multiple instances of the BIND backend is not allowed.

## `load-modules` [¶](https://doc.powerdns.com/authoritative/settings.html\#load-modules "Permalink to this headline")

- Paths, separated by commas

If backends are available in nonstandard directories, specify their
location here. Multiple files can be loaded if separated by commas. Only
available in non-static distributions.

## `local-address` [¶](https://doc.powerdns.com/authoritative/settings.html\#local-address "Permalink to this headline")

Changed in version 4.3.0: now also accepts IPv6 addresses

Changed in version 4.3.0: Before 4.3.0, this setting only supported IPv4 addresses.

- IPv4/IPv6 Addresses, with optional port numbers, separated by commas or whitespace
- Default: `0.0.0.0, ::`

Local IP addresses to which we bind. Each address specified can
include a port number; if no port is included then the
[local-port](https://doc.powerdns.com/authoritative/settings.html#setting-local-port) port will be used for that address. If a
port number is specified, it must be separated from the address with a
‘:’; for an IPv6 address the address must be enclosed in square
brackets.

Examples:

```
local-address=127.0.0.1 ::1
local-address=0.0.0.0:5353
local-address=[::]:8053
local-address=127.0.0.1:53, [::1]:5353
```

## `local-address-nonexist-fail` [¶](https://doc.powerdns.com/authoritative/settings.html\#local-address-nonexist-fail "Permalink to this headline")

- Boolean
- Default: yes

Fail to start if one or more of the
[local-address](https://doc.powerdns.com/authoritative/settings.html#setting-local-address)’s do not exist on this server.

## `local-ipv6` [¶](https://doc.powerdns.com/authoritative/settings.html\#local-ipv6 "Permalink to this headline")

Deprecated since version 4.5.0: Use [local-address](https://doc.powerdns.com/authoritative/settings.html#setting-local-address) instead

## `local-ipv6-nonexist-fail` [¶](https://doc.powerdns.com/authoritative/settings.html\#local-ipv6-nonexist-fail "Permalink to this headline")

Changed in version 4.3.0: This setting has been removed, use [local-address-nonexist-fail](https://doc.powerdns.com/authoritative/settings.html#setting-local-address-nonexist-fail)

- Boolean
- Default: no

Fail to start if one or more of the [local-ipv6](https://doc.powerdns.com/authoritative/settings.html#setting-local-ipv6)
addresses do not exist on this server.

## `local-port` [¶](https://doc.powerdns.com/authoritative/settings.html\#local-port "Permalink to this headline")

- Integer
- Default: 53

Local port to bind to.
If an address in [local-address](https://doc.powerdns.com/authoritative/settings.html#setting-local-address) does not have an explicit port, this port is used.

## `log-dns-details` [¶](https://doc.powerdns.com/authoritative/settings.html\#log-dns-details "Permalink to this headline")

- Boolean
- Default: no

If set to ‘no’, informative-only DNS details will not even be sent to
syslog, improving performance.

## `log-dns-queries` [¶](https://doc.powerdns.com/authoritative/settings.html\#log-dns-queries "Permalink to this headline")

- Boolean
- Default: no

Tell PowerDNS to log all incoming DNS queries. This will lead to a lot
of logging! Only enable for debugging! Set [loglevel](https://doc.powerdns.com/authoritative/settings.html#setting-loglevel)
to at least 5 to see the logs.

## `log-timestamp` [¶](https://doc.powerdns.com/authoritative/settings.html\#log-timestamp "Permalink to this headline")

- Bool
- Default: yes

When printing log lines to stderr, prefix them with timestamps.
Disable this if the process supervisor timestamps these lines already.

Note

The systemd unit file supplied with the source code already disables timestamp printing

## `logging-facility` [¶](https://doc.powerdns.com/authoritative/settings.html\#logging-facility "Permalink to this headline")

If set to a digit, logging is performed under this LOCAL facility. See [Logging to syslog](https://doc.powerdns.com/authoritative/running.html#logging-to-syslog).
Do not pass names like ‘local0’!

## `loglevel` [¶](https://doc.powerdns.com/authoritative/settings.html\#loglevel "Permalink to this headline")

- Integer
- Default: 4

Amount of logging. The higher the number, the more lines logged.
Corresponds to “syslog” level values (e.g. 0 = emergency, 1 = alert, 2 = critical, 3 = error, 4 = warning, 5 = notice, 6 = info, 7 = debug).
Each level includes itself plus the lower levels before it.
Not recommended to set this below 3.

## `loglevel-show` [¶](https://doc.powerdns.com/authoritative/settings.html\#loglevel-show "Permalink to this headline")

- Bool
- Default: no

New in version 4.9.0.

When enabled, log messages are formatted like structured logs, including their log level/priority: `msg="Unable to launch, no backends configured for querying" prio="Error"`

## `lua-axfr-script` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-axfr-script "Permalink to this headline")

- String
- Default: empty

Script to be used to edit incoming AXFRs, see [Modifying a secondary zone using a script](https://doc.powerdns.com/authoritative/modes-of-operation.html#modes-of-operation-axfrfilter)

## `lua-consistent-hashes-cleanup-interval` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-consistent-hashes-cleanup-interval "Permalink to this headline")

- Integer
- Default: 3600

New in version 4.9.0.

Amount of time (in seconds) between subsequent cleanup routines for pre-computed hashes related to [`pickchashed()`](https://doc.powerdns.com/authoritative/lua-records/functions.html#pickchashed "pickchashed").

## `lua-consistent-hashes-expire-delay` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-consistent-hashes-expire-delay "Permalink to this headline")

- Integer
- Default: 86400

New in version 4.9.0.

Amount of time (in seconds) a pre-computed hash entry will be considered as expired when unused. See [`pickchashed()`](https://doc.powerdns.com/authoritative/lua-records/functions.html#pickchashed "pickchashed").

## `lua-global-include-dir` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-global-include-dir "Permalink to this headline")

- String
- Default: empty
- Example: `/etc/pdns/lua-global/`

New in version 5.0.0.

When creating a Lua context, scan this directory for additional lua files. All files that end with
.lua are loaded in order using `POSIX` as locale with Lua scripts.

## `lua-health-checks-expire-delay` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-health-checks-expire-delay "Permalink to this headline")

- Integer
- Default: 3600

New in version 4.3.0.

Amount of time (in seconds) to expire (remove) a LUA monitoring check when the record
isn’t used any more (either deleted or modified).

## `lua-health-checks-interval` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-health-checks-interval "Permalink to this headline")

- Integer
- Default: 5

New in version 4.3.0.

Amount of time (in seconds) between subsequent monitoring health checks. Does nothing
if the checks take more than that time to execute.

## `lua-prequery-script` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-prequery-script "Permalink to this headline")

- Path

Lua script to run before answering a query. This is a feature used
internally for regression testing. The API of this functionality is not
guaranteed to be stable, and is in fact likely to change.

## `lua-records-exec-limit` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-records-exec-limit "Permalink to this headline")

- Integer
- Default: 1000

Limit LUA records scripts to `lua-records-exec-limit` instructions.
Setting this to any value less than or equal to 0 will set no limit.

## `lua-records-insert-whitespace` [¶](https://doc.powerdns.com/authoritative/settings.html\#lua-records-insert-whitespace "Permalink to this headline")

- Boolean
- Default: no in 5.0, yes before that

New in version 4.9.1.

When combining the `"` delimited chunks of a LUA record, whether to insert whitespace between each chunk.

## `master` [¶](https://doc.powerdns.com/authoritative/settings.html\#master "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [primary](https://doc.powerdns.com/authoritative/settings.html#setting-primary).
Removed in 4.9.0.

- Boolean
- Default: no

Turn on primary support. See [Primary operation](https://doc.powerdns.com/authoritative/modes-of-operation.html#primary-operation).

## `max-cache-entries` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-cache-entries "Permalink to this headline")

- Integer
- Default: 1000000

Maximum number of entries in the query cache. 1 million (the default)
will generally suffice for most installations.

## `max-ent-entries` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-ent-entries "Permalink to this headline")

- Integer
- Default: 100000

Maximum number of empty non-terminals to add to a zone. This is a
protection measure to avoid database explosion due to long names.

## `max-include-depth` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-include-depth "Permalink to this headline")

- Integer
- Default: 20

Maximum number of nested `$INCLUDE` directives while processing a zone file.
Zero mean no `$INCLUDE` directives will be accepted.

## `max-generate-steps` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-generate-steps "Permalink to this headline")

- Integer
- Default: 0

Maximum number of steps for a ‘$GENERATE’ directive when parsing a
zone file. This is a protection measure to prevent consuming a lot of
CPU and memory when untrusted zones are loaded. Default to 0 which
means unlimited.

## `max-nsec3-iterations` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-nsec3-iterations "Permalink to this headline")

- Integer
- Default: 100

Limit the number of NSEC3 hash iterations for zone configurations.
For more information see [Setting the NSEC modes and parameters](https://doc.powerdns.com/authoritative/dnssec/operational.html#dnssec-operational-nsec-modes-params).

Note

Pre 4.5.0 the default was 500.

## `max-packet-cache-entries` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-packet-cache-entries "Permalink to this headline")

- Integer
- Default: 1000000

Maximum number of entries in the packet cache. 1 million (the default)
will generally suffice for most installations.

## `max-queue-length` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-queue-length "Permalink to this headline")

- Integer
- Default: 5000

If this many packets are waiting for database attention, consider the
situation hopeless and respawn the server process.
This limit is per receiver thread.

## `max-signature-cache-entries` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-signature-cache-entries "Permalink to this headline")

- Integer
- Default: 2^31-1 (on most systems), 2^63-1 (on ILP64 systems)

Maximum number of DNSSEC signature cache entries. This cache is
automatically reset once per week or when the cache is full. If you
use NSEC narrow mode, this cache can grow large.

## `max-tcp-connection-duration` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-tcp-connection-duration "Permalink to this headline")

- Integer
- Default: 0

Maximum time in seconds that a TCP DNS connection is allowed to stay
open. 0 means unlimited. Note that exchanges related to an AXFR or IXFR
are not affected by this setting.

## `max-tcp-connections` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-tcp-connections "Permalink to this headline")

- Integer
- Default: 20

Allow this many incoming TCP DNS connections simultaneously.

## `max-tcp-connections-per-client` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-tcp-connections-per-client "Permalink to this headline")

- Integer
- Default: 0

Maximum number of simultaneous TCP connections per client. 0 means
unlimited.

## `max-tcp-transactions-per-conn` [¶](https://doc.powerdns.com/authoritative/settings.html\#max-tcp-transactions-per-conn "Permalink to this headline")

- Integer
- Default: 0

Allow this many DNS queries in a single TCP transaction. 0 means
unlimited. Note that exchanges related to an AXFR or IXFR are not
affected by this setting.

## `module-dir` [¶](https://doc.powerdns.com/authoritative/settings.html\#module-dir "Permalink to this headline")

- Path

Directory for modules. Default depends on `PKGLIBDIR` during
compile-time.

## `negquery-cache-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#negquery-cache-ttl "Permalink to this headline")

- Integer
- Default: 60

Seconds to store queries with no answer in the Query Cache. See [Query Cache](https://doc.powerdns.com/authoritative/performance.html#query-cache).

## `no-config` [¶](https://doc.powerdns.com/authoritative/settings.html\#no-config "Permalink to this headline")

- Boolean
- Default: no

Do not attempt to read the configuration file. Useful for configuration
by parameters from the command line only.

## `no-shuffle` [¶](https://doc.powerdns.com/authoritative/settings.html\#no-shuffle "Permalink to this headline")

- Boolean
- Default: no

Do not attempt to shuffle query results, used for regression testing.

## `non-local-bind` [¶](https://doc.powerdns.com/authoritative/settings.html\#non-local-bind "Permalink to this headline")

- Boolean
- Default: no

Bind to addresses even if one or more of the
[local-address](https://doc.powerdns.com/authoritative/settings.html#setting-local-address)’s do not exist on this server.
Setting this option will enable the needed socket options to allow
binding to non-local addresses. This feature is intended to facilitate
ip-failover setups, but it may also mask configuration issues and for
this reason it is disabled by default.

## `only-notify` [¶](https://doc.powerdns.com/authoritative/settings.html\#only-notify "Permalink to this headline")

- IP Ranges, separated by commas or whitespace
- Default: 0.0.0.0/0, ::/0

For type=MASTER zones (or SLAVE zones with [secondary-do-renotify](https://doc.powerdns.com/authoritative/settings.html#setting-secondary-do-renotify) enabled)
PowerDNS automatically sends NOTIFYs to the name servers specified in
the NS records. By specifying networks/mask as whitelist, the targets
can be limited. The default is to notify the world. To completely
disable these NOTIFYs set `only-notify` to an empty value. Independent
of this setting, the IP addresses or netmasks configured with
[also-notify](https://doc.powerdns.com/authoritative/settings.html#setting-also-notify) and `ALSO-NOTIFY` zone metadata
always receive AXFR NOTIFYs.

IP addresses and netmasks can be excluded by prefixing them with a `!`.
To notify all IP addresses apart from the 192.168.0.0/24 subnet use the following:

```
only-notify=0.0.0.0/0, ::/0, !192.168.0.0/24
```

Note

Even if NOTIFYs are limited by a netmask, PowerDNS first has to
resolve all the hostnames to check their IP addresses against the
specified whitelist. The resolving may take considerable time,
especially if those hostnames are slow to resolve. If you do not need to
NOTIFY the slaves defined in the NS records (e.g. you are using another
method to distribute the zone data to the slaves), then set
[only-notify](https://doc.powerdns.com/authoritative/settings.html#setting-only-notify) to an empty value and specify the notification targets
explicitly using [also-notify](https://doc.powerdns.com/authoritative/settings.html#setting-also-notify) and/or
[ALSO-NOTIFY](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-also-notify) zone metadata to avoid this potential bottleneck.

Note

If your secondaries support an Internet Protocol version, which your primary does not,
then set `only-notify` to include only supported protocol version.
Otherwise, there will be error trying to resolve address.

For example, secondaries support both IPv4 and IPv6, but PowerDNS primary have only IPv4,
so allow only IPv4 with `only-notify`:

```
only-notify=0.0.0.0/0
```

## `outgoing-axfr-expand-alias` [¶](https://doc.powerdns.com/authoritative/settings.html\#outgoing-axfr-expand-alias "Permalink to this headline")

- One of `no`, `yes`, or `ignore-errors`, String
- Default: no

Changed in version 4.9.0: Option ignore-errors added.

If this is enabled, ALIAS records are expanded (synthesized to their
A/AAAA) during outgoing AXFR. This means slaves will not automatically
follow changes in those A/AAAA records unless you AXFR regularly!

If this is disabled (the default), ALIAS records are sent verbatim
during outgoing AXFR. Note that if your slaves do not support ALIAS,
they will return NODATA for A/AAAA queries for such names.

If the ALIAS target cannot be resolved during AXFR the AXFR will fail.
To allow outgoing AXFR also if the ALIAS targets are broken set this
setting to ignore-errors.
Be warned, this will lead to inconsistent zones between Primary and
Secondary name servers.

## `overload-queue-length` [¶](https://doc.powerdns.com/authoritative/settings.html\#overload-queue-length "Permalink to this headline")

- Integer
- Default: 0 (disabled)

If this many packets are waiting for database attention, answer any new
questions strictly from the packet cache. Packets not in the cache will
be dropped, and [overload-drops](https://doc.powerdns.com/authoritative/performance.html#stat-overload-drops) will be incremented.

## `prevent-self-notification` [¶](https://doc.powerdns.com/authoritative/settings.html\#prevent-self-notification "Permalink to this headline")

- Boolean
- Default: yes

PowerDNS Authoritative Server attempts to not send out notifications to
itself in primary mode. In very complicated situations we could guess
wrong and not notify a server that should be notified. In that case, set
prevent-self-notification to “no”.

## `primary` [¶](https://doc.powerdns.com/authoritative/settings.html\#primary "Permalink to this headline")

Changed in version 4.5.0: This was called [master](https://doc.powerdns.com/authoritative/settings.html#setting-master) before 4.5.0.

- Boolean
- Default: no

Turn on operating as a primary. See [Primary operation](https://doc.powerdns.com/authoritative/modes-of-operation.html#primary-operation).

## `proxy-protocol-from` [¶](https://doc.powerdns.com/authoritative/settings.html\#proxy-protocol-from "Permalink to this headline")

New in version 4.6.0.

- IP addresses or netmasks, separated by commas
- Default: empty

Ranges that are required to send a Proxy Protocol version 2 header in front of UDP and TCP queries, to pass the original source and destination addresses and ports to the Authoritative.
Queries that are not prefixed with such a header will not be accepted from clients in these ranges. Queries prefixed by headers from clients that are not listed in these ranges will be dropped.

Note that once a Proxy Protocol header has been received, the source address from the proxy header instead of the address of the proxy will be checked against primary addresses sending NOTIFYs, and the ACLs for any client requesting AXFRs.
When using this setting combined with [trusted-notification-proxy](https://doc.powerdns.com/authoritative/settings.html#setting-trusted-notification-proxy), please be aware that the trusted address will also be checked against the source address in the PROXY header.

The dnsdist docs have [more information about the PROXY protocol](https://dnsdist.org/advanced/passing-source-address.html#proxy-protocol).

## `proxy-protocol-maximum-size` [¶](https://doc.powerdns.com/authoritative/settings.html\#proxy-protocol-maximum-size "Permalink to this headline")

New in version 4.6.0.

- Integer
- Default: 512

The maximum size, in bytes, of a Proxy Protocol payload (header, addresses and ports, and TLV values). Queries with a larger payload will be dropped.

## `query-cache-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#query-cache-ttl "Permalink to this headline")

- Integer
- Default: 20

Seconds to store queries with an answer in the Query Cache. See [Query Cache](https://doc.powerdns.com/authoritative/performance.html#query-cache).

## `query-local-address` [¶](https://doc.powerdns.com/authoritative/settings.html\#query-local-address "Permalink to this headline")

Changed in version 4.4.0: Accepts both IPv4 and IPv6 addresses. Also accept more than one address per
address family.

- IP addresses, separated by spaces or commas
- Default: 0.0.0.0 ::

The IP addresses to use as a source address for sending queries. Useful if
you have multiple IPs and PowerDNS is not bound to the IP address your
operating system uses by default for outgoing packets.

PowerDNS will pick the correct address family based on the remote’s address (v4
for outgoing v4, v6 for outgoing v6). However, addresses are selected at random
without taking into account ip subnet reachability. It is highly recommended to
use the defaults in that case (the kernel will pick the right source address for
the network).

## `query-local-address6` [¶](https://doc.powerdns.com/authoritative/settings.html\#query-local-address6 "Permalink to this headline")

Deprecated since version 4.5.0: Removed. Use [query-local-address](https://doc.powerdns.com/authoritative/settings.html#setting-query-local-address).

## `query-logging` [¶](https://doc.powerdns.com/authoritative/settings.html\#query-logging "Permalink to this headline")

- Boolean
- Default: no

Boolean, hints to a backend that it should log a textual representation
of queries it performs. Can be set at runtime.

## `queue-limit` [¶](https://doc.powerdns.com/authoritative/settings.html\#queue-limit "Permalink to this headline")

- Integer
- Default: 1500

Maximum number of milliseconds to queue a query. See [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html).

## `receiver-threads` [¶](https://doc.powerdns.com/authoritative/settings.html\#receiver-threads "Permalink to this headline")

- Integer
- Default: 1

Number of receiver (listening) threads to start. See [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html).

## `resolver` [¶](https://doc.powerdns.com/authoritative/settings.html\#resolver "Permalink to this headline")

- IP Address with optional port
- Default: unset

Recursive DNS server to use for ALIAS lookups and the internal stub resolver. Only one address can be given.

It is assumed that the specified recursive DNS server, and the network path to it, are trusted.

Examples:

```
resolver=127.0.0.1
resolver=[::1]:5300
```

Warning

You should make sure that the [resolver](https://doc.powerdns.com/authoritative/settings.html#setting-resolver) does not point to
PowerDNS itself, to prevent infinite query loops.

## `retrieval-threads` [¶](https://doc.powerdns.com/authoritative/settings.html\#retrieval-threads "Permalink to this headline")

- Integer
- Default: 2

Number of AXFR secondary threads to start.

## `reuseport` [¶](https://doc.powerdns.com/authoritative/settings.html\#reuseport "Permalink to this headline")

- Boolean
- Default: No

On Linux 3.9 and some BSD kernels the `SO_REUSEPORT` option allows
each receiver-thread to open a new socket on the same port which allows
for much higher performance on multi-core boxes. Setting this option
will enable use of `SO_REUSEPORT` when available and seamlessly fall
back to a single socket when it is not available. A side-effect is that
you can start multiple servers on the same IP/port combination which may
or may not be a good idea. You could use this to enable transparent
restarts, but it may also mask configuration issues and for this reason
it is disabled by default.

## `rng` [¶](https://doc.powerdns.com/authoritative/settings.html\#rng "Permalink to this headline")

- String
- Default: auto

Specify which random number generator to use. Permissible choices are:

- auto - choose automatically
- sodium - Use libsodium `randombytes_uniform`
- openssl - Use libcrypto `RAND_bytes`
- getrandom - Use libc getrandom, falls back to urandom if it does not really work
- arc4random - Use BSD `arc4random_uniform`
- urandom - Use `/dev/urandom`
- kiss - Use simple settable deterministic RNG. **FOR TESTING PURPOSES ONLY!**

Note

Not all choices are available on all systems.

## `secondary` [¶](https://doc.powerdns.com/authoritative/settings.html\#secondary "Permalink to this headline")

Changed in version 4.5.0: This was called [slave](https://doc.powerdns.com/authoritative/settings.html#setting-slave) before 4.5.0.

- Boolean
- Default: no

Turn on operating as a secondary. See [Secondary operation](https://doc.powerdns.com/authoritative/modes-of-operation.html#secondary-operation).

## `secondary-do-renotify` [¶](https://doc.powerdns.com/authoritative/settings.html\#secondary-do-renotify "Permalink to this headline")

Changed in version 4.5.0: This was called [slave-renotify](https://doc.powerdns.com/authoritative/settings.html#setting-slave-renotify) before 4.5.0.

- Boolean
- Default: no

This setting will make PowerDNS renotify the secondaries after an AXFR is
_received_ from a primary. This is useful, among other situations, when running a
signing secondary.

See [SLAVE-RENOTIFY](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-slave-renotify) to set this per-zone.

## `security-poll-suffix` [¶](https://doc.powerdns.com/authoritative/settings.html\#security-poll-suffix "Permalink to this headline")

- String
- Default: secpoll.powerdns.com.

Zone name from which to query security update notifications. Setting
this to an empty string disables secpoll.

## `send-signed-notify` [¶](https://doc.powerdns.com/authoritative/settings.html\#send-signed-notify "Permalink to this headline")

- Boolean
- Default: yes

If yes, outgoing NOTIFYs will be signed if a TSIG key is configured for the zone.
If there are multiple TSIG keys configured for a zone, PowerDNS will use the
first one retrieved from the backend, which may not be the correct one for the
respective secondary. Hence, in setups with multiple slaves with different TSIG keys
it may be required to send NOTIFYs unsigned.

## `server-id` [¶](https://doc.powerdns.com/authoritative/settings.html\#server-id "Permalink to this headline")

- String
- Default: The hostname of the server

This is the server ID that will be returned on an EDNS NSID query.

## `setgid` [¶](https://doc.powerdns.com/authoritative/settings.html\#setgid "Permalink to this headline")

- String

If set, change group id to this gid for more security. See [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html).

## `setuid` [¶](https://doc.powerdns.com/authoritative/settings.html\#setuid "Permalink to this headline")

- String

If set, change user id to this uid for more security. See [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html).

## `signing-threads` [¶](https://doc.powerdns.com/authoritative/settings.html\#signing-threads "Permalink to this headline")

- Integer
- Default: 3

Tell PowerDNS how many threads to use for signing. It might help improve
signing speed by changing this number.

## `slave` [¶](https://doc.powerdns.com/authoritative/settings.html\#slave "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [secondary](https://doc.powerdns.com/authoritative/settings.html#setting-secondary).
Removed in 4.9.0.

## `slave-cycle-interval` [¶](https://doc.powerdns.com/authoritative/settings.html\#slave-cycle-interval "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [xfr-cycle-interval](https://doc.powerdns.com/authoritative/settings.html#setting-xfr-cycle-interval).
Removed in 4.9.0.

## `slave-renotify` [¶](https://doc.powerdns.com/authoritative/settings.html\#slave-renotify "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [secondary-do-renotify](https://doc.powerdns.com/authoritative/settings.html#setting-secondary-do-renotify).
Removed in 4.9.0.

- Boolean
- Default: no

This setting will make PowerDNS renotify the secondaries after an AXFR is
_received_ from a primary. This is useful when running a
signing-secondary.

See [SLAVE-RENOTIFY](https://doc.powerdns.com/authoritative/domainmetadata.html#metadata-slave-renotify) to set this per-zone.

## `soa-expire-default` [¶](https://doc.powerdns.com/authoritative/settings.html\#soa-expire-default "Permalink to this headline")

- Integer
- Default: 604800

Deprecated since version 4.2.0: This setting was removed in 4.4.0

Default [SMIMEA](https://doc.powerdns.com/authoritative/appendices/types.html#types-soa) expire.

## `soa-minimum-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#soa-minimum-ttl "Permalink to this headline")

- Integer
- Default: 3600

Deprecated since version 4.2.0: This setting was removed in 4.4.0

Default [SMIMEA](https://doc.powerdns.com/authoritative/appendices/types.html#types-soa) minimum ttl.

## `soa-refresh-default` [¶](https://doc.powerdns.com/authoritative/settings.html\#soa-refresh-default "Permalink to this headline")

- Integer
- Default: 10800

Deprecated since version 4.2.0: This setting was removed in 4.4.0

Default [SMIMEA](https://doc.powerdns.com/authoritative/appendices/types.html#types-soa) refresh.

## `soa-retry-default` [¶](https://doc.powerdns.com/authoritative/settings.html\#soa-retry-default "Permalink to this headline")

- Integer
- Default: 3600

Deprecated since version 4.2.0: This setting was removed in 4.4.0

Default [SMIMEA](https://doc.powerdns.com/authoritative/appendices/types.html#types-soa) retry.

## `socket-dir` [¶](https://doc.powerdns.com/authoritative/settings.html\#socket-dir "Permalink to this headline")

- Path

Where the controlsocket will live. The default depends on
`LOCALSTATEDIR` during compile-time (usually `/var/run` or
`/run`). See [Control Socket](https://doc.powerdns.com/authoritative/running.html#control-socket).

This path will also contain the pidfile for this instance of PowerDNS
called `pdns.pid` by default. See [config-name](https://doc.powerdns.com/authoritative/settings.html#setting-config-name)
and [Virtual Hosting](https://doc.powerdns.com/authoritative/guides/virtual-instances.html) how this can differ.

## `superslave` [¶](https://doc.powerdns.com/authoritative/settings.html\#superslave "Permalink to this headline")

Deprecated since version 4.5.0: Renamed to [autosecondary](https://doc.powerdns.com/authoritative/settings.html#setting-autosecondary).
Removed in 4.9.0.

- Boolean
- Default: no

Turn on autosecondary support. See [Autoprimary: automatic provisioning of secondaries](https://doc.powerdns.com/authoritative/modes-of-operation.html#autoprimary-operation).

## `svc-autohints` [¶](https://doc.powerdns.com/authoritative/settings.html\#svc-autohints "Permalink to this headline")

- Boolean
- Default: no

New in version 4.5.0.

Whether or not to enable IPv4 and IPv6 [autohints](https://doc.powerdns.com/authoritative/guides/svcb.html#svc-autohints).

## `tcp-control-address` [¶](https://doc.powerdns.com/authoritative/settings.html\#tcp-control-address "Permalink to this headline")

- IP Address

Address to bind to for TCP control.

## `tcp-control-port` [¶](https://doc.powerdns.com/authoritative/settings.html\#tcp-control-port "Permalink to this headline")

- Integer
- Default: 53000

Port to bind to for TCP control.

## `tcp-control-range` [¶](https://doc.powerdns.com/authoritative/settings.html\#tcp-control-range "Permalink to this headline")

- IP Ranges, separated by commas or whitespace

Limit TCP control to a specific client range.

## `tcp-control-secret` [¶](https://doc.powerdns.com/authoritative/settings.html\#tcp-control-secret "Permalink to this headline")

- String

Password for TCP control.

## `tcp-fast-open` [¶](https://doc.powerdns.com/authoritative/settings.html\#tcp-fast-open "Permalink to this headline")

- Integer
- Default: 0 (Disabled)

Enable TCP Fast Open support, if available, on the listening sockets.
The numerical value supplied is used as the queue size, 0 meaning
disabled.

## `tcp-idle-timeout` [¶](https://doc.powerdns.com/authoritative/settings.html\#tcp-idle-timeout "Permalink to this headline")

- Integer
- Default: 5

Maximum time in seconds that a TCP DNS connection is allowed to stay
open while being idle, meaning without PowerDNS receiving or sending
even a single byte.

## `traceback-handler` [¶](https://doc.powerdns.com/authoritative/settings.html\#traceback-handler "Permalink to this headline")

- Boolean
- Default: yes

Enable the Linux-only traceback handler.

## `trusted-notification-proxy` [¶](https://doc.powerdns.com/authoritative/settings.html\#trusted-notification-proxy "Permalink to this headline")

Changed in version 4.4.0: This option now accepts a comma-separated list of IP ranges. This was a list of IP addresses before.

- IP ranges, separated by commas

IP ranges of incoming notification proxies.

## `udp-truncation-threshold` [¶](https://doc.powerdns.com/authoritative/settings.html\#udp-truncation-threshold "Permalink to this headline")

- Integer
- Default: 1232

EDNS0 allows for large UDP response datagrams, which can potentially
raise performance. Large responses however also have downsides in terms
of reflection attacks. Maximum value is 65535, but values above
4096 should probably not be attempted.

Note

Why 1232?

1232 is the largest number of payload bytes that can fit in the smallest IPv6 packet.
IPv6 has a minimum MTU of 1280 bytes ( [**RFC 8200, section 5**](https://tools.ietf.org/html/rfc8200.html#section-5)), minus 40 bytes for the IPv6 header, minus 8 bytes for the UDP header gives 1232, the maximum payload size for the DNS response.

## `upgrade-unknown-types` [¶](https://doc.powerdns.com/authoritative/settings.html\#upgrade-unknown-types "Permalink to this headline")

- Boolean
- Default: no

New in version 4.4.0.

Transparently upgrade records stored as TYPE#xxx and RFC 3597 (hex format)
contents, if the type is natively supported.
When this is disabled, records stored in this format cannot be served.

Recommendation: keep disabled for better performance.
Enable for testing PowerDNS upgrades, without changing stored records.
Enable for upgrading record content on secondaries, or when using the API (see [upgrade notes](https://doc.powerdns.com/authoritative/upgrading.html)).
Disable after record contents have been upgraded.

This option is supported by the bind and Generic SQL backends.

Note

When using a generic SQL backend, records with an unknown record type (see [Supported Record Types](https://doc.powerdns.com/authoritative/appendices/types.html)) can be identified with the following SQL query:

```
SELECT * from records where type like 'TYPE%';
```

## `version-string` [¶](https://doc.powerdns.com/authoritative/settings.html\#version-string "Permalink to this headline")

- Any of: `anonymous`, `powerdns`, `full`, String
- Default: full

When queried for its version over DNS
(`dig chaos txt version.bind @pdns.ip.address`), PowerDNS normally
responds truthfully. With this setting you can overrule what will be
returned. Set the `version-string` to `full` to get the default
behaviour, to `powerdns` to just make it state
`Served by PowerDNS - https://www.powerdns.com/`. The `anonymous`
setting will return a ServFail, much like Microsoft nameservers do. You
can set this response to a custom value as well.

## `views` [¶](https://doc.powerdns.com/authoritative/settings.html\#views "Permalink to this headline")

- Boolean
- Default: no

New in version 5.0.0.

Enable [Views](https://doc.powerdns.com/authoritative/views.html).

## `webserver` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver "Permalink to this headline")

- Boolean
- Default: no

Start a webserver for monitoring. See [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html)”.

## `webserver-address` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-address "Permalink to this headline")

- IP Address
- Default: 127.0.0.1

IP Address for webserver/API to listen on.

Changed in version 5.0.0: A path to a UNIX domain socket may be used instead of an IP address.

## `webserver-allow-from` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-allow-from "Permalink to this headline")

- IP ranges, separated by commas or whitespace
- Default: 127.0.0.1,::1

Webserver/API access is only allowed from these subnets.
Ignored if `webserver-address` is set to a UNIX domain socket.

## `webserver-hash-plaintext-credentials` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-hash-plaintext-credentials "Permalink to this headline")

New in version 4.6.0.

- Boolean
- Default: no

Whether passwords and API keys supplied in the configuration as plaintext should be hashed during startup, to prevent the plaintext versions from staying in memory. Doing so increases significantly the cost of verifying credentials and is thus disabled by default.
Note that this option only applies to credentials stored in the configuration as plaintext, but hashed credentials are supported without enabling this option.

## `webserver-loglevel` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-loglevel "Permalink to this headline")

- String, one of “none”, “normal”, “detailed”
- Default: normal

The amount of logging the webserver must do. “none” means no useful webserver information will be logged.
When set to “normal”, the webserver will log a line per request that should be familiar:

```
[webserver] e235780e-a5cf-415e-9326-9d33383e739e 127.0.0.1:55376 "GET /api/v1/servers/localhost/bla HTTP/1.1" 404 196
```

When set to “detailed”, all information about the request and response are logged:

```
[webserver] e235780e-a5cf-415e-9326-9d33383e739e Request Details:
[webserver] e235780e-a5cf-415e-9326-9d33383e739e  Headers:
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   accept-encoding: gzip, deflate
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   accept-language: en-US,en;q=0.5
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   connection: keep-alive
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   dnt: 1
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   host: 127.0.0.1:8081
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   upgrade-insecure-requests: 1
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   user-agent: Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0
[webserver] e235780e-a5cf-415e-9326-9d33383e739e  No body
[webserver] e235780e-a5cf-415e-9326-9d33383e739e Response details:
[webserver] e235780e-a5cf-415e-9326-9d33383e739e  Headers:
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   Connection: close
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   Content-Length: 49
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   Content-Type: text/html; charset=utf-8
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   Server: PowerDNS/0.0.15896.0.gaba8bab3ab
[webserver] e235780e-a5cf-415e-9326-9d33383e739e  Full body:
[webserver] e235780e-a5cf-415e-9326-9d33383e739e   <!html><title>Not Found</title><h1>Not Found</h1>
[webserver] e235780e-a5cf-415e-9326-9d33383e739e 127.0.0.1:55376 "GET /api/v1/servers/localhost/bla HTTP/1.1" 404 196
```

The value between the hooks is a UUID that is generated for each request. This can be used to find all lines related to a single request.

Note

The webserver logs these line on the NOTICE level. The [loglevel](https://doc.powerdns.com/authoritative/settings.html#setting-loglevel) setting must be 5 or higher for these lines to end up in the log.

## `webserver-max-bodysize` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-max-bodysize "Permalink to this headline")

- Integer
- Default: 2

Maximum request/response body size in megabytes.

## `webserver-connection-timeout` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-connection-timeout "Permalink to this headline")

New in version 4.8.5.

- Integer
- Default: 5

Request/response timeout in seconds.

## `webserver-password` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-password "Permalink to this headline")

Changed in version 4.6.0: This setting now accepts a hashed and salted version.

- String

Password required to access the webserver. Since 4.6.0 the password can be hashed and salted using `pdnsutil hash-password` instead of being present in the configuration in plaintext, but the plaintext version is still supported.

## `webserver-port` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-port "Permalink to this headline")

- Integer
- Default: 8081

The port where webserver/API will listen on.
Ignored if `webserver-address` is set to a UNIX domain socket.

## `webserver-print-arguments` [¶](https://doc.powerdns.com/authoritative/settings.html\#webserver-print-arguments "Permalink to this headline")

- Boolean
- Default: no

If the webserver should print arguments.

## `write-pid` [¶](https://doc.powerdns.com/authoritative/settings.html\#write-pid "Permalink to this headline")

- Boolean
- Default: yes

If a PID file should be written.

## `workaround-11804` [¶](https://doc.powerdns.com/authoritative/settings.html\#workaround-11804 "Permalink to this headline")

- Boolean
- Default: no

Workaround for [issue #11804 (outgoing AXFR may try to overfill a chunk and fail)](https://github.com/PowerDNS/pdns/issues/11804).

Default of no implies the pre-4.8 behaviour of up to 100 RRs per AXFR chunk.

If enabled, only a single RR will be put into each AXFR chunk, making some zones transferable when they were not otherwise.

## `xfr-cycle-interval` [¶](https://doc.powerdns.com/authoritative/settings.html\#xfr-cycle-interval "Permalink to this headline")

Changed in version 4.5.0: This was called [slave-cycle-interval](https://doc.powerdns.com/authoritative/settings.html#setting-slave-cycle-interval) before 4.5.0.

- Integer
- Default: 60

On a primary, this is the amount of seconds between the primary checking
the SOA serials in its database to determine to send out NOTIFYs to the
secondaries. On secondaries, this is the number of seconds between the
check for zones where the REFRESH period has expired. For zones where
that is the case, secondaries will request updates from the primary.

## `xfr-max-received-mbytes` [¶](https://doc.powerdns.com/authoritative/settings.html\#xfr-max-received-mbytes "Permalink to this headline")

- Integer
- Default: 100

Specifies the maximum number of received megabytes allowed on an
incoming AXFR/IXFR update, to prevent resource exhaustion. A value of 0
means no restriction.

## `zone-cache-refresh-interval` [¶](https://doc.powerdns.com/authoritative/settings.html\#zone-cache-refresh-interval "Permalink to this headline")

- Integer
- Default: 300

Seconds to cache a list of all known zones. A value of 0 will disable the cache.

If your backends do not respond to unknown or dynamically generated zones, it is suggested to enable [consistent-backends](https://doc.powerdns.com/authoritative/settings.html#setting-consistent-backends) (default since 4.5) and leave this option at its default of 300.

If [views](https://doc.powerdns.com/authoritative/settings.html#setting-views) are enabled, the zone cache **must** be enabled.

## `zone-metadata-cache-ttl` [¶](https://doc.powerdns.com/authoritative/settings.html\#zone-metadata-cache-ttl "Permalink to this headline")

Changed in version 4.5.0: This was called [domain-metadata-cache-ttl](https://doc.powerdns.com/authoritative/settings.html#setting-domain-metadata-cache-ttl) before 4.5.0.

- Integer
- Default: 60

Seconds to cache zone metadata from the database. A value of 0
disables caching.

[ixfrdist.yml](https://doc.powerdns.com/authoritative/manpages/ixfrdist.yml.5.html "previous chapter (use the left arrow)")

[Security Advisories](https://doc.powerdns.com/authoritative/security-advisories/index.html "next chapter (use the right arrow)")

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/security-advisories/index.html "Security Advisories") \|
- [previous](https://doc.powerdns.com/authoritative/manpages/ixfrdist.yml.5.html "ixfrdist.yml") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

---

### 2. Setting up a self-hosted authoritative DNS server with PowerDNS - Tarneo's blog


**Source:** [https://tarneo.fr/posts/powerdns/](https://tarneo.fr/posts/powerdns/)
**Domain:** `tarneo.fr`
**Quality Score:** 5

*Programming, Linux, self-hosting, ergo keyboards, IT ethics...*

I have been using Cloudflare for over a year now for multiple domain names. I wanted to migrate away from that, and chose to self-host DNS using [PowerDNS](https://www.powerdns.com/).

PowerDNS provides multiple types DNS servers, but what you’ll want to host our own domain is an authoritative name server. This will publish the DNS records for our domain so that recursive name servers (like Google’s, Cloudflare’s or your ISP’s) can forward the data to clients.

## Prerequisites

Most registrars will require you to have two different name servers, which is a good practice (I chose OVH as my registrar but anything should work with this tutorial).

Ideally you want to have your two DNS servers at two different locations to provide enough redundancy. I chose to have one server on a VPS and another at home on the main [Renn.es](https://renn.es/) server. Make sure your ISP allows opening port 53 and requests come through correctly though, as most don’t.

## Compose example

Here is a `docker-compose` example:

```yaml
services:
  pdns:
    container_name: pdns
    image: powerdns/pdns-auth-49 # See what the latest version is on docker hub
    ports:
      - "53:53"
      - "53:53/udp"
    volumes:
      - "/data/pdns/varlib:/var/lib/powerdns"
      - "/data/pdns/etc:/etc/powerdns"
```

You should of course change `/data/pdns` to wherever you want to host your PowerDNS related files.

Run `docker-compose up -d` once before proceeding to create the volume directories. It will probably just fail to start because of a missing database file.

## Creating the database

Download the database schema from [GitHub](https://github.com/PowerDNS/pdns/blob/master/modules/gsqlite3backend/schema.sqlite3.sql).

Then run:

```sh
sudo sqlite3 /data/pdns/varlib/pdns.sqlite3 < schema.sqlite3.sql
```

I had a permission issue when trying to run the container again, so I ran a `sudo chown -R 953:953 /data/pdns`. Make sure there is no UID or GID 953 on your system because that user would have access to `/data/pdns` (or make sure that `/data` is not readable by that user).

Then run `docker-compose up -d` again. The container’s log should end with the following line:

```
Done launching threads, ready to distribute questions
```

## Editing zones

There are many frontends for PowerDNS, but I chose to not install any and use the included [pdnsutil](https://doc.powerdns.com/authoritative/manpages/pdnsutil.1.html) command-line utility for simplicity.

Create an empty zone for your domain name (I’ll use `charennes.org` from now on as an example):

```sh
docker exec -it pdns pdnsutil create-zone charennes.org
```

Edit the zone (I hope you’re familiar with `vi`):

```sh
docker exec -it pdns pdnsutil edit-zone charennes.org
```

I first changed the default [SOA record](https://en.wikipedia.org/wiki/SOA_record) to match the configuration I wanted:

```dns
charennes.org   3600    IN      SOA     ns.charennes.org admin.charennes.org 0 10800 3600 604800 3600
```

This tells DNS that the name of the main DNS server for your zone is `ns.yourdomain.org` (`ns.charennes.org` in my case). You should also add an email address with the `@` replaced by a dot. If there are dots in your email address (before the `@`), use a backslash to escape them.

So let’s create an A record for `ns.charennes.org`:

```dns
ns.charennes.org        3600    IN      A       82.64.143.64
```

Of course you should replace the IP to match your public IP.

Let’s also add our VPS’s public IP, which will be used as a backup:

```dns
ns2.charennes.org       3600    IN      A       51.210.180.14
```

We can then add two NS records to point to the DNS servers we just defined:

```dns
charennes.org   3600    IN      NS      ns.charennes.org
charennes.org   3600    IN      NS      ns2.charennes.org
```

I also added the following to set the IPv4 address of `charennes.org`:

```dns
charennes.org   3600    IN      A       82.64.143.64
```

Here’s the final file:

```dns
; Warning - every name in this file is ABSOLUTE!
$ORIGIN .
charennes.org   3600    IN      SOA     ns.charennes.org admin.charennes.org 0 10800 3600 604800 3600
charennes.org   3600    IN      A       82.64.143.64
charennes.org   3600    IN      NS      ns.charennes.org
charennes.org   3600    IN      NS      ns2.charennes.org
ns.charennes.org        3600    IN      A       82.64.143.64
ns2.charennes.org       3600    IN      A       51.210.180.14
```

Now I was able to test the server with the following command:

```sh
nslookup charennes.org <server-ip>
```

```
...
Address: 82.64.143.64
...
```

Remember to open port 53 (for both TCP and UDP) and check that queries also work from outside your firewall!

I also ran the following command to enable DNSSEC:

```sh
docker exec -it pdns pdnsutil secure-zone charennes.org
docker exec -it pdns pdnsutil rectify-zone charennes.org
```

Note that you will have to find a way to sync the server’s database between your two servers. I chose to use a one-way rsync script which I run every time I update stuff. Remember to restart the docker container whenever you overwrite the database because it won’t reread it by itself. Also know that overwriting databases is not the best practice in most cases, but I think it’s OK here since the database isn’t being written to without modifying domains.

## Letting DNS know about our new server

Now you’ll need to tell your registrar about the server you just created. This is a bit tricky as you need to give the registrar the domain names of your servers, but they don’t have one yet as the DNS isn’t propagated. What I did was add A records for `ns.charennes.org` and `ns2.charennes.org` matching the ones I had defined on my own name server, and then set the DNS servers to those which worked alright. It took some time though, around an hour to get to my own PC, but it could be up to two days until every computer on the internet has the new correct records (due to cache time to live).

## Errata

You also need to add a DS record in your registrar’s control panel for DNSSEC to work! Here is how to find the DS record(s):

```
docker exec -it pdns pdnsutil show-zone charennes.org
```

Two of the outputted lines will be something like:

```
ID = 3 (CSK), flags = 257, tag = 7327, algo = 13, bits = 256      Active         Published  ( ECDSAP256SHA256 )
CSK DNSKEY = charennes.org. IN DNSKEY 257 3 13 <base64 encoded key> ; ( ECDSAP256SHA256 )
```

Copy the key to your registrar, and you’re done! I had to enter key tag 7327, flag 257, algorithm 13 and the base64 encoded key.

For security, I would also recommend setting the `version-string` option to `anonymous` to avoid bots scanning your server for vulnerable versions.

(I have also fixed the docker image to use as I had used the development image instead of the production one.)

---

### 3. PowerDNS Configuration Requirements

**Source:** [https://docs.cloudblue.com/cbc/21.0/DNS-Hosting-Services/PowerDNS-Configuration-Requirements.htm](https://docs.cloudblue.com/cbc/21.0/DNS-Hosting-Services/PowerDNS-Configuration-Requirements.htm)
**Domain:** `docs.cloudblue.com`
**Quality Score:** 5

# PowerDNS Configuration Requirements

On each server that you prepared, install and configure PowerDNS so that the following requirements are met:

**Note:** To learn how to install and configure PowerDNS, please refer to [its documentation](https://doc.powerdns.com/authoritative/index.html).

01. The PowerDNS Authoritative service is installed.

02. The backend of the PowerDNS Authoritative service is installed.

03. The service is configured to use the required backend.

04. The service and its backend are configured to start automatically.

05. The service uses a public IP address. For example:


    ```
    /etc/pdns/pdns.conf
    ...
    local-address=PUBLIC_IP_ADDRESS_OF_POWERDNS_SERVER
    ...
    ```

06. The service can act as a primary or secondary DNS server. For example:


    ```
    /etc/pdns/pdns.conf
    ...
    master=yes
    slave=yes
    ...
    ```

07. DNS zone transfer is allowed between primary and secondary PowerDNS servers. For example:


    ```
    /etc/pdns/pdns.conf
    ...
    disable-axfr=no
    allow-axfr-ips=PUBLIC_IP_ADDRESS_OF_POWERDNS_SERVER_1  PUBLIC_IP_ADDRESS_OF_POWERDNS_SERVER_2
    ...
    ```

08. The REST API of the service is enabled and uses the 127.0.0.1 IP address. For example:


    ```
    /etc/pdns/pdns.conf
    ...
    api=yes
    api-key=REST_API_KEY
    webserver-address=127.0.0.1
    webserver-port=8081
    webserver-allow-from=127.0.0.1
    ...
    ```

09. The service and its backend are running.
10. HTTPS access to the REST API of the service is configured:


    - An HTTPS proxy is installed and configured on the server. It uses a private IP address configured on the server and proxies connections to the REST API.

    - This HTTPS proxy uses an SSL certificate that contains the private IP address of the server in its Subject Alternative Name (SAN).


For example, you can generate such an SSL certificate in the following way:

    1. Generate a self-signed certificate:


       ```
       openssl genrsa -out ca.key 2048
       openssl req -new -x509 -days 365 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt
       ```

    2. Generate a certificate that contains the required private IP address in its SAN and sign it by the certificate you created in step a.


       ```
       openssl req -newkey rsa:2048 -nodes -keyout cert.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=*.example.com" -out cert.csr
       openssl x509 -req -extfile <(printf "subjectAltName=IP:PRIVATE_IP_ADDRESS_OF_POWERDNS_SERVER") -days 365 -in cert.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out cert.crt
       ```


For example, you can install [NGINX](https://www.nginx.com/) on the server and configure it to proxy connections:
    1. Install NGINX:


       ```
       yum install nginx -y
       ```

    2. Disable the default server in `/etc/nginx/nginx.conf`:


       ```
       #    server {
       #        listen       80;
       #        listen       [::]:80;
       #        server_name  _;
       #        root         /usr/share/nginx/html;
       #
       #        # Load configuration files for the default server block.
       #        include /etc/nginx/default.d/*.conf;
       #
       #        error_page 404 /404.html;
       #        location = /404.html {
       #        }
       #
       #        error_page 500 502 503 504 /50x.html;
       #        location = /50x.html {
       #        }
       #    }
       ```

    3. Place your SSL certificate, which contains the private IP address of the server in its SAN, and its private key (`cert.key` and `cert.crt`) to `/etc/nginx/`.

    4. Create `/etc/nginx/conf.d/powerdns.conf`:


       ```
       server {

         listen 443 ssl;

         ssl_certificate /etc/nginx/cert.crt;
         ssl_certificate_key /etc/nginx/cert.key;

         ssl_session_cache builtin:1000 shared:SSL:10m;
         ssl_protocols TLSv1.2;
         ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
         ssl_prefer_server_ciphers on;

         access_log /var/log/nginx/powerdns.access.log;

         location / {

           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           proxy_pass http://127.0.0.1:8081;
           proxy_read_timeout 90;

           proxy_redirect http://127.0.0.1:8081 https://PRIVATE_IP_ADDRESS_OF_POWERDNS_SERVER;
         }
       }
       ```

    5. Configure NGINX to start automatically:


       ```
       systemctl enable nginx
       ```

    6. Start NGINX and check its status:


       ```
       systemctl start nginx
       systemctl status nginx
       ```

**Note**: After you prepare the server, check that the Operations Support System (oss) component can connect to the PowerDNS REST API of that server. To do this, execute this command in an OSS pod of your Kubernetes cluster: `curl -v -k -H 'X-API-Key: REST_API_KEY' https://PRIVATE_IP_ADDRESS_OF_POWERDNS_SERVER/api/v1/servers/localhost`

---

### 4.
Hosting your own authoritative DNS servers using PowerDNS | Bluemedia



**Source:** [https://bluemedia.dev/blog/authorative-dns-server-using-powerdns/](https://bluemedia.dev/blog/authorative-dns-server-using-powerdns/)
**Domain:** `bluemedia.dev`
**Quality Score:** 3

# Hosting your own authoritative DNS servers using PowerDNS


Bluemedia (Oliver)
\|

Dec 22, 2021


\| 5
min read


![Hosting your own authoritative DNS servers using PowerDNS](https://bluemedia.dev/images/general/server-rack.jpg)

## Intro

A quick disclaimer at first: This post is not intended to be a complete guide on how to build your own system. It is more intended as an example of how I solved my personal requirements. PowerDNS is a very powerful tool and offers many ways to solve problems in different ways. In the end, everyone has to decide for themselves what they think is an ideal configuration and whether they want to leave it to the “big bad internet” like this.

**Should you run your own authoritative DNS servers?**

_In most cases, probably not._

**Am I doing it anyway?**

_Of course I do._

**Why, you may ask?**

_Because I can, and it’s a good way to learn more about DNS._

I’m generally a big fan of having important services under my own control, as you may have noticed already from some other posts. This allows me to customize them exactly as I want to. My infrastructure is mostly automated, so I don’t have to waste my free time on maintaining it. Unfortunately, my registrar, where I get almost all my domain names, doesn’t have a particularly great API for managing DNS records. This is, of course, a problem in such a case.

Because of this, I’ve been using Cloudflare as my DNS provider for a while now. The free package with the included features is quite usable, and they have a really great API. After the second major outage of Cloudflare, however, I realized that it might not be the best idea to make half of the Internet depend on one provider. For this reason and also because I’m generally interested in the topic from a technical perspective, it ended up on my to-do list at some point.

## Starting off with a plan

So what are the things you need to consider if you really want to run such a service yourself?

In my opinion, you should know what you are doing before you actually start doing it. Accordingly, the topic has started for me by first reading up on “best practices” for DNS and the documentation of my desired software ( [PowerDNS](https://www.powerdns.com/)) over a good cup of coffee. While doing so, a more or less finished concept formed in my head, which I’m fairly certain is perfectly acceptable as is.

Based on my initial starting position, I knew it had to be highly available, fault-tolerant, and relatively inexpensive. These things are not necessarily opposed to each other here.

To meet my requirements, I’m using two small servers at different providers (Hetzner and Netcup) located at different sites (Nuremberg and Falkenstein). Furthermore, because both servers are in different top-level domains (.dev and.re), even the theoretical failure of an entire top-level domain can be compensated.

Each server runs a MariaDB instance and PowerDNS with a minimal configuration. NS1 is the primary system, which is also used for administration. NS2 hosts a read-only replica of the PowerDNS database and PowerDNS itself. Both externally accessible PowerDNS instances have read-only access to the database and no enabled special functions, such as the HTTP API. They merely act as “dumb” resolvers.

On NS1, there is also another PowerDNS instance running inside Docker, this time with write access to the database and an enabled HTTP API, as well as an instance of [PowerDNS-Admin](https://github.com/PowerDNS-Admin/PowerDNS-Admin) for the actual administration. From the outside, PowerDNS-Admin is accessible via an Nginx reverse proxy that takes care of things like TLS termination and logging. Both servers are connected by a WireGuard tunnel for the MariaDB replication traffic.

PowerDNS-Admin is a comprehensive administration toolkit for PowerDNS. It provides full multi-tenancy in terms of zone management and can manage API keys restricted to individual zones. It also provides a well-organized web interface for the overall administration.

This is how my finished concept looks on the drawing board:
![](https://bluemedia.dev/images/posts/authorative-dns-server-using-powerdns/pdns-architecture.png)

## Keeping security in mind

If you operate such a service publicly, you should also take some time to think about security. After all, you don’t want your own infrastructure to be immediately taken over by the next best troll or abused for DDoS.

Therefore, it is necessary to think about the following rules:

- Only absolutely necessary services should be accessible from external sources
- Systems must be protected against unauthorized access (e.g., SSH only via public key authentication)
- Always use strong passwords and 2FA everywhere (in this case, PowerDNS-Admin)
- All software should be kept up-to-date and patches should be installed in a timely manner after their release

With DNS, there are some additional things that will save you and others from trouble:

- Both PowerDNS instances are authoritative-only and do not allow recursive queries
- Zone transfer (AXFR) should be disabled if not required, or at least restricted to certain IPs. This prevents all DNS entries (entire zones) from being retrieved at once
- You should configure appropriate rate limits in PowerDNS to make it as difficult as possible for attackers to abuse your servers for DNS reflection attacks (DDoS amplification)

## Conclusion

With a bit of ingenuity, the right planning, and the relevant documentation, an idea like this can certainly become a reality. This opens up countless possibilities to customize the system to your own needs. You need an additional DNS server? Just set up another replica. If necessary, all of this can also be automated.

By now, I’ve been running my two DNS servers productively for almost two months and have already survived the first failures without any problems. Both servers were offline for a short period of time due to problems with their respective host systems, but due to the separation of the two instances, it was still possible to resolve the domains at any time.

Because PowerDNS is very resource-saving and I don’t expect many DNS requests anyway, I can use the smallest server size that the respective hosting company offers. This brings my total cost to about 6 euros per month, which is still quite impressive in my opinion.

---

### 5. Guides and How Tos — PowerDNS Authoritative Server  documentation

**Source:** [https://doc.powerdns.com/authoritative/guides/index.html](https://doc.powerdns.com/authoritative/guides/index.html)
**Domain:** `doc.powerdns.com`
**Quality Score:** 3

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/guides/basic-database.html "Basic setup: configuring database connectivity") \|
- [previous](https://doc.powerdns.com/authoritative/lua-records/reference/misc.html "Other functions") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

[PowerDNS Authoritative Server](https://doc.powerdns.com/authoritative/indexTOC.html)

#### Previous topic

[Other functions](https://doc.powerdns.com/authoritative/lua-records/reference/misc.html "previous chapter")

#### Next topic

[Basic setup: configuring database connectivity](https://doc.powerdns.com/authoritative/guides/basic-database.html "next chapter")

## Contents

- [PowerDNS Authoritative Nameserver](https://doc.powerdns.com/authoritative/index.html)
- [Installing PowerDNS](https://doc.powerdns.com/authoritative/installation.html)
- [Upgrade Notes](https://doc.powerdns.com/authoritative/upgrading.html)
- [DNS Modes of Operation](https://doc.powerdns.com/authoritative/modes-of-operation.html)
- [Migrating to PowerDNS](https://doc.powerdns.com/authoritative/migration.html)
- [Running and Operating](https://doc.powerdns.com/authoritative/running.html)
- [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html)
- [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html)
- [DNSSEC](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [Per zone settings: Domain Metadata](https://doc.powerdns.com/authoritative/domainmetadata.html)
- [Dynamic DNS Update (RFC 2136)](https://doc.powerdns.com/authoritative/dnsupdate.html)
- [Catalog Zones (RFC 9432)](https://doc.powerdns.com/authoritative/catalog.html)
- [TSIG](https://doc.powerdns.com/authoritative/tsig.html)
- [Views](https://doc.powerdns.com/authoritative/views.html)
- [Lua Records](https://doc.powerdns.com/authoritative/lua-records/index.html)
- [Guides and How Tos](https://doc.powerdns.com/authoritative/guides/index.html#)
  - [Basic setup: configuring database connectivity](https://doc.powerdns.com/authoritative/guides/basic-database.html)
  - [Migrating from using recursion on the Authoritative Server to using a Recursor](https://doc.powerdns.com/authoritative/guides/recursion.html)
  - [Running Virtual Instances](https://doc.powerdns.com/authoritative/guides/virtual-instances.html)
  - [Using ALIAS records](https://doc.powerdns.com/authoritative/guides/alias.html)
  - [Using SVCB and derived records](https://doc.powerdns.com/authoritative/guides/svcb.html)
  - [KSK Rollover](https://doc.powerdns.com/authoritative/guides/kskroll.html)
  - [KSK Rollover using CDS & CDNSKEY Key Rollover](https://doc.powerdns.com/authoritative/guides/kskrollcdnskey.html)
  - [ZSK Rollover](https://doc.powerdns.com/authoritative/guides/zskroll.html)
  - [Algorithm Rollover](https://doc.powerdns.com/authoritative/guides/algoroll.html)
  - [Adding new DNS record types](https://doc.powerdns.com/authoritative/guides/addingrecords.html)
- [Backends](https://doc.powerdns.com/authoritative/backends/index.html)
- [Built-in Webserver and HTTP API](https://doc.powerdns.com/authoritative/http-api/index.html)
- [Manual Pages](https://doc.powerdns.com/authoritative/manpages/index.html)
- [Authoritative Server Settings](https://doc.powerdns.com/authoritative/settings.html)
- [Security Advisories](https://doc.powerdns.com/authoritative/security-advisories/index.html)
- [Changelogs](https://doc.powerdns.com/authoritative/changelog/index.html)
- [End of life statements](https://doc.powerdns.com/authoritative/appendices/EOL.html)
- [Frequently Asked Questions](https://doc.powerdns.com/authoritative/appendices/FAQ.html)
- [Backend writers’ guide](https://doc.powerdns.com/authoritative/appendices/backend-writers-guide.html)
- [Compiling PowerDNS](https://doc.powerdns.com/authoritative/appendices/compiling.html)
- [Cryptographic software and export control](https://doc.powerdns.com/authoritative/appendices/crypto-export.html)
- [Internals](https://doc.powerdns.com/authoritative/appendices/internals.html)
- [Supported Record Types](https://doc.powerdns.com/authoritative/appendices/types.html)
- [PowerDNS/dnsdist license](https://doc.powerdns.com/authoritative/common/license.html)

### This Page

- [Show Source](https://doc.powerdns.com/authoritative/_sources/guides/index.rst.txt)

1. [Docs](https://doc.powerdns.com/authoritative/indexTOC.html)
2. Guides and How Tos

# Guides and How Tos [¶](https://doc.powerdns.com/authoritative/guides/index.html\#guides-and-how-tos "Permalink to this headline")

- [Basic setup: configuring database connectivity](https://doc.powerdns.com/authoritative/guides/basic-database.html)
- [Migrating from using recursion on the Authoritative Server to using a Recursor](https://doc.powerdns.com/authoritative/guides/recursion.html)
- [Running Virtual Instances](https://doc.powerdns.com/authoritative/guides/virtual-instances.html)
- [Using ALIAS records](https://doc.powerdns.com/authoritative/guides/alias.html)
- [Using SVCB and derived records](https://doc.powerdns.com/authoritative/guides/svcb.html)
- [KSK Rollover](https://doc.powerdns.com/authoritative/guides/kskroll.html)
- [KSK Rollover using CDS & CDNSKEY Key Rollover](https://doc.powerdns.com/authoritative/guides/kskrollcdnskey.html)
- [ZSK Rollover](https://doc.powerdns.com/authoritative/guides/zskroll.html)
- [Algorithm Rollover](https://doc.powerdns.com/authoritative/guides/algoroll.html)
- [Adding new DNS record types](https://doc.powerdns.com/authoritative/guides/addingrecords.html)

[Other functions](https://doc.powerdns.com/authoritative/lua-records/reference/misc.html "previous chapter (use the left arrow)")

[Basic setup: configuring database connectivity](https://doc.powerdns.com/authoritative/guides/basic-database.html "next chapter (use the right arrow)")

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/guides/basic-database.html "Basic setup: configuring database connectivity") \|
- [previous](https://doc.powerdns.com/authoritative/lua-records/reference/misc.html "Other functions") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

---

### 6. Performance and Tuning — PowerDNS Authoritative Server  documentation

**Source:** [https://doc.powerdns.com/authoritative/performance.html](https://doc.powerdns.com/authoritative/performance.html)
**Domain:** `doc.powerdns.com`
**Quality Score:** 3

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/dnssec/index.html "DNSSEC") \|
- [previous](https://doc.powerdns.com/authoritative/security.html "Security of PowerDNS") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

[PowerDNS Authoritative Server](https://doc.powerdns.com/authoritative/indexTOC.html)

#### Previous topic

[Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html "previous chapter")

#### Next topic

[DNSSEC](https://doc.powerdns.com/authoritative/dnssec/index.html "next chapter")

## Contents

- [PowerDNS Authoritative Nameserver](https://doc.powerdns.com/authoritative/index.html)
- [Installing PowerDNS](https://doc.powerdns.com/authoritative/installation.html)
- [Upgrade Notes](https://doc.powerdns.com/authoritative/upgrading.html)
- [DNS Modes of Operation](https://doc.powerdns.com/authoritative/modes-of-operation.html)
- [Migrating to PowerDNS](https://doc.powerdns.com/authoritative/migration.html)
- [Running and Operating](https://doc.powerdns.com/authoritative/running.html)
- [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html)
- [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html#)
  - [Performance related settings](https://doc.powerdns.com/authoritative/performance.html#performance-related-settings)
  - [Packet Cache](https://doc.powerdns.com/authoritative/performance.html#packet-cache)
  - [Query Cache](https://doc.powerdns.com/authoritative/performance.html#query-cache)
  - [Caches & Memory Allocations & glibc](https://doc.powerdns.com/authoritative/performance.html#caches-memory-allocations-glibc)
  - [Performance Monitoring](https://doc.powerdns.com/authoritative/performance.html#performance-monitoring)
    - [Counters](https://doc.powerdns.com/authoritative/performance.html#metricnames)
      - [corrupt-packets](https://doc.powerdns.com/authoritative/performance.html#corrupt-packets)
      - [deferred-cache-inserts](https://doc.powerdns.com/authoritative/performance.html#deferred-cache-inserts)
      - [deferred-cache-lookup](https://doc.powerdns.com/authoritative/performance.html#deferred-cache-lookup)
      - [deferred-packetcache-inserts](https://doc.powerdns.com/authoritative/performance.html#deferred-packetcache-inserts)
      - [deferred-packetcache-lookup](https://doc.powerdns.com/authoritative/performance.html#deferred-packetcache-lookup)
      - [dnsupdate-answers](https://doc.powerdns.com/authoritative/performance.html#dnsupdate-answers)
      - [dnsupdate-changes](https://doc.powerdns.com/authoritative/performance.html#dnsupdate-changes)
      - [dnsupdate-queries](https://doc.powerdns.com/authoritative/performance.html#dnsupdate-queries)
      - [dnsupdate-refused](https://doc.powerdns.com/authoritative/performance.html#dnsupdate-refused)
      - [incoming-notifications](https://doc.powerdns.com/authoritative/performance.html#incoming-notifications)
      - [key-cache-size](https://doc.powerdns.com/authoritative/performance.html#key-cache-size)
      - [latency](https://doc.powerdns.com/authoritative/performance.html#latency)
      - [meta-cache-size](https://doc.powerdns.com/authoritative/performance.html#meta-cache-size)
      - [open-tcp-connections](https://doc.powerdns.com/authoritative/performance.html#open-tcp-connections)
      - [overload-drops](https://doc.powerdns.com/authoritative/performance.html#overload-drops)
      - [packetcache-hit](https://doc.powerdns.com/authoritative/performance.html#packetcache-hit)
      - [packetcache-miss](https://doc.powerdns.com/authoritative/performance.html#packetcache-miss)
      - [packetcache-size](https://doc.powerdns.com/authoritative/performance.html#packetcache-size)
      - [qsize-q](https://doc.powerdns.com/authoritative/performance.html#qsize-q)
      - [query-cache-hit](https://doc.powerdns.com/authoritative/performance.html#query-cache-hit)
      - [query-cache-miss](https://doc.powerdns.com/authoritative/performance.html#query-cache-miss)
      - [query-cache-size](https://doc.powerdns.com/authoritative/performance.html#query-cache-size)
      - [rd-queries](https://doc.powerdns.com/authoritative/performance.html#rd-queries)
      - [receive-latency](https://doc.powerdns.com/authoritative/performance.html#receive-latency)
      - [recursing-answers](https://doc.powerdns.com/authoritative/performance.html#recursing-answers)
      - [recursing-questions](https://doc.powerdns.com/authoritative/performance.html#recursing-questions)
      - [recursion-unanswered](https://doc.powerdns.com/authoritative/performance.html#recursion-unanswered)
      - [security-status](https://doc.powerdns.com/authoritative/performance.html#security-status)
      - [send-latency](https://doc.powerdns.com/authoritative/performance.html#send-latency)
      - [servfail-packets](https://doc.powerdns.com/authoritative/performance.html#servfail-packets)
      - [signature-cache-size](https://doc.powerdns.com/authoritative/performance.html#signature-cache-size)
      - [signatures](https://doc.powerdns.com/authoritative/performance.html#signatures)
      - [sys-msec](https://doc.powerdns.com/authoritative/performance.html#sys-msec)
      - [tcp-answers-bytes](https://doc.powerdns.com/authoritative/performance.html#tcp-answers-bytes)
      - [tcp-answers](https://doc.powerdns.com/authoritative/performance.html#tcp-answers)
      - [tcp-queries](https://doc.powerdns.com/authoritative/performance.html#tcp-queries)
      - [tcp4-answers-bytes](https://doc.powerdns.com/authoritative/performance.html#tcp4-answers-bytes)
      - [tcp4-answers](https://doc.powerdns.com/authoritative/performance.html#tcp4-answers)
      - [tcp4-queries](https://doc.powerdns.com/authoritative/performance.html#tcp4-queries)
      - [tcp6-answers-bytes](https://doc.powerdns.com/authoritative/performance.html#tcp6-answers-bytes)
      - [tcp6-answers](https://doc.powerdns.com/authoritative/performance.html#tcp6-answers)
      - [tcp6-queries](https://doc.powerdns.com/authoritative/performance.html#tcp6-queries)
      - [timedout-packets](https://doc.powerdns.com/authoritative/performance.html#timedout-packets)
      - [udp-answers-bytes](https://doc.powerdns.com/authoritative/performance.html#udp-answers-bytes)
      - [udp-answers](https://doc.powerdns.com/authoritative/performance.html#udp-answers)
      - [udp-do-queries](https://doc.powerdns.com/authoritative/performance.html#udp-do-queries)
      - [udp-in-csum-errors](https://doc.powerdns.com/authoritative/performance.html#udp-in-csum-errors)
      - [udp-in-errors](https://doc.powerdns.com/authoritative/performance.html#udp-in-errors)
      - [udp-noport-errors](https://doc.powerdns.com/authoritative/performance.html#udp-noport-errors)
      - [udp-queries](https://doc.powerdns.com/authoritative/performance.html#udp-queries)
      - [udp-recvbuf-errors](https://doc.powerdns.com/authoritative/performance.html#udp-recvbuf-errors)
      - [udp-sndbuf-errors](https://doc.powerdns.com/authoritative/performance.html#udp-sndbuf-errors)
      - [udp4-answers-bytes](https://doc.powerdns.com/authoritative/performance.html#udp4-answers-bytes)
      - [udp4-answers](https://doc.powerdns.com/authoritative/performance.html#udp4-answers)
      - [udp4-queries](https://doc.powerdns.com/authoritative/performance.html#udp4-queries)
      - [udp6-answers-bytes](https://doc.powerdns.com/authoritative/performance.html#udp6-answers-bytes)
      - [udp6-answers](https://doc.powerdns.com/authoritative/performance.html#udp6-answers)
      - [udp6-in-csum-errors](https://doc.powerdns.com/authoritative/performance.html#udp6-in-csum-errors)
      - [udp6-in-errors](https://doc.powerdns.com/authoritative/performance.html#udp6-in-errors)
      - [udp6-noport-errors](https://doc.powerdns.com/authoritative/performance.html#udp6-noport-errors)
      - [udp6-queries](https://doc.powerdns.com/authoritative/performance.html#udp6-queries)
      - [udp6-recvbuf-errors](https://doc.powerdns.com/authoritative/performance.html#udp6-recvbuf-errors)
      - [udp6-sndbuf-errors](https://doc.powerdns.com/authoritative/performance.html#udp6-sndbuf-errors)
      - [uptime](https://doc.powerdns.com/authoritative/performance.html#uptime)
      - [user-msec](https://doc.powerdns.com/authoritative/performance.html#user-msec)
    - [Ring buffers](https://doc.powerdns.com/authoritative/performance.html#ring-buffers)
    - [Sending metrics to Graphite/Metronome over Carbon](https://doc.powerdns.com/authoritative/performance.html#sending-metrics-to-graphite-metronome-over-carbon)
- [DNSSEC](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [Per zone settings: Domain Metadata](https://doc.powerdns.com/authoritative/domainmetadata.html)
- [Dynamic DNS Update (RFC 2136)](https://doc.powerdns.com/authoritative/dnsupdate.html)
- [Catalog Zones (RFC 9432)](https://doc.powerdns.com/authoritative/catalog.html)
- [TSIG](https://doc.powerdns.com/authoritative/tsig.html)
- [Views](https://doc.powerdns.com/authoritative/views.html)
- [Lua Records](https://doc.powerdns.com/authoritative/lua-records/index.html)
- [Guides and How Tos](https://doc.powerdns.com/authoritative/guides/index.html)
- [Backends](https://doc.powerdns.com/authoritative/backends/index.html)
- [Built-in Webserver and HTTP API](https://doc.powerdns.com/authoritative/http-api/index.html)
- [Manual Pages](https://doc.powerdns.com/authoritative/manpages/index.html)
- [Authoritative Server Settings](https://doc.powerdns.com/authoritative/settings.html)
- [Security Advisories](https://doc.powerdns.com/authoritative/security-advisories/index.html)
- [Changelogs](https://doc.powerdns.com/authoritative/changelog/index.html)
- [End of life statements](https://doc.powerdns.com/authoritative/appendices/EOL.html)
- [Frequently Asked Questions](https://doc.powerdns.com/authoritative/appendices/FAQ.html)
- [Backend writers’ guide](https://doc.powerdns.com/authoritative/appendices/backend-writers-guide.html)
- [Compiling PowerDNS](https://doc.powerdns.com/authoritative/appendices/compiling.html)
- [Cryptographic software and export control](https://doc.powerdns.com/authoritative/appendices/crypto-export.html)
- [Internals](https://doc.powerdns.com/authoritative/appendices/internals.html)
- [Supported Record Types](https://doc.powerdns.com/authoritative/appendices/types.html)
- [PowerDNS/dnsdist license](https://doc.powerdns.com/authoritative/common/license.html)

### This Page

- [Show Source](https://doc.powerdns.com/authoritative/_sources/performance.rst.txt)

1. [Docs](https://doc.powerdns.com/authoritative/indexTOC.html)
2. Performance and Tuning

# Performance and Tuning [¶](https://doc.powerdns.com/authoritative/performance.html\#performance-and-tuning "Permalink to this headline")

In general, best performance is achieved on recent Linux kernels with
the bindbackend, or if something more database-like is preferred,
the LMDB backend. Meanwhile many of the largest PowerDNS installations are
based on PostgreSQL or MySQL.

Database servers can require configuration to achieve decent
performance. It is especially worth noting that several vendors ship
PostgreSQL with a slow default configuration.

Warning

When deploying (large scale) IPv6, please be aware some
Linux distributions leave IPv6 routing cache tables at very small
default values. Please check and if necessary raise
`sysctl net.ipv6.route.max_size`.

## Performance related settings [¶](https://doc.powerdns.com/authoritative/performance.html\#performance-related-settings "Permalink to this headline")

When PowerDNS starts up it creates a number of threads to listen for
packets. This is configurable with the
[receiver-threads](https://doc.powerdns.com/authoritative/settings.html#setting-receiver-threads) setting which
defines how many sockets will be opened by the powerdns process. In
versions of linux before kernel 3.9 having too many receiver threads set
up resulted in decreased performance due to socket contention between
multiple CPUs - the typical sweet spot was 3 or 4. For optimal
performance on kernel 3.9 and following with
[reuseport](https://doc.powerdns.com/authoritative/settings.html#setting-reuseport) enabled you’ll typically want
a receiver thread for each core on your box if backend
latency/performance is not an issue and you want top performance.

Different backends will have different characteristics - some will want
to have more parallel instances than others. In general, if your backend
is latency bound, like most relational databases are, it pays to open
more backends.

This is done with the
[distributor-threads](https://doc.powerdns.com/authoritative/settings.html#setting-distributor-threads) setting
which says how many distributors will be opened for each receiver
thread. Of special importance is the choice between 1 or more backends.
In case of only 1 thread, PowerDNS reverts to unthreaded operation which
may be a lot faster, depending on your operating system and
architecture.

Other very important settings are
[cache-ttl](https://doc.powerdns.com/authoritative/settings.html#setting-cache-ttl). PowerDNS caches entire
packets it sends out so as to save the time to query backends to
assemble all data. The default setting of 20 seconds may be low for high
traffic sites, a value of 60 seconds rarely leads to problems. Please be
aware that if any TTL in the answer is shorter than this setting, the
packet cache will respect the answer’s shortest TTL.

Some PowerDNS operators set cache-ttl to many hours or even days, and
use [pdns\_control purge](https://doc.powerdns.com/authoritative/running.html#running-pdnscontrol) to
selectively or globally notify PowerDNS of changes made in the backend.
Also look at the [Query Cache](https://doc.powerdns.com/authoritative/performance.html#query-cache) described in this
chapter. It may materially improve your performance.

To determine if PowerDNS is unable to keep up with packets, determine
the value of the [qsize-q](https://doc.powerdns.com/authoritative/performance.html#stat-qsize-q) variable. This represents the number of
packets waiting for database attention. During normal operations the
queue should be small.
This number is a total over all receiver threads.

The [max-queue-length](https://doc.powerdns.com/authoritative/settings.html#setting-max-queue-length) and [overload-queue-length](https://doc.powerdns.com/authoritative/settings.html#setting-overload-queue-length) settings determine how PowerDNS deals with growing queues.
If the queue for a single receiver thread (and its associated distributor threads) grows beyond the `overload` number, queries are answered only from the packet cache so the database can hopefully recover.
If we reach the `max` number, we consider the situation hopeless and respawn the server process.

The value of [queue-limit](https://doc.powerdns.com/authoritative/settings.html#setting-queue-limit) should be set to only keep queries in
queue for as long as someone would be interested in knowing the answer. Many
resolvers will query other name servers for the zone quite aggressively.

Logging truly kills performance as answering a question from the cache
is an order of magnitude less work than logging a line about it. Busy
sites will prefer to turn [log-dns-details](https://doc.powerdns.com/authoritative/settings.html#setting-log-dns-details) off.

## Packet Cache [¶](https://doc.powerdns.com/authoritative/performance.html\#packet-cache "Permalink to this headline")

PowerDNS by default uses the ‘Packet Cache’ to recognise identical
questions and supply them with identical answers, without any further
processing. The default time to live is 20 seconds and can be changed by
setting `cache-ttl`. It has been observed that the utility of the
packet cache increases with the load on your nameserver.

Not all backends may benefit from the packet cache. If your backend is
memory based and does not lead to context switches, the packet cache may
actually hurt performance.

## Query Cache [¶](https://doc.powerdns.com/authoritative/performance.html\#query-cache "Permalink to this headline")

Besides entire packets, PowerDNS can also cache individual backend
queries. Each DNS query leads to a number of backend queries, the most
obvious additional backend query is the check for a possible CNAME. So,
when a query comes in for the ‘A’ record for ‘www.powerdns.com’,
PowerDNS must first check for a CNAME for ‘www.powerdns.com’.

The Query Cache caches these backend queries, many of which are quite
repetitive. The maximum number of entries in the cache is controlled by
the `max-cache-entries` setting. Before 4.1 this setting also controls
the maximum number of entries in the packet cache.

Most gain is made from caching negative entries, ie, queries that have
no answer. As these take little memory to store and are typically not a
real problem in terms of speed-of-propagation, the default TTL for
negative queries is a rather high 60 seconds.

This only is a problem when first doing a query for a record, adding it,
and immediately doing a query for that record again. It may then take up
to 60 seconds to appear. Changes to existing records however do not fall
under the negative query ttl
( [negquery-cache-ttl](https://doc.powerdns.com/authoritative/settings.html#setting-negquery-cache-ttl)), but under
the generic [query-cache-ttl](https://doc.powerdns.com/authoritative/settings.html#setting-query-cache-ttl) which
defaults to 20 seconds.

The default values should work fine for many sites. When tuning, keep in
mind that the Query Cache mostly saves database access but that the
Packet Cache also saves a lot of CPU because zero internal processing is
done when answering a question from the Packet Cache.

## Caches & Memory Allocations & glibc [¶](https://doc.powerdns.com/authoritative/performance.html\#caches-memory-allocations-glibc "Permalink to this headline")

Managing the two caches described above involves a lot of memory management, that is handled by `malloc` in your libc.
To avoid contention between threads, the allocator in glibc separates memory into separate arenas, sometimes even hundreds of them.
This avoids locking, but it may cause massive memory fragmentation, that could make PowerDNS take [an order of magnitude more memory](https://sourceware.org/bugzilla/show_bug.cgi?id=11261) in some situations.

If you suspect this is happening on your setup, you can consider lowering `MALLOC_ARENA_MAX` to a small number.
Several users have reported that `4` works well for them.
Via `systemctl edit pdns` you can put `Environment=MALLOC_ARENA_MAX=4` in your pdns unit file to enable this tweak.

Note that [newer glibc versions replace MALLOC\_ARENA\_MAX with a different setting syntax](https://www.gnu.org/software/libc/manual/html_node/Tunables.html#Tunables).
The new syntax is `GLIBC_TUNABLES=glibc.malloc.arena_max=4`, please check which syntax is valid for your glibc version (it is quite likely that both syntaxes will work).

## Performance Monitoring [¶](https://doc.powerdns.com/authoritative/performance.html\#performance-monitoring "Permalink to this headline")

A number of counters and variables are set during PowerDNS Authoritative
Server operation.

### Counters [¶](https://doc.powerdns.com/authoritative/performance.html\#metricnames "Permalink to this headline")

All counters that show the “number of X” count since the last startup of the daemon.

#### corrupt-packets [¶](https://doc.powerdns.com/authoritative/performance.html\#corrupt-packets "Permalink to this headline")

Number of corrupt packets received

#### deferred-cache-inserts [¶](https://doc.powerdns.com/authoritative/performance.html\#deferred-cache-inserts "Permalink to this headline")

Number of cache inserts that were deferred because of maintenance

#### deferred-cache-lookup [¶](https://doc.powerdns.com/authoritative/performance.html\#deferred-cache-lookup "Permalink to this headline")

Number of cache lookups that were deferred because of maintenance

#### deferred-packetcache-inserts [¶](https://doc.powerdns.com/authoritative/performance.html\#deferred-packetcache-inserts "Permalink to this headline")

Number of packet cache inserts that were deferred because of maintenance

#### deferred-packetcache-lookup [¶](https://doc.powerdns.com/authoritative/performance.html\#deferred-packetcache-lookup "Permalink to this headline")

Number of packet cache lookups that were deferred because of maintenance

#### dnsupdate-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#dnsupdate-answers "Permalink to this headline")

Number of DNS update packets successfully answered

#### dnsupdate-changes [¶](https://doc.powerdns.com/authoritative/performance.html\#dnsupdate-changes "Permalink to this headline")

Total number of changes to records from DNS update

#### dnsupdate-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#dnsupdate-queries "Permalink to this headline")

Number of DNS update packets received

#### dnsupdate-refused [¶](https://doc.powerdns.com/authoritative/performance.html\#dnsupdate-refused "Permalink to this headline")

Number of DNS update packets that were refused

#### incoming-notifications [¶](https://doc.powerdns.com/authoritative/performance.html\#incoming-notifications "Permalink to this headline")

Number of NOTIFY packets that were received

#### key-cache-size [¶](https://doc.powerdns.com/authoritative/performance.html\#key-cache-size "Permalink to this headline")

Number of entries in the key cache

#### latency [¶](https://doc.powerdns.com/authoritative/performance.html\#latency "Permalink to this headline")

Average number of microseconds a packet spends within PowerDNS

#### meta-cache-size [¶](https://doc.powerdns.com/authoritative/performance.html\#meta-cache-size "Permalink to this headline")

Number of entries in the metadata cache

#### open-tcp-connections [¶](https://doc.powerdns.com/authoritative/performance.html\#open-tcp-connections "Permalink to this headline")

Number of currently open TCP connections

#### overload-drops [¶](https://doc.powerdns.com/authoritative/performance.html\#overload-drops "Permalink to this headline")

Number of questions dropped because backends overloaded (backends are overloaded if they have more outstanding queries than the value of [overload-queue-length](https://doc.powerdns.com/authoritative/settings.html#setting-overload-queue-length))

#### packetcache-hit [¶](https://doc.powerdns.com/authoritative/performance.html\#packetcache-hit "Permalink to this headline")

Number of packets which were answered out of the cache

#### packetcache-miss [¶](https://doc.powerdns.com/authoritative/performance.html\#packetcache-miss "Permalink to this headline")

Number of times a packet could not be answered out of the cache

#### packetcache-size [¶](https://doc.powerdns.com/authoritative/performance.html\#packetcache-size "Permalink to this headline")

Amount of packets in the packetcache

#### qsize-q [¶](https://doc.powerdns.com/authoritative/performance.html\#qsize-q "Permalink to this headline")

Number of packets waiting for database attention, only available if [distributor-threads](https://doc.powerdns.com/authoritative/settings.html#setting-distributor-threads) \> 1

#### query-cache-hit [¶](https://doc.powerdns.com/authoritative/performance.html\#query-cache-hit "Permalink to this headline")

Number of hits on the [Query Cache](https://doc.powerdns.com/authoritative/performance.html#query-cache)

#### query-cache-miss [¶](https://doc.powerdns.com/authoritative/performance.html\#query-cache-miss "Permalink to this headline")

Number of misses on the [Query Cache](https://doc.powerdns.com/authoritative/performance.html#query-cache)

#### query-cache-size [¶](https://doc.powerdns.com/authoritative/performance.html\#query-cache-size "Permalink to this headline")

Number of entries in the query cache

#### rd-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#rd-queries "Permalink to this headline")

Number of packets sent by clients requesting recursion (regardless of if we’ll be providing them with recursion).

#### receive-latency [¶](https://doc.powerdns.com/authoritative/performance.html\#receive-latency "Permalink to this headline")

Average number of microseconds needed to receive a query

#### recursing-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#recursing-answers "Permalink to this headline")

Number of packets we supplied an answer to after recursive processing

#### recursing-questions [¶](https://doc.powerdns.com/authoritative/performance.html\#recursing-questions "Permalink to this headline")

Number of packets we performed recursive processing for.

#### recursion-unanswered [¶](https://doc.powerdns.com/authoritative/performance.html\#recursion-unanswered "Permalink to this headline")

Number of packets we sent to our recursor, but did not get a timely answer for.

#### security-status [¶](https://doc.powerdns.com/authoritative/performance.html\#security-status "Permalink to this headline")

Security status based on [Security Polling](https://doc.powerdns.com/authoritative/security.html#securitypolling).

#### send-latency [¶](https://doc.powerdns.com/authoritative/performance.html\#send-latency "Permalink to this headline")

Average number of microseconds needed to send the answer

#### servfail-packets [¶](https://doc.powerdns.com/authoritative/performance.html\#servfail-packets "Permalink to this headline")

Amount of packets that could not be answered due to database problems

#### signature-cache-size [¶](https://doc.powerdns.com/authoritative/performance.html\#signature-cache-size "Permalink to this headline")

Number of entries in the signature cache

#### signatures [¶](https://doc.powerdns.com/authoritative/performance.html\#signatures "Permalink to this headline")

Number of DNSSEC signatures created

#### sys-msec [¶](https://doc.powerdns.com/authoritative/performance.html\#sys-msec "Permalink to this headline")

Number of CPU milliseconds sent in system time

#### tcp-answers-bytes [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp-answers-bytes "Permalink to this headline")

Total number of answer bytes sent over TCP

#### tcp-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp-answers "Permalink to this headline")

Number of answers sent out over TCP

#### tcp-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp-queries "Permalink to this headline")

Number of questions received over TCP

#### tcp4-answers-bytes [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp4-answers-bytes "Permalink to this headline")

Total number of answer bytes sent over TCPv4

#### tcp4-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp4-answers "Permalink to this headline")

Number of answers sent out over TCPv4

#### tcp4-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp4-queries "Permalink to this headline")

Number of questions received over TCPv4

#### tcp6-answers-bytes [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp6-answers-bytes "Permalink to this headline")

Total number of answer bytes sent over TCPv6

#### tcp6-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp6-answers "Permalink to this headline")

Number of answers sent out over TCPv6

#### tcp6-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#tcp6-queries "Permalink to this headline")

Number of questions received over TCPv6

#### timedout-packets [¶](https://doc.powerdns.com/authoritative/performance.html\#timedout-packets "Permalink to this headline")

Amount of packets that were dropped because they had to wait too long internally

#### udp-answers-bytes [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-answers-bytes "Permalink to this headline")

Total number of answer bytes sent over UDP

#### udp-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-answers "Permalink to this headline")

Number of answers sent out over UDP

#### udp-do-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-do-queries "Permalink to this headline")

Number of queries received with the DO (DNSSEC OK) bit set

#### udp-in-csum-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-in-csum-errors "Permalink to this headline")

Number of UDP packets received with an invalid checksum

#### udp-in-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-in-errors "Permalink to this headline")

Number of packets received faster than the OS could process them

#### udp-noport-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-noport-errors "Permalink to this headline")

Number of UDP packets where an ICMP response was received that the remote port was not listening

#### udp-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-queries "Permalink to this headline")

Number of questions received over UDP

#### udp-recvbuf-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-recvbuf-errors "Permalink to this headline")

Number of errors caused in the UDP receive buffer

#### udp-sndbuf-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp-sndbuf-errors "Permalink to this headline")

Number of errors caused in the UDP send buffer

#### udp4-answers-bytes [¶](https://doc.powerdns.com/authoritative/performance.html\#udp4-answers-bytes "Permalink to this headline")

Total number of answer bytes sent over UDPv4

#### udp4-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#udp4-answers "Permalink to this headline")

Number of answers sent out over UDPv4

#### udp4-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#udp4-queries "Permalink to this headline")

Number of questions received over UDPv4

#### udp6-answers-bytes [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-answers-bytes "Permalink to this headline")

Total number of answer bytes sent over UDPv6

#### udp6-answers [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-answers "Permalink to this headline")

Number of answers sent out over UDPv6

#### udp6-in-csum-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-in-csum-errors "Permalink to this headline")

Number of IPv6 UDP packets received with an invalid checksum

#### udp6-in-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-in-errors "Permalink to this headline")

Number of IPv6 UDP packets received faster than the OS could process them

#### udp6-noport-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-noport-errors "Permalink to this headline")

Number of IPv6 UDP packets where an ICMP response was received that the remote port was not listening

#### udp6-queries [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-queries "Permalink to this headline")

Number of questions received over UDPv6

#### udp6-recvbuf-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-recvbuf-errors "Permalink to this headline")

Number of errors caused in the IPv6 UDP receive buffer

#### udp6-sndbuf-errors [¶](https://doc.powerdns.com/authoritative/performance.html\#udp6-sndbuf-errors "Permalink to this headline")

Number of errors caused in the IPv6 UDP send buffer

#### uptime [¶](https://doc.powerdns.com/authoritative/performance.html\#uptime "Permalink to this headline")

Uptime in seconds of the daemon

#### user-msec [¶](https://doc.powerdns.com/authoritative/performance.html\#user-msec "Permalink to this headline")

Number of milliseconds spend in CPU ‘user’ time

### Ring buffers [¶](https://doc.powerdns.com/authoritative/performance.html\#ring-buffers "Permalink to this headline")

Besides counters, PowerDNS also maintains the ringbuffers. A ringbuffer
records events, each new event gets a place in the buffer until it is
full. When full, earlier entries get overwritten, hence the name ‘ring’.

By counting the entries in the buffer, statistics can be generated.
These statistics can currently only be viewed using the webserver and
are in fact not even collected without the webserver running.

The following ringbuffers are available:

- **logmessages**: All messages logged
- **noerror-queries**: Queries for existing records but for a type we
don’t have. Queries for, say, the AAAA record of a domain, when only
an A is available. Queries are listed in the following format:
name/type. So an AAAA query for pdns.powerdns.com looks like
pdns.powerdns.com/AAAA.
- **nxdomain-queries**: Queries for non-existing records within
existing domains. If PowerDNS knows it is authoritative over a
domain, and it sees a question for a record in that domain that does
not exist, it is able to send out an authoritative ‘no such domain’
message. Indicates that hosts are trying to connect to services
really not in your zone.
- **udp-queries**: All UDP queries seen.
- **remotes**: Remote server IP addresses. Number of hosts querying
PowerDNS. Be aware that UDP is anonymous - person A can send queries
that appear to be coming from person B.
- **remote-corrupts**: Remotes sending corrupt packets. Hosts sending
PowerDNS broken packets, possibly meant to disrupt service. Be aware
that UDP is anonymous - person A can send queries that appear to be
coming from person B.
- **remote-unauth**: Remotes querying domains for which we are not
authoritative. It may happen that there are misconfigured hosts on
the internet which are configured to think that a PowerDNS
installation is in fact a resolving nameserver. These hosts will not
get useful answers from PowerDNS. This buffer lists hosts sending
queries for domains which PowerDNS does not know about.
- **servfail-queries**: Queries that could not be answered due to
backend errors. For one reason or another, a backend may be unable to
extract answers for a certain domain from its storage. This may be
due to a corrupt database or to inconsistent data. When this happens,
PowerDNS sends out a ‘servfail’ packet indicating that it was unable
to answer the question. This buffer shows which queries have been
causing servfails.
- **unauth-queries**: Queries for domains that we are not authoritative
for. If a domain is delegated to a PowerDNS instance, but the backend
is not made aware of this fact, questions come in for which no answer
is available, nor is the authority. Use this ringbuffer to spot such
queries.

### Sending metrics to Graphite/Metronome over Carbon [¶](https://doc.powerdns.com/authoritative/performance.html\#sending-metrics-to-graphite-metronome-over-carbon "Permalink to this headline")

For carbon/graphite/metronome, we use the following namespace.
Everything starts with ‘pdns.’, which is then followed by the local hostname.
Thirdly, we add ‘auth’ to signify the daemon generating the metrics.
This is then rounded off with the actual name of the metric. As an example: ‘pdns.ns1.auth.questions’.

Care has been taken to make the sending of statistics as unobtrusive as possible, the daemons will not be hindered by an unreachable carbon server, timeouts or connection refused situations.

To benefit from our carbon/graphite support, either install Graphite, or use our own lightweight statistics daemon, Metronome, currently available on [GitHub](https://github.com/ahupowerdns/metronome/).

To enable sending metrics, set [carbon-server](https://doc.powerdns.com/authoritative/settings.html#setting-carbon-server), possibly [carbon-interval](https://doc.powerdns.com/authoritative/settings.html#setting-carbon-interval) and possibly [carbon-ourname](https://doc.powerdns.com/authoritative/settings.html#setting-carbon-ourname) in the configuration.

Warning

If your hostname includes dots, they will be replaced by underscores so as not to confuse the namespace.

If you include dots in [carbon-ourname](https://doc.powerdns.com/authoritative/settings.html#setting-carbon-ourname), they will **not** be replaced by underscores.
As PowerDNS assumes you know what you are doing if you override your hostname.

[Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html "previous chapter (use the left arrow)")

[DNSSEC](https://doc.powerdns.com/authoritative/dnssec/index.html "next chapter (use the right arrow)")

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/dnssec/index.html "DNSSEC") \|
- [previous](https://doc.powerdns.com/authoritative/security.html "Security of PowerDNS") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

---

### 7. PowerDNS Authoritative Nameserver — PowerDNS Authoritative Server  documentation

**Source:** [https://doc.powerdns.com/authoritative/index.html](https://doc.powerdns.com/authoritative/index.html)
**Domain:** `doc.powerdns.com`
**Quality Score:** 3

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/installation.html "Installing PowerDNS") \|
- [previous](https://doc.powerdns.com/authoritative/indexTOC.html "PowerDNS Authoritative Server") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

[PowerDNS Authoritative Server](https://doc.powerdns.com/authoritative/indexTOC.html)

#### Previous topic

[PowerDNS Authoritative Server](https://doc.powerdns.com/authoritative/indexTOC.html "previous chapter")

#### Next topic

[Installing PowerDNS](https://doc.powerdns.com/authoritative/installation.html "next chapter")

## Contents

- [PowerDNS Authoritative Nameserver](https://doc.powerdns.com/authoritative/index.html#)
  - [Getting Started](https://doc.powerdns.com/authoritative/index.html#getting-started)
  - [Getting Support](https://doc.powerdns.com/authoritative/index.html#getting-support)
    - [My information is confidential, must I send it to the mailing list, discuss it on IRC, or post it in a GitHub ticket?](https://doc.powerdns.com/authoritative/index.html#my-information-is-confidential-must-i-send-it-to-the-mailing-list-discuss-it-on-irc-or-post-it-in-a-github-ticket)
    - [I have a question!](https://doc.powerdns.com/authoritative/index.html#i-have-a-question)
    - [What details should I supply?](https://doc.powerdns.com/authoritative/index.html#what-details-should-i-supply)
    - [I found a bug!](https://doc.powerdns.com/authoritative/index.html#i-found-a-bug)
    - [I found a security issue!](https://doc.powerdns.com/authoritative/index.html#i-found-a-security-issue)
    - [I have a good idea for a feature!](https://doc.powerdns.com/authoritative/index.html#i-have-a-good-idea-for-a-feature)
- [Installing PowerDNS](https://doc.powerdns.com/authoritative/installation.html)
- [Upgrade Notes](https://doc.powerdns.com/authoritative/upgrading.html)
- [DNS Modes of Operation](https://doc.powerdns.com/authoritative/modes-of-operation.html)
- [Migrating to PowerDNS](https://doc.powerdns.com/authoritative/migration.html)
- [Running and Operating](https://doc.powerdns.com/authoritative/running.html)
- [Security of PowerDNS](https://doc.powerdns.com/authoritative/security.html)
- [Performance and Tuning](https://doc.powerdns.com/authoritative/performance.html)
- [DNSSEC](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [Per zone settings: Domain Metadata](https://doc.powerdns.com/authoritative/domainmetadata.html)
- [Dynamic DNS Update (RFC 2136)](https://doc.powerdns.com/authoritative/dnsupdate.html)
- [Catalog Zones (RFC 9432)](https://doc.powerdns.com/authoritative/catalog.html)
- [TSIG](https://doc.powerdns.com/authoritative/tsig.html)
- [Views](https://doc.powerdns.com/authoritative/views.html)
- [Lua Records](https://doc.powerdns.com/authoritative/lua-records/index.html)
- [Guides and How Tos](https://doc.powerdns.com/authoritative/guides/index.html)
- [Backends](https://doc.powerdns.com/authoritative/backends/index.html)
- [Built-in Webserver and HTTP API](https://doc.powerdns.com/authoritative/http-api/index.html)
- [Manual Pages](https://doc.powerdns.com/authoritative/manpages/index.html)
- [Authoritative Server Settings](https://doc.powerdns.com/authoritative/settings.html)
- [Security Advisories](https://doc.powerdns.com/authoritative/security-advisories/index.html)
- [Changelogs](https://doc.powerdns.com/authoritative/changelog/index.html)
- [End of life statements](https://doc.powerdns.com/authoritative/appendices/EOL.html)
- [Frequently Asked Questions](https://doc.powerdns.com/authoritative/appendices/FAQ.html)
- [Backend writers’ guide](https://doc.powerdns.com/authoritative/appendices/backend-writers-guide.html)
- [Compiling PowerDNS](https://doc.powerdns.com/authoritative/appendices/compiling.html)
- [Cryptographic software and export control](https://doc.powerdns.com/authoritative/appendices/crypto-export.html)
- [Internals](https://doc.powerdns.com/authoritative/appendices/internals.html)
- [Supported Record Types](https://doc.powerdns.com/authoritative/appendices/types.html)
- [PowerDNS/dnsdist license](https://doc.powerdns.com/authoritative/common/license.html)

### This Page

- [Show Source](https://doc.powerdns.com/authoritative/_sources/index.rst.txt)

1. [Docs](https://doc.powerdns.com/authoritative/indexTOC.html)
2. PowerDNS Authoritative Nameserver

# PowerDNS Authoritative Nameserver [¶](https://doc.powerdns.com/authoritative/index.html\#powerdns-authoritative-nameserver "Permalink to this headline")

The PowerDNS Authoritative Server is a versatile nameserver which
supports a large number of backends. These backends can either be plain
zone files or be more dynamic in nature.

PowerDNS has the concepts of ‘backends’. A backend is a datastore that
the server will consult that contains DNS records (and some metadata).
The backends range from database backends ( [MySQL](https://doc.powerdns.com/authoritative/backends/generic-mysql.html), [PostgreSQL](https://doc.powerdns.com/authoritative/backends/generic-postgresql.html))
and [BIND zone files](https://doc.powerdns.com/authoritative/backends/bind.html) to [co-processes](https://doc.powerdns.com/authoritative/backends/pipe.html) and [JSON API’s](https://doc.powerdns.com/authoritative/backends/remote.html).

Multiple backends can be enabled in the configuration by using the
[launch](https://doc.powerdns.com/authoritative/settings.html#setting-launch) option. Each backend can be configured separately.

See the [backend](https://doc.powerdns.com/authoritative/backends/index.html) documentation for more information.

This documentation is also available as a [PDF document](https://doc.powerdns.com/authoritative/PowerDNS-Authoritative.pdf).

## Getting Started [¶](https://doc.powerdns.com/authoritative/index.html\#getting-started "Permalink to this headline")

- [Install the Authoritative Server](https://doc.powerdns.com/authoritative/installation.html)
- [Configure the Server](https://doc.powerdns.com/authoritative/settings.html)
- [Configure the backend(s)](https://doc.powerdns.com/authoritative/backends/index.html)

## Getting Support [¶](https://doc.powerdns.com/authoritative/index.html\#getting-support "Permalink to this headline")

PowerDNS is an open source program so you may get help from the PowerDNS users’ community or from its authors.
You may also help others (please do).

Public support is available via several different channels:

- This documentation
- [The mailing list](https://www.powerdns.com/mailing-lists.html)
- `#powerdns` on [irc.oftc.net](irc://irc.oftc.net/#powerdns)

The Open-Xchange/PowerDNS company can provide help or support you in private as well.
Please [contact PowerDNS](https://www.powerdns.com/contact-us).

### My information is confidential, must I send it to the mailing list, discuss it on IRC, or post it in a GitHub ticket? [¶](https://doc.powerdns.com/authoritative/index.html\#my-information-is-confidential-must-i-send-it-to-the-mailing-list-discuss-it-on-irc-or-post-it-in-a-github-ticket "Permalink to this headline")

Yes, we have a support policy called [“Open Source Support: out in the open”](https://blog.powerdns.com/2016/01/18/open-source-support-out-in-the-open/).

If you desire privacy, please consider entering a support relationship with us, in which case we invite you to [contact PowerDNS](https://www.powerdns.com/contact-us).

### I have a question! [¶](https://doc.powerdns.com/authoritative/index.html\#i-have-a-question "Permalink to this headline")

This happens, we’re here to help!
Read below on how you can get help

### What details should I supply? [¶](https://doc.powerdns.com/authoritative/index.html\#what-details-should-i-supply "Permalink to this headline")

Start out with stating what you think should be happening.
Quite often, wrong expectations are the actual problem.
Furthermore, your operating system, which version of PowerDNS you use and where you got it from (RPM, .DEB, tar.bz2).
If you compiled it yourself, what were the `./configure` parameters.

If possible, supply the actual name of your domain and the IP address of your server(s).

### I found a bug! [¶](https://doc.powerdns.com/authoritative/index.html\#i-found-a-bug "Permalink to this headline")

As much as we’d like to think we are perfect, bugs happen.
If you have found a bug, please file a bug report on [GitHub](https://github.com/PowerDNS/pdns/issues/new?template=bug_report.md).
Please fill in the template and we’ll try our best to help you.

### I found a security issue! [¶](https://doc.powerdns.com/authoritative/index.html\#i-found-a-security-issue "Permalink to this headline")

Please report this in private, see the [PowerDNS Security Policy](https://doc.powerdns.com/authoritative/security.html#securitypolicy).

### I have a good idea for a feature! [¶](https://doc.powerdns.com/authoritative/index.html\#i-have-a-good-idea-for-a-feature "Permalink to this headline")

We like to work on new things!
You can file a feature request on [GitHub](https://github.com/PowerDNS/pdns/issues/new?template=feature_request.md).

[PowerDNS Authoritative Server](https://doc.powerdns.com/authoritative/indexTOC.html "previous chapter (use the left arrow)")

[Installing PowerDNS](https://doc.powerdns.com/authoritative/installation.html "next chapter (use the right arrow)")

### Navigation

- [index](https://doc.powerdns.com/authoritative/genindex.html "General Index")
- [routing table](https://doc.powerdns.com/authoritative/http-routingtable.html "HTTP Routing Table") \|
- [next](https://doc.powerdns.com/authoritative/installation.html "Installing PowerDNS") \|
- [previous](https://doc.powerdns.com/authoritative/indexTOC.html "PowerDNS Authoritative Server") \|
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/indexTOC.html) »

---

### 8. Local DNS configuration and best practices - Super User

**Source:** [https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices)
**Domain:** `superuser.com`
**Quality Score:** 3

*I have recently set up a PowerDNS + PowerAdmin server on my home network. I have set this up as a combination authoritative + recursive DNS server just to keep things simple for me. I have set 8.8....*

**Stack Internal**

Knowledge at work

Bring the best of human thought and AI automation together at your work.

[Explore Stack Internal](https://stackoverflow.co/internal/?utm_medium=referral&utm_source=superuser-community&utm_campaign=side-bar&utm_content=explore-teams-compact-popover)

# [Local DNS configuration and best practices](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices)

[Ask Question](https://superuser.com/questions/ask)

Asked9 years, 3 months ago

Modified [3 years, 6 months ago](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices?lastactivity "2022-05-12 02:18:44Z")

Viewed
4k times


This question shows research effort; it is useful and clear

0

Save this question.

[Timeline](https://superuser.com/posts/1113260/timeline)

Show activity on this post.

I have recently set up a PowerDNS + PowerAdmin server on my home network. I have set this up as a combination authoritative + recursive DNS server just to keep things simple for me. I have set 8.8.8.8 as the recursor.

I have confirmed that I can do: "dig google.com @(ip of dns server)" and it works great.

My goal basically is to be able to use DNS on my home network for the various vms that I'm running. Let's use wiki servers for this example.

I was originally going to be doing something like: wiki01.catpants.lan for the names, but I was told this is a bad idea. (using a fake tld) So now I'll just buy a domain and do things like wiki.catpants.com (or whatever I decide to use).

So I have a few questions.

1. Is it considered ok to use 8.8.8.8 for the recursor? I know google's DNS servers are commonly used, but I was wondering if maybe there is a more appropriate choice.

2. I want to be able to tell at a glance if a server is "internal only" or is available externally also. I was considering using another subdomain, so it would be something like wiki01.lan.catpants.com for an "internal only" wiki, and wiki02.catpants.com for an externally available wiki. It would work, but I think is a bit ugly and requires extra typing. Or, should I buy and use a domain name just for internal use? Seems like a bit of a waste to me, since I have external services I want to run anyway. See, using .lan definitely has some advantages in my mind. The advantages being free and easy to tell if a server is internal only or available externally.

3. (Main question) I've been trying to test creating a few internal dns records with a domain I already own. Call it foo.com. I am using he.net for the nameservers for foo.com currently. When I try to create a master zone for foo.com with poweradmin, it creates an SOA record for it, but the defaults are: `8.8.8.8  2016081300 28800 7200 604800 86400`
IIRC, When configuring poweradmin for the first time, it asked me a question about some sort of defaults (possibly SOA related). Not knowing what goes there, I just put 8.8.8.8 thinking it was asking about the recursor. Of course it looks like there is no way to edit that setting now, so not sure what it was. **What should the SOA record look like?**

4. Should I be using DNSSEC? I can research it on my own if it's considered "best practice".

5. Is it possible to get "leakage"? ie, I think from a security perspective it would be nice if packets with my internal DNS records never get routed on the internet. If someone was capturing all outbound traffic from my network, the string "wiki01.lan.catpants.com" should _never_ appear in that traffic. Could that occur with this setup?


Thanks!!

- [dns](https://superuser.com/questions/tagged/dns "show questions tagged 'dns'")

[Share](https://superuser.com/q/1113260 "Short permalink to this question")

Share a link to this question

Copy link [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/ "The current license for this post: CC BY-SA 3.0")

[Improve this question](https://superuser.com/posts/1113260/edit "")

Follow



Follow this question to receive notifications

[edited Aug 18, 2016 at 21:36](https://superuser.com/posts/1113260/revisions "show all edits to this post")

asked Aug 13, 2016 at 20:20

[![cat pants's user avatar](https://www.gravatar.com/avatar/44c6e0cb82df26797533f6efc84143b5?s=64&d=identicon&r=PG)](https://superuser.com/users/123960/cat-pants)

[cat pants](https://superuser.com/users/123960/cat-pants)

29955 gold badges1616 silver badges3131 bronze badges

[Add a comment](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") \| [Expand to show all comments on this post](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices# "Expand to show all comments on this post")

## 1 Answer 1

Sorted by:
[Reset to default](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices?answertab=scoredesc#tab-top)

Highest score (default)

Date modified (newest first)

Date created (oldest first)


This answer is useful

2

Save this answer.

[Timeline](https://superuser.com/posts/1113312/timeline)

Show activity on this post.

Please configure separate DNS services for internal and external clients. This can be done with split DNS or different servers. I use both options.

1. If you are doing recursive queries you should start with the root servers. They should be populated from the hints file. Don't provide this service to hosts connecting from the internet. If you do you will find your network bandwidth is used to create amplification attacks.
2. There are several mechanisms for separating external and internal entries. Using a subdomain is one. Configure these addresses so that they don't leak to the internet. Buying a separate domain for internal use is overkill.
3. Your internal address should not be listed on the he.net domain servers. The addresses should not be valid on the internet and should not be served by an internet-facing DNS server. Create your own internal zone for these addresses.
4. At some point you should use DNSSEC. Leave this until later.
5. Use a private IP address from the range 10.0.0./8, 172.16.0.0/12 and 192.168.0.0/16, and traffic won't be routed to the internet. In any case, if your DNS server and clients are on the same LAN, traffic won't be routed between servers over the internet.

[Share](https://superuser.com/a/1113312 "Short permalink to this answer")

Share a link to this answer

Copy link [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Improve this answer](https://superuser.com/posts/1113312/edit "")

Follow



Follow this answer to receive notifications

[edited May 12, 2022 at 2:18](https://superuser.com/posts/1113312/revisions "show all edits to this post")

answered Aug 14, 2016 at 1:33

[![BillThor's user avatar](https://www.gravatar.com/avatar/42aa353db48aba46e0d2947220e8d8a1?s=64&d=identicon&r=PG)](https://superuser.com/users/37947/billthor)

[BillThor](https://superuser.com/users/37947/billthor)

11.4k22 gold badges2828 silver badges2525 bronze badges

[Add a comment](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") \| [Expand to show all comments on this post](https://superuser.com/questions/1113260/local-dns-configuration-and-best-practices# "Expand to show all comments on this post")

## You must [log in](https://superuser.com/users/login?ssrc=question_page&returnurl=https%3a%2f%2fsuperuser.com%2fquestions%2f1113260) to answer this question.

Start asking to get answers

Find the answer to your question by asking.

[Ask question](https://superuser.com/questions/ask)

Explore related questions

- [dns](https://superuser.com/questions/tagged/dns "show questions tagged 'dns'")

See similar questions with these tags.

---
