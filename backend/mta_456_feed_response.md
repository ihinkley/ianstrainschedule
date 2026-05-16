# MTA 4/5/6 Feed Response

Endpoint called:

```text
https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs
```

Called at: `2026-05-16T16:32:20Z`

HTTP status: `200`

Content type: `text/plain`

Response size: `154723 bytes`

Raw protobuf response saved to:

```text
backend/mta_456_feed_response.pb
```

Raw response headers saved to:

```text
backend/mta_456_feed_headers.txt
```

## Note

This endpoint returns **GTFS Realtime protobuf binary**, not JSON or plain text. The `.pb` file is the actual API response. We need a GTFS Realtime protobuf parser before extracting station arrivals.

## Response Preview

First 256 bytes as hex:

```text
0a 7b 0a 03 31 2e 30 18 90 b8 a2 d0 06 ca 3e 6d 0a 03 31 2e 30 12 0b 0a 01 31 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 32 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 33 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 34 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 35 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 36 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 37 12 06 10 90 b8 a2 d0 06 12 0b 0a 01 53 12 06 10 90 b8 a2 d0 06 12 cc 08 0a 06 30 30 30 30 30 31 1a c1 08 0a 35 0a 11 30 36 37 31 30 30 5f 31 2e 2e 4e 30 33 58 30 35 32 1a 08 32 30 32 36 30 35 31 36 2a 01 31 ca 3e 12 0a 10 30 31 20 31 31 31 31 20 20 53 46 54 2f 32 34 32 12 14 1a 06 10 84 92 a2 d0 06 22 04 31 34 32 4e ca 3e 03 0a 01 34 12 1c 12 06 10 9a 93 a2 d0 06 1a 06 10 9a 93 a2 d0 06 22 04 31 33 39 4e ca 3e 03 0a 01 34 12 1c 12 06 10 d6 93 a2 d0 06
```

First 256 bytes as base64:

```text
CnsKAzEuMBiQuKLQBso+bQoDMS4wEgsKATESBhCQuKLQBhILCgEyEgYQkLii0AYSCwoBMxIGEJC4otAGEgsKATQSBhCQuKLQBhILCgE1EgYQkLii0AYSCwoBNhIGEJC4otAGEgsKATcSBhCQuKLQBhILCgFTEgYQkLii0AYSzAgKBjAwMDAwMRrBCAo1ChEwNjcxMDBfMS4uTjAzWDA1MhoIMjAyNjA1MTYqATHKPhIKEDAxIDExMTEgIFNGVC8yNDISFBoGEISSotAGIgQxNDJOyj4DCgE0EhwSBhCak6LQBhoGEJqTotAGIgQxMzlOyj4DCgE0EhwSBhDWk6LQBg==
```

## Headers

```text
HTTP/2 200 
content-type: text/plain
content-length: 154723
date: Sat, 16 May 2026 16:32:19 GMT
x-amzn-trace-id: Root=1-6a089c13-5387e8784b3255531aee4e52
x-amzn-requestid: 75e85db1-dc03-4d7b-96ad-78882ccfc17a
access-control-allow-origin: *
x-amz-apigw-id: dd1TLHBmIAMEYNg=
x-cache: Miss from cloudfront
via: 1.1 52b969a4ab7956a248b07efba57c92a4.cloudfront.net (CloudFront)
x-amz-cf-pop: EWR53-P1
x-amz-cf-id: eiiURRIGESU594Cv6aryv9vUl5GN-y6ohMpbmxH55uavTQnxY-83pw==
```
