# Outputs

```
outputs/
├── raw_frequency/            <- Directory to place raw data from word frequency analysis. Only default ones are used as stopwords.
|    ├── title_only/          <- Word frequency analysis considering titles only.
|    └── title_and_abstract/  <- Word frequency analysis considering titles and abstracts.
|
├── adjusted_frequency/       <- Directory to place adjusted data from word frequency analysis. Custom stopwords are considered.
|    ├── title_only/          <- Word frequency analysis considering titles only.
|    └── title_and_abstract/  <- Word frequency analysis considering titles and abstracts.
|
└── wordcloud/                <- Directory to place wordcloud image.
     ├── title_only/          <- Word frequency analysis considering titles only.
     └── title_and_abstract/  <- Word frequency analysis considering titles and abstracts.
```