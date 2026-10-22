# Migration notes — October 22, 2026

## Discovery and coverage

Routes were recovered from the live Wix public route model and its page, blog and dynamic-item sitemaps. `tools/page-inventory.json` lists the recreated routes and aliases. This covers published, publicly accessible content, including pages omitted from the menu; it cannot recover unpublished Wix editor drafts, private account records or backend settings.

The following source routes were confirmed:

- `copy-of-home`: Welcome Home alternate design.
- `about-1`: Meet the Team / Our Story.
- `general-7`: Edmonton Communities / Where We've Built.
- `copy-of-home-1`: STEF TESTER HOMEPAGE, containing the welcome/lot contact screen.
- `digitalwelcome`: the same welcome/lot contact screen.
- `copy-of-about`: referral promotion and registration.
- `copy-of-show-homes`: Keswick community video.

## Changes to unfinished source sections

The Communities page contained Wix instruction text, unfilled testimonial sections, empty Lot/Size/Timeline labels and a draft Summerside case-study teaser with no working article. These unfinished sections have been left out of the public layout. Actual published location coordinates and the new-neighbourhood description are preserved.

The team page used stock placeholder portraits rather than an identified staff photograph. They are not presented as a photograph of Casey. The source misspellings “Casey Skarkey” and “Area Sales Managaer” were corrected.

The `items` collection contained three Wix sample records (“This is a Title 01/02/03”). These URLs now offer links to the real Homes and Gallery content. The original `fullscreen-page` was empty and popup routes returned 404; appropriate navigation/fallback pages are provided.

## Original content needs review

The original Show Homes page labels LOANNA sold, while Quick Possession labels LOANNA for sale. Those source labels are preserved on their respective pages; confirm its current availability before treating the copy as current inventory.

The original Show Homes page refers to ELEANOR at 4621 Knight Point; Quick Possession refers to ELEANOR III at that address. Labels and brochure associations remain as published in their respective source pages.

The original referral promotion and blog contain historical dollar amounts, dates, claims and warranty descriptions. These have not been independently updated or represented as newly verified offers.

## Services

Booking calendars, intake forms, member accounts, registration and checkout remain on the original website. No private records, booking logic, mailing subscriptions or form submissions were migrated. Links clearly take visitors to that service.

The Google Maps embed remains an external dependency. The community selector retains all locations published in the original map. It starts centered on Edmonton and can display a selected location. Contact, directions and social links remain functional external links.
