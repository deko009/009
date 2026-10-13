# 06-open launch · Oct 13, 8:00 AM ET · two segments

Copy is the client's (06-open-public.html / 06-open-waitlist.html). Design follows the cream Figma frames
"LAUNCH · 06-open · PUBLIC / WAITLIST · Oct 13 8AM ET" on the EDM page.

| File | Segment | Subject (from client `<title>`) |
|---|---|---|
| 06-open-waitlist.html | waitlist segment only | Ronini is open. Your 15% code is inside. |
| 06-open-public.html | all subscribers, **excluding the waitlist segment** | Ronini is open. |

Before scheduling in Klaviyo:
1. Upload `assets/bottle-5oz.png`, `assets/bottle-8oz.png` and `assets/burst-10.png` to the Klaviyo image library, then replace the matching `assets/...` URLs in each file (each appears once).
   All other images already point at the client's Klaviyo CDN.
2. Make sure a coupon named exactly `EARLY15` exists with codes available (used by `{% coupon_code 'EARLY15' %}`).
3. Schedule both for Oct 13, 8:00 AM America/New_York; send-in-local-time off. Consider turning Smart Sending off for the waitlist send.
4. Send a test of each and check the code + the discount link on the waitlist version.

`build.py` regenerates both files from one template.
