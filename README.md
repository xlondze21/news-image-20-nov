# news-image-20-nov

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xlondze21/news-image-20-nov/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xlondze21/news-image-20-nov/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A 1024x1024 newspaper-style infographic summing up 20 November 2026's world news in one image — "20 November 2026 — The World in One Day".

## Run it

```sh
python3 render.py              # draw entry.png
python3 main.py                # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Requires Pillow (`pip install Pillow`). No network. Deterministic:
running the generator twice produces byte-identical PNGs.

## The image

- **Hero:** the ICJ finds Myanmar guilty of genocide against the Rohingya
  (9–6) — the first time the court has held a state responsible.
- **Four stories:** the Trump–Xi–Putin peace declaration in Shenzhen;
  Anthropic's Nasdaq debut, up 17%; the Senate rejects the Iran
  war-powers vote 51–48; the UK pledges 1,000+ drones for Ukraine.
- **Strip:** fossil fuels cut from the COP31 draft deal.
- **Ticker:** US markets, final closes of Thursday 19 November 2026
  (labelled as such — the 20 Nov close did not exist yet at build time).

## License

MIT — see LICENSE.

---

<sub>Entered on [make.fun](https://make.fun/?ref=3f98mdh8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
