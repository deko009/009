"""Builds the two 06-open launch emails (public + waitlist) from one template.

Copy comes verbatim from the client's 06-open-public.html / 06-open-waitlist.html.
Layout follows the cream Figma frame "LAUNCH · 06-open-to-everyone · REDESIGN".
Run: python3 build.py  ->  writes public.html and waitlist.html next to this file.
"""
from pathlib import Path

HERE = Path(__file__).parent

# Klaviyo-hosted assets (already in the client's Klaviyo library)
LOGO = "https://cdn.klaviyomail.com/company/RLiMzU/images/1d508d4e-fc3b-45a4-8ce6-d589726cc938.png"
PHOTO = "https://cdn.klaviyomail.com/company/RLiMzU/images/6bc3749b-e3ac-4578-ade8-b9e72916bf34.png"
BAND = "https://cdn.klaviyomail.com/company/RLiMzU/images/9ab928b8-7b72-4281-92cf-8c1b9cb19010.jpeg"
HELPER = "https://cdn.klaviyomail.com/company/RLiMzU/images/d986a5b7-bd54-4cba-965f-6c3d205ced5b.png"
INSTAGRAM = "https://cdn.klaviyomail.com/company/RLiMzU/images/50e6aefb-d99f-424f-8c97-2724fa1f0f90.png"
# New assets: upload assets/bottle-5oz.png, bottle-8oz.png, burst-10.png, venting-tube.png to Klaviyo and paste their URLs here
BOTTLE_5 = "assets/bottle-5oz.png"
BOTTLE_8 = "assets/bottle-8oz.png"
BURST_10 = "assets/burst-10.png"
TUBE = "assets/venting-tube.png"

PRODUCT_URL = "https://ronini.com/products/the-ronini-wrapped-glass-bottle"
DISCOUNT_URL = "https://ronini.com/discount/{% coupon_code 'EARLY15' %}?redirect=%2Fproducts%2Fthe-ronini-wrapped-glass-bottle"

NAVY, ORANGE, INK, PERI = "#230052", "#FC4C02", "#5B3F7D", "#758AFD"
CREAM, SAND, PAPER, SKY, DASH = "#F5F2EA", "#ECE6D8", "#FFFBF1", "#E6EDFF", "#C9BFA8"
H = "font-family:'Parkinsans',Arial,Helvetica,sans-serif;font-weight:600;mso-line-height-rule:exactly;"
B = "font-family:'Onest',Arial,Helvetica,sans-serif;mso-line-height-rule:exactly;"

VARIANTS = {
    "public": dict(
        title="Ronini is open.",
        preheader="The Wrapped Glass Bottle: glass inside, silicone molded on. From $60 a pair.",
        intro="Starting today, anyone can order the Wrapped Glass Bottle: glass where the milk goes, with soft silicone molded on outside. From $60&nbsp;a&nbsp;pair.",
        cta_label="Shop the Wrapped Glass Bottle &rarr;",
        cta_url=PRODUCT_URL,
        price_note="Regular one-time prices for a pair. Prefer plain glass? The Glass Bottle starts at $40 a pair, and The Duo, one pair of each, at&nbsp;$90.",
        coupon=False,
    ),
    "waitlist": dict(
        title="Ronini is open. Your 15% code is inside.",
        preheader="Good through Sunday, October 18, with a free Venting Tube 2-pack on your first order.",
        intro="Starting today, anyone can order the Wrapped Glass Bottle: glass where the milk goes, with soft silicone molded on outside. Thank you for being here before the doors&nbsp;opened.",
        cta_label="Shop with your 15% &rarr;",
        cta_url=DISCOUNT_URL,
        price_note="Regular one-time prices for a pair, before your 15%. Prefer plain glass? The Glass Bottle starts at $40 a pair, and The Duo, one pair of each, at&nbsp;$90.",
        coupon=True,
    ),
}


