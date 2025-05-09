# YouTube Source Crawling

This module focuses on **collecting source-level data** from external platforms like [youtubers.me](https://us.youtubers.me/) and [playboard.co](https://playboard.co/), which are used to discover trending creators and viral content globally.

## 🌍 Purpose

To gather a broad and diverse list of **YouTube channels by country and category**, and collect data on **currently trending Shorts videos** for further analysis in the D’NOVA project.

## 🔗 Data Sources

- 🌐 **[youtubers.me](https://us.youtubers.me/)** — Top YouTubers by country and category  
- 📊 **[playboard.co](https://playboard.co/)** — Real-time data on trending Shorts and influencer performance

## 📁 File Descriptions

| File | Description |
|------|-------------|
| `country_category_url.xlsx` | A list of URLs on `youtubers.me`, covering 30 countries × 17 YouTube categories. |
| `youtube_api_channel_collection.ipynb` | Script for collecting channel metadata via the official YouTube API. |
| `youtuberme_global.ipynb` | Script to crawl top YouTubers from youtubers.me by country and category. |
| `playboard_crawling.ipynb` | Scraper to collect real-time trending Shorts data from playboard.co. |
| `data_union.ipynb` | Combines data from both youtubers.me and playboard to create a unified dataset. |
| `Archive/` | Legacy scripts or temporary versions retained for reference. |

## 🛠️ Output Usage

The collected data supports:

- 📌 Influencer discovery by market/industry
- 📈 Viral Shorts monitoring
- 📊 Trend forecasting at the creator/channel level

---

*This folder forms the foundation of D'NOVA's upstream data pipeline by sourcing channel-level insights across global YouTube ecosystems.*
