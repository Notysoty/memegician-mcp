---
name: make-memes
description: Use when the user wants a meme, a funny image caption, a reaction image, or meme ideas for a situation, post, team chat, presentation or social media; also when they name a classic meme format (Drake, Distracted Boyfriend, This Is Fine, Two Buttons...).
---

# Making memes with Memegician

Memegician has 400+ classic meme templates. A meme only lands when the captions follow the template's
traditional format, so pick the format first and write for it.

## One meme (free, no sign-in)

1. **Find formats.** Call `search_meme_templates` with the emotion or situation, not the topic's nouns
   ("choosing between two options", "pretending everything is fine", "overconfidence"). For timely picks,
   `get_trending_meme_templates` lists the most-searched formats in the latest month of search data (it names the month; data lags 1-2 months).
2. **Pick the format whose joke structure matches** (comparison, escalation, reaction, before/after...).
   Mention the alternatives briefly if the user may prefer another.
3. **Read the slots.** Call `get_meme_template`. Each slot's label says what goes there, in order; the
   example captions show the tone.
4. **Write captions.** 2-7 words per slot, in slot order, in the template's usual voice. Concrete beats
   clever: use the user's real situation. Leave a slot as `""` only if the format allows it.
5. **Render.** Call `render_meme` with `template_id` and `captions`. Use `aspect_ratio` (`1:1`, `3:4`,
   `4:3`, `9:16`, `16:9`) when the user names a platform (`9:16` for stories/reels, `1:1` for feeds).
6. Show the image and offer one tweak (different format, sharper caption, other tone). If the user wants
   to share it, give the `shareUrl` from the result: it opens the template on memegician.ai, where friends can
   make their own.

Free renders carry a small memegician.ai watermark (25 per day).

## Several ready-made options (signed in)

If the user wants a batch of options rather than one specific meme, `generate_memes` returns 6 finished
memes for a situation. It uses 1 credit from the user's Memegician account, so say that before calling
it. The first call asks the user to sign in; new accounts get 15 credits. Paid plans are watermark-free.

## Good captions

- Keep it workplace-safe unless the user asks otherwise; never target real private people.
- Don't put private information in captions: rendered memes get a public URL.
- If the joke needs explaining, pick another format.
