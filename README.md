# DET Handler

### Description

This is a super simple Flask application to handle incoming data entry trigger (DET) requests from a REDCap server. This application is designed to be used in conjunction with the [BioradConfig](https://github.com/JovingeLabSoftware/BioradConfig) package to sync data between REDCap and LabGuru.


### Requirements

- A REDCap server configured to send you DETs and take API calls
- A LabGuru account with an API key
- Anything required in [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04) used to configure the server to serve the `Flask` app
- The [BioradConfig](https://github.com/JovingeLabSoftware/BioradConfig) package installed
- A running instance of [Rserve](https://rforge.net/Rserve/) launched with the script `rserve/launch-rserve.R`