def button(label, url, bg, fg, full=False, border=None):
    disp = "block" if full else "inline-block"
    edge = f"border:2px solid {border};" if border else ""
    width = ' width="100%"' if full else ""
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"{width} style="border-collapse:separate;">'
            f'<tr><td align="center" bgcolor="{bg}" style="background:{bg};border-radius:999px;{edge}">'
            f'<a href="{url}" style="display:{disp};padding:16px 30px;{B}font-weight:600;font-size:16px;line-height:20px;color:{fg};text-decoration:none;border-radius:999px;">{label}</a>'
            f'</td></tr></table>')


def coupon_card():
    # Light ticket-style card, centered: arch + pill offer mark (brand shapes), title, offer, dashed code slot, terms.
    return f'''
  <!-- ============ WAITLIST THANK-YOU (waitlist only) ============ -->
  <tr>
    <td class="px" style="padding:32px 40px 0 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{SKY}" style="background:{SKY};border:2px solid {NAVY};border-radius:24px;border-collapse:separate;">
        <tr>
          <td class="card" align="center" style="padding:28px 28px 26px 28px;text-align:center;">
            <table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;border-collapse:separate;"><tr>
              <td align="center" valign="middle" width="88" height="100" bgcolor="{ORANGE}" style="width:88px;height:100px;background:{ORANGE};border-radius:44px 44px 8px 8px;text-align:center;">
                <p style="padding-top:14px;{H}font-size:28px;line-height:30px;letter-spacing:-0.6px;color:{PAPER};text-align:center;">15%</p>
                <p style="{B}font-weight:600;font-size:13px;line-height:16px;color:{PAPER};text-align:center;">off</p>
              </td>
              <td width="8" style="width:8px;font-size:0;line-height:0;">&nbsp;</td>
              <td align="center" valign="top" width="28" height="100" bgcolor="{PERI}" style="width:28px;height:100px;background:{PERI};border-radius:6px 6px 14px 14px;">
                <table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:16px auto 0 auto;border-collapse:separate;"><tr>
                  <td width="12" height="12" bgcolor="{NAVY}" style="width:12px;height:12px;background:{NAVY};border-radius:999px;font-size:0;line-height:0;">&nbsp;</td>
                </tr></table>
              </td>
              <td width="10" style="width:10px;font-size:0;line-height:0;">&nbsp;</td>
              <td valign="middle" style="{H}font-size:26px;line-height:26px;color:{NAVY};">+</td>
              <td width="8" style="width:8px;font-size:0;line-height:0;">&nbsp;</td>
              <td valign="middle" width="56"><img src="{TUBE}" width="56" height="103" alt="Free Venting Tube" style="width:56px;height:103px;"/></td>
            </tr></table>
            <p style="padding-top:14px;{B}font-weight:600;font-size:12px;line-height:16px;letter-spacing:1.5px;text-transform:uppercase;color:{PERI};text-align:center;">For the waitlist</p>
            <h3 style="padding-top:6px;{H}font-size:22px;line-height:28px;color:{NAVY};text-align:center;">Your waitlist thank-you</h3>
            <p style="padding-top:12px;{B}font-size:15px;line-height:23px;color:{INK};text-align:center;">15% off your first order, plus a free Venting&nbsp;Tube&nbsp;2-pack.</p>
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{PAPER}" style="margin-top:18px;background:{PAPER};border:1.5px dashed #F6A482;border-radius:14px;border-collapse:separate;">
              <tr>
                <td align="center" class="codef" style="padding:16px 18px;{B}font-weight:600;font-size:22px;line-height:30px;letter-spacing:1px;color:{NAVY};word-break:break-all;text-align:center;">{{% coupon_code 'EARLY15' %}}</td>
              </tr>
            </table>
            <p style="padding-top:16px;{B}font-size:12px;line-height:18px;color:{INK};text-align:center;">Use it once, through Sunday, October 18 at 11:59 pm ET. It stacks with the 10% subscription savings. The Venting Tube is sized for the 5 oz bottle; in the 8 oz, fill to 5&nbsp;oz or&nbsp;less.</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>'''


