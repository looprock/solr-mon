solr-mon
========

A solr monitoring utility geared for solr 4 which doesn't require enabling jsp support

# Usage

> Usage: solr-mon.py [options]
> 
> Options:
>   --version             show program's version number and exit
>   -h, --help            show this help message and exit
>   -a, --allcores        Execute check against all cores [only valid for type
>                         'status, path relative to status/<core>']
>   -d, --debug           Enable debug mode
>   -D, --datecompare     Do a date comparison, seconds from current time
>   -H SOLR_SERVER, --host=SOLR_SERVER
>                         SOLR Server IPADDRESS
>   -p SOLR_SERVER_PORT, --port=SOLR_SERVER_PORT
>                         SOLR Server port
>   -t STATUS_TYPE, --type=STATUS_TYPE
>                         Which admin interface to hit: status, ping, stats
>   -e EVAL_TYPE, --eval=EVAL_TYPE
>                         Type of evaluation: gt, lt, eq, ne, le, ge, is, not
>   -P PATH, --path=PATH  Path inside the json object you want to check, /
>                         delimited, RE: responseHeader/status
>   -w Warning, --warning=Warning
>                         Exit with WARNING status if criteria met
>   -c Critical, --critical=Critical
                        Exit with ERROR status if criteria met

# Examples

> $ ./solr-mon.py -H etl15.vast.com -p 8990 -w 86400 -e gt -P index/lastModified -t status -a -D 
> OK
> $ echo $?
> 0

> $ ./solr-mon.py -H etl15.vast.com -p 8990 -w 22 -e gt -P index/lastModified -t status -a -D 
> WARNING: status/for_rent/index/lastModified greater than 22
> $ echo $?
> 1

> $ ./solr-mon.py -H etl15.vast.com -p 9000 -w 22 -e gt -P status/bah/index/lastModified -t status -D 
> WARNING: status/bah/index/lastModified greater than 22
> $ echo $?
> 1

> $ ./solr-mon.py -H etl15.vast.com -p 8990 -c 0 -e ne -P responseHeader/status -t ping 
> OK
> $ echo $?
> 0

> $ ./solr-mon.py -H etl15.vast.com -p 9000 -c 0 -e eq -P index/numDocs -t status -a 
> OK
> $ echo $?
> 0
