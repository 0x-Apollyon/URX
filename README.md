# URX: Url Shortener
URX was made as a side project. This idea of the URL shortener and its features comes from the "Don't spoil the surprise" proposal submitted to CCExtractor in GSoC 2024.
[The proposal can be found here](https://ccextractor.org/public/gsoc/2022/urlshortener/)

### Tech Stack
URX uses the following tech stack
- Backend: Flask as the server runtime, SQLite as the database
- APIs: URX has support for multiple third party email vendor APIs aswell as SMTP support for email notification delivery
- Frontend: The frontend is vanilla HTML/CSS/JS. No fancy framework like React/Vue/Svelte has been used

### Features
- URLs can be made as a "walled garden" so only some specific people can open it. No complex auth system, just send a confirmation link to that email so they can open it from there.
- URLs can be made to expire after a certain time
- URLs can be made to send notification to the owner of the URL when it is opened

### Known drawbacks and fixes
Drawback: Not very scalable <br>
Fix: Use a key value database such as MongoDB or Redis to store the data