def arch_card(oz, ml, price, pad_side, bottle):
    # The arch frames the bottle: soft periwinkle sky at the top fading into paper,
    # bottle standing on its own shadow, size + price centered underneath.
    return f'''<td width="50%" valign="top" style="padding-{pad_side}:8px;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{PAPER}" style="background-color:{PAPER};background-image:linear-gradient(180deg,#E4E9FF 0%,{PAPER} 62%,{PAPER} 100%);border:1.5px solid {NAVY};border-radius:118px 118px 18px 18px;border-collapse:separate;">
                    <tr>
                      <td align="center" style="padding:26px 12px 24px 12px;text-align:center;">
                        <img src="{bottle}" width="120" height="174" alt="{oz} Wrapped Glass Bottle" style="width:120px;height:174px;margin:0 auto;"/>
                        <p style="padding-top:8px;{H}font-size:20px;line-height:24px;color:{NAVY};text-align:center;">{oz}</p>
                        <p style="margin-top:2px;{B}font-size:14px;line-height:18px;color:{INK};text-align:center;">{ml}</p>
                        <p class="price" style="margin-top:10px;{H}font-size:42px;line-height:44px;letter-spacing:-1.2px;color:{ORANGE};text-align:center;">{price}</p>
                        <p style="margin-top:2px;{B}font-weight:600;font-size:13px;line-height:18px;color:{NAVY};white-space:nowrap;text-align:center;">per pair</p>
                      </td>
                    </tr>
                  </table>
                </td>'''


