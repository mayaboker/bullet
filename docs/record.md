
```
gst-launch-1.0 \
v4l2src name=camera device=/dev/video0 \
! video/x-raw,format=YUY2,width=640,height=512,framerate=30/1 \
! videoconvert \
! video/x-raw,format=I420 \
! fakesink

```