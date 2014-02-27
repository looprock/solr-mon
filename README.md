solr-mon
========

A solr monitoring utility geared for solr 4 which doesn't require enabling jsp support.

# Features

Check any data point from the following routes:<br>
http://host:port/solr/admin/cores?action=STATUS&wt=json&memory=true<br>
http://host:port/solr/admin/ping?wt=json<br>
http://host:port/solr/admin/plugins?stats=true&wt=json

Run generic tests across all cores.

Support for many operators:<br>
gt - greater than, int operaion<br>
lt - less than, int operation<br>
eq - equal, int operation<br>
ne - not equal, int operation<br>
le - less than or equal to, int operation<br>
ge - greater than or equal to, int operation<br>
is - matches, string operation<br>
not - doesn't match, string operation

Test length of time between date and now.

# Usage

> Usage: solr-mon.py [options]<br>
> <br>
> Options:<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--version             show program's version number and exit<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-h, --help            show this help message and exit<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-a, --allcores        Execute check against all cores [only valid for type<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        'status, path relative to status/<core>']<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-d, --debug           Enable debug mode<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-D, --datecompare     Do a date comparison, seconds from current time<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-H SOLR_SERVER, --host=SOLR_SERVER<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        SOLR Server IPADDRESS<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-p SOLR_SERVER_PORT, --port=SOLR_SERVER_PORT<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        SOLR Server port<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-t STATUS_TYPE, --type=STATUS_TYPE<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        Which admin interface to hit: status, ping, stats<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-e EVAL_TYPE, --eval=EVAL_TYPE<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        Type of evaluation: gt, lt, eq, ne, le, ge, is, not<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-P PATH, --path=PATH  Path inside the json object you want to check, /<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        delimited, RE: responseHeader/status<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-w Warning, --warning=Warning<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                        Exit with WARNING status if criteria met<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-c Critical, --critical=Critical<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                      Exit with ERROR status if criteria met<br>

# Examples

> $ ./solr-mon.py -H localhost -p 8990 -w 86400 -e gt -P index/lastModified -t status -a -D <br>
> OK<br>
> $ echo $?<br>
> 0<p>

> $ ./solr-mon.py -H localhost -p 8990 -w 22 -e gt -P index/lastModified -t status -a -D <br>
> WARNING: status/for_rent/index/lastModified greater than 22<br>
> $ echo $?<br>
> 1<p>

> $ ./solr-mon.py -H localhost -p 9000 -w 22 -e gt -P status/bah/index/lastModified -t status -D <br>
> WARNING: status/bah/index/lastModified greater than 22<br>
> $ echo $?<br>
> 1<p>

> $ ./solr-mon.py -H localhost -p 8990 -c 0 -e ne -P responseHeader/status -t ping <br>
> OK<br>
> $ echo $?<br>
> 0<p>

> $ ./solr-mon.py -H localhost -p 9000 -c 0 -e eq -P index/numDocs -t status -a <br>
> OK<br>
> $ echo $?<br>
> 0<p>