def build(v):
    hero_cta_extra = "" if v["coupon"] else ""
    coupon = coupon_card() if v["coupon"] else ""
    return f'''<!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<meta content="IE=edge" http-equiv="X-UA-Compatible"/>
<meta name="x-apple-disable-message-reformatting"/>
<meta content="light only" name="color-scheme"/>
<meta content="light" name="supported-color-schemes"/>
<title>{v["title"]}</title>
<!-- 06-open · Oct 13 launch · cream design (Figma: LAUNCH · 06-open-to-everyone · REDESIGN). Copy from client file. -->
<style>:root {{color-scheme:light only;supported-color-schemes:light}}</style>
<style>
@font-face {{font-family:"Onest";font-style:normal;font-weight:400;src:url(https://fonts.gstatic.com/s/onest/v11/gNMZW3F-SZuj7zOT0IfSjTS16cPh9R-Zsg.ttf) format("truetype")}}
@font-face {{font-family:"Onest";font-style:normal;font-weight:600;src:url(https://fonts.gstatic.com/s/onest/v11/gNMZW3F-SZuj7zOT0IfSjTS16cPhKxiZsg.ttf) format("truetype")}}
@font-face {{font-family:"Parkinsans";font-style:normal;font-weight:600;src:url(https://fonts.gstatic.com/s/parkinsans/v3/-W_uXJXvQyPb1QfpBpRrVEgjj0W4zSUk4gQI7h8K.ttf) format("truetype")}}
body {{margin:0;padding:0;background:#E9E2D2;-webkit-text-size-adjust:100%}}
table {{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0}}
td {{padding:0}}
img {{border:0;display:block;outline:none;text-decoration:none}}
p, h1, h2, h3 {{margin:0}}
a {{color:{NAVY}}}
@media only screen and (max-width:620px) {{
  .wrap {{width:100% !important}}
  .px {{padding-left:20px !important;padding-right:20px !important}}
  .px-panel {{padding-left:12px !important;padding-right:12px !important}}
  .stack {{display:block !important;width:100% !important;padding-left:0 !important;padding-right:0 !important}}
  .stack-gap {{padding-bottom:14px !important}}
  .hide-sm {{display:none !important}}
  .h1 {{font-size:40px !important;line-height:44px !important}}
  .h2 {{font-size:24px !important;line-height:30px !important}}
  .full {{width:100% !important;height:auto !important}}
  .panel {{padding:28px 18px !important}}
  .card {{padding:24px 20px !important}}
  .codef {{font-size:18px !important;line-height:26px !important}}
  .burst-cell {{width:76px !important;padding-left:8px !important}}
  .burst {{width:76px !important;height:76px !important}}
  .price {{font-size:34px !important;line-height:38px !important}}
}}
</style>
</head>
<body style="margin:0;padding:0;background:#E9E2D2;">
<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">{v["preheader"]} &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; &#65279;&#847; </div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#E9E2D2" style="background:#E9E2D2;"><tr><td align="center" style="padding:24px 0;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="{CREAM}" style="width:600px;background:{CREAM};">

  <!-- ============ HEADER ============ -->
  <tr>
    <td class="px" style="padding:28px 40px 0 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
        <td valign="middle"><a href="https://ronini.com/"><img src="{LOGO}" width="112" height="23" alt="Ronini" style="width:112px;height:23px;"/></a></td>
        <td valign="middle" align="right" style="{B}font-weight:600;font-size:12px;line-height:16px;letter-spacing:0.5px;color:{NAVY};">October 13</td>
      </tr></table>
    </td>
  </tr>

  <!-- ============ HERO ============ -->
  <tr>
    <td class="px" align="center" style="padding:40px 40px 0 40px;text-align:center;">
      <table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:8px auto 0 auto;border-collapse:separate;"><tr>
        <td bgcolor="{PAPER}" style="background:{PAPER};border:1px solid #B9C6F7;border-radius:999px;padding:8px 18px;{B}font-size:15px;line-height:20px;color:{NAVY};">Open to everyone</td>
      </tr></table>
      <h1 class="h1" style="padding-top:18px;{H}font-size:52px;line-height:54px;letter-spacing:-1.6px;color:{NAVY};text-align:center;">Ronini is <span style="color:{ORANGE};">open.</span></h1>
      <p style="padding-top:18px;{B}font-size:16px;line-height:25px;color:{INK};text-align:center;">{v["intro"]}</p>
      <table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:26px auto 0 auto;"><tr><td>{button(v["cta_label"], v["cta_url"], ORANGE, "#FFFFFF")}</td></tr></table>
    </td>
  </tr>
{coupon}
  <!-- ============ PRODUCT ============ -->
  <tr>
    <td class="px" style="padding:44px 40px 0 40px;">
      <a href="{PRODUCT_URL}"><img src="{PHOTO}" width="520" height="520" alt="The Wrapped Glass Bottle in 5 oz and 8 oz." class="full" style="width:520px;height:520px;border-radius:24px;"/></a>
      <p style="padding-top:28px;{B}font-weight:600;font-size:12px;line-height:16px;letter-spacing:1.5px;text-transform:uppercase;color:{ORANGE};">The Wrapped Glass Bottle</p>
      <h2 class="h2" style="padding-top:10px;{H}font-size:30px;line-height:36px;letter-spacing:-0.6px;color:{NAVY};">Glass inside. Silicone molded on.</h2>
      <p style="padding-top:14px;{B}font-size:16px;line-height:25px;color:{INK};">Every part the milk touches is glass or silicone. The silicone is molded directly onto the glass, so it stays on through washing and softens everyday knocks. Each bottle comes with its nipple, collar and cap.</p>
    </td>
  </tr>

  <!-- ============ PRICES (gradient panel + arch cards) ============ -->
  <tr>
    <td class="px-panel" style="padding:28px 24px 0 24px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#A9B6F4" style="background-color:#A9B6F4;background-image:linear-gradient(160deg,#D3DCF9 0%,#A9B6F4 50%,#8494F0 100%);border-radius:28px;border-collapse:separate;">
        <tr>
          <td class="panel" style="padding:32px 32px 32px 32px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
              {arch_card("5 oz", "160 ml", "$60", "right", BOTTLE_5)}
              {arch_card("8 oz", "240 ml", "$64", "left", BOTTLE_8)}
            </tr></table>
            <p style="padding-top:16px;{B}font-size:12px;line-height:18px;color:{NAVY};">{v["price_note"]}</p>
            <div style="padding-top:22px;">{button(v["cta_label"], v["cta_url"], NAVY, "#FFFFFF", full=True)}</div>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ============ SUBSCRIBE AND SAVE ============ -->
  <tr>
    <td class="px" style="padding:48px 40px 0 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{SKY}" style="background:{SKY};border-radius:24px;border-collapse:separate;">
        <tr>
          <td class="card" style="padding:28px 28px 28px 28px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
              <td valign="top">
                <p style="{B}font-weight:600;font-size:12px;line-height:16px;letter-spacing:1.5px;text-transform:uppercase;color:{PERI};">Subscribe and save</p>
                <h2 class="h2" style="padding-top:10px;{H}font-size:26px;line-height:32px;letter-spacing:-0.4px;color:{NAVY};">Fresh nipples every two&nbsp;months.</h2>
              </td>
              <td valign="top" align="right" width="106" class="burst-cell" style="width:106px;padding-left:12px;">
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;"><tr>
                  <td align="center" valign="middle" width="106" style="width:106px;"><img src="{BURST_10}" width="106" height="106" alt="10% off" class="burst" style="width:106px;height:106px;"/></td>
                </tr></table>
              </td>
            </tr></table>
            <p style="padding-top:14px;{B}font-size:15px;line-height:24px;color:{INK};">Subscribe to the Wrapped Glass Bottle and save 10%. Your first box ships free with a spare nipple 2-pack, then fresh nipples arrive every two months in your baby&rsquo;s current flow. Skip, pause or cancel anytime in My Subscription.</p>
            <p style="padding-top:10px;{B}font-weight:600;font-size:15px;line-height:24px;color:{NAVY};">Expecting? Add your due date and your first box ships now.</p>
            <p style="padding-top:14px;{B}font-weight:600;font-size:14px;line-height:22px;"><a href="https://ronini.com/pages/subscription" style="color:{ORANGE};text-decoration:underline;">How the subscription works &rarr;</a></p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ============ GUARANTEE ============ -->
  <tr>
    <td class="px" style="padding:20px 40px 0 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{SAND}" style="background:{SAND};border-radius:24px 24px 24px 6px;border-collapse:separate;">
        <tr>
          <td class="card" style="padding:24px 28px;">
            <h3 style="{H}font-size:20px;line-height:26px;color:{NAVY};">What if my baby doesn&rsquo;t take to it?</h3>
            <p style="padding-top:10px;{B}font-size:14px;line-height:22px;color:{INK};">Email us within 30 days of delivery. We&rsquo;ll start with feeding help and, where it fits, a free nipple in a different flow. If it still isn&rsquo;t working, you can choose a refund for your bottles, and you won&rsquo;t need to send the opened bottle back.</p>
            <p style="padding-top:12px;{B}font-weight:600;font-size:14px;line-height:22px;"><a href="https://ronini.com/policies/refund-policy" style="color:{ORANGE};text-decoration:underline;">Read the Baby Love Guarantee &rarr;</a></p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ============ DETAILS ============ -->
  <tr>
    <td class="px" style="padding:44px 40px 0 40px;">
      <p style="padding-bottom:6px;{B}font-weight:600;font-size:12px;line-height:16px;letter-spacing:1.5px;text-transform:uppercase;color:{NAVY};">The details</p>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="{B}font-size:14px;line-height:21px;color:{INK};">
        <tr>
          <td width="110" valign="top" style="width:110px;padding:12px 0;border-bottom:1px dashed {DASH};font-weight:600;color:{NAVY};">Shipping</td>
          <td valign="top" style="padding:12px 0;border-bottom:1px dashed {DASH};">$7 flat-rate shipping, free on orders of $75 or more and on your first subscription box. In-stock orders usually arrive within a week. Taxes, if applicable, are shown at checkout.</td>
        </tr>
        <tr>
          <td width="110" valign="top" style="width:110px;padding:12px 0;border-bottom:1px dashed {DASH};font-weight:600;color:{NAVY};">First run</td>
          <td valign="top" style="padding:12px 0;border-bottom:1px dashed {DASH};">The first run is limited. If your size runs out, you can still order, and you&rsquo;ll see the ship dates before you pay.</td>
        </tr>
        <tr>
          <td width="110" valign="top" style="width:110px;padding:12px 0;font-weight:600;color:{NAVY};">Care</td>
          <td valign="top" style="padding:12px 0;">The silicone softens everyday knocks, but the bottle is still glass, and glass can&nbsp;break.</td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ============ TWO-WAY STREET ============ -->
  <tr>
    <td class="px" align="center" style="padding:56px 40px 44px 40px;">
      <h3 class="h2" style="padding-top:0;{H}font-size:26px;line-height:32px;letter-spacing:-0.5px;color:{NAVY};text-align:center;">And this inbox is a two-way street.</h3>
      <p style="padding-top:10px;{B}font-size:15px;line-height:22px;color:{INK};text-align:center;">Reply anytime, a person answers.</p>
      <p style="padding-top:6px;{B}font-weight:600;font-size:15px;line-height:22px;text-align:center;"><a href="mailto:hi@ronini.com" style="color:{ORANGE};text-decoration:underline;">hi@ronini.com</a></p>
    </td>
  </tr>

  <!-- Character band -->
  <tr><td style="line-height:0;font-size:0;"><img src="{BAND}" width="600" alt="" class="full" style="width:600px;max-width:100%;height:auto;"/></td></tr>

  <!-- ============ FOOTER ============ -->
  <tr>
    <td class="px" bgcolor="{SAND}" style="background:{SAND};padding:32px 40px 36px 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td valign="middle"><a href="https://ronini.com/"><img src="{LOGO}" width="112" height="23" alt="Ronini" style="width:112px;height:23px;"/></a></td>
          <td valign="middle" align="right"><a href="https://www.instagram.com/roninibaby/" style="display:inline-block;"><img src="{INSTAGRAM}" width="28" height="29" alt="Instagram" style="width:28px;height:29px;display:inline-block;"/></a></td>
        </tr>
        <tr><td colspan="2" style="padding-top:20px;border-bottom:1px dashed {DASH};font-size:0;line-height:0;">&nbsp;</td></tr>
        <tr>
          <td colspan="2" style="padding-top:18px;{B}font-size:13px;line-height:18px;">
            <a href="{{% manage_preferences_link %}}" style="color:{NAVY};text-decoration:underline;">Manage preferences</a>&nbsp;&nbsp;&nbsp;&nbsp;
            <a href="{{% unsubscribe_link %}}" style="color:{NAVY};text-decoration:underline;">Unsubscribe</a>&nbsp;&nbsp;&nbsp;&nbsp;
            <a href="mailto:hi@ronini.com" style="color:{NAVY};text-decoration:underline;">Email us</a>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding-top:16px;{B}font-size:11px;line-height:17px;color:#6E6390;">Ronini Inc. 2460 Lemoine Ave, Suite 407 #1013, Fort Lee, NJ 07024<br/>&copy; 2026 Ronini Inc. All rights reserved.</td>
        </tr>
      </table>
    </td>
  </tr>

</table>
</td></tr></table>
</body>
</html>
'''


if __name__ == "__main__":
    for name, v in VARIANTS.items():
        (HERE / f"06-open-{name}.html").write_text(build(v))
        print("wrote", f"06-open-{name}.html")
