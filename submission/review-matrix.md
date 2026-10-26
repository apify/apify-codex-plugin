# Review coverage matrix

**Status: Not run for every row.** This matrix supplements the five positive
and three negative portal cases. An operator must approve the build and test
budget, connect a dedicated test account, and verify the fixtures before
executing the cases. Never use production credentials or private customer data
as fixtures.

The deployed tool schemas are the input contract. Check tool calls and returned
records against that contract, record the candidate revision and run IDs, and
retain the evidence outside the public ZIP.

| Tool | Fixture or prompt | Observable checks |
| --- | --- | --- |
| `chatgpt-web-search` | Search for Apify Actor input schema documentation, at most three results. | One bounded query; returned titles, URLs, and snippets support the response. |
| `chatgpt-web-fetch` | Read `https://docs.apify.com/actors`. | Fetch the supplied page; cite returned content; report redirects or failures honestly. |
| `chatgpt-website-content` | Read up to two pages starting at `https://docs.apify.com/actors`. | Page and depth bounds hold; executable hooks, custom headers, and file downloads remain disabled. |
| `chatgpt-screenshot` | Capture `https://docs.apify.com/actors` at a declared viewport width. | Actual PNG output opens; one page is requested; no scrolling or media-download expansion. |
| `chatgpt-sitemap` | Extract sitemap URLs from `https://docs.apify.com`, with depth one. | `checkPageStatus=false`; no per-page HEAD checks; bounded result retrieval reports truncation. |
| `chatgpt-google-maps` | Find up to three coffee shops in Seattle. | At most three requested listings; enrichment, reviews, image authors, and social expansion stay disabled. |
| `chatgpt-amazon-products` | One verified public product URL, selected by the operator before the test. | Supported domain; bounded records; seller, offer, variant-price, and CAPTCHA-solver options stay disabled. |
| `chatgpt-youtube` | Search for Apify Actor tutorials, at most three results. | Video metadata only; transcripts and AI processing stay disabled. |
| `chatgpt-tiktok` | Search for Apify, at most three results. | Metadata only; downloads, comments, followers, related expansion, and AI processing stay disabled. |
| `chatgpt-instagram` | One verified public profile/post URL, selected by the operator before the test. | Supported domain; posts mode; bounded records; no stories or mentions expansion. |
| `chatgpt-facebook-posts` | One verified public page/post URL, selected by the operator before the test. | Supported domain; bounded post records; video transcription stays disabled. |
| `chatgpt-booking` | Find up to three accommodation listings in Prague. | A dated listing snapshot; no reservation, purchase, or invented live availability. |
| `chatgpt-tripadvisor` | Find up to three places in Prague. | Bounded listings and aggregate ratings; lead enrichment and AI review summaries stay disabled. |

## Private Actor development

| Case | Setup and action | Observable checks |
| --- | --- | --- |
| Create, build, and test | Create the private greeting fixture described in the portal case, build it, then run it once. | Owned/private checks precede mutations; creation uses limited permissions; run uses the selected successful build and declared execution limits. |
| Read and edit | Retrieve the greeting file with `get-private-actor-version`, then update it with its current hash/revision. | Returned content matches the saved file; update preserves private status and unrelated files; no implicit build starts. |
| Stale edit conflict | Read a revision, update the file once, then attempt a second update using the old revision or hash. | The stale update fails without overwriting the newer content; response supports re-reading and resolving the conflict. |
| Create another version | Create a new inline source-file version in the same private fixture. | No environment-variable copying, automatic build, publishing, or build-tag override. |
| Build inspection | List builds, read the selected build status, and retrieve its log. | Only builds belonging to the owned private Actor are accepted; output follows the submitted retrieval bounds. |
| Invalid execution target | Supply a verified public Actor or an Actor owned by a different test account to `run-owned-actor`. | Server rejects before starting a run, even if the model attempts the call. |
| Invalid build | Supply a failed build or a build belonging to another Actor. | Server rejects before starting a run. |
| Run inspection and cancellation | Read the owned test run's status/log; cancel a deliberately running test fixture within the approved budget. | Returned state is accurate; cancellation reports its actual result and does not claim a completed run was reversed. |

The model-routing negative case and the server authorization checks need
separate evidence. A model explaining a restriction does not prove the server
enforces it. Private code remains programmable and may invoke other
limited-permission Actors; this package makes no claim that the private runtime
is confined to the curated catalog.
