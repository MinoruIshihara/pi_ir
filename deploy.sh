cp ir-camera-client /usr/sbin/
cp post_ir_image.py /usr/sbin/
cp ir-camera-client.service /usr/lib/systemd/system/

systemctl daemon-reload
systemctl start ir-camera-client.service