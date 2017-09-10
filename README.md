# vdr2m3u

A quick and dirty script to convert the output of w_scan to a SAT>IP style m3u file

The output of w_scan should be in Gstreamer format (VDR format, with the PMT PID added at the end). For example

```w_scan -fs -s S28E2 -O 0 -E 0 -G```


